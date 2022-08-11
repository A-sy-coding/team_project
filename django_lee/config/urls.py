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

# Summernote 설정
from django.conf import settings
from django.conf.urls.static import static

urlpatterns +=[path('summernote/', include('django_summernote.urls'))]
if settings.DEBUG : 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)