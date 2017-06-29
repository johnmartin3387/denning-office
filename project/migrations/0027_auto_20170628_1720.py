# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0026_auto_20170628_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normal',
            name='secretary',
            field=models.ForeignKey(related_name='secretary', blank=True, to='project.Contact', null=True),
        ),
    ]
