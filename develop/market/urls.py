from django.urls import path
from . import views

app_name = 'market'

urlpatterns=[
    
    # /market/
    path('', views.ChallengeView.as_view(), name='market_page'),
]