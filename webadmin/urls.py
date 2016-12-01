from django.conf.urls import url

from webadmin.views import *

urlpatterns = [
    url(r'^$', admin_product, name="admin_product"),
    url(r'^home/$', admin_home, name="admin_home"),
    url(r'^add_new_product/$', add_new_product, name="add_new_product"),
    url(r'^admin_all_product/$', admin_all_product, name="admin_all_product"),
    url(r'^accept_transaction/$', accept_transaction, name="accept_transaction"),
    url(r'^reject_transaction/$', reject_transaction, name="reject_transaction"),
    url(r'^admin_transaction/$', admin_transaction, name="admin_transaction"),
    url(r'^enter_delivery_code/$', enter_delivery_code, name="enter_delivery_code"),
    url(r'^add_product_images/$', add_product_images, name='add_product_images'),
    url(r'^edit_product/(?P<product_id>[0-9]+)/$', edit_product, name="edit_product"),
    url(r'^update_product/$', update_product, name='update_product'),
    url(r'^edit_product_images/$', edit_product_images, name='edit_product_images'),
    url(r'^delete_product/(?P<product_id>[0-9]+)/$', delete_product, name='delete_product'),
]
