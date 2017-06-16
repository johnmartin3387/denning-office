# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_contact_gst_reg_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matter_code',
            name='category',
            field=models.ForeignKey(related_name='category', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='matter_code',
            name='department',
            field=models.ForeignKey(related_name='department', blank=True, to='project.Attribute', null=True),
        ),
    ]
