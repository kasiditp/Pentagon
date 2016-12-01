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
    transaction_list = Transaction.objects.filter(status__gte=3)
    ctemp = []
    for tl in transaction_list:
        ctemp.append(tl.invoice_number)
    cart_list = Cart.objects.filter(invoice_number__in=ctemp)
    dtemp = []
    for cl in cart_list:
        dtemp.append(cl.stock_id)
    stock = Stock.objects.filter(pk__in=dtemp)
    sell_out = {}
    for s in stock:
        cart_amount = Cart.objects.filter(stock=s)[0]
        if s.product.brand in sell_out:
            sell_out[s.product.brand] += cart_amount.amount
        else:
            sell_out[s.product.brand] = cart_amount.amount

    sell_out_price = {}
    for s in stock:
        cart_amount = Cart.objects.filter(stock=s)[0]
        if s.product.brand in sell_out_price:
            sell_out_price[s.product.brand] += (s.product.price*cart_amount.amount)
        else:
            sell_out_price[s.product.brand] = (s.product.price*cart_amount.amount)

    total_price = 0
    for tl in transaction_list:
        total_price += tl.total_amount

    context = {
        'sell_out': json.dumps(sell_out),
        'sell_out_price': json.dumps(sell_out_price),
        'total_price': total_price
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/admin/admin-home.html', context)


def admin_product(request):
    return render(request, 'pages/admin/admin-product.html', get_nav_context(request))

@ajax
@csrf_exempt
def add_new_product(request):
    # print request
    product = request.POST
    print product
    name = product['product_name']
    print name
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
    new_product = Product.objects.create(name=name, type=product_type, sex=sex, brand=brand, price=price,
                                         description=description)
    # print json.loads(product['product_size'])
    for size_list in json.loads(product['product_size']):
        size = size_list['size']
        amount = size_list['amount']
        stock = Stock.objects.create(product=new_product, size=size, amount=amount)
    request.session['temp-product'] = new_product.id
    context = {
        "result": True,
        "message": "Success add new product"
    }
    context.update(get_nav_context(request))
    return context


@ajax
@csrf_exempt
def update_product(request):
    # print request
    product = request.POST
    # print product
    product_id = product['product_id']
    # print 'AAA ' + product_id
    name = product['product_name']
    # print name
    price = product['product_price']
    # print price
    product_type = product['product_type']
    # print product_type
    brand = product['product_brand']
    # print brand
    description = product['product_description']
    # print description
    sex = product['product_sex']
    # print sex
    size_list = json.loads(product['product_size'])
    if name and product_type and sex and brand and price and description:
        Product.objects.filter(pk=product_id).update(name=name, type=product_type, sex=sex, brand=brand,
                                                               price=price, description=description)
        temp_product = Product.objects.filter(pk=product_id)
        for size in size_list:
            amount = size['amount']
            edit_size = size['size']
            Stock.objects.filter(product=temp_product, size=edit_size).update(amount=amount)
        request.session['temp-product'] = product_id
        context = {
            "result": True,
            "message": "Success edit product"
        }
        # context.update(get_nav_context(request))
        print 'Success'
        return context
    else:
        context = {
            "result": False,
            "message": "Fail to edit product"
        }
        return context


def add_product_images(request):
    product = Product.objects.filter(id=request.session['temp-product'])
    ProductImage.objects.create(product=product, image=request.FILES.get('product-img'))
    return render(request, 'pages/admin/admin-all-product.html-product.html', get_nav_context(request))


def edit_product_images(request):
    if request.FILES.get('img-file'):
        image_product = ProductImage.objects.get(product=request.session['temp-product'])
        image_product.image = request.FILES.get('img-file')
        image_product.save()
    else:
        print 'did not edit image'
    return HttpResponseRedirect(reverse('webadmin:admin_all_product'))


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
    context.update(get_nav_context(request))
    return render(request, 'pages/admin/admin-all-product.html', context)


def edit_product(request, product_id):
    product = Product.objects.filter(id=product_id)[0]
    context = {
        'result_product': product,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/admin/edit-product.html', context)


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
            cart.status = 3
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


def delete_product(request, product_id):
    product = Product.objects.filter(pk=product_id)
    ProductImage.objects.filter(product=product).delete()
    Stock.objects.filter(product=product).delete()
    product.delete()
    return HttpResponseRedirect(reverse('webadmin:admin_all_product'))


def enter_delivery_code(request):
    if request.method == 'POST':
        invoice_number = request.POST['invoice_number']
        delivery_code = request.POST['delivery_code']
        focusing_transaction = Transaction.objects.get(invoice_number=invoice_number)
        focusing_transaction.delivery_code = delivery_code
        focusing_transaction.status = 4
        focusing_transaction.save()

        return HttpResponseRedirect(reverse('webadmin:admin_transaction'))
