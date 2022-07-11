from django.shortcuts import render, redirect
import requests
from .classRandomForest import MyRandomForest
from .form import DocumentForm


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'prediction/prediction.html', {
        'form': form
    })


def index(request):
    model = MyRandomForest()
    model.fit_model()
    predict = model.predict_data()
    metric = model.get_metric()
    form = DocumentForm(request.POST, request.FILES)
    context = {'metric': metric, 'predict': predict, 'form': form}
    return render(request, 'prediction/prediction.html', context)
