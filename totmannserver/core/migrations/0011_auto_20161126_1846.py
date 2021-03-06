# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20151215_0925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='check',
            options={'ordering': ['prefix', 'name']},
        ),
        migrations.AddField(
            model_name='check',
            name='prefix',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='check',
            name='name',
            field=models.CharField(help_text=b'Define an optional prefix to sort your checks.', max_length=64),
        ),
    ]
