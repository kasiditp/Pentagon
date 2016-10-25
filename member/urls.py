from django.conf.urls import include, url

from member.views import *

urlpatterns = [
    url(r'^login', login_view, name='login_view')
]
