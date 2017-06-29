# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20170623_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='privilege',
            field=models.ForeignKey(blank=True, to='project.Group', null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='contact',
            field=models.ForeignKey(blank=True, to='project.Contact', null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='tenure_employed',
            field=models.ForeignKey(related_name='tenure', blank=True, to='project.Attribute', null=True),
        ),
    ]
