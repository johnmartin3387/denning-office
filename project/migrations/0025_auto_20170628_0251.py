# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_auto_20170627_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='buml_lot',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='malay',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='approving_authority',
            field=models.ForeignKey(related_name='approving_authority', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='building_description',
            field=models.ForeignKey(related_name='building_description', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='building_type',
            field=models.ForeignKey(related_name='building_type', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='category_land_use',
            field=models.ForeignKey(related_name='category_land_use', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='express_condition',
            field=models.ForeignKey(related_name='express_condition', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='lot_type',
            field=models.ForeignKey(related_name='lot_type', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='mukim',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='mukim_val',
            field=models.ForeignKey(blank=True, to='project.Mukim', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='other_restriction',
            field=models.ForeignKey(related_name='other_restriction', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='restriction_against',
            field=models.ForeignKey(related_name='restriction_against', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='tenure',
            field=models.ForeignKey(related_name='property_tenure', blank=True, to='project.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='title_type',
            field=models.ForeignKey(related_name='title_type', blank=True, to='project.Attribute', null=True),
        ),
    ]
