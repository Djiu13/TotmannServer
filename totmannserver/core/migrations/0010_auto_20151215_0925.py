# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20151130_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
