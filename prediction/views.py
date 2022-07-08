from django.shortcuts import render
import requests

from .classRandomForest import MyRandomForest



def index(request):
    model = MyRandomForest()
    model.fit_model()
    predict = model.predict_data()
    metric = model.get_metric()
    context = {'metric': metric, 'predict': predict}
    return render(request, 'prediction/prediction.html', context)
