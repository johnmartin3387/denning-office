# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='license_commencement_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='license_expiry_date',
        ),
        migrations.AddField(
            model_name='project',
            name='license_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
