# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20170615_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='gst_reg_no',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
