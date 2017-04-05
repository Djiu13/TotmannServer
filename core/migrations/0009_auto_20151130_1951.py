# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_totmannruntimedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totmannruntimedata',
            name='last_cron_run',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
