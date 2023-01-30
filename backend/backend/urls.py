from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

API_URL = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{API_URL}/auth/', include('apps.users.api.urls')),
    path(f'{API_URL}/payments/', include('apps.payments.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
