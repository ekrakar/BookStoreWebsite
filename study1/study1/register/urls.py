# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views as v

urlpatterns = [
    path("", LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("home/", v.home, name = "home"),
    path("view/", v.view_account, name = "view"),
    path("update/", v.update, name="update"),
    path("logout/", v.logout_view, name="logout"),
    path("change-password/", v.change_password, name="change_password")
]