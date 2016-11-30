from django.conf.urls import url

from product.views import *

urlpatterns = [
    url(r'^$', product_view, name="product_view"),
    url(r'^(?P<product_id>[0-9]+)/$', product_details, name="product_details"),
    url(r'^filtered/$', filtered, name="filtered"),
    url(r'^change_page/$', change_page, name="change_page"),
    url(r'^get_product_stock', get_product_stock, name="get_product_stock"),
    url(r'^put_in_cart_by_simulate', put_in_cart_by_simulate, name="put_in_cart_by_simulate"),
    url(r'^get_brand/$', get_brand, name="get_brand"),
    url(r'^put_in_cart/$', put_in_cart, name="put_in_cart"),
    url(r'^admin_product_view/$', admin_product_view, name="admin_product_view"),
    url(r'^add_new_product/$', add_new_product, name="add_new_product"),
    url(r'^simulate/$', simulate_view, name="simulate_view"),
    url(r'^(?P<product_type>[\w]+)/$', product_type_view, name="product_type"),


]