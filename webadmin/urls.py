from django.conf.urls import url

from admin.views import *

urlpatterns = [
    url(r'^$', admin_product_view, name="admin_product_view"),
    url(r'^add_new_product/$', add_new_product, name="add_new_product")
]
