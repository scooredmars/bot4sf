from django.contrib import admin

from .models import FaqList, PermissionList, Plan

# Register your models here.

admin.site.register(PermissionList)
admin.site.register(Plan)
admin.site.register(FaqList)
