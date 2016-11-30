import json
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax
from django.urls import reverse

from base.views import get_nav_context
from product.models import Product, Stock, ProductImage
from models import *
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
    request.session['temp-product'] = new_product.id
    context = {
        "result": True,
        "message": "Success add new product"
    }
    # context.update(get_nav_context(request))
    return context


def add_product_images(request):
    print 'add image function \n'
    print request.FILES
    print request.FILES.get('product-img')
    return render(request, 'pages/admin/admin-product.html', get_nav_context(request))


def admin_all_product(request):
    product_list = Product.objects.all()
    num_product = Product.objects.filter().count()
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 10)
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    context = {
        'product_list': product_list,
        'num_product' : num_product
    }

    return render(request, 'pages/admin/admin-all-product.html', context)

def admin_transaction(request):
    transaction_list = Transaction.objects.all()
    num_transaction = Transaction.objects.filter().count()

    context = {
        'transaction_list' : transaction_list,
        'num_transaction' : num_transaction
    }

    return render(request,'pages/admin/admin-transaction.html' , context)

def accept_transaction(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        order_match = 2 #mock up
        focusing_order = Transaction.objects.get(order = order_match)
        print focusing_order
        focusing_order.status = 2
        focusing_order.save()

        return HttpResponseRedirect(reverse('webadmin:admin_transaction'))

def reject_transaction(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        focusing_order = Transaction.objects.get(order =order_id)
        focusing_order.delete()

        return HttpResponseRedirect(reverse('webadmin:admin_transaction'))

