# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0039_auto_20170719_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='email_verification',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
