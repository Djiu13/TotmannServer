from django.core.management.base import BaseCommand, CommandError
from core import models
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Searches for late checks and notifies the users."

    def handle(self, *args, **kwargs):
        checks = models.Check.objects.filter(enabled=True).all()
        for c in checks:
            if c.is_late() and (c.last_late_notification == None or c.interval < (now() - c.last_late_notification)):
                c.notify_late()
            c.delete_old_events()
        models.TotmannRuntimeData.touch_cron_run()
