from django.contrib import admin

from .models import Bots, FaqList, PermissionList, Plan, Profile, Currency, Orders

admin.site.register(FaqList)


@admin.register(Bots)
class BotsAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "username",
        "country",
        "server",
        "status",
        "time_left",
        "converted_time",
    )
    list_filter = ("profile", "server", "status")
    search_fields = ["username", "profile__user__username"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "wallet")
    list_filter = ["plan"]
    search_fields = ["user__username"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("price", "value")


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("profile", "order_create", "currency_package")
    list_filter = ["profile", "order_create", "currency_package"]
    search_fields = ["profile"]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "max_time", "max_bots")


@admin.register(PermissionList)
class PermissionListAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "description")
    list_filter = ["icon"]
