from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='prediction'),
    path('pdf', views.getpdf, name='getpdf')

]
