import os

from django.contrib.auth.models import User
from django.http import HttpResponse
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

from .models import UserProfile
from .models import ResultFiles

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "home/home.html")


def show_data(request):
    try:
        user_predict = ResultFiles.objects.get(created_at=request.GET.get("created_at"))
        data = user_predict.result
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=prediction.csv'
    except FileNotFoundError:
        return render(request, 'prediction/prediction.html', {'flag_save_csv': True})

    return response


def profile(request):
    if UserProfile.objects.filter(user_id=request.user.pk).exists():
        if UserProfile.objects.filter(user_id=request.user.pk).exists():
            user_n_predict = UserProfile.objects.get(user_id=request.user.pk)
            context_n_predict = user_n_predict
        else:
            user_current = UserProfile()
            user_current.user_id = request.user.pk
            user_current.n_predict = 0
            user_current.save()
            context_n_predict = user_current

        if ResultFiles.objects.filter(user_id=request.user.pk).exists():
            user_result_file = ResultFiles.objects.filter(user_id=request.user.pk)
            context_result_file = user_result_file
        else:
            user_current = ResultFiles()
            user_current.user_id = request.user.pk
            user_current.n_predict = 0
            user_current.save()
            context_result_file = user_current

        context = {'user_n_predict': context_n_predict, 'user_result_file': context_result_file}
        return render(request, "registration/user_profile.html", context)
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
