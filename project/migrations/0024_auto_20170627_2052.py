# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20170627_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='annual_quit_rent',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='building_age',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
