from django.urls import path
from django.urls import re_path

from . import views

app_name = 'exercise'
urlpatterns = [
    # ex) 127.0.0.1:8000/exercise/
    path('',views.exercise, name= 'exercise'),
]