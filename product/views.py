from django.shortcuts import render, get_object_or_404


# Create your views here.
from product.models import Product, SEX, PRODUCT_TYPE


def product_view(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list,
    }

    return render(request, 'pages/product/product.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sex = SEX[product.sex - 1][1]
    type = PRODUCT_TYPE[product.type - 1][1]
    context = {
        'product': product,
        'sex': sex,
        'type': type
    }
    return render(request, 'pages/productdetails/details.html', context)
