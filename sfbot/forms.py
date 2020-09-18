from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponseRedirect
from .models import Bots, User
from django.utils import timezone
import datetime

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
        bot_data = super(SettingsForm, self).save(commit=False)
        if commit:
            if status == True:
                bot_data.start = timezone.now()
                bot_data.save()
                if bot_data.profile.plan.name != "PREMIUM":
                    if str(bot_data.time_left) != "00:00:00":
                        # calculate data bot stop
                        converted_time_left = str(bot_data.time_left)
                        date_time = datetime.datetime.strptime(
                            converted_time_left, "%H:%M:%S"
                        )
                        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
                        seconds = a_timedelta.total_seconds()
                        stop_time = bot_data.start + datetime.timedelta(0, seconds)
                        bot_data.stop = stop_time
                        bot_data.save()
            elif status == False:
                bot_data.start = None
                if bot_data.profile.plan.name != "PREMIUM":
                    bot_data.stop = None
                bot_data.save()
        return bot_data


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

        # Check if current QuerySet Bot exists.
        username_change = Bots.objects.filter(username=username)

        if username_change.exists():
            # Check if current bot username exists on server.
            # If bot doesn't exist return epmty list. Needed for validations.
            bot_server_qs = Bots.objects.filter(server=server).filter(username=username)

            # Assignment pk value from request to variable.
            # This is used for check if pk != data.id.
            session_pk = self.request

            # Return a QuerySet for currnet session bot, using id.
            currnet_bot = Bots.objects.filter(username=username).only("id")

            # Access to values in QuerySet and assign them to variable.
            for bot_data in currnet_bot:
                data = bot_data

            # Check if user  data was change.
            # If data are same as in base, then return to 'dashboard'.
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


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        
    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")

        username_qs = User.objects.exclude(pk=self.instance.pk).filter(username=username)
        email_qs = User.objects.exclude(pk=self.instance.pk).filter(email=email)
        if not username_qs:
            if username:
                if len(username) < 10:
                    raise forms.ValidationError('This username is too short.')
                elif len(username) > 25:
                    raise forms.ValidationError('This username is too long.')
        else:
            raise forms.ValidationError('This username is already in use. Please supply a different username.')
        if email_qs:
            raise forms.ValidationError('This email is already in use. Please supply a different email.')

        # po zmianie email ma zostac wyslany mail potwierdzajacy
        # poprawic wyswietlanie bledu (zeby nie zamykalo okienka jesli jest blad) to samo w dodawaniu bota
        return super(UserSettingsForm, self).clean(*args, **keyargs)
