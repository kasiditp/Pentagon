from __future__ import unicode_literals

from django.db import models

import product
from product.models import Order

# Create your models here.

def payment_image_path_name(self, filename):
    return '/'.join(['webadmin/images', filename])

class Transaction(models.Model):
    order = models.ForeignKey(product.models.Order , null = False , blank = False)
    payment_image = models.ImageField(verbose_name='Payment Image' , upload_to=payment_image_path_name , blank = True , null = True)

