from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import LoginForm

app_name = "core"
urlpatterns = [
    path("", views.index, name="home"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        LoginView.as_view(
            authentication_form=LoginForm, template_name="core/login.html"
        ),
        name="login",
    ),
]
