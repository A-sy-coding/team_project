from django.urls import path
from . import views
app_name='users'
urlpatterns = [
    path('login/',views.login_view, name='login'),
    path('login/register/',views.register, name='register'),
    path('clear/',views.clear, name='clear'),
    path('login/register/emailvalid/', views.email_validater, name='validation'),
    path('login/register/idvalid/', views.iddupl, name='iddupl'),
    path('login/register/authnumvalid/', views.auth_num_validater, name='authnumval'),
    path('logout/', views.logout, name='logout'),
]