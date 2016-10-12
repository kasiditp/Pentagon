from django.db.models import Max
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from product.models import Product, PRODUCT_TYPE, SEX, ProductImage, Stock

SIZE_LIST = ['S', 'M', 'L', 'XL', 'XXL']


def product_view(request):
    product_list = Product.objects.all()
    max_price = Product.objects.all().aggregate(Max('price'))

    context = {
        'product_list': product_list,
        'max_price': max_price,
    }

    return render(request, 'pages/product/product.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    images = product.get_all_image()
    stocks = product.get_stocks()
    error = False
    error_message = ""
    if request.session.get('error'):
        error = True
        error_message = request.session.get('error_message')
        request.session['error'] = False

    sex = SEX[(product.sex - 1)][1]
    product_type = PRODUCT_TYPE[(product.type - 1)][1]
    # print sex
    context = {
        'product': product,
        'sex': sex,
        'type': product_type,
        'images': images,
        'stocks': stocks,
        'error': error,
        'error_message': error_message
    }

    return render(request, 'pages/productdetails/details.html', context)


def put_in_cart(request):
    product_id = request.POST['product_id']
    stock_id = request.POST['size_select']
    product = get_object_or_404(Product, pk=product_id)
    stock = get_object_or_404(Stock, pk=stock_id)
    if stock.amount <= 0:
        request.session['error'] = True
        request.session['error_message'] = "There is something wrong putting this item into your cart. Please check again"
        return HttpResponseRedirect(reverse('product:product_details', args=[product_id]))
    else:
        return HttpResponse(" " + str(product) + " " + str(stock_id))


@ajax
@csrf_exempt
def filtered(request):
    if request.POST:
        filter_product = None
        filter_button = request.POST.get('button_id')
        if filter_button in SIZE_LIST:
            filter_product = Product.objects.filter(size=filter_button)
        print "is number? %s" % is_number(filter_button)
        if is_number(filter_button):
            filter_product = Product.objects.filter(price__lte=float(filter_button))

        template = loader.get_template('pages/product/item/product_item.html')
        context = Context({'product_list': filter_product})
        rendered = template.render(context)

        return {'result': True, 'rendered': rendered}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False