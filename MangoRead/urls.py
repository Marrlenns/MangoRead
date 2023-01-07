from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from .yasg import urlpatterns as swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('manga.urls')),
    path('user/', include('users.urls'))
] + swagger + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
