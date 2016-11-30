from django.contrib import admin

# Register your models here.
from product.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'sex', 'brand', 'type', 'price', 'description')
    search_fields = ['name']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'amount')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'amount', 'status', 'updated', 'invoice_number')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Cart, CartAdmin)
