from __future__ import unicode_literals

import random

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


def product_image_path_name(self, filename):
    return '/'.join(['product/images', filename])


# Create your models here.
class Product(models.Model):
    name = models.CharField(verbose_name="Name", max_length=64, null=False, blank=False)
    type = models.IntegerField(verbose_name="Product Type", choices=PRODUCT_TYPE, null=True)
    sex = models.IntegerField(verbose_name="Sex", choices=SEX, null=False)
    brand = models.CharField(verbose_name="Brand", max_length=64, null=False, blank=True)
    price = models.FloatField(verbose_name="Price", default=0, null=False, blank=False)
    description = models.TextField(verbose_name="Description", null=True, blank=True)

    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return u"%s" % self.name

    def get_all_image(self):
        return ProductImage.objects.filter(product=self)

    def get_image(self):
        return ProductImage.objects.filter(product=self)[0]

    def get_stocks(self):
        return Stock.objects.filter(product=self)

    def get_type_name(self):
        return PRODUCT_TYPE[self.type - 1][1]

    def get_sex_name(self):
        return SEX[self.sex - 1][1]

    def suggest_product(self):
        suggest_pool = Product.objects.filter(type=self.type).exclude(id=self.id)
        sample_size = 3
        suggest_size = suggest_pool.count()
        if suggest_size < 3:
            sample_size = suggest_size
        suggest = random.sample(suggest_pool, sample_size)
        return suggest


class ProductImage(models.Model):
    product = models.ForeignKey('Product', null=False, blank=False)
    image = models.ImageField(verbose_name='Product Image', upload_to=product_image_path_name, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return u"%s" % self.image


class Stock(models.Model):
    product = models.ForeignKey('Product', null=False, blank=False)
    size = models.CharField(verbose_name="Size", max_length=8)
    amount = models.IntegerField(verbose_name="Amount", default=0)

    def __str__(self):
        return "%s %s" % (self.product, self.size)


class Cart(models.Model):
    stock_id = models.ForeignKey('Stock', null=False, blank=False)
    user_id = models.ForeignKey('member.User', null=False, blank=False)

    @staticmethod
    def get_total_price(user_id):
        this_cart = Cart.objects.filter(user_id__unique_id=user_id)
        total_price = 0
        for item in this_cart:
            total_price += item.stock_id.product.price
        return total_price
