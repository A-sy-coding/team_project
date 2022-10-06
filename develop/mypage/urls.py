from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns=[
    path('',views.mypageView,name='mypage_view'),
    path('update/',views.update,name='update'),
]