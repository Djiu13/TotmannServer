# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151127_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationreceiver',
            name='confirmation_token',
            field=models.CharField(default=core.models.create_confirmation_token, max_length=64, blank=True),
        ),
    ]
