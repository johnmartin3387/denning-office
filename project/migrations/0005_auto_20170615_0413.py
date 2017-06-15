# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20170614_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='normal',
            name='contact_person',
        ),
        migrations.RemoveField(
            model_name='normal',
            name='email',
        ),
        migrations.AddField(
            model_name='normal',
            name='template',
            field=models.ForeignKey(blank=True, to='project.Contact_Template', null=True),
        ),
    ]
