from django.conf.urls import url

from  member.views import *

urlpatterns = [
    url(r'^register/$', register_view, name="register_view"),

]

