from django.shortcuts import render
from django.views.generic import ListView

from .models import GeneratePage

# Create your views here.


class Home(ListView):
    template_name = "home.html"
    model = GeneratePage
