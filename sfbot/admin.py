from django.contrib import admin

from .models import PermissionList, Plan

# Register your models here.

admin.site.register(PermissionList)
admin.site.register(Plan)
