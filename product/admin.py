from django.contrib import admin

# Register your models here.
from product.models import Product, ProductImage, Stock, Cart


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'sex', 'brand', 'type', 'price', 'description')
    search_fields = ['name']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'picture', 'image')


class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'amount')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'stock_id')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Cart, CartAdmin)