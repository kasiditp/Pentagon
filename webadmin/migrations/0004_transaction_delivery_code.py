# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webadmin', '0003_auto_20161130_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='delivery_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Delivery Code'),
        ),
    ]