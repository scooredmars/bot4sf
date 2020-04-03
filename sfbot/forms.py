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
