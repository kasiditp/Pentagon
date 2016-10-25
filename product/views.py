from django.db.models import Max
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context

from base.views import get_nav_context
from member.models import User
from product.models import Product, PRODUCT_TYPE, SEX, ProductImage, Stock, Cart

SIZE_LIST = ['S', 'M', 'L', 'XL', 'XXL']


def product_view(request):
    product_list = Product.objects.all()
    max_price = Product.objects.all().aggregate(Max('price'))

    context = {
        'product_list': product_list,
        'max_price': max_price,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/product/product.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    images = product.get_all_image()
    stocks = product.get_stocks()
    error = False
    error_message = ""
    success = False
    success_message = ""
    if request.session.get('error'):
        error = True
        error_message = request.session.get('error_message')
        request.session['error'] = False

    if request.session.get('success'):
        success = True
        success_message = request.session.get('success_message')
        request.session['success'] = False

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
        'error_message': error_message,
        'success': success,
        'success_message': success_message,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/productdetails/details.html', context)


def put_in_cart(request):
    product_id = request.POST['product_id']
    stock_id = request.POST['size_select']
    user_unique_id = request.session['user_unique_id']
    product = get_object_or_404(Product, pk=product_id)
    stock = get_object_or_404(Stock, pk=stock_id)
    user = get_object_or_404(User, unique_id=user_unique_id)
    if stock.amount <= 0:
        request.session['error'] = True
        request.session['error_message'] = "There is something wrong putting this item into your cart. Please check again"
        return HttpResponseRedirect(reverse('product:product_details', args=[product_id]))
    else:
        new_cart_item = Cart(user_id=user, stock_id=stock)
        new_cart_item.save()
        stock.amount -= 1
        stock.save()
        request.session['success'] = True
        request.session['success_message'] = "Done! Successfully added this item into your cart."
        return HttpResponseRedirect(reverse('product:product_details', args=[product_id]))


def manage_cart(request):
    user_id = 1
    cart_items = []
    cart = Cart.objects.filter(user_id=user_id)
    # for item in cart:
    #     stock = get_object_or_404(Stock, pk=item.stock_id)
    #     cart_items.append(stock)
    context = {
        'cart': cart,
        'sex': SEX,
        'type': PRODUCT_TYPE,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/cart/manage_cart.html', context)


def remove_from_cart(request):
    cart_item_id = request.POST['cart_id']
    cart_to_delete = get_object_or_404(Cart, pk=cart_item_id)
    cart_to_delete.stock_id.amount += 1
    cart_to_delete.stock_id.save()
    Cart.delete(cart_to_delete)

    return HttpResponseRedirect(reverse('manage_cart'))

@ajax
@csrf_exempt
def filtered(request):
    if request.POST:
        filter_product = None
        filter_button = request.POST.get('button_id')
        if filter_button in SIZE_LIST:
            filter_product = Product.objects.filter(size=filter_button)

        template = loader.get_template('pages/product/item/product_item.html')
        context = Context({'product_list': filter_product})
        rendered = template.render(context)

        return {'result': True, 'rendered': rendered}
