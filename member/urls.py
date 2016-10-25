from django.conf.urls import url

from  member.views import *

urlpatterns = [
    url(r'^register/$', register_view, name="register_view"),
    url(r'^add/$', add_new_user, name="add_new_user"),
    url(r'^profile/$', profile_view, name="profile_view"),
    url(r'^success/$', success, name="success_page"),
    url(r'^login/$', login, name="login"),
]