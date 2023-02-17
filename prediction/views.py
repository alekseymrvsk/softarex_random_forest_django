import logging
import os
from pathlib import Path
import requests
import pandas as pd
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from users.models import ResultFiles
from users.models import UserProfile
from .classRandomForest import MyRandomForest

NUMBER_COLUMNS_TEST = 42

NUMBER_COLUMNS_TRAIN = 43

INPUT_FILE_FORMAT = '.csv'

logger = logging.getLogger(__name__)

is_user_train = False

url = 'http://localhost:8000/get_data'

# For checking train dataset set check_train True, for checking test dataset - False
def check_dataset(file, check_train=True):      #МОЖНО УДАЛЯТЬ ИЗ-ЗА API
    if Path(file).suffix == INPUT_FILE_FORMAT:
        dataset = pd.read_csv(file)
        if check_train:
            if len(dataset.columns) == NUMBER_COLUMNS_TRAIN:
                return True
            else:
                logger.warning("Invalid file")
                return False
        else:
            if len(dataset.columns) == NUMBER_COLUMNS_TEST:
                return True
            else:
                logger.warning("Invalid file")
                return False


def index(request, user_id):
    model = MyRandomForest()

    if not UserProfile.objects.filter(user_id=user_id).exists():
        user_current = UserProfile()
        user_current.user_id = user_id
        user_current.n_predict = 0
        user_current.save()

    else:
        user_current = User.objects.get(pk=user_id)
        user_n_predict = UserProfile.objects.get(user_id=user_id)
        if request.method == "POST":
            if request.FILES.get('file_to_train') is not None:
                uploaded_file_train = request.FILES.get('file_to_train')
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file_train.name, uploaded_file_train)
                uploaded_file_train_url = fs.url(filename)
                is_user_train = True
                if not check_dataset(uploaded_file_train_url[1:], True):
                    return render(request, 'error/error_dataset.html')
                logger.info("Train model using user data")
            else:
                is_user_train = False
                logger.info("Train model using default data")
            if request.FILES.get('file_to_process') is not None:
                uploaded_file_predict = request.FILES.get('file_to_process')
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file_predict.name, uploaded_file_predict)
                uploaded_file_url = fs.url(filename)

                if not check_dataset(uploaded_file_url[1:], False):
                    return render(request, 'error/error_dataset.html')

                user_result_file = ResultFiles()
                user_result_file.user_id = user_id
                user_result_file.save()
                if is_user_train:
                    files = {'INPUT_TEST': open(uploaded_file_url[1:], 'rb'),
                             'INPUT_TRAIN': open(uploaded_file_train_url[1:], 'rb')}
                else:
                    files = {'INPUT_TEST': open(uploaded_file_url[1:], 'rb')}

                resp = requests.get(url=url, files=files, allow_redirects=True)
                with open("prediction/user_output_data/prediction"+user_current.username + str(
                            user_result_file.pk)+".csv", "w") as f:
                     f.write(resp.text)

                user_result_file.result = os.path.join(
                    "prediction/user_output_data/prediction" + user_current.username + str(
                        user_result_file.pk) + ".csv")

                predict = pd.read_csv("prediction/user_output_data/prediction"+user_current.username + str(
                            user_result_file.pk)+".csv")

                predict = predict.drop(columns=['Id'])

                logger.info("Predict data")

                user_n_predict.n_predict += 1

                user_result_file.save()
                user_current.save()
                user_n_predict.save()
                context = {'predict': predict, 'user_result_pk': user_result_file.pk,
                           "is_predict": True}
                return render(request, 'prediction/prediction.html', context)
            else:
                return render(request, 'error/error_dataset.html')

    return render(request, 'prediction/prediction.html')


def save_file(request, user_id, file_pk):
    try:
        user_predict = User.objects.get(pk=user_id)
        data = open(
            os.path.join("prediction/user_output_data/prediction" + user_predict.username + str(file_pk) + ".csv"),
            'r').read()
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=prediction.csv'
    except FileNotFoundError:
        return render(request, 'prediction/prediction.html', {'flag_save_csv': True})

    return response
