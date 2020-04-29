from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="index"),
    path("dashboard", views.Dashboard.as_view(), name="dashboard"),
    path("profile", views.Profile.as_view(), name="profile"),
    path("shop", views.Shop.as_view(), name="shop"),
    path("faq", views.Faq.as_view(), name="faq"),
    path("contact", views.contact, name="contact"),
]
