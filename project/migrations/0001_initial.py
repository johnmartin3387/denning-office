# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Attribute',
            },
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'Checklist',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_type', models.IntegerField(default=0, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('citizenship', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='Contact_Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postcode', models.CharField(max_length=255, null=True, blank=True)),
                ('town', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('fax', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('website', models.CharField(max_length=255, null=True, blank=True)),
                ('contact_person', models.CharField(max_length=255, null=True, blank=True)),
                ('mail_preference', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Contact_Info',
            },
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'Grant',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('parent', models.ForeignKey(blank=True, to='project.Group', null=True)),
            ],
            options={
                'db_table': 'Group',
            },
        ),
        migrations.CreateModel(
            name='Matter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_number', models.CharField(max_length=255, null=True, blank=True)),
                ('open_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(max_length=255, null=True, blank=True)),
                ('related', models.CharField(max_length=255, null=True, blank=True)),
                ('pocket_location', models.CharField(max_length=255, null=True, blank=True)),
                ('physical_location', models.CharField(max_length=255, null=True, blank=True)),
                ('box_location', models.CharField(max_length=255, null=True, blank=True)),
                ('close_date', models.DateTimeField(null=True, blank=True)),
                ('turnaround', models.IntegerField(default=0, null=True, blank=True)),
                ('billing_code', models.CharField(max_length=255, null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('additional_info', models.TextField(null=True, blank=True)),
                ('checklist', models.ForeignKey(blank=True, to='project.Checklist', null=True)),
            ],
            options={
                'db_table': 'Matter',
            },
        ),
        migrations.CreateModel(
            name='Matter_Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255, null=True, blank=True)),
                ('matter_tp', models.TextField(null=True, blank=True)),
                ('category', models.CharField(max_length=255, null=True, blank=True)),
                ('department', models.CharField(max_length=255, null=True, blank=True)),
                ('turnaround', models.IntegerField(default=0, null=True, blank=True)),
                ('billing_code', models.CharField(max_length=255, null=True, blank=True)),
                ('favourites', models.BooleanField(default=False)),
                ('additional_info', models.TextField(null=True, blank=True)),
                ('checklist', models.ForeignKey(blank=True, to='project.Checklist', null=True)),
                ('related', models.ForeignKey(blank=True, to='project.Matter_Code', null=True)),
            ],
            options={
                'db_table': 'Matter_Code',
            },
        ),
        migrations.CreateModel(
            name='Matter_Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.ForeignKey(blank=True, to='project.Contact', null=True)),
                ('matter', models.ForeignKey(blank=True, to='project.Matter', null=True)),
            ],
            options={
                'db_table': 'Matter_Contact',
            },
        ),
        migrations.CreateModel(
            name='Normal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=255, null=True, blank=True)),
                ('old_ic', models.CharField(max_length=255, null=True, blank=True)),
                ('additional_info', models.TextField(null=True, blank=True)),
                ('contact', models.ForeignKey(blank=True, to='project.Contact', null=True)),
            ],
            options={
                'db_table': 'Normal',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('info', models.ForeignKey(blank=True, to='project.Contact_Info', null=True)),
            ],
            options={
                'db_table': 'Phone',
            },
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('parent', models.ForeignKey(blank=True, to='project.Privilege', null=True)),
            ],
            options={
                'db_table': 'Privilege',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('individual', models.BooleanField(default=False)),
                ('title_type', models.CharField(max_length=255, null=True, blank=True)),
                ('title_no', models.CharField(max_length=255, null=True, blank=True)),
                ('lot_type', models.CharField(max_length=255, null=True, blank=True)),
                ('lot_no', models.CharField(max_length=255, null=True, blank=True)),
                ('daerah', models.CharField(max_length=255, null=True, blank=True)),
                ('negeri', models.CharField(max_length=255, null=True, blank=True)),
                ('area', models.CharField(max_length=255, null=True, blank=True)),
                ('tenure', models.CharField(max_length=255, null=True, blank=True)),
                ('lease_expiry_date', models.DateTimeField(null=True, blank=True)),
                ('title_registeration_date', models.DateTimeField(null=True, blank=True)),
                ('interest', models.CharField(max_length=255, null=True, blank=True)),
                ('restriction_against', models.CharField(max_length=255, null=True, blank=True)),
                ('approving_authority', models.CharField(max_length=255, null=True, blank=True)),
                ('other_restriction', models.CharField(max_length=255, null=True, blank=True)),
                ('category_land_use', models.CharField(max_length=255, null=True, blank=True)),
                ('express_condition', models.CharField(max_length=255, null=True, blank=True)),
                ('building_type', models.CharField(max_length=255, null=True, blank=True)),
                ('building_age', models.IntegerField(default=0, null=True, blank=True)),
                ('postal_address', models.CharField(max_length=255, null=True, blank=True)),
                ('assessment_rate', models.IntegerField(default=0, null=True, blank=True)),
                ('annual_quit_rent', models.IntegerField(default=0, null=True, blank=True)),
                ('previous_title', models.CharField(max_length=255, null=True, blank=True)),
                ('additional_info', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'Property',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_id', models.CharField(max_length=255, null=True, blank=True)),
                ('password', models.CharField(max_length=255, null=True, blank=True)),
                ('nickname', models.CharField(max_length=255, null=True, blank=True)),
                ('marital', models.BooleanField(default=False)),
                ('spouse_name', models.CharField(max_length=255, null=True, blank=True)),
                ('number_children', models.IntegerField(default=0, null=True, blank=True)),
                ('qualification', models.CharField(max_length=255, null=True, blank=True)),
                ('department', models.CharField(max_length=255, null=True, blank=True)),
                ('position_type', models.CharField(max_length=255, null=True, blank=True)),
                ('monthly_salary', models.IntegerField(default=0, null=True, blank=True)),
                ('prev_adjustment_date', models.DateTimeField(null=True, blank=True)),
                ('annual_leave', models.IntegerField(default=0, null=True, blank=True)),
                ('date_commenced', models.DateTimeField(null=True, blank=True)),
                ('date_ceased', models.DateTimeField(null=True, blank=True)),
                ('tenure_employed', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.CharField(max_length=255, null=True, blank=True)),
                ('tax_file_no', models.IntegerField(default=0, null=True, blank=True)),
                ('socso_no', models.IntegerField(default=0, null=True, blank=True)),
                ('epf_no', models.IntegerField(default=0, null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('contact', models.ForeignKey(blank=True, to='project.Group', null=True)),
            ],
            options={
                'db_table': 'Staff',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=255, null=True, blank=True)),
                ('category', models.CharField(max_length=255, null=True, blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('after', models.CharField(max_length=255, null=True, blank=True)),
                ('est_time', models.DateTimeField(null=True, blank=True)),
                ('due_time', models.DateTimeField(null=True, blank=True)),
                ('done_time', models.DateTimeField(null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('checklist', models.ForeignKey(blank=True, to='project.Checklist', null=True)),
            ],
            options={
                'db_table': 'Task',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('path', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('language', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('matter', models.ForeignKey(blank=True, to='project.Matter', null=True)),
                ('task', models.ForeignKey(blank=True, to='project.Task', null=True)),
            ],
            options={
                'db_table': 'Template',
            },
        ),
        migrations.AddField(
            model_name='normal',
            name='privilege',
            field=models.ForeignKey(blank=True, to='project.Privilege', null=True),
        ),
        migrations.AddField(
            model_name='matter',
            name='matter_code',
            field=models.ForeignKey(blank=True, to='project.Matter_Code', null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='group',
            field=models.ForeignKey(blank=True, to='project.Group', null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='privilege',
            field=models.ForeignKey(blank=True, to='project.Privilege', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='info',
            field=models.ForeignKey(blank=True, to='project.Contact_Info', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='info',
            field=models.ForeignKey(blank=True, to='project.Contact_Info', null=True),
        ),
    ]
