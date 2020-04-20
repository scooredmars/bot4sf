from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .forms import ContactForm
from .models import Bots, FaqList, GeneratePage, Plan

# Create your views here.


class Home(ListView):
    template_name = "home.html"
    model = GeneratePage


class Dashboard(ListView):
    template_name = "user/dashboard.html"
    model = Bots
    context_object_name = "bots"

    def get_queryset(self):
        return Bots.objects.filter(user=self.request.user)


class Shop(ListView):
    template_name = "user/shop.html"
    model = Plan
    context_object_name = "plans"


class Faq(ListView):
    template_name = "user/faq.html"
    model = FaqList
    context_object_name = "faqs"


def contact(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data["message"]
            try:
                send_mail(subject, message, from_email, ["support@sfbot.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
    return render(request, "user/contact.html", {"form": form})
