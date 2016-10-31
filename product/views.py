from sets import Set

from django.db.models import Max
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context

from member.models import User
from product.models import Product, PRODUCT_TYPE, SEX, ProductImage, Stock, Cart

SIZE_LIST = ['S', 'M', 'L', 'XL', 'XXL']
SEX_LIST = ['Men','Women','Unisex']
num = 0

def product_view(request):
    product_list = Product.objects.all()
    max_price = Product.objects.all().aggregate(Max('price'))
    brands = get_all_brand()
    context = {
        'product_list': product_list,
        'max_price': max_price,
        'brands' : brands
    }

    return render(request, 'pages/product/product.html', context)

@ajax
@csrf_exempt
def get_brand(request):
    brand = set()
    for product in Product.objects.all():
        brand.add(product.brand)

    return {'brand' : brand}

def get_all_brand():
    brand = set()
    for product in Product.objects.all():
        brand.add(product.brand)

    return brand



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

    return render(request, 'pages/productdetails/details.html', context)


def put_in_cart(request):
    product_id = request.POST['product_id']
    stock_id = request.POST['size_select']
    user_id = 1 #request.session.get('user')
    product = get_object_or_404(Product, pk=product_id)
    stock = get_object_or_404(Stock, pk=stock_id)
    user = get_object_or_404(User, pk=user_id)
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

        print filter_data

        for data in filter_data:
            # print data
            if data == 'null':
                continue

            elif data in SIZE_LIST:
                stock = Stock.objects.filter(size=data) # get array of filter
                stock_set = Set()
                for item in stock:
                    stock_set.add(item.product)

                if len(filter_product_set) == 0:
                    filter_product_set.union_update(stock_set)
                else:
                    filter_product_set.intersection_update(stock_set)


            # print filter_product_list
            # print "is number? %s" % is_number(data)
            elif is_number(data):
                product = Product.objects.filter(price__lte=float(data))
                product_set = Set(product)
                if len(filter_product_set) == 0:
                    filter_product_set.union_update(product_set)
                else:
                    filter_product_set.intersection_update(product_set)

            elif data == 'c1':
                filter_product_set = Product.objects.all()
                break

            elif data == 's1':
                brand = request.POST.get('brand')

                product = Product.objects.filter(brand=brand)
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
                        temp_set.update(Set(Product.objects.filter(sex=sex)))
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
                while True:
                    if filter_data[num] in get_all_brand():
                        temp_set.update(Set(Product.objects.filter(brand=filter_data[num])))
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


        # print filter_product_set
        template = loader.get_template('pages/product/item/product_item.html')
        context = Context({'product_list': filter_product_set})
        rendered = template.render(context)

        return {'result': True, 'rendered': rendered}

        # --------------------------

        # if filter_button in SIZE_LIST:
        #     print "Size"
        #     stock = Stock.objects.filter(size=filter_button)
        #     for item in stock :
        #         filter_product = []
        #         filter_product.append(item.product)
        #     print filter_product
        # print "is number? %s" % is_number(filter_button)
        # if is_number(filter_button):
        #     filter_product = Product.objects.filter(price__lte=float(filter_button))
        #
        # if filter_button == 'clear':
        #     filter_product = Product.objects.all()
        #
        # if filter_button == 'search':
        #     brand = request.POST.get('brand')
        #     filter_product = Product.objects.filter(brand=brand)
        #
        #
        # template = loader.get_template('pages/product/item/product_item.html')
        # context = Context({'product_list': filter_product})
        # rendered = template.render(context)
        #
        # return {'result': True, 'rendered': rendered}

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
