# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_auto_20170629_0211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grant',
            name='group',
        ),
        migrations.RemoveField(
            model_name='grant',
            name='privilege',
        ),
        migrations.RemoveField(
            model_name='privilege',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='group',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='normal',
            name='privilege',
        ),
        migrations.AddField(
            model_name='group',
            name='privilege_json',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Grant',
        ),
        migrations.DeleteModel(
            name='Privilege',
        ),
    ]
