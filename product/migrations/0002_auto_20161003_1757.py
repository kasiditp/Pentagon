# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0, verbose_name='Price'),
        ),
    ]
