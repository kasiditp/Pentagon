from django.conf.urls import url

from product.views import *

urlpatterns = [
    url(r'^$', product_view, name="product_view"),
    url(r'^(?P<product_id>[0-9]+)/$', product_details, name="product_details"),
    url(r'^filtered/$', filtered, name="filtered"),
    url(r'^put_in_cart/$', put_in_cart, name="put_in_cart"),

]

