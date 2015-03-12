# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_auto_20150118_0457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queryjob',
            old_name='uploaded_csv_asJSON',
            new_name='Json',
        ),
        migrations.AddField(
            model_name='queryjob',
            name='postcode_column',
            field=models.TextField(default='1234'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queryjob',
            name='state_column',
            field=models.TextField(default='1234'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queryjob',
            name='street_column',
            field=models.TextField(default='1234'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queryjob',
            name='suburb_column',
            field=models.TextField(default='1234'),
            preserve_default=False,
        ),
    ]
