from allauth.account.views import PasswordChangeView
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .forms import AddBotForm, ContactForm, SettingsForm
from .models import Bots, FaqList, GeneratePage, Plan, Profile, User

# Create your views here.


class Home(ListView):
    template_name = "home.html"
    model = GeneratePage


def dashboard(request):
    bots_q = Bots.objects.all()
    user_bots = bots_q.filter(profile__user=request.user)
    current_user = Profile.objects.filter(user=request.user)

    if current_user:
        pass
    else:
        starter_plan = Plan.objects.get(name="FOR BEGINNERS")
        user_profile = Profile(user=request.user, plan=starter_plan)
        user_profile.save()

    amount_user_bots = user_bots.count()
    current_plan_q = Plan.objects.get(
        profile=(Profile.objects.get(user=request.user)))
    if amount_user_bots >= current_plan_q.max_bots:
        lock_add = True
    else:
        lock_add = False

    context = {
        "user_bots": user_bots,
        "lock_add": lock_add,
    }

    return render(request, "user/dashboard.html", context)


class ProfileView (ListView):
    template_name = "user/profile.html"
    model = Bots
    context_object_name = "user_info"

    def get_queryset(self):
        current_user = Profile.objects.filter(user=self.request.user)

        if current_user:
            max_user_bots = Bots.objects.filter(
                profile__user=self.request.user).count()
            if max_user_bots != 0:
                return Bots.objects.filter(profile__user=self.request.user)
            else:
                return User.objects.filter(username=self.request.user)
        else:
            return User.objects.filter(username=self.request.user)


class AddBot(CreateView):
    template_name = "user/add_bot.html"
    model = Bots
    form_class = AddBotForm

    def form_valid(self, form):
        # check if user profile is created
        current_user = Profile.objects.filter(
            user=self.request.user)

        if current_user:
            # amount of all bots for current user
            max_user_bots = Bots.objects.filter(
                profile__user=self.request.user).count()
            # acces to user current plan query
            current_plan_q = Plan.objects.get(profile=(Profile.objects.get(
                user=self.request.user)))
            if max_user_bots < current_plan_q.max_bots:
                obj = form.save(commit=False)
                # Set current user profile
                obj.profile = Profile.objects.get(
                    user=self.request.user)
                obj.time_left = current_plan_q.max_time
                obj.save()
                return HttpResponseRedirect(obj.get_absolute_url())
            else:
                # TODO add lock to button
                return HttpResponseRedirect("dashboard")
        else:
            starter_plan = Plan.objects.get(name="FOR BEGINNERS")
            user_profile = Profile(user=self.request.user, plan=starter_plan)
            user_profile.save()

            # acces to user current plan query
            current_plan_q = Plan.objects.get(profile=(Profile.objects.get(
                user=self.request.user)))
            obj = form.save(commit=False)
            # Set current user profile
            obj.profile = Profile.objects.get(
                user=self.request.user)
            obj.time_left = current_plan_q.max_time
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())


class SettingsView(UpdateView):
    template_name = "user/settings.html"
    model = Bots
    form_class = SettingsForm
    success_url = "dashboard"

    def get_queryset(self):
        return Bots.objects.filter(profile__user=self.request.user)


class UserBotDetails(DetailView):
    model = Bots


class Shop(ListView):
    template_name = "user/shop.html"
    model = Plan
    context_object_name = "plans"


class Faq(ListView):
    template_name = "user/faq.html"
    model = FaqList
    context_object_name = "faqs"


class Regulations(ListView):
    template_name = "account/regulations.html"
    model = GeneratePage


class PrivacyPolicy(ListView):
    template_name = "account/privacy-policy.html"
    model = GeneratePage


class MyPasswordChangeView(PasswordChangeView):
    success_url = "/login/"
