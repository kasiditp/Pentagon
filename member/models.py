from __future__ import unicode_literals

from django.db import models

SEX = [
    (1, "Men"),
    (2, "Women"),
    (3, "Unisex")
]
TYPE = [
    (1, "member"),
    (2, "admin")
]


class User(models.Model):
    unique_id = models.CharField(verbose_name='Unique id', max_length=10, null=False, blank=False)
    username = models.CharField(verbose_name='Username', max_length=64, null=False, blank=False)
    password = models.CharField(verbose_name='Password', max_length=256, null=False, blank=False)
    email = models.EmailField(verbose_name='Email', null=False, blank=True)
    sex = models.IntegerField(verbose_name="Sex", choices=SEX, null=False)
    birth_date = models.DateField(verbose_name='Birth date', null=False, blank=False)
    first_name = models.CharField(verbose_name='Firstname', max_length=64, null=False, blank=False)
    last_name = models.CharField(verbose_name='Lastname', max_length=64, null=False, blank=False)
    address = models.TextField(verbose_name='Address', null=True, blank=False)
    type = models.IntegerField(verbose_name="User Type", choices=TYPE, null=False, default=1)

