from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class AcountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','date_joined','is_active')
    list_display_links=('email','first_name','last_name','username','date_joined','is_active')
    readonly_fields=('date_joined',)
    ordering=('date_joined',)
    fieldsets=()
    list_filter=()
    filter_horizontal=()
admin.site.register(Account,AcountAdmin)
