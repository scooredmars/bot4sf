from allauth.account.views import PasswordChangeView
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .forms import AddBotForm, SettingsForm, EditBotForm, UserSettingsForm
from .models import Bots, FaqList, GeneratePage, Plan, Profile, User
from django.contrib import messages


def error_404(request, exception):
    return render(request, "404.html")


def error_500(request):
    return render(request, "404.html")


def home_view(request):
    plans = Plan.objects.all()
    users = User.objects.all().count()
    bots = Bots.objects.all().count()
    working_bots = Bots.objects.filter(status=True).count()
    context = {
        "plans": plans,
        "users": users,
        "bots": bots,
        "working_bots": working_bots,
    }
    return render(request, "home.html", context)


def dashboard_add_bot_view(request):
    # Dashboard
    bots_q = Bots.objects.all()
    user_bots = bots_q.filter(profile__user=request.user)
    current_user = Profile.objects.filter(user=request.user)

    if not current_user:
        starter_plan = Plan.objects.get(name="STARTER")
        user_profile = Profile(user=request.user, plan=starter_plan)
        user_profile.save()

    amount_user_bots = user_bots.count()
    current_plan_q = Plan.objects.get(profile=(Profile.objects.get(user=request.user)))
    if amount_user_bots >= current_plan_q.max_bots:
        lock_add = True
    else:
        lock_add = False

    # Add Bot
    form = AddBotForm()
    if request.method == "POST":
        form = AddBotForm(request.POST)
        if form.is_valid():
            # check if user profile is created
            current_user = Profile.objects.filter(user=request.user)
            if current_user:
                # amount of all bots for current user
                max_user_bots = Bots.objects.filter(profile__user=request.user).count()
                # acces to user current plan query
                current_plan_q = Plan.objects.get(
                    profile=(Profile.objects.get(user=request.user))
                )
                if max_user_bots < current_plan_q.max_bots:
                    obj = form.save(commit=False)
                    # Set current user profile
                    obj.profile = Profile.objects.get(user=request.user)
                    # Convert float form plan to time in bot
                    if current_plan_q.max_time == 24.0:
                        obj.time_left = "{0:02.0f}:{1:02.0f}".format(
                            *divmod(float("23.99") * 60, 60)
                        )
                    else:
                        obj.time_left = "{0:02.0f}:{1:02.0f}".format(
                            *divmod(float(current_plan_q.max_time) * 60, 60)
                        )
                    obj.save()
                    messages.add_message(request, messages.SUCCESS, 'A new bot has been added.')
                    return HttpResponseRedirect(obj.get_absolute_url())

    context = {
        "user_bots": user_bots,
        "lock_add": lock_add,
        "form": form,
    }

    return render(request, "user/dashboard.html", context)


def profile_view(request):
    current_user = Profile.objects.filter(user=request.user)

    if current_user:
        max_user_bots = Bots.objects.filter(profile__user=request.user).count()
        if max_user_bots != 0:
            current_user_qs = Bots.objects.filter(profile__user=request.user)
        else:
            current_user_qs = User.objects.filter(username=request.user)
    else:
        current_user_qs = User.objects.filter(username=request.user)

    user_data = User.objects.get(username=request.user)
    form = UserSettingsForm()
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            
            obj = form.save(commit=False)
            
            if not username:
                obj.username = user_data.username
            if not first_name:
                obj.first_name = user_data.first_name
            if not last_name:
                obj.last_name = user_data.last_name
            if not email:
                obj.email = user_data.email
            messages.add_message(request, messages.SUCCESS, 'Profile details updated.')
            obj.save()
            form = UserSettingsForm()
        else:
            messages.add_message(request, messages.ERROR, 'Wrong data provided')

    context = {
        "current_user_qs": current_user_qs,
        "form": form,
    }

    return render(request, "user/profile.html", context)


class SettingsView(UpdateView):
    template_name = "user/settings.html"
    model = Bots
    form_class = SettingsForm
    success_url = "dashboard"

    def get_queryset(self):
        return Bots.objects.filter(profile__user=self.request.user)


class UserBotDetails(DetailView):
    model = Bots


class EditBotDetails(UpdateView):
    template_name = "user/edit-bot.html"
    model = Bots
    form_class = EditBotForm
    success_url = "../dashboard"
    context_object_name = "edit_info"

    def get_queryset(self):
        return Bots.objects.filter(profile__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(EditBotDetails, self).get_form_kwargs()
        # Update the existing form kwargs dict with the pk session.
        kwargs.update({"pk": self.kwargs["pk"]})
        return kwargs


def shop_view(request):
    plans = Plan.objects.all()
    user_profile = Profile.objects.get(user=request.user)
    user_plan = user_profile.plan.name
    context = {
        "plans": plans,
        "user_plan": user_plan,
    }
    return render(request, "user/shop.html", context)


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
