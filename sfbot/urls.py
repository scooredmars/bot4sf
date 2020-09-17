from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="index"),
    path("dashboard", views.dashboard_add_bot_view, name="dashboard"),
    path("<int:pk>", views.SettingsView.as_view(), name="settings"),
    path("<int:pk>", views.UserBotDetails.as_view(), name="bot-detail"),
    path("edit/<int:pk>", views.EditBotDetails.as_view(), name="edit-bot"),
    path("profile", views.profile_view, name="profile"),
    path("shop", views.shop_view, name="shop"),
    path("faq", views.Faq.as_view(), name="faq"),
    path("regulations", views.Regulations.as_view(), name="regulations"),
    path("privacy-policy", views.PrivacyPolicy.as_view(), name="privacy-policy"),
]
