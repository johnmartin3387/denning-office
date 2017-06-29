# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20170626_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='master_title',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='property',
            name='project',
            field=models.ForeignKey(blank=True, to='project.Project', null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='template',
            field=models.ForeignKey(blank=True, to='project.Contact_Template', null=True),
        ),
    ]
