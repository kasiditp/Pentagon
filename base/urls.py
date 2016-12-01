from django.conf.urls import include, url

from base.views import *

urlpatterns = [
    url(r'^$', index, name='index'),

]
