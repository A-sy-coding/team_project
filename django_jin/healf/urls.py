from django.urls import path
from . import views
urlpatterns = [
<<<<<<< Updated upstream
    path("",views.main),
]
=======
    path("",views.main,name='main'),
    path("mypage/",views.mypage, name='mypage'),
] 
>>>>>>> Stashed changes
