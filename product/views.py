from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django_ajax.decorators import ajax
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from product.models import Product, PRODUCT_TYPE, SEX, ProductImage

SIZE_LIST = ['S', 'M', 'L', 'XL', 'XXL']


def product_view(request):
    product_list = Product.objects.all()
    max_price = Product.objects.all().aggregate(Max('price'))

    context = {
        'product_list': product_list,
        'max_price': max_price,
    }

    return render(request, 'pages/product/product.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    images = product.get_all_image()

    sex = SEX[(product.sex - 1)][1]
    product_type = PRODUCT_TYPE[(product.type - 1)][1]
    # print sex
    context = {
        'product': product,
        'sex': sex,
        'type': product_type,
        'images': images
    }
    return render(request, 'pages/productdetails/details.html', context)


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