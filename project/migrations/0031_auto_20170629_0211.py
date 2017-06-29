# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_auto_20170629_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matter',
            name='primary_client',
            field=models.ForeignKey(related_name='primary_client', blank=True, to='project.Normal', null=True),
        ),
    ]
