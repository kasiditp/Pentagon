import json
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from base.views import get_nav_context
from product.models import Product, Stock, ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    context.update(get_nav_context(request))
    return render(request, 'pages/admin/admin-all-product.html', context)


def edit_product(request, product_id):
    product = Product.objects.filter(id=product_id)[0]
    context = {
        'result_product': product,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/admin/edit-product.html', context)
