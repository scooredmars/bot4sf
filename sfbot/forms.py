from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponseRedirect
from .models import Bots


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {"name": "first_name",
                "pattern": "[a-zA-Z]*", "placeholder": "First Name"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"name": "last_name",
                "pattern": "[a-zA-Z]*", "placeholder": "Last Name"}
        )

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, min_length=6)
    message = forms.CharField(widget=forms.Textarea,
                              required=True, min_length=10)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["from_email"].widget.attrs.update(
            {"name": "from_email", "placeholder": "Your Email"}
        )
        self.fields["subject"].widget.attrs.update(
            {"name": "subject", "placeholder": "Subject"}
        )
        self.fields["message"].widget.attrs.update(
            {"name": "message", "placeholder": "Message", "rows": "10"}
        )


class AddBotForm(forms.ModelForm):
    class Meta:
        model = Bots
        fields = (
            "username",
            "password",
            "country",
            "server"
        )
        widgets = {
            "password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddBotForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username"})
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Password"})
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
            "arena_settings"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update(
            {'class': 'onoffswitch-checkbox'})
        self.fields['tavern_status'].widget.attrs.update(
            {'class': 'onoffswitch-checkbox'})
        self.fields['arena_status'].widget.attrs.update(
            {'class': 'onoffswitch-checkbox'})


class EditBotForm(forms.ModelForm):
    class Meta:
        model = Bots
        fields = (
            "username",
            "password",
            "country",
            "server"
        )

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        server = self.cleaned_data.get("server")

        # check if current queryset bot exist
        username_change = Bots.objects.filter(username=username)
        all_bots = Bots.objects.all()

        # username was change and queryset exist
        if username_change.exists():
            # list of usernames for current server
            current_server_username_list = Bots.objects.filter(
                server=server).filter(username=username)
            # user id
            currnet_user_id = Bots.objects.filter(username=username).only("id")
            for bot_data in currnet_user_id:
                # data for current user
                data_user = Bots.objects.get(pk=bot_data.id)
            # check if user data was change
            if (data_user.username == username) & (data_user.password == password) & (data_user.server == server):
                return HttpResponseRedirect("dashboard")
            elif data_user.password != password:
                if len(password) < 5:
                    raise forms.ValidationError("Password is too short")
                if len(password) > 30:
                    raise forms.ValidationError("Password is too long")
                if data_user in all_bots:
                    if (data_user.username == username) | (data_user.server == server):
                        if current_server_username_list.exists():
                            current_server_username = Bots.objects.filter(
                                server=server).get(username=username)
                            if current_server_username in current_server_username_list:
                                raise forms.ValidationError(
                                    "An account with this username already exists on this server")
            elif data_user.server != server:
                if data_user in all_bots:
                    if current_server_username_list.exists():
                        current_server_username = Bots.objects.filter(
                            server=server).get(username=username)
                        if current_server_username in current_server_username_list:
                            raise forms.ValidationError(
                                "An account with this username already exists on this server")
            elif data_user.username != username:
                if data_user in all_bots:
                    if current_server_username_list.exists():
                        current_server_username = Bots.objects.filter(
                            server=server).get(username=username)
                        if current_server_username in current_server_username_list:
                            raise forms.ValidationError(
                                "An account with this username already exists on this server")

        return super(EditBotForm, self).clean(*args, **keyargs)
