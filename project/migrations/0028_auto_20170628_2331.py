# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0027_auto_20170628_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='matter',
            name='clerk_in_charge',
            field=models.ForeignKey(related_name='clerk_in_charge', blank=True, to='project.Staff', null=True),
        ),
        migrations.AddField(
            model_name='matter',
            name='file_number2',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='matter',
            name='la_in_charge',
            field=models.ForeignKey(related_name='la_in_charge', blank=True, to='project.Staff', null=True),
        ),
        migrations.AddField(
            model_name='matter',
            name='partner_in_charge',
            field=models.ForeignKey(related_name='partner_in_charge', blank=True, to='project.Staff', null=True),
        ),
        migrations.AddField(
            model_name='matter',
            name='primary_client',
            field=models.ForeignKey(related_name='primary_client', blank=True, to='project.Staff', null=True),
        ),
    ]
