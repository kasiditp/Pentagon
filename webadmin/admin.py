from django.contrib import admin
from webadmin.models import *
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = 'order' , 'payment_image'

admin.site.register(Transaction,TransactionAdmin)
