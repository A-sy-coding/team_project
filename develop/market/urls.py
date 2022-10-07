from django.urls import path
from . import views

app_name = 'market'

urlpatterns=[
    
    # /market/   
    #-- item info view
    path('', views.MarketView.as_view(), name='market_page'),
    path('<int:pk>/', views.MarketDV.as_view(), name='item_detail'), # 각 등록 정보들의 자세한 정보들

    #-- item create/update/delete
    path('item_register/', views.ItemRegisterView.as_view(), name='item_register'),  # 아이템 등록
    path('<int:pk>/item_update/', views.ItemUpdate.as_view(), name='item_update'),  # 아이템 등록정보 수정
    path('<int:pk>/item_delete/', views.ItemDelete.as_view(), name='item_delete'),  # 아이템 등록정보 삭제

    #-- item category
    path('equipmnet/', views.EquipmentView.as_view(), name='equipmnet_page'),
    path('shoes/', views.ShoesView.as_view(), name='shoes_page'),
    path('sportwear/', views.SportswearView.as_view(), name='sportwear_page'),
    path('supplements/', views.SupplementsView.as_view(), name='supplements_page'),
    path('etc/', views.EtcView.as_view(), name='etc_page'),
    

    #-- 좋아요 기능
    # path('like/', views.Like, name='likes'),
    # path('<int:pk>/', views.Like, name='likes'),
    
]