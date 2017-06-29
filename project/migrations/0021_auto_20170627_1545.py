# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_property_area_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='interest',
            field=models.BooleanField(default=False),
        ),
    ]
