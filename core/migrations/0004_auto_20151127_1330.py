# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151126_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='interval',
            field=models.DurationField(default=datetime.timedelta(30), help_text=b'Format: days hours:minutes:seconds'),
        ),
        migrations.AlterField(
            model_name='check',
            name='store_events',
            field=models.DurationField(default=datetime.timedelta(14), help_text=b'Time after which events are deleted. Format: days hours:minutes:seconds'),
        ),
    ]
