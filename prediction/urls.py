from django.urls import path
from . import views

urlpatterns = [

    path('<int:user_id>', views.index, name='prediction'),
    path('get_csv/<int:user_id>', views.save_file, name='get_csv'),

]
