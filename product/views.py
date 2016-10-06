from django.db.models import Max
from django.shortcuts import render, get_object_or_404



# Create your views here.
from product.models import Product, PRODUCT_TYPE, SEX, ProductImage


def product_view(request):
    product_picture = ProductImage.objects.all()
    product_list = Product.objects.all()
    max_price = Product.objects.all().aggregate(Max('price'))

    context = {
        'product_list': product_list,
        'max_price': max_price,
    }

    return render(request, 'pages/product/product.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sex = SEX[(product.sex - 1)][1]
    product_type = PRODUCT_TYPE[(product.type - 1)][1]
    #print sex
    context = {
        'product': product,
        'sex': sex,
        'type': product_type
    }
    return render(request, 'pages/productdetails/details.html', context)
