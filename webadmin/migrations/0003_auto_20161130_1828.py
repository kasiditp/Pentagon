# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webadmin', '0002_auto_20161130_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(0, 'In cart'), (1, 'Ordered'), (2, 'Waiting for payment confirmation'), (3, 'Payment accepted'), (4, 'Delivery')], default=0, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='updated'),
        ),
    ]
