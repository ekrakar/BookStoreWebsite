from django import forms
#from datetime import datetime
#from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserInfo


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditUserAccountForm(forms.Form):
    First_Name = forms.CharField()
    Last_Name = forms.CharField()
    billing_address = forms.CharField(help_text="Enter Billing Address here.")
    mailing_address = forms.CharField(help_text="Enter Mailing Address here.")
    card_type = forms.CharField(help_text="V - Visa, M - MasterCard, D - Discover, A - American Express")
    credit_card_number = forms.CharField(help_text="Enter Cards Number")
    Expiration_Date = forms.DateField(help_text="Enter Expiration Date (YYYY-MM-DD)")
