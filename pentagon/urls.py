from django.conf.urls import include, url
from django.contrib import admin

from base.views import search_redirect
from member.views import login_view
from product.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'pentagon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('base.urls', namespace='home')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^product/', include('product.urls', namespace='product')),
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^admin_page/', include('webadmin.urls', namespace='webadmin')),
    url(r'^cart/', manage_cart, name='manage_cart'),
    url(r'^remove_cart/', remove_from_cart, name='remove_from_cart'),
    url(r'^update_cart_amount/', update_cart_amount, name='update_cart_amount'),
    url(r'^clear_cart/', clear_cart, name='clear_cart'),
    url(r'^checkout/', order_checkout, name="checkout"),
    url(r'^login', login_view, name='login_view'),
<<<<<<< HEAD
    url(r'^search_redirect/$', search_redirect, name='search_redirect')
=======
    url(r'^purchase_complete/', purchase_complete, name="purchase_complete"),
    # url(r'^webadmin/', include(admin.site.urls)),
>>>>>>> master
]
