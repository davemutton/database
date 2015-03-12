# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20150116_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queryjob',
            name='uploaded_csv',
        ),
        migrations.AddField(
            model_name='queryjob',
            name='uploaded_csv_asJSON',
            field=jsonfield.fields.JSONField(default=''),
            preserve_default=False,
        ),
    ]
