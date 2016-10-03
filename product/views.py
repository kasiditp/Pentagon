from django.shortcuts import render

# Create your views here.
from product.models import Product


def product_view(request) :
    product_list = Product.objects.all()

    context = {
        'product_list' : product_list
    }

    return render(request, "product/product.html", context)

# type brand search

