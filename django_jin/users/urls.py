from django.urls import path
from . import views
app_name='users'
urlpatterns = [
    path('login/',views.login_view, name='login'),
    path('login/signup/',views.signup, name='signup'),
    path('clear/',views.clear, name='clear'),
    path('login/signup/emailvalid/', views.email_validater, name='validation'),
    path('login/signup/idvalid/', views.iddupl, name='iddupl'),
    path('login/signup/authnumvalid/', views.auth_num_validater, name='authnumval'),
]