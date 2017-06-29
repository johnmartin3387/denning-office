# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20170616_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id_type',
            field=models.ForeignKey(related_name='id_type', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='title',
            field=models.ForeignKey(related_name='title', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='department',
            field=models.ForeignKey(related_name='department_staff', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='position_type',
            field=models.ForeignKey(related_name='position_type', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='qualification',
            field=models.ForeignKey(related_name='qualification', blank=True, to='project.Attribute', null=True),
        ),
    ]
