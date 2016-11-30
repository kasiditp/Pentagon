# coding=utf8
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from member.models import User, SEX
from product.models import Cart, Product, PRODUCT_TYPE

# from product.views import product_details

SEX_LIST = ['Men', 'Women', 'Unisex']
PRODUCT_TYPES = {
    "all": 0,
    "top": 1,
    "bottom": 2,
    "overall": 3,
    "footwear": 4,
    "accessory": 5
}


def index(request):
    return render(request, 'pages/base/home.html', get_nav_context(request))


def get_nav_context(request):
    if 'is_login' in request.session and request.session['is_login']:
        member_user = User.objects.filter(unique_id=request.session['user_unique_id'])[0]
        product = Product.objects.all()
        print product
        context = {
            'is_login': request.session['is_login'],
            'user': member_user,
            'product_amount': Cart.objects.filter(user_id=member_user).count,
            'top': "top",
            'product': product
        }
        return context
    else:
        product = Product.objects.all()
        context = {
            'is_login': False,
            'user': 000000,
            'product_amount': None,
            'product': product
        }
        return context


@ajax
@csrf_exempt
def search_redirect(request):
    name = request.POST['product_name']
    product = Product.objects.filter(name=name)[0]

    return HttpResponseRedirect(reverse('product:product_details', kwargs={'product_id':product.id}))