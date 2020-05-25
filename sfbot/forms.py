from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import Bots


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


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, min_length=6)
    message = forms.CharField(widget=forms.Textarea, required=True, min_length=10)

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
            "SF_Username",
            "SF_Password",
            "country",
            "server",
        )
        widgets = {
            "SF_Password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddBotForm, self).__init__(*args, **kwargs)
        self.fields["SF_Username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["SF_Password"].widget.attrs.update({"placeholder": "Password"})
        self.fields["country"].widget.attrs.update({"class": "country-input"})
        self.fields["server"].widget.attrs.update({"class": "server-input"})

    def clean(self, *args, **keyargs):
        SF_Username = self.cleaned_data.get("SF_Username")
        SF_Password = self.cleaned_data.get("SF_Password")
        server = self.cleaned_data.get("server")

        sf_username_qs = Bots.objects.filter(SF_Username=SF_Username)
        country_qs = Bots.objects.filter(server=server)
        if sf_username_qs.exists():
            if country_qs.exists():
                raise forms.ValidationError(
                    "An account with this username already exists on this server"
                )

        if len(SF_Password) < 5:
            raise forms.ValidationError("Password must be greater than 5 characters")

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
        self.fields['status'].widget.attrs.update({'class': 'onoffswitch-checkbox'})
        self.fields['tavern_status'].widget.attrs.update({'class': 'onoffswitch-checkbox'})
        self.fields['arena_status'].widget.attrs.update({'class': 'onoffswitch-checkbox'})


