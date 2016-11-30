from __future__ import unicode_literals

from django.db import models

import product
from product.models import *

# Create your models here.

def payment_image_path_name(self, filename):
    return '/'.join(['webadmin/images', filename])

class Transaction(models.Model):
    cart = models.ForeignKey(product.models.Cart , null = False , blank = False)
    payment_image = models.ImageField(verbose_name='Payment Image' , upload_to=payment_image_path_name , blank = True , null = True)

