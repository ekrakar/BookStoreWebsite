from django import forms
#from datetime import datetime
#from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
#from .models import CustomUser

'''
class RegisterForm(UserCreationForm):
    student_ID = forms.CharField(max_length = 10)
    first_Name = forms.CharField(max_length = 50)
    last_Name = forms.CharField(max_length = 50)
    email = forms.EmailField(required = False)
    mailing_Address = forms.CharField(max_length = 200, required = False)
    billing_Address = forms.CharField(max_length = 200, required = False)
    choice = [("1","Visa"), ("2", "MasterCard"), ("3", "Discover"), ("4", "American Express")]
    credit_Card_Type = forms.ChoiceField(choices=choice, label="Choices", required = False)
    #creditCardType = forms.CharField(max_length = 20)
    credit_Card_Number = forms.CharField(max_length = 20, required = False)
    expiration_Date = forms.DateField(required = False)
    userName = forms.CharField(max_length = 50)

    class Meta:
        model = User
        fields = [
            "student_ID",
            "first_Name",
            "last_Name",
            "email",
            "mailing_Address",
            "billing_Address",
            "credit_Card_Type",
            "credit_Card_Number",
            "expiration_Date",
            "userName",
            "password1", 
            "password2"
        ]
'''
'''
class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = [
            "student_ID",
            "first_Name",
            "last_Name",
            "email",
            "mailing_Address",
            "billing_Address",
            "credit_Card_Type",
            "credit_Card_Number",
            "expiration_Date",
            "userName",
            #"password1", 
            #"password2",
            #"password"
        ]
'''
'''
class EditUserAccountForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = [
            "student_ID",
            "first_Name",
            "last_Name",
            "email",
            "mailing_Address",
            "billing_Address",
            "credit_Card_Type",
            "credit_Card_Number",
            "expiration_Date",
            "userName",
            #"password1", 
            #"password2"
            #"password",
        ]
'''


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

class EditUserAccountForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
'''
class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        #fields = ["username", "password1"]
        #fields = ["username"]
'''