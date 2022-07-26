import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import (EditProfileForm)
from .models import ResultFiles
from .models import UserProfile

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "home/home.html")


def show_data(request, file_id):
    # try:
    user_predict = ResultFiles.objects.get(pk=file_id)
    data = open(user_predict.result, 'r').read()
    response = HttpResponse(data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=prediction.csv'
    logger.info("Download result")
    # except FileNotFoundError:
    # return render(request, 'error/error_dataset.html')

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
            logger.info("Edit profile")
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
    logger.info("Sign up")
