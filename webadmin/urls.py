from django.conf.urls import url

from webadmin.views import *

urlpatterns = [
    url(r'^$', admin_product, name="admin_product"),
    url(r'^add_new_product/$', add_new_product, name="add_new_product"),
]
