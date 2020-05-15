from django.contrib import admin

from .models import Bots, FaqList, PermissionList, Plan, Profile

# Register your models here.

admin.site.register(PermissionList)
admin.site.register(Plan)
admin.site.register(FaqList)
admin.site.register(Bots)
admin.site.register(Profile)
