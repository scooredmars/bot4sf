from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponseRedirect
from .models import Bots
from django.utils import timezone
from sfbot.tasks import bot_time


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {"name": "first_name", "pattern": "[a-zA-Z]*", "placeholder": "First Name"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"name": "last_name", "pattern": "[a-zA-Z]*", "placeholder": "Last Name"}
        )

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()


class AddBotForm(forms.ModelForm):
    class Meta:
        model = Bots
        fields = ("username", "password", "country", "server")
        widgets = {
            "password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddBotForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["country"].widget.attrs.update({"class": "country-input"})
        self.fields["server"].widget.attrs.update({"class": "server-input"})

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        server = self.cleaned_data.get("server")

        sf_username_qs = Bots.objects.filter(username=username)
        country_qs = Bots.objects.filter(server=server)
        if sf_username_qs.exists():
            if country_qs.exists():
                raise forms.ValidationError(
                    "An account with this username already exists on this server"
                )
        if len(password) < 5:
            raise forms.ValidationError("Password is too short")
        if len(password) > 30:
            raise forms.ValidationError("Password is too long")

        return super(AddBotForm, self).clean(*args, **keyargs)


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Bots
        fields = (
            "status",
            "tavern_status",
            "tavern_settings",
            "arena_status",
            "arena_settings",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "onoffswitch-checkbox"})
        self.fields["tavern_status"].widget.attrs.update(
            {"class": "onoffswitch-checkbox"}
        )
        self.fields["arena_status"].widget.attrs.update(
            {"class": "onoffswitch-checkbox"}
        )

    def save(self, commit=True):
        status = self.cleaned_data.get("status")
        instance = super(SettingsForm, self).save(commit=False)
        if commit:
            if status == True:
                instance.start = timezone.now()
                instance.save()
                bot_id = instance.id
                profile_name = instance.profile.plan.name
                bot_time(bot_id, profile_name)
            elif status == False:
                instance.start = None
                instance.save()
        return instance


class EditBotForm(forms.ModelForm):
    class Meta:
        model = Bots
        fields = ("username", "password", "country", "server")

    def __init__(self, *args, **kwargs):
        # get pk value from views and set them to request
        self.request = kwargs.pop("pk", None)
        super(EditBotForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        server = self.cleaned_data.get("server")

        """
        Check if current QuerySet Bot exists.
        """
        username_change = Bots.objects.filter(username=username)

        if username_change.exists():
            """
            Check if current bot username exists on server.
            If bot doesn't exist return epmty list. Needed for validations.
            """
            bot_server_qs = Bots.objects.filter(server=server).filter(username=username)

            """
            Assignment pk value from request to variable.
            This is used for check if pk != data.id.
            """
            session_pk = self.request

            """
            Return a QuerySet for currnet session bot, using id.
            """
            currnet_bot = Bots.objects.filter(username=username).only("id")

            """
            Access to values in QuerySet and assign them to variable.
            """
            for bot_data in currnet_bot:
                data = bot_data

            """
            Check if user  data was change.
            If data are same as in base, then return to 'dashboard'.
            """
            if (
                (data.username == username)
                & (data.password == password)
                & (data.server == server)
            ):
                return HttpResponseRedirect("dashboard")
            elif data.server != server:
                if bot_server_qs.exists():
                    bot_server_data = Bots.objects.filter(server=server).get(
                        username=username
                    )
                    if bot_server_data in bot_server_qs:
                        raise forms.ValidationError(
                            "An account with this username already exists on this server"
                        )
            elif data.password != password:
                if len(password) < 5:
                    raise forms.ValidationError("Password is too short")
                if len(password) > 30:
                    raise forms.ValidationError("Password is too long")
                if (data.username == username) and (data.id != session_pk):
                    raise forms.ValidationError(
                        "An account with this username already exists on this server"
                    )

        if len(password) < 5:
            raise forms.ValidationError("Password is too short")
        if len(password) > 30:
            raise forms.ValidationError("Password is too long")

        return super(EditBotForm, self).clean(*args, **keyargs)
