# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20170623_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='date_ceased',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='date_commenced',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
