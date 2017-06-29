# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_auto_20170627_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='individual',
            field=models.BooleanField(default=True),
        ),
    ]
