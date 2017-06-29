# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_auto_20170628_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matter',
            name='related',
            field=models.ForeignKey(blank=True, to='project.Matter', null=True),
        ),
    ]
