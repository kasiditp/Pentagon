from django.contrib import admin

# Register your models here.
from member.models import User


class UserAdmin(admin.ModelAdmin) :
    list_display = ('id', 'unique_id', 'username', 'password', 'email', 'sex', 'birth_date', 'first_name', 'last_name')
    search_fields = ['first_name']


admin.site.register(User, UserAdmin)
