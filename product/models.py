from __future__ import unicode_literals

from django.db import models

PRODUCT_TYPE = [
    (1, "Top"),
    (2, "Bottom"),
    (3, "Overall"),
    (4, "Footwear"),
    (5, "Accessory")
]

SEX = [
    (1, "Men"),
    (2, "Women"),
    (3, "Unisex")
]


# Create your models here.
class Product(models.Model):
    name = models.CharField(verbose_name="Name", max_length=64, null=False, blank=False)
    type = models.IntegerField(verbose_name="Product Type", choices=PRODUCT_TYPE, null=True)
    sex = models.IntegerField(verbose_name="Sex", choices=SEX, null=False)
    brand = models.CharField(verbose_name="Brand", max_length=64, null=False, blank=True)
    size = models.CharField(verbose_name="Size", max_length=64, null=False, blank=False)
    price = models.FloatField(verbose_name="Price", default=0, null=False, blank=False)
    description = models.TextField(verbose_name="Description", null=True, blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey('Product', null=False, blank=False)
    picture = models.CharField(verbose_name="Picture", max_length=256, null=True, blank=True)




