# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20161127_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.IntegerField(choices=[(0, 'In cart'), (1, 'Ordered'), (2, 'Payment accepted'), (3, 'Delivery')], default=0, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='updated'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
