from django.conf.urls import url

from webadmin.views import *

urlpatterns = [
    url(r'^$', admin_product, name="admin_product"),
    url(r'^add_new_product/$', add_new_product, name="add_new_product"),
    url(r'^admin_all_product/$', admin_all_product, name="admin_all_product"),
]
