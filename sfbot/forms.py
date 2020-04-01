from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import authenticate, get_user_model


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
