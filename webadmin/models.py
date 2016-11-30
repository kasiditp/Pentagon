from __future__ import unicode_literals
from django.db import models
import product
from product.models import Cart

# Create your models here.

ORDERSTATUS = [
    (0, "In cart"),
    (1, "Ordered"),
    (2, "Waiting for payment confirmation"),
    (3, "Payment accepted"),
    (4, "Delivery"),
]


def payment_image_path_name(self, filename):
    return '/'.join(['webadmin/images', filename])

class Transaction(models.Model):
    invoice_number = models.CharField(verbose_name="Invoice Number", blank=True, default=None, null=True,max_length=10)
    total_amount = models.IntegerField(verbose_name="Total Amount" , blank= True , null=True,max_length=10)
    status = models.IntegerField(verbose_name="status", choices=ORDERSTATUS, blank=False, null=False, default=0)
    updated = models.DateTimeField(verbose_name="updated", auto_now_add=False, auto_now=True, null=True)
    payment_image = models.ImageField(verbose_name='Payment Image' , upload_to=payment_image_path_name , blank = True , null = True)
    delivery_code = models.CharField(verbose_name="Delivery Code" , blank=True , null=True, max_length= 20)


