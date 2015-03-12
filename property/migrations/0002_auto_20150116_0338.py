# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyquery',
            name='linkedproperty',
            field=models.ForeignKey(blank=True, to='property.Property', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='propertyquery',
            name='matcheduncertainty',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='propertyquery',
            name='postcode',
            field=models.IntegerField(db_index=True, max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='propertyquery',
            name='queryID',
            field=models.ForeignKey(blank=True, to='property.QueryJob', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='propertyquery',
            name='state',
            field=models.CharField(db_index=True, max_length=3, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='propertyquery',
            name='street_address',
            field=models.CharField(max_length=255, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='propertyquery',
            name='suburb',
            field=models.CharField(db_index=True, max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
    ]
