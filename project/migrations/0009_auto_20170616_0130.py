# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20170615_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matter_code',
            name='additional_info',
            field=models.TextField(default='[]', null=True, blank=True),
        ),
    ]
