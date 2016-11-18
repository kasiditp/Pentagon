from django.conf.urls import url

from product.views import *

urlpatterns = [
    url(r'^$', product_view, name="product_view"),
    url(r'^(?P<product_id>[0-9]+)/$', product_details, name="product_details"),
    url(r'^filtered/$', filtered, name="filtered"),
    url(r'^get_brand/$', get_brand, name="get_brand"),
    url(r'^put_in_cart/$', put_in_cart, name="put_in_cart"),
    url(r'^(?P<product_type>[\w]+)/$', product_type_view, name="product_type")

]

