# coding=utf-8
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from datetime import timedelta
from tagging.registry import register

import re
import uuid
import hashlib

class CheckEvent(models.Model):
    EVENT_START = 'start'
    EVENT_FINISHED = 'finished'
    EVENT_LOG = 'log'
    EVENTS = (
        (EVENT_START, 'Started'),
        (EVENT_FINISHED, 'Finished'),
        (EVENT_LOG, 'Log Output'),
    )
    
    source = models.ForeignKey('Check')
    timestamp = models.DateTimeField(default=now)
    event = models.CharField(max_length = 10, choices = EVENTS, default = EVENT_FINISHED)
    content = models.TextField(blank=True)

    def __str__(self):
        checkmark = u" ✓" if self.is_success() else u" ⚠" if self.is_violation() else u""
        return u"%s%s | %s | %s" % (dict(CheckEvent.EVENTS)[self.event], checkmark, self.source.name, self.timestamp.strftime("%c") if self.timestamp else "")

    def is_violation(self):
        return self.is_failed_finish() or self.violates_expected_regex() or self.violates_alert_regex()
    
    def is_success(self):
        return self.event == CheckEvent.EVENT_FINISHED and self.content in self.source.allowed_return_codes_list()

    def is_failed_finish(self):
        return self.event == CheckEvent.EVENT_FINISHED and self.content not in self.source.allowed_return_codes_list()

    def violates_expected_regex(self):
        return self.source.expected_regex != "" and not re.search(self.source.expected_regex, self.content)
    
    def violates_alert_regex(self):
        return self.source.alert_regex != "" and re.search(self.source.alert_regex, self.content)

    def get_verbose_description(self):
        if self.event == CheckEvent.EVENT_START:
            return "Started."
        elif self.is_failed_finish():
            return "Failed with error code %s." % self.content
        elif self.event == CheckEvent.EVENT_LOG and self.violates_expected_regex() and self.violates_alert_regex():
            return "Not matching expected regex AND matching alert regex!"
        elif self.event == CheckEvent.EVENT_LOG and self.violates_expected_regex():
            return "Not matching expected regex."
        elif self.event == CheckEvent.EVENT_LOG and self.violates_alert_regex():
            return "Matches alert regex!"
        elif self.event == CheckEvent.EVENT_LOG:
            return "Log without anomalies."
        else:
            return "Finished without errors (return code %s)." % self.content

    def get_unified_status(self):
        
        if self.event == CheckEvent.EVENT_START:
            return "started"
        elif self.is_failed_finish():
            return 'failed'
        elif self.event == CheckEvent.EVENT_LOG and self.violates_expected_regex() or self.violates_alert_regex():
            return 'warning'
        elif self.event == CheckEvent.EVENT_LOG:
            return "log"
        else:
            return "finished"

    

allowed_return_codes_validator = RegexValidator(regex=r"^ *(-? *[0-9]+)( *, *-? *[0-9]+)* *$", message="Numbers, separated by commas. Example: '-1, -2, 3, 4'.")

def regex_validator(value):
    if len(value) == 0:
        return
    try:
        re.compile(value)
    except Exception as e:
        raise ValidationError("Illegal Regex Syntax: %s" % e.message)

class Check(models.Model):
    owner = models.ForeignKey(User)
    enabled = models.BooleanField(default=True)
    apikey = models.UUIDField(unique=True, db_index=True,
                              default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, help_text="Define an optional prefix to sort your checks.")
    prefix = models.CharField(max_length=64, null=True, blank=True)
    interval = models.DurationField(help_text="Format: days hours:minutes:seconds", default=timedelta(days=30))
    expected_regex = models.CharField(help_text="If not empty, all incoming logs for this check have to match (as in python's re.search) this regular expression or a notification is sent.", max_length=128, default="", blank=True, validators=[regex_validator])
    alert_regex = models.CharField(help_text="If not empty and an incoming log file matches this regular expression (as in python's re.search), a notification is sent.", max_length = 128, default="", blank=True, validators=[regex_validator])
    allowed_return_codes = models.CharField(help_text="Comma-separated list of return codes that are not considered an error for this job. (Default: '0')",
                     max_length=128, default="0",
                     validators=[allowed_return_codes_validator])
    notifications = models.ManyToManyField('NotificationReceiver', blank=True)
    store_events = models.DurationField(help_text="Time after which events are deleted. Format: days hours:minutes:seconds", default=timedelta(days=14))
    last_late_notification = models.DateTimeField(editable=False,
                                                  null=True, blank=True, default=None)

    def __str__(self):
        return "%s | %s" % (self.name, reverse('core:event-finished', args=[self.apikey]))

    def allowed_return_codes_list(self):
        return [str(int(x.strip())) for x in self.allowed_return_codes.split(',')]
    
    def is_late(self):
        latest = CheckEvent.objects.filter(source=self,
                                           timestamp__gte=now()-self.interval,
                                           event=CheckEvent.EVENT_FINISHED,
                                           content__in=self.allowed_return_codes_list()).count()
        return latest == 0

    def last_success(self):
        try:
            return CheckEvent.objects.filter(source=self,
                                             event=CheckEvent.EVENT_FINISHED,
                                             content__in=self.allowed_return_codes_list()).order_by('-timestamp').all()[0]
        except IndexError:
            return None
        
    def last_action(self):
        try:
            return CheckEvent.objects.filter(source=self).order_by('-timestamp').all()[0]
        except IndexError:
            return None
    
    def delete_old_events(self):
        events = CheckEvent.objects.filter(source=self,
                                           timestamp__lte=now()-self.store_events).all()
        for e in events:
            e.delete()

    def notify_late(self):
        last_success = self.last_success()
        last_action = self.last_action()
        last_action_text = last_action.timestamp.strftime("%c") if last_action else ""
        last_action_type = dict(CheckEvent.EVENTS)[last_action.event] if last_action else "none recorded"
        last_success_text = last_success.timestamp.strftime("%c") if last_success else "(none recorded)"
        for n in self.notifications.all():
            n.send("%sJob is running late: %s" % (self.get_prefix_for_email(), self.name),
                   "The job %s failed to finish successfully within the defined interval. Its last action was recorded on %s (%s), its last successful run was recorded on %s." % (self.name, last_action_text, last_action_type, last_success_text))
        self.last_late_notification = now()
        self.save()

    def notify_failed_finish(self, event):
        date = event.timestamp.strftime("%c")
        last_success = self.last_success()
        last_action = self.last_action()
        last_action_text = last_action.timestamp.strftime("%c") if last_action else ""
        last_action_type = dict(CheckEvent.EVENTS)[last_action.event] if last_action else "none recorded"
        last_success_text = last_success.timestamp.strftime("%c") if last_success else "(none recorded)"
        for n in self.notifications.all():
            n.send("%sJob returned error: %s" % (self.get_prefix_for_email(), self.name),
                   "The job %s returned an error code (%s) that indicates failure of the job execution. Before, its last action was recorded on %s (%s), its last successful run was recorded on %s. If you think that this error code does not indicate failure, please change the 'allowed return codes' setting for the corresponding check." % (self.name, event.content, last_action_text, last_action_type, last_success_text))
        
    def notify_alert_regex(self, event):
        date = event.timestamp.strftime("%c")
        for n in self.notifications.all():
            n.send("%sJob output is triggering alert: %s" % (self.get_prefix_for_email(), self.name),
                   "The job %s reported a log file at %s that triggered the alert regular expression (%s). The last 1000 characters of the log file are attached below.\n\n-------------------------------\n\n(...) %s" % (self.name, date, self.alert_regex, event.content[-1000:]))

    def notify_expected_regex(self, event):
        date = event.timestamp.strftime("%c")
        for n in self.notifications.all():
            n.send("%sJob output unexpected: %s" % (self.get_prefix_for_email(), self.name),
                   "The job %s reported a log file at %s that did not match the 'expected' regular expression (%s). The last 1000 characters of the log file are attached below.\n\n-------------------------------\n\n(...) %s" % (self.name, date, self.expected_regex, event.content[-1000:]))

    def notify_resurrection(self, event):
        last_success = self.last_success()
        last_success_text = last_success.timestamp.strftime("%c") if last_success else "(none recorded)"
        now_text = now().strftime("%c")
        for n in self.notifications.all():
            n.send("%sJob is running again: %s" % (self.get_prefix_for_email(), self.name),
                   "The job %s is up and running again, as of %s. Before, it was running late and was run successfully last on %s." % (self.name, now_text, last_success_text))

    def get_history(self):
        return CheckEvent.objects.filter(source=self, event__in = [CheckEvent.EVENT_FINISHED, CheckEvent.EVENT_LOG]).order_by('-timestamp')[:6]
    # add handling of first event (i.e., no warning before first event, no resurrection mail or other mail instead)

    def get_prefix_for_email(self):
        return '[%s] ' % self.prefix if self.prefix else ''

    def get_prefix_for_web(self):
        return '%s/' % self.prefix if self.prefix else ''

    class Meta:
        ordering = ['prefix', 'name']


def create_confirmation_token():
    return hashlib.sha256(uuid.uuid4().bytes + settings.SECRET_KEY.encode('ascii')).hexdigest()[:10]

class NotificationReceiver(models.Model):
    owner = models.ForeignKey(User)
    address = models.CharField(max_length = 128)
    confirmation_token = models.CharField(max_length=64, default=create_confirmation_token, blank=True, null=True) # empty confirmation token means that no further confirmation is needed

    def __str__(self):
        return "%s" % (self.address)

    def is_confirmed(self):
        return self.confirmation_token == None

    def send(self, subject, text, send_unconfirmed=False):
        if send_unconfirmed or self.is_confirmed():
            send_mail(subject, text, settings.EMAIL_FROM, [self.address])
    
    def send_confirmation_token(self, request):
        if self.is_confirmed():
            return
        url = request.build_absolute_uri(reverse("web:confirm-email", kwargs={'token': self.confirmation_token}))
        self.send(
            "Confirm notification receiver address",
            "Please confirm that you want to receive notifications from the 'totmann' cron job checker by clicking on the following link: %s" % url,
            True)


class TotmannRuntimeData(models.Model):
    last_cron_run = models.DateTimeField(default=None, null=True)

    @classmethod
    def touch_cron_run(cls):
        data, created = cls.objects.get_or_create()
        data.last_cron_run = now()
        data.save()

    @classmethod
    def check_cron_run(cls):
        data, created = cls.objects.get_or_create()
        if created or data.last_cron_run == None:
            is_delayed = True
        else:
            is_delayed = now() - data.last_cron_run > timedelta(seconds=settings.TOTMANN_EXPECT_CRON)
        if is_delayed:
            receivers = [x.email for x in User.objects.filter(is_staff=True, is_active=True).all()]
            send_mail('Totmann cron job is delayed!', "Totmann just noticed that the cron job checking totmann\'s checks does not run as expected. The cron job run is expected every %d seconds. The last cron job run was at %s. It is now %s." % (settings.TOTMANN_EXPECT_CRON, data.last_cron_run, now()), settings.EMAIL_FROM, receivers)

@receiver(pre_save)
def send_immediate_notifications(sender, **kwargs):
    if sender != CheckEvent or kwargs['instance'].id != None:
        return
    event = kwargs['instance']
    check = event.source
    if not check.enabled:
        return
    if check.is_late() and event.is_success():
        check.notify_resurrection(event)
    if event.is_failed_finish():
        check.notify_failed_finish(event)
    if event.event == 'log':
        if event.violates_expected_regex():
            check.notify_expected_regex(event)
        if event.violates_alert_regex():
            check.notify_alert_regex(event)

            
@receiver(post_save)
def add_notification_for_new_user(sender, **kwargs):
    if sender != User or NotificationReceiver.objects.filter(owner = kwargs['instance']).count() > 0:
        return
    user = kwargs['instance']
    n = NotificationReceiver(owner=user, address=user.email, confirmation_token=None)
    n.save()

           
@receiver(post_save)
def check_cron_run(sender, **kwargs):
    if sender != CheckEvent:
        return
    TotmannRuntimeData.check_cron_run()
    
register(Check)
