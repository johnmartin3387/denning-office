# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_mukim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='mukim',
            field=models.ForeignKey(blank=True, to='project.Mukim', null=True),
        ),
    ]
