from django.urls import path
from . import views

app_name = 'market'

urlpatterns=[
    
    # /market/
    path('', views.ChallengeView.as_view(), name='market_page'),
    path('item_register/', views.ItemRegisterView.as_view(), name='item_register'),
    path('item/', views.ItemView.as_view(), name='item'),
]