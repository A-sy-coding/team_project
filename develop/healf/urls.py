from django.urls import path
from . import views
app_name='healf'
urlpatterns = [
    path("",views.main,name='main'),
    path("mypage/",views.mypage, name='mypage'),
] 