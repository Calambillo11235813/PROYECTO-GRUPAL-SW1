"""
URL configuration for Backend project.

For more information, see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('usuario.urls')),  # Include usuario URLs under /api/auth/
    path('api/audio/', include('audio.urls')),
    path('api/texto/', include('texto.urls')),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
