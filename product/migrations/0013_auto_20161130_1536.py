# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20161130_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='invoice_number',
            field=models.CharField(default=None, max_length=10, verbose_name='Invoice Number'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.IntegerField(choices=[(0, 'In cart'), (1, 'Ordered'), (2, 'Waiting for payment confirmation'), (3, 'Payment accepted')], default=0, verbose_name='status'),
        ),
    ]
