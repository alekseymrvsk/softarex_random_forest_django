from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
import logging
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import (EditProfileForm, ProfileForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "registration/home.html")


def profile(request):
    return render(request, "registration/user_profile.html")


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user_form = form.save()
            custom_form = form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('/user_profile/')
    else:
        form = EditProfileForm(instance=request.user)

        context = {'form': form}
        return render(request, 'registration/edit_profile.html', context)


def redirect_view(request):
    response = redirect('/prediction/')
    return response


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    logger.error("Sign up")
