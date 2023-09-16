from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateUser.as_view(), name='registration'),
    ]
