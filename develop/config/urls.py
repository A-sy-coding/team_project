from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    # home(main page) -> ex)127.0.0.1:[port]
    path('', views.HomeView, name = 'home'),

    path("admin/", admin.site.urls),
    path("users/",include('users.urls')), 
    path('challenge/', include('challenge.urls')),
    path("exercsie/",include('exercise.urls')),
]
