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


def getpdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prediction.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Times-Roman", 55)
    p.drawString(100, 700, "Hello, Javatpoint.")
    p.showPage()
    p.save()
    return response
