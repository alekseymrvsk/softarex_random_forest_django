from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('/redirect/', views.redirect_view),
    path('user_profile/', views.profile, name='user_profile'),
    path('view_profile/edit_profile/', views.edit_profile, name='edit_profile'),

]
