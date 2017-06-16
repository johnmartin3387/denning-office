# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20170615_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id_type',
            field=models.ForeignKey(blank=True, to='project.Attribute', null=True),
        ),
    ]
