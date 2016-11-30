from django.conf.urls import url

from webadmin.views import *

urlpatterns = [
    url(r'^$', admin_product, name="admin_product"),
    url(r'^add_new_product/$', add_new_product, name="add_new_product"),
    url(r'^admin_all_product/$', admin_all_product, name="admin_all_product"),
    url(r'^accept_transaction/$', accept_transaction, name="accept_transaction"),
    url(r'^reject_transaction/$', reject_transaction, name="reject_transaction"),
    url(r'^admin_transaction/$', admin_transaction, name="admin_transaction"),
    url(r'^add_product_images/$', add_product_images, name='add_product_images'),

]
