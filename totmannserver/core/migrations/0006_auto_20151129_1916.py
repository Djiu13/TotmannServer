# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_notificationreceiver_confirmation_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationreceiver',
            name='confirmation_token',
            field=models.CharField(default=core.models.create_confirmation_token, max_length=64, null=True, blank=True),
        ),
    ]
