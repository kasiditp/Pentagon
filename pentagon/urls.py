from django.conf.urls import include, url
from django.contrib import admin

from product.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'pentagon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('base.urls', namespace='home')),
    url(r'^product/', include('product.urls', namespace='product')),
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^cart/$', manage_cart, name='manage_cart'),
    url(r'^remove_cart/$', remove_from_cart, name='remove_from_cart')
]
