from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("sfbot.urls", "sfbot"))),
    path("", include("allauth.urls")),
]
