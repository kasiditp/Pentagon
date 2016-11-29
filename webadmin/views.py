import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from base.views import get_nav_context
from product.models import Product, Stock, ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def admin_product(request):
    return render(request, 'pages/admin/admin-product.html', get_nav_context(request))
    # return render(request, 'pages/base/home.html', get_nav_context(request))
    # return None

@ajax
@csrf_exempt
def add_new_product(request):
    print request
    product = request.POST
    print product
    # print product['product_name']
    name = product['product_name']
    print name
    # image = request.FILES.get('image')
    price = product['product_price']
    print price
    product_type = product['product_type']
    print product_type
    brand = product['product_brand']
    print brand
    description = product['product_description']
    print description
    sex = product['product_sex']
    print sex
    new_product = Product.objects.create(name=name, type=product_type, sex=sex, brand=brand, price=price, description=description)

    print json.loads(product['product_size'])
    for size_list in json.loads(product['product_size']):
        size = size_list['size']
        amount = size_list['amount']
        Stock.objects.create(product=new_product, size=size, amount=amount)

    # ProductImage.objects.create(product=new_product, image=image)
    context = {
        "result": True,
        "message": "Success add new product"
    }
    # context.update(get_nav_context(request))
    return context


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