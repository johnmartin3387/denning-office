# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0040_staff_email_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='change_password',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
