import random
import string
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
from product.models import *
from webadmin.views import create_transaction

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
    if len(product_list) > 8:
        num_page = (len(product_list)/8) + 1
        product_list = product_list[0:8]
    else:
        num_page = 1

    context = {
        'product_list': product_list,
        'max_price': max_price,
        'min_price': min_price,
        'brands': brands,
        'type': PRODUCT_TYPES['all'],
        'num_page': range(num_page),
        'all_page': num_page

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
        if len(product_list) > 8:
            num_page = (len(product_list) / 8) + 1
            product_list = product_list[0:8]
        else:
            num_page = 1

        context = {
            'product_list': product_list,
            'max_price': max_price,
            'min_price': min_price,
            'brands': brands,
            'type': PRODUCT_TYPES[product_type],
            'size_universe': size_universe,
            'num_page': range(num_page),
            'all_page': num_page
        }
        context.update(get_nav_context(request))
        return render(request, 'pages/product/product.html', context)
    else:
        return HttpResponse(reverse('product_view'))


def simulate_view(request):
    simulate_list_top = Product.objects.filter(type=PRODUCT_TYPES["top"])
    simulate_list_brand_top = get_all_brand('top')
    simulate_list_bottom = Product.objects.filter(type=PRODUCT_TYPES["bottom"])
    simulate_list_brand_bottom = get_all_brand('bottom')
    context = {
        'simulate_list_top': simulate_list_top,
        'simulate_list_bottom': simulate_list_bottom,
        'simulate_list_brand_top': simulate_list_brand_top,
        'simulate_list_brand_bottom': simulate_list_brand_bottom
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/simulate/simulate.html',context)


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
    else:
        brand_universe = Product.objects.all()

    for product in brand_universe:
        brand.add(product.brand)

    return brand


def value_to_key(type):
    if type == '0' or type == 0:
        return 'all'
    elif type == '1' or type == 1:
        return 'top'
    elif type == '2' or type == 2:
        return 'bottom'
    elif type == '3' or type == 3:
        return 'overall'
    elif type == '4' or type == 4:
        return 'footwear'
    elif type == '5' or type == 5:
        return 'accessory'
    else:
        return 'error'


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    images = product.get_all_image()
    stocks = product.get_stocks()
    no_stock = False
    if stocks.__len__() == 0:
        no_stock = True
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
        'no_stock': no_stock,
    }
    context.update(get_nav_context(request))
    return render(request, 'pages/productdetails/details.html', context)


def put_in_cart(request):
    product_id = request.POST['product_id']
    stock_id = request.POST['size_select']
    user_unique_id = request.session['user_unique_id']
    print product_id
    # product = get_object_or_404(Product, pk=product_id)
    stock = get_object_or_404(Stock, pk=stock_id)
    user = get_object_or_404(User, unique_id=user_unique_id)
    if stock.amount <= 0:
        request.session['error'] = True
        request.session['error_message'] = "There is something wrong putting this item into your cart. Please check again"
        return HttpResponseRedirect(reverse('product:product_details', args=[product_id]))
    else:
        cart_check = Cart.objects.filter(stock=stock, user=user, status=0)
        if cart_check.__len__() < 1:
            new_cart_item = Cart(user=user, stock=stock, amount=1, status=0, invoice_number=None)
            new_cart_item.save()
        else:
            for cart in cart_check:
                cart.amount += 1
                cart.save()

        stock.amount -= 1
        stock.save()

        request.session['success'] = True
        request.session['success_message'] = "Done! Successfully added this item into your cart."
        return HttpResponseRedirect(reverse('product:product_details', args=[product_id]))


@ajax
@csrf_exempt
def put_in_cart_by_simulate(request):
    if request.POST:
        user_unique_id = request.session['user_unique_id']
        user = get_object_or_404(User,unique_id=user_unique_id)
        if request.POST.get('top_stock_id') != 'null':
            top_stock_id = request.POST.get('top_stock_id')
            top_stock = get_object_or_404(Stock, pk=top_stock_id)
            if top_stock.amount <= 0:
                print "Do nothing"
            else:
                new_cart_item = Cart(user=user, stock=top_stock, amount=1, status=0, invoice_number=None)
                new_cart_item.save()
                top_stock.amount -=1
                top_stock.save()

        if request.POST.get('bottom_stock_id') != 'null':
            bottom_stock_id = request.POST.get('bottom_stock_id')
            bottom_stock = get_object_or_404(Stock, pk=bottom_stock_id)
            if bottom_stock.amount <= 0:
                print "Do nothing"
            else:
                new_cart_item = Cart(user=user, stock=bottom_stock, amount=1, status=0, invoice_number=None)
                new_cart_item.save()
                bottom_stock.amount -=1
                bottom_stock.save()
        if request.POST.get('top_stock_id') == 'null' and request.POST.get('bottom_stock_id') == 'null':
            return {'Fail': True }
        return HttpResponseRedirect(reverse('manage_cart'))


def manage_cart(request):
    user_id = request.session['user_unique_id']
    cart_items = []
    cart = Cart.objects.filter(user__unique_id=user_id, status=0)
    # for item in cart:
    #     stock = get_object_or_404(Stock, pk=item.stock)
    #     cart_items.append(stock)
    total_price = Cart.get_total_price_in_cart(user_id)
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
    carts = Cart.objects.filter(user=user, status=0)
    total_price = Cart.get_total_price_in_cart(user_id)
    context = {
        'user': user,
        'carts': carts,
        'total_price': total_price,
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
    all_cart = Cart.objects.filter(user__unique_id=user_id, status=0)
    for item in all_cart:
        item.stock.amount += item.amount
        item.stock.save()
        Cart.delete(item)
    request.session['success'] = True
    request.session['success_message'] = "Successfully updated your cart."
    return HttpResponseRedirect(reverse('manage_cart'))


def purchase_complete(request):
    context = {}
    context.update(get_nav_context(request))
    return render(request, 'pages/cart/purchase_complete.html', context)


def transfer_ordered(request):
    user_id = request.session.get('user_unique_id')
    shipment = request.POST.get('shipment')
    user = get_object_or_404(User, unique_id=user_id)
    carts = Cart.objects.filter(user=user, status=0)
    trans_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    for cart in carts:
        print(cart.stock.product.name)
        cart.status = 1
        cart.invoice_number = trans_id
        cart.shipment = shipment
        cart.save()
    create_transaction()
    return HttpResponseRedirect(reverse('purchase_complete'))

@ajax
@csrf_exempt
def paypal_ordered(request):
    if request.POST:
        print("POST1")
        user_id = request.POST.get('user')
        shipment = request.POST.get('shipment')
        print(user_id)
        user = get_object_or_404(User, unique_id=user_id)
        print(user.first_name)
        carts = Cart.objects.filter(user=user, status=0)
        trans_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        print("POST2")
        for cart in carts:
            print(cart.stock.product.name)
            cart.status = 3
            cart.invoice_number = trans_id
            cart.shipment = shipment
            cart.save()
            print(cart.updated)
        create_transaction()

    return HttpResponseRedirect(reverse('purchase_complete'))


@ajax
@csrf_exempt
def change_page(request):
    if request.POST:
        type = request.POST.get('type')
        if int(type) == 0:
            product_list = Product.objects.all()
        else:
            product_list = filter_by_value(request.POST.get('data_id'), int(type), request.POST.get('brand'))
        num_page = request.POST.get('page')
        all_page = request.POST.get('all_page')
        if len(product_list) - int(num_page)*8 >= 0:
            product_list = product_list[(int(num_page)-1)*8:(int(num_page)-1)*8+8]
        else:
            product_list = product_list[(int(num_page)-1)*8:]

        template = loader.get_template('pages/product/item/product_item.html')
        context = Context({
            'product_list': product_list,
            'num_page': range(int(all_page))
        })
        rendered = template.render(context)
        return {'result': True, 'rendered': rendered}


@ajax
@csrf_exempt
def get_product_stock(request):
    if request.POST:
        return_list = []
        stock_id_list = []
        product_name = request.POST.get('name')
        product = Product.objects.filter(name=product_name)
        if product is None:
            return {'result': False}
        stock_list = Stock.objects.filter(product=product).order_by('-size')

        for stock in stock_list:
            return_list.append(stock.size)
            stock_id_list.append(stock.id)

        return {'result': True, 'content' : return_list, 'stock_id': stock_id_list }


@ajax
@csrf_exempt
def filtered(request):
    if request.POST:
        filter_product_set = filter_by_value(request.POST.get('data_id'),request.POST.get('type'),request.POST.get('brand'))
        if len(filter_product_set) > 8:
            num_page = (len(filter_product_set) / 8) + 1
            filter_product_set = filter_product_set[0:8]
        else:
            num_page = 1

        template = loader.get_template('pages/product/item/product_item.html')
        context = Context({
            'product_list': filter_product_set,
            'num_page': range(num_page)
        })
        rendered = template.render(context)

        return {'result': True, 'rendered': rendered}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def filter_by_value(filter, type, brand):
    # filter_product = None
    filter_product_set = Set()
    # filter_button = request.POST.get('button_id')
    raw_filter_data = filter
    remove_quote_filter_data = raw_filter_data.replace("\"", "")
    remove_front_bracket_data = remove_quote_filter_data.replace("{", "")
    remove_back_bracket_data = remove_front_bracket_data.replace("}", "")
    remove_colon_bracket_data = remove_back_bracket_data.replace(":", "")
    remove_size_bracket_data = remove_colon_bracket_data.replace("size", "")
    remove_maxprice_bracket_data = remove_size_bracket_data.replace("maxprice", "")
    remove_clear_bracket_data = remove_maxprice_bracket_data.replace("clear", "")
    remove_search_bracket_data = remove_clear_bracket_data.replace("search", "")
    remove_front = remove_search_bracket_data.replace("[", ",")
    remove_back = remove_front.replace("]", ",end")

    filter_data = remove_back.split(',')
    type = type

    if type == 0:
        universe_set = Product.objects.all()
    else:
        universe_set = Product.objects.filter(type=type)

    for data in filter_data:
        if data == 'null':
            continue

        elif data in SIZE_LIST:
            stock = Stock.objects.filter(size=data)  # get array of filter
            stock_set = Set()

            for item in stock:
                if str(item.product.type) == str(type):
                    stock_set.add(item.product)

            if len(filter_product_set) == 0:
                filter_product_set.union_update(stock_set)
            else:
                filter_product_set.intersection_update(stock_set)

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
                    num += 1
                elif filter_data[num] == 'end':
                    if len(filter_product_set) == 0:
                        filter_product_set.union_update(temp_set)
                    else:
                        filter_product_set.intersection_update(temp_set)
                    break
                else:
                    num += 1
                    break

        elif data == 'brand':
            temp_set = set()
            num += 2
            key = value_to_key(int(type))
            while True:
                if filter_data[num] in get_all_brand(key):
                    temp_set.update(Set(universe_set.filter(brand=filter_data[num])))
                    num += 1
                elif filter_data[num] == 'end':
                    if len(filter_product_set) == 0:
                        filter_product_set.union_update(temp_set)
                    else:
                        filter_product_set.intersection_update(temp_set)
                    break
                else:
                    num += 1
                    break

    if filter_data[0] == 'null' and filter_data[1] == 'null' and filter_data[5] == '' and filter_data[8] == '' and filter_data[3] != 's1':
        filter_product_set = universe_set

    filter_product_set = list(filter_product_set)
    return filter_product_set


def what_sex(sex):
    if sex == 'Men':
        return 1
    elif sex == 'Women':
        return 2
    elif sex == 'Unisex':
        return 3


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
