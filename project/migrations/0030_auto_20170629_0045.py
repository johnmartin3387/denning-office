# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_auto_20170629_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matter',
            name='status',
            field=models.ForeignKey(blank=True, to='project.Attribute', null=True),
        ),
    ]
