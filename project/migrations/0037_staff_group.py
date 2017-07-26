# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_auto_20170718_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='group',
            field=models.ForeignKey(blank=True, to='project.Group', null=True),
        ),
    ]
