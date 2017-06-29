# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20170628_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='spa_area_unit',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
