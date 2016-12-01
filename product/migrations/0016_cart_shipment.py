# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_merge_20161130_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='shipment',
            field=models.IntegerField(choices=[(0, 'THAILAND POST'), (1, 'DHL'), (2, 'FEDEX')], default=None, null=True, verbose_name='shipment'),
        ),
    ]
