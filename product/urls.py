from django.conf.urls import include, url
from django.contrib import admin

from product.views import product_details

urlpatterns = [
    # Examples:
    # url(r'^$', 'pentagon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<product_id>[0-9]+)/$', product_details, name="product_details")
]
