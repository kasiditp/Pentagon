from django.contrib import admin

# Register your models here.
from product.models import Product, ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'sex', 'brand', 'type', 'price', 'description')
    search_fields = ['name']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'picture')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
