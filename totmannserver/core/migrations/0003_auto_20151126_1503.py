# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151125_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='alert_regex',
            field=models.CharField(default=b'', help_text=b"If not empty and an incoming log file matches this regular expression (as in python's re.search), a notification is sent.", max_length=128, blank=True, validators=[core.models.regex_validator]),
        ),
        migrations.AlterField(
            model_name='check',
            name='expected_regex',
            field=models.CharField(default=b'', help_text=b"If not empty, all incoming logs for this check have to match (as in python's re.search) this regular expression or a notification is sent.", max_length=128, blank=True, validators=[core.models.regex_validator]),
        ),
    ]
