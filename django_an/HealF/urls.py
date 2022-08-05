# HealF application에 config 프로젝트와 연결된 urls.py파일 생성

from django.urls import path
from . import views

app_name = 'HealF'
urlpatterns = [
    # --------------- main page --------------
    
    # /HealF/
    path('', views.HealFMainView.as_view() , name = 'main'),
    # /HealF/challenge
    path('challenge/', views.HealFchallengeView.as_view(), name = 'challenge'),
    # /HealF/exercise
    path('exercise/', views.HealFexerciseView.as_view(), name= 'exercise'),
    # /HealF/community
    path('community/', views.HealFcommunityView.as_view(), name = 'community'),
    # /HealF/market
    path('market/', views.HealFmarketView.as_view(), name='market'),
    # /HealF/mypage
    path('mypage/', views.HealFmypageView.as_view(), name='mypage'),

    # --------------- login & sign-up page --------------
    path('login/', views.HealFloginView.as_view(), name = 'login'),
    path('sign-up/', views.HealFsignupView.as_view(), name = 'sign-up'),

    # --------------- challenge page --------------
    path('challenge/exercise/', views.Challenge_exerciseView.as_view(), name = 'challenge_exercise'),
    path('challenge/diet/', views.Challenge_dietView.as_view(), name = 'challenge_diet'),

    # --------------- market page --------------
    path('market/product/', views.MkarketproductView.as_view(), name = 'market_product'),

]