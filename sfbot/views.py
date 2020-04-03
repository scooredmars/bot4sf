from django.shortcuts import render
from django.views.generic import ListView

from .models import GeneratePage, PermissionList, Plan

# Create your views here.


class Home(ListView):
    template_name = "home.html"
    model = GeneratePage


class Dashboard(ListView):
    template_name = "user/dashboard.html"
    model = GeneratePage


class Shop(ListView):
    template_name = "user/shop.html"
    model = Plan
    context_object_name = "plans"
