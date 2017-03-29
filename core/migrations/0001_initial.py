# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('apikey', models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)),
                ('name', models.CharField(max_length=32)),
                ('interval', models.DurationField()),
                ('expected_regex', models.CharField(default=b'', help_text=b"If not empty, all incoming logs for this check have to match (as in python's re.search) this regular expression or a notification is sent.", max_length=128, blank=True)),
                ('alert_regex', models.CharField(default=b'', help_text=b"If not empty and an incoming log file matches this regular expression (as in python's re.find), a notification is sent.", max_length=128, blank=True)),
                ('allowed_return_codes', models.CharField(default=b'0', help_text=b"Comma-separated list of return codes that are not considered an error for this job. (Default: '0')", max_length=128, validators=[django.core.validators.RegexValidator(regex=b'^ *(-? *[0-9]+)( *, *-? *[0-9]+)* *$', message=b"Numbers, separated by commas. Example: '-1, -2, 3, 4'.")])),
                ('store_events', models.DurationField()),
                ('last_late_notification', models.DateTimeField(default=None, null=True, editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event', models.CharField(default=b'finished', max_length=10, choices=[(b'start', b'Started'), (b'finished', b'Finished'), (b'log', b'Log Output')])),
                ('content', models.TextField(blank=True)),
                ('source', models.ForeignKey(to='core.Check')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationReceiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='notifications',
            field=models.ManyToManyField(to='core.NotificationReceiver'),
        ),
        migrations.AddField(
            model_name='check',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
