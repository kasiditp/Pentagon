from django.contrib import admin

# Register your models here.
from product.models import Product


class ProductAdmin(admin.ModelAdmin) :
    list_display = ('id','name', 'type', 'sex', 'brand', 'type', 'price', 'description', 'picture')
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)
