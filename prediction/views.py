from django.shortcuts import render, redirect
import requests
from .classRandomForest import MyRandomForest
from .form import DocumentForm
from .models import Files


# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             file = Files.objects.last()
#             model = MyRandomForest()
#             model.fit_model()
#             predict = model.predict_data(file)
#             metric = model.get_metric()
#             form = DocumentForm(request.POST, request.FILES)
#             context = {'metric': metric, 'predict': predict, 'form': form}
#             render(request, 'prediction/prediction.html', context)
#     else:
#         form = DocumentForm()
#     return render(request, 'prediction/prediction.html', {
#         'form': form
#     })


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file = Files.objects.last()
            model = MyRandomForest()
            model.fit_model()
            predict = model.predict_data(file)
            metric = model.get_metric()
            form = DocumentForm(request.POST, request.FILES)
            context = {'metric': metric, 'predict': predict, 'form': form}
            render(request, 'prediction/prediction.html', context)
    else:
        form = DocumentForm()
    return render(request, 'prediction/prediction.html', {
        'form': form
    })