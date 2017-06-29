# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_auto_20170626_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='local_authority',
            field=models.ForeignKey(related_name='local_authority', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='approval',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
