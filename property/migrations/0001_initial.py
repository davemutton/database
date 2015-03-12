# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('clientUID', models.AutoField(serialize=False, primary_key=True)),
                ('client_name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('propertyUID', models.AutoField(serialize=False, primary_key=True)),
                ('street_address', models.CharField(max_length=255, db_index=True)),
                ('suburb', models.CharField(max_length=120, db_index=True)),
                ('state', models.CharField(max_length=3, db_index=True)),
                ('postcode', models.IntegerField(db_index=True, max_length=4, blank=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('baths', models.IntegerField(default=0, max_length=2)),
                ('cars', models.IntegerField(default=0, max_length=2)),
                ('beds', models.IntegerField(default=0, max_length=2)),
                ('imagesourceURL', models.URLField(max_length=255, blank=True)),
                ('imagefile', models.ImageField(upload_to=b'photos/%Y/%m/%d', blank=True)),
                ('client', models.ManyToManyField(to='property.Client', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PropertyQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street_address', models.CharField(max_length=255, db_index=True)),
                ('suburb', models.CharField(max_length=120, db_index=True)),
                ('state', models.CharField(max_length=3, db_index=True)),
                ('postcode', models.IntegerField(db_index=True, max_length=4, blank=True)),
                ('matcheduncertainty', models.PositiveSmallIntegerField(blank=True)),
                ('linkedproperty', models.ForeignKey(to='property.Property')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QueryJob',
            fields=[
                ('queryUID', models.AutoField(serialize=False, primary_key=True)),
                ('uploaded_csv', models.FileField(upload_to=b'querycsv//%Y/%m/%d')),
                ('client', models.ManyToManyField(to='property.Client', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='propertyquery',
            name='queryID',
            field=models.ForeignKey(to='property.QueryJob'),
            preserve_default=True,
        ),
    ]
