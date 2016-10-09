from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'pentagon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('base.urls', namespace='home')),
    url(r'^product/', include('product.urls', namespace='product')),
    url(r'^member/', include('member.urls', namespace='member')),
]
