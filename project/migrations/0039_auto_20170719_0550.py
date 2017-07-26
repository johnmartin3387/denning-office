# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0038_phone_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matter',
            name='close_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='matter',
            name='open_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='date_ceased',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='date_commenced',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='prev_adjustment_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
