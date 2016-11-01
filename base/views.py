# coding=utf8
from django.shortcuts import render

# Create your views here.
from member.models import User
from product.models import Cart


def index(request):
    return render(request, 'pages/base/home.html', get_nav_context(request))


def get_nav_context(request):
    member_user = User.objects.filter(unique_id=request.session['user_unique_id'])[0]
    context = {
        'is_login': request.session['is_login'],
        'user': User.objects.filter(unique_id=request.session['user_unique_id'])[0],
        'product_amount': Cart.objects.filter(user_id=member_user).count
    }
    return context