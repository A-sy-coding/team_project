from django import urls
from django.urls import path

from . import views

app_name='exercise'
urlpatterns = [
    path('',views.exercise, name='exercise'),
]