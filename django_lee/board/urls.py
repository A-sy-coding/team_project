from django.urls import path
from . import views

app_name='board'
urlpatterns = [
    path('', views.board_list, name='board_list')
]