from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from .classRandomForest import MyRandomForest
import logging
logger = logging.getLogger(__name__)


def index(request):
    model = MyRandomForest()
    if request.method == "POST":
        if request.FILES.get('file_to_train') is not None:
            uploaded_file_train = request.FILES.get('file_to_train')
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file_train.name, uploaded_file_train)
            uploaded_file_train_url = fs.url(filename)
            model.fit_model(uploaded_file_train_url[1:])
            logger.error("Train model using user data")
        else:
            model.fit_model()
            logger.error("Train model using default data")

        uploaded_file_predict = request.FILES.get('file_to_process')
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file_predict.name, uploaded_file_predict)
        uploaded_file_url = fs.url(filename)

        predict = model.predict_data(uploaded_file_url[1:])
        logger.error("Predict data")
        metric = model.get_metric()
        logger.error("Get metric")

        context = {'metric': metric, 'predict': predict, }
        return render(request, 'prediction/prediction.html', context)

    return render(request, 'prediction/prediction.html')
