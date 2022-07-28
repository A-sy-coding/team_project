from django.urls import path
from . import views
app_name='users'
urlpatterns = [
    path('login/',views.login, name='login'),
    path('login/signup/',views.signup, name='signup'),
    path('clear/',views.clear, name='clear'),
]