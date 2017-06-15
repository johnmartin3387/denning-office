# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_property_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='mukim',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='property',
            name='mukim_val',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
