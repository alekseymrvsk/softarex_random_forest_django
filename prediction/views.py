import numpy as np
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from users.models import UserProfile
from .classRandomForest import MyRandomForest
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def index(request, user_id):
    model = MyRandomForest()
    user_n_predict = User.objects.get(pk=user_id)

    if request.method == "POST":
        if request.FILES.get('file_to_train') is not None:
            uploaded_file_train = request.FILES.get('file_to_train')
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file_train.name, uploaded_file_train)
            uploaded_file_train_url = fs.url(filename)
            dataset = pd.read_csv(uploaded_file_train_url[1:])
            if len(dataset.columns) == 43:
                model.fit_model(uploaded_file_train_url[1:])
            else:
                return render(request, 'error/error_dataset.html')
            logger.error("Train model using user data")
        else:
            model.fit_model()
            logger.error("Train model using default data")
        if request.FILES.get('file_to_process') is not None:
            uploaded_file_predict = request.FILES.get('file_to_process')
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file_predict.name, uploaded_file_predict)
            uploaded_file_url = fs.url(filename)

            dataset = pd.read_csv(uploaded_file_url[1:])
            if len(dataset.columns) == 42:
                predict = model.predict_data(uploaded_file_url[1:])
            else:
                return render(request, 'error/error_dataset.html')
            logger.error("Predict data")
            metric = model.get_metric()
            logger.error("Get metric")
        else:
            return render(request, 'error/error_dataset.html')

        user_n_predict.n_predict += 1
        user_n_predict.save()
        context = {'metric': metric, 'predict': predict, }
        return render(request, 'prediction/prediction.html', context)

    return render(request, 'prediction/prediction.html')
