from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .forms import AddBotForm, ContactForm, SettingsForm
from .models import Bots, FaqList, GeneratePage, Plan, Profile

# Create your views here.


class Home(ListView):
    template_name = "home.html"
    model = GeneratePage


class Dashboard(ListView):
    template_name = "user/dashboard.html"
    model = Bots
    context_object_name = "bots"

    def get_queryset(self):
        return Bots.objects.filter(profile__user=self.request.user)


class ProfileView(ListView):
    template_name = "user/profile.html"
    model = Bots
    context_object_name = "bots"

    def get_queryset(self):
        return Bots.objects.filter(profile__user=self.request.user)


class AddBot(CreateView):
    template_name = "user/add_bot.html"
    model = Bots
    form_class = AddBotForm

    def form_valid(self, form):
        current_user = Profile.objects.filter(user=self.request.user)
        if current_user:
            obj = form.save(commit=False)
            obj.profile = Profile.objects.get(user=self.request.user) # Set current user profile
            current_plan = Plan.objects.get(profile=obj.profile)
            plan_max_time = current_plan.max_time
            obj.time_left = plan_max_time
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            starter_plan = Plan.objects.get(name="FOR BEGINNERS")
            user_profile = Profile(user=self.request.user, plan=starter_plan)
            user_profile.save()
            
            obj = form.save(commit=False)
            obj.profile = Profile.objects.get(user=self.request.user) # Set current user profile
            current_plan = Plan.objects.get(profile=obj.profile)
            plan_max_time = current_plan.max_time
            obj.time_left = plan_max_time
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())


class SettingsView(UpdateView):
    template_name = "user/settings.html"
    model = Bots
    form_class = SettingsForm
    success_url = "dashboard"

    def get_queryset(self):
        return Bots.objects.filter(profile__user=self.request.user)


class UserDetail(DetailView):
    model = Bots 

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
