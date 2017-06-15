# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20170614_0236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('json', models.TextField(default='{}', null=True, blank=True)),
            ],
            options={
                'db_table': 'Contact_Template',
            },
        ),
        migrations.RemoveField(
            model_name='address',
            name='info',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='info',
        ),
        migrations.AddField(
            model_name='contact',
            name='id_value',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contact_info',
            name='address1',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contact_info',
            name='address2',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contact_info',
            name='address3',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='normal',
            name='contact_person',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='normal',
            name='directors',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='normal',
            name='registered_office',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='normal',
            name='secretary',
            field=models.ForeignKey(blank=True, to='project.Staff', null=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='contact',
            field=models.ForeignKey(blank=True, to='project.Contact', null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='id_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
