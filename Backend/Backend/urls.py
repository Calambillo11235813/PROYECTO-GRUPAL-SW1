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
    path('', include('audio.urls')),  # Moved to root to serve the main interface at /
    path('api/audio/', include('audio.api_urls')),  # API endpoints under /api/audio/
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
