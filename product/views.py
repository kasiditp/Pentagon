from django.shortcuts import render, get_object_or_404


# Create your views here.
from product.models import Product


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'pages/productdetails/details.html', context)
