from django.contrib import admin
from django.urls import include, path
from sfbot.views import MyPasswordChangeView

handler404 = "sfbot.views.error_404"

handler500 = "sfbot.views.error_500"

handler403 = "sfbot.views.error_404"

handler400 = "sfbot.views.error_404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("sfbot.urls", "sfbot"))),
    path("password/change/", MyPasswordChangeView.as_view(),
         name="account_change_password"),
    path("", include("allauth.urls")),
]
