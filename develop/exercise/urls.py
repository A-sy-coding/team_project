from django import urls
from django.urls import path

from . import views

app_name='exercise'
urlpatterns = [
    path('back/',views.exercise, name='exercise'),
    path('shoulder/',views.shoulder, name='shoulder'),
    path('hache/',views.hache, name='hache'),
    path('chest/',views.chest, name='chest'),
    path('arm/',views.arm, name='arm'),
    path('exercisestart/',views.exercisestart, name='exercisestart'),
    path('basic/',views.basic, name='basic'),
    path('middle/',views.middle, name='middle'),
    path('advanced/',views.advanced, name='advanced'),
]