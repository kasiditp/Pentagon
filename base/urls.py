from django.conf.urls import include, url

from base.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'pentagon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name='index')

]
