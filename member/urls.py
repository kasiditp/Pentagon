from django.conf.urls import url

from  member.views import *

urlpatterns = [
    url(r'^register/$', register_view, name="register_view"),
    url(r'^add/$', add_new_user, name="add_new_user"),
    url(r'^change_password/$', change_password, name="change_password"),
    url(r'^change_general/$', change_general, name="change_general"),
    url(r'^profile/$', profile_view, name="profile_view"),
    url(r'^success/$', success, name="success_page"),
]

