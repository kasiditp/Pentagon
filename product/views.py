from sets import Set

from django.db.models import Max,Min
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

SIZE_LIST = set()
SEX_LIST = ['Men', 'Women', 'Unisex']
PRODUCT_TYPES = {
    "all": 0,
    "top": 1,
    "bottom": 2,
    "overall": 3,
    "footwear": 4,
    "accessory": 5
}
ORDERSTATUS = [
    (1, "Ordered"),
    (2, "Payment accepted"),
    (3, "Delivery")
]

num = 0


def product_view(request):
    product_list = Product.objects.all()
    max_price = Product.objects.all().aggregate(Max('price'))
    min_price = Product.objects.all().aggregate(Min('price'))
    brands = get_all_brand('all')
    context = {
        'product_list': product_list,
        'max_price': max_price,
        'min_price': min_price,
        'brands': brands,
        'type': PRODUCT_TYPES['all']
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/product/product.html', context)


def product_type_view(request, product_type):
    if product_type in PRODUCT_TYPES:
        product_list = Product.objects.filter(type=PRODUCT_TYPES[product_type])
        max_price = product_list.aggregate(Max('price'))
        min_price = product_list.aggregate(Min('price'))
        brands = get_all_brand(product_type)
        stock = Stock.objects.all()
        size_universe = set()
        for item in stock:
            if str(item.product.type) == str(PRODUCT_TYPES[product_type]):
                size_universe.add(item.size)

        SIZE_LIST.update(size_universe)
        context = {
            'product_list': product_list,
            'max_price': max_price,
            'min_price': min_price,
            'brands': brands,
            'type': PRODUCT_TYPES[product_type],
            'size_universe': size_universe
        }
        context.update(get_nav_context(request))
        return render(request, 'pages/product/product.html', context)
    else:
        return HttpResponse(reverse('product_view'))

@ajax
@csrf_exempt
def get_brand(request):
    brand = set()
    for product in Product.objects.all():
        brand.add(product.brand)

    return {'brand': brand}


def get_all_brand(type):
    brand = set()
    if type == 'all':
        brand_universe = Product.objects.all()
    elif type in PRODUCT_TYPES:
        brand_universe = Product.objects.filter(type=PRODUCT_TYPES[type])

    for product in brand_universe:
        brand.add(product.brand)

    return brand

def value_to_key(type):
    if type == '0':
        return 'all'
    elif type == '1':
        return 'top'
    elif type == '2':
        return 'bottom'
    elif type == '3':
        return 'overall'
    elif type == '4':
        return 'footwear'
    elif type == '5':
        return 'accessory'
    else:
        return 'error'


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
    suggest = product.suggest_product()
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
        'suggest': suggest,
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
        new_cart_item = Cart(user=user, stock=stock, amount=1, status=0)
        new_cart_item.save()
        stock.amount -= 1
        stock.save()
        request.session['success'] = True
        request.session['success_message'] = "Done! Successfully added this item into your cart."
        return HttpResponseRedirect(reverse('product:product_details', args=[product_id]))


def manage_cart(request):
    user_id = request.session['user_unique_id']
    cart_items = []
    cart = Cart.objects.filter(user__unique_id=user_id)
    # for item in cart:
    #     stock = get_object_or_404(Stock, pk=item.stock)
    #     cart_items.append(stock)
    total_price = Cart.get_total_price(user_id)
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
    context = {
        'cart': cart,
        'sex': SEX,
        'type': PRODUCT_TYPE,
        'total_price': total_price,
        'error': error,
        'error_message': error_message,
        'success': success,
        'success_message': success_message,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/cart/manage_cart.html', context)


def order_checkout(request):
    user_id = request.session['user_unique_id']
    user = get_object_or_404(User, unique_id=user_id)
    carts = Cart.objects.filter(user=user)
    context = {
        'user': user,
        'carts': carts,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/cart/order.html', context)


def update_cart_amount(request):
    cart_id = request.POST['cart_id']
    cart = get_object_or_404(Cart, pk=cart_id)
    new_amount = int(request.POST['select_amount'])
    cart.stock.amount += cart.amount
    cart.stock.save()
    if cart.stock.amount < new_amount:
        cart.stock.amount -= cart.amount
        request.session['error'] = True
        request.session['error_message'] = "Looks like that number is not available anymore. Please try again."
        cart.stock.save()
    else:
        cart.stock.amount -= new_amount
        cart.amount = new_amount
        request.session['success'] = True
        request.session['success_message'] = "Successfully updated your cart."
        cart.stock.save()
        cart.save()
    return HttpResponseRedirect(reverse('manage_cart'))


def remove_from_cart(request):
    cart_item_id = request.POST['cart_id']
    cart_to_delete = get_object_or_404(Cart, pk=cart_item_id)
    cart_to_delete.stock.amount += cart_to_delete.amount
    cart_to_delete.stock.save()
    Cart.delete(cart_to_delete)
    request.session['success'] = True
    request.session['success_message'] = "Successfully updated your cart."

    return HttpResponseRedirect(reverse('manage_cart'))


def clear_cart(request):
    user_id = request.session['user_unique_id']
    all_cart = Cart.objects.filter(user__unique_id=user_id)
    for item in all_cart:
        item.stock.amount += item.amount
        item.stock.save()
        Cart.delete(item)
    request.session['success'] = True
    request.session['success_message'] = "Successfully updated your cart."
    return HttpResponseRedirect(reverse('manage_cart'))


@ajax
@csrf_exempt
def paypal_ordered(request):
    if request.POST:
        print("POST1")
        user_id = request.POST.get('user')
        print(user_id)
        user = get_object_or_404(User, unique_id=user_id)
        print(user.first_name)
        carts = Cart.objects.filter(user=user)
        print("POST2")
        for cart in carts:
            print(cart.stock.product.name)
            cart.status = 2
            cart.save()
            print(cart.updated)

    request.session['success'] = True
    request.session['success_message'] = "Thank you for shopping with us!"
    return HttpResponseRedirect(reverse('product'))


@ajax
@csrf_exempt
def filtered(request):
    if request.POST:
        # filter_product = None
        filter_product_set = Set()
        # filter_button = request.POST.get('button_id')
        raw_filter_data = request.POST.get('data_id')
        remove_quote_filter_data = raw_filter_data.replace("\"","")
        remove_front_bracket_data = remove_quote_filter_data.replace("{","")
        remove_back_bracket_data = remove_front_bracket_data.replace("}","")
        remove_colon_bracket_data = remove_back_bracket_data.replace(":","")
        remove_size_bracket_data = remove_colon_bracket_data.replace("size","")
        remove_maxprice_bracket_data = remove_size_bracket_data.replace("maxprice","")
        remove_clear_bracket_data = remove_maxprice_bracket_data.replace("clear","")
        remove_search_bracket_data = remove_clear_bracket_data.replace("search","")
        remove_front = remove_search_bracket_data.replace("[",",")
        remove_back = remove_front.replace("]",",end")

        filter_data = remove_back.split(',')
        type = request.POST.get('type')

        if type == 0:
            universe_set = Product.objects.all()
        else:
            universe_set = Product.objects.filter(type=type)

        print "Size universe is %s"%SIZE_LIST

        print "filter data is %s"%filter_data

        for data in filter_data:
            # print data
            if data == 'null':
                continue

            elif data in SIZE_LIST:
                stock = Stock.objects.filter(size=data) # get array of filter
                stock_set = Set()

                for item in stock:
                    if str(item.product.type) == str(type):
                        stock_set.add(item.product)

                if len(filter_product_set) == 0:
                    filter_product_set.union_update(stock_set)
                else:
                    filter_product_set.intersection_update(stock_set)


            # print filter_product_list
            # print "is number? %s" % is_number(data)
            elif is_number(data):
                product = universe_set.filter(price__lte=float(data))
                product_set = Set(product)
                if len(filter_product_set) == 0:
                    filter_product_set.union_update(product_set)
                else:
                    filter_product_set.intersection_update(product_set)

            elif data == 'c1':
                filter_product_set = universe_set
                break

            elif data == 's1':
                brand = request.POST.get('brand')

                product = universe_set.filter(brand=brand)
                product_set = Set(product)
                if len(filter_product_set) == 0:
                    filter_product_set.union_update(product_set)
                else:
                    filter_product_set.intersection_update(product_set)
            elif data == 'sex':
                temp_set = set()
                num = 5
                while True:
                    if filter_data[num] in SEX_LIST:
                        sex = what_sex(filter_data[num])
                        temp_set.update(Set(universe_set.filter(sex=sex)))
                        num+=1
                    elif filter_data[num] == 'end':
                        if len(filter_product_set) == 0:
                            filter_product_set.union_update(temp_set)
                        else:
                            filter_product_set.intersection_update(temp_set)
                        break
                    else:
                        num+=1
                        break

            elif data == 'brand':
                temp_set = set()
                num+=2
                key = value_to_key(type)
                while True:
                    if filter_data[num] in get_all_brand(key):
                        temp_set.update(Set(universe_set.filter(brand=filter_data[num])))
                        num+=1
                    elif filter_data[num] == 'end':
                        if len(filter_product_set) == 0:
                            filter_product_set.union_update(temp_set)
                        else:
                            filter_product_set.intersection_update(temp_set)
                        break
                    else:
                        num+=1
                        break

        if filter_data[0] == 'null' and filter_data[1] == 'null' and filter_data[5] == '' and filter_data[8] == '' and filter_data[3] != 's1':
            filter_product_set = universe_set

        print "filtered product is %s"%filter_product_set

        template = loader.get_template('pages/product/item/product_item.html')
        context = Context({'product_list': filter_product_set})
        rendered = template.render(context)

        return {'result': True, 'rendered': rendered}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def what_sex(sex):
    if sex == 'Men':
        return 1
    elif sex == 'Women':
        return 2
    elif sex == 'Unisex':
        return 3