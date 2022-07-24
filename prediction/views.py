import os
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from users.models import UserProfile
from users.models import ResultFiles
from .classRandomForest import MyRandomForest
import logging
import pandas as pd
from pathlib import Path
from django.core.files import File

logger = logging.getLogger(__name__)


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

        # if os.path.exists("prediction/user_output_data/prediction" + user_current.username + ".csv"):
        # os.remove("prediction/user_output_data/prediction" + user_current.username + ".csv")
        if request.method == "POST":
            if request.FILES.get('file_to_train') is not None:
                uploaded_file_train = request.FILES.get('file_to_train')
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file_train.name, uploaded_file_train)
                uploaded_file_train_url = fs.url(filename)

                if Path(uploaded_file_train_url[1:]).suffix == '.csv':
                    dataset = pd.read_csv(uploaded_file_train_url[1:])
                else:
                    return render(request, 'error/error_dataset.html')

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

                if Path(uploaded_file_url[1:]).suffix == '.csv':
                    dataset = pd.read_csv(uploaded_file_url[1:])
                else:
                    return render(request, 'error/error_dataset.html')

                if len(dataset.columns) == 42:
                    predict = model.predict_data(uploaded_file_url[1:])
                else:
                    return render(request, 'error/error_dataset.html')

                logger.error("Predict data")
                metric = model.get_metric()
                logger.error("Get metric")

                if metric is not None:
                    user_result_file = ResultFiles()
                    user_result_file.user_id = user_id
                    user_result_file.save()

                    df = pd.DataFrame(predict)
                    df.columns = ["Prediction"]
                    df.to_csv(
                        "prediction/user_output_data/prediction" + user_current.username + str(
                            user_result_file.pk) + ".csv",
                        index_label="Id")

                    user_result_file.result = os.path.join(
                        "prediction/user_output_data/prediction" + user_current.username + str(
                            user_result_file.pk) + ".csv")

                    user_n_predict.n_predict += 1

                    user_result_file.save()
                    user_current.save()
                    user_n_predict.save()
                    context = {'metric': metric, 'predict': predict, 'user_result_pk': user_result_file.pk, "is_predict": True}
                    return render(request, 'prediction/prediction.html', context)
            else:
                return render(request, 'error/error_dataset.html')

    return render(request, 'prediction/prediction.html')


def save_file(request, user_id, file_pk):
    try:
        user_predict = User.objects.get(pk=user_id)
        data = open(os.path.join("prediction/user_output_data/prediction" + user_predict.username + str(file_pk) + ".csv"), 'r').read()
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=prediction.csv'
    except FileNotFoundError:
        return render(request, 'prediction/prediction.html', {'flag_save_csv': True})

    return response
