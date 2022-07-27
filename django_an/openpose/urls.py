# HealF application에 config 프로젝트와 연결된 urls.py파일 생성

from django.urls import path
from . import views

app_name = 'openpose'
urlpatterns = [
    # /openpose/
    path('', views.OpenPoseView , name = 'model'),
]