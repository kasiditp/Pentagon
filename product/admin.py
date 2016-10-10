from django.contrib import admin

# Register your models here.
from product.models import Product, ProductImage, Stock


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'sex', 'brand', 'type', 'price', 'description')
    search_fields = ['name']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'picture')


class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'amount')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Stock, StockAdmin)
