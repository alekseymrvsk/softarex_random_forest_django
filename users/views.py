from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
import logging
logger = logging.getLogger(__name__)


def home(request):
    return render(request, "registration/home.html")


def redirect_view(request):
    response = redirect('/prediction/')
    return response


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    logger.error("Sign up")
