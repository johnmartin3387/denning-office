# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_auto_20170627_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='area_unit',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
