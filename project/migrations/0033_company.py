# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0032_auto_20170629_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('initials', models.CharField(max_length=255, null=True, blank=True)),
                ('phone1', models.CharField(max_length=255, null=True, blank=True)),
                ('phone2', models.CharField(max_length=255, null=True, blank=True)),
                ('phone3', models.CharField(max_length=255, null=True, blank=True)),
                ('fax1', models.CharField(max_length=255, null=True, blank=True)),
                ('fax2', models.CharField(max_length=255, null=True, blank=True)),
                ('commencement_date', models.DateTimeField(null=True, blank=True)),
                ('gst_registered', models.BooleanField(default=True)),
                ('registration_no', models.CharField(max_length=255, null=True, blank=True)),
                ('register_date', models.DateTimeField(null=True, blank=True)),
                ('effective_date', models.DateTimeField(null=True, blank=True)),
                ('taxable_period', models.IntegerField(default=3, null=True, blank=True)),
                ('partner_label', models.TextField(default='', null=True, blank=True)),
                ('partner_qualification', models.TextField(default='', null=True, blank=True)),
                ('la_clerk', models.TextField(default='', null=True, blank=True)),
                ('tax_invoice', models.TextField(default='', null=True, blank=True)),
                ('quotation', models.TextField(default='', null=True, blank=True)),
                ('receipt', models.TextField(default='', null=True, blank=True)),
                ('message', models.TextField(default='', null=True, blank=True)),
                ('description1', models.ForeignKey(related_name='description1', blank=True, to='project.Attribute', null=True)),
                ('description2', models.ForeignKey(related_name='description2', blank=True, to='project.Attribute', null=True)),
                ('info', models.ForeignKey(blank=True, to='project.Contact_Info', null=True)),
            ],
            options={
                'db_table': 'Company',
            },
        ),
    ]
