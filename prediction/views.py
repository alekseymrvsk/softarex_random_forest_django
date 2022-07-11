from django.shortcuts import render, redirect
import requests
from .classRandomForest import MyRandomForest
from .form import DocumentForm
from .models import Files


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            model = MyRandomForest()
            model.fit_model()
            predict = model.predict_data()
            metric = model.get_metric()
            context = {'metric': metric, 'predict': predict, 'form': form}
            return render(request, 'prediction/prediction.html', context)

    else:
        form = DocumentForm(request.POST, request.FILES)
    return render(request, 'prediction/prediction.html', {'form': form})


