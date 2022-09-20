from django.urls import path
from . import views

app_name = 'market'

urlpatterns=[
    
    # /market/
    path('', views.ChallengeView.as_view(), name='market_page'),
    path('item_register/', views.ItemRegisterView.as_view(), name='item_register'),  # 아이템 등록
    # path('item_update/', views.ItemUpdate.as_view(), name='item_update'),  # 아이템 등록정보 수정

    path('item/', views.ItemView.as_view(), name='item_index'), # 등록 정보들이 들어올 url
    path('item/<int:pk>/', views.ItemDV.as_view(), name='item_detail') # 각 등록 정보들의 자세한 정보들
]