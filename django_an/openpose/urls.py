# HealF application에 config 프로젝트와 연결된 urls.py파일 생성

from django.urls import path
from . import views

app_name = 'openpose'
urlpatterns = [
    # /openpose/
    
    # /openpose/webcam  --> html 파일을 사용하여 webcam 실행하기
    path('webcam/', views.HtmlWebcamView, name = 'webcam'),
    path('webcam/canvas_image', views.canvas_image, name='canvas'),
    path('webcam/record_video', views.record_video, name='record'),

]