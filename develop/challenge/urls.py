from django.urls import path
from . import views

app_name ='challenge'
urlpatterns = [
    path('', views.ChallengeView.as_view(), name = 'challenge'),
    path('exercise/', views.Challenge_exerciseView.as_view(), name = 'challenge_exercise'),
    path('diet/', views.Challenge_dietView.as_view(), name = 'challenge_diet'),
    
    # /challenge/webcam  --> html 파일을 사용하여 webcam 실행하기
    path('webcam/', views.HtmlWebcamView.as_view(), name = 'webcam'),
    path('webcam/record_video', views.record_video, name='record'), # 데이터를 받을 임시 경로
]