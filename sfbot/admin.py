from django.contrib import admin

from .models import Bots, FaqList, PermissionList, Plan, Profile

admin.site.register(FaqList)


@admin.register(Bots)
class BotsAdmin(admin.ModelAdmin):
    list_display = ("profile", "username", "country", "server", "status")
    list_filter = ("profile", "server")
    search_fields = ["username", "profile__user__username"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "plan")
    list_filter = ["plan"]
    search_fields = ["user__username"]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "max_time", "max_bots")


@admin.register(PermissionList)
class PermissionListAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "description")
    list_filter = ["icon"]
