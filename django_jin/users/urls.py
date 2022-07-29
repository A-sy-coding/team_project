from django.urls import path
from . import views
urlpatterns = [
<<<<<<< Updated upstream
    path('login/',views.login, name='login'),
    path('login/signup/',views.signup),
=======
    path('login/',views.login_view, name='login'),
    path('login/signup/',views.signup, name='signup'),
    path('clear/',views.clear, name='clear'),
>>>>>>> Stashed changes
]