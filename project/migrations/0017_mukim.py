# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20170626_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mukim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mukim', models.CharField(max_length=255, null=True, blank=True)),
                ('district', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(max_length=255, null=True, blank=True)),
                ('code', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Mukim',
            },
        ),
    ]
