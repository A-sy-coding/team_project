from django.urls import path
from . import views

app_name = 'markets'
urlpatterns = [
    # markets
    path('', views.market_main, name='market_main'),
    # markets/item_register
    path('item_register/', views.item_register, name='item_register'),  # 아이템 등록 페이지
]