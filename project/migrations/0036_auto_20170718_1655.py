# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_auto_20170718_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='commencement_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='effective_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='register_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
