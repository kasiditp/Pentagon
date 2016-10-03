from django.conf.urls import include,url

from product.views import *

urlpatterns = {
    url(r'^$', product_view, name="product_view")
}