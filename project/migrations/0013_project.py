# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20170623_2322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('phase', models.CharField(max_length=255, null=True, blank=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('license_no', models.CharField(max_length=255, null=True, blank=True)),
                ('license_commencement_date', models.DateTimeField(null=True, blank=True)),
                ('license_expiry_date', models.DateTimeField(null=True, blank=True)),
                ('permit_no', models.CharField(max_length=255, null=True, blank=True)),
                ('permit_commencement_date', models.DateTimeField(null=True, blank=True)),
                ('permit_expiry_date', models.DateTimeField(null=True, blank=True)),
                ('complete_date', models.DateTimeField(null=True, blank=True)),
                ('lease_expiry_date', models.DateTimeField(null=True, blank=True)),
                ('note1', models.CharField(max_length=255, null=True, blank=True)),
                ('note2', models.CharField(max_length=255, null=True, blank=True)),
                ('hda_no', models.CharField(max_length=255, null=True, blank=True)),
                ('approval', models.ForeignKey(related_name='approval', blank=True, to='project.Attribute', null=True)),
                ('bank', models.ForeignKey(related_name='bank', blank=True, to='project.Normal', null=True)),
                ('developer', models.ForeignKey(related_name='developer', blank=True, to='project.Normal', null=True)),
                ('encumbrances', models.ForeignKey(related_name='encumbrances', blank=True, to='project.Normal', null=True)),
                ('land_tenure', models.ForeignKey(related_name='land_tenure', blank=True, to='project.Attribute', null=True)),
                ('proprietor', models.ForeignKey(related_name='proprietor', blank=True, to='project.Normal', null=True)),
            ],
            options={
                'db_table': 'Project',
            },
        ),
    ]
