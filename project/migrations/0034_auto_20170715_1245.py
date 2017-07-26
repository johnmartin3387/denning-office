# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0033_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='privilege',
        ),
        migrations.AddField(
            model_name='group',
            name='company',
            field=models.ForeignKey(blank=True, to='project.Company', null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='company',
            field=models.ForeignKey(blank=True, to='project.Company', null=True),
        ),
    ]
