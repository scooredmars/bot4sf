from django.contrib import admin

from .models import AcSettings, Bots, FaqList, GameSettings, PermissionList, Plan

# Register your models here.

admin.site.register(PermissionList)
admin.site.register(Plan)
admin.site.register(FaqList)
admin.site.register(Bots)
admin.site.register(AcSettings)
admin.site.register(GameSettings)
