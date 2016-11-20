from django.shortcuts import render

from base.views import get_nav_context
from product.models import Product, Stock, ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def admin_product(request):
    return render(request, 'pages/admin/admin-product.html', get_nav_context(request))
    # return render(request, 'pages/base/home.html', get_nav_context(request))
    # return None


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

def admin_all_product(request):
    product_list = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 10)
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    context = {
        'product_list': product_list
    }
    return render(request, 'pages/admin/admin-all-product.html', context)