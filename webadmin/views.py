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

def admin_home(request):
    return render(request, 'pages/admin/admin-home.html',get_nav_context(request))

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
    create_transaction()
    transaction_list = Transaction.objects.all()
    num_transaction = Transaction.objects.filter().count()
    cart_list = Cart.objects.all()

    context = {
        'transaction_list' : transaction_list,
        'num_transaction' : num_transaction,
        'cart_list' : cart_list,
    }

    context.update(get_nav_context(request))

    return render(request,'pages/admin/admin-transaction.html' , context)

def create_transaction():
    for cart in Cart.objects.all():
        cart_invoice_number = cart.invoice_number

        if not Transaction.objects.filter(invoice_number = cart_invoice_number):
            total_amount = find_total_amount(cart_invoice_number)
            Transaction.objects.create(invoice_number = cart_invoice_number , status  = cart.status, updated = cart.updated , total_amount = total_amount)



def find_total_amount(invoice_number):
    sum = 0
    for cart in Cart.objects.filter(invoice_number=invoice_number):
        sum  = sum + (cart.amount * cart.stock.product.price)
    return  sum



def accept_transaction(request):
    if request.method == 'POST':
        invoice_number = request.POST['invoice_number']
        focusing_transaction = Transaction.objects.get(invoice_number = invoice_number)
        for cart in Cart.objects.filter(invoice_number = invoice_number):
            cart.invoice_number = 3
            cart.save()
        focusing_transaction.status = 3
        focusing_transaction.save()

        return HttpResponseRedirect(reverse('webadmin:admin_transaction'))

def reject_transaction(request):
    if request.method == 'POST':
        invoice_number = request.POST['invoice_number']
        focusing_transaction = Transaction.objects.get(invoice_number=invoice_number)
        focusing_transaction.delete()

        return HttpResponseRedirect(reverse('webadmin:admin_transaction'))

def enter_delivery_code(request):
    if request.method == 'POST':
        invoice_number = request.POST['invoice_number']
        delivery_code = request.POST['delivery_code']
        focusing_transaction = Transaction.objects.get(invoice_number=invoice_number)
        focusing_transaction.delivery_code = delivery_code
        focusing_transaction.status = 4
        focusing_transaction.save()

        return HttpResponseRedirect(reverse('webadmin:admin_transaction'))
