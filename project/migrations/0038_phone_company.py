# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_staff_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phone_Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('company', models.ForeignKey(blank=True, to='project.Company', null=True)),
            ],
            options={
                'db_table': 'Phone_Company',
            },
        ),
    ]
