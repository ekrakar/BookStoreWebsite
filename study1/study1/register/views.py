from django.shortcuts import render, redirect
from .forms import RegistrationForm, EditUserAccountForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = RegistrationForm()
    return render(request, "register/register.html", {"form":form})

def view_account(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    return render(request, "register/viewAccount.html", {'user':request.user})

def update(request):
    if request.method == "POST":
        form = EditUserAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/view")
    else:
        form = EditUserAccountForm(instance=request.user)
        return render(request, "register/update.html", {"form":form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("/view")
        else:
            return redirect("/change-password")
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'register/change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, "register/logout.html", {})


def home(response):
	return render(response, "register/home.html", {"name":"test"})