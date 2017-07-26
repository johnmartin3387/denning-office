# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0034_auto_20170715_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='fax1',
            new_name='fax',
        ),
        migrations.AddField(
            model_name='company',
            name='gst_rate',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='la_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='partner',
            field=models.TextField(default='', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='partner_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
