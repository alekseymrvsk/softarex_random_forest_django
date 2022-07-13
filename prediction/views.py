from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from .classRandomForest import MyRandomForest


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file_to_process')
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)

        model = MyRandomForest()
        model.fit_model()
        predict = model.predict_data(uploaded_file_url[1:])
        metric = model.get_metric()

        context = {'metric': metric, 'predict': predict, }
        return render(request, 'prediction/prediction.html', context)

    return render(request, 'prediction/prediction.html')
