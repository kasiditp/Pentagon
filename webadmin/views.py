from django.shortcuts import render

from base.views import get_nav_context
from product.models import Product, Stock, ProductImage


def admin_product_view(request):
    return render(request, 'pages/admin/admin-product.html', get_nav_context(request))


def add_new_product(request):
    product = request.POST
    name = product['name']
    image = request.FILES.get('img-file')
    price = product['price']
    product_type = product['type']
    brand = product['brand']
    description = product['description']
    sex = product['sex']
    size = product['size']
    amount = product['amount']
    new_product = Product.objects.create(name=name, type=product_type, sex=sex, brand=brand, price=price, description=description)
    Stock.objects.create(product=new_product, size=size, amount=amount)
    ProductImage.objects.create(product=new_product, image=image)
    context = {
        "message": "Success add new product"
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/admin/admin-product.html', context)