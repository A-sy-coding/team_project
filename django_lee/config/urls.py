from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('healf.urls')),
    path('', RedirectView.as_view(url='/home/')),
    path('user/', include('user.urls')),
]
