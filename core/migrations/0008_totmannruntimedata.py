# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotmannRuntimeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_cron_run', models.DateTimeField(default=None)),
            ],
        ),
    ]
