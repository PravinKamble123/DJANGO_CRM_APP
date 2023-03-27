from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('user/', include('user.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/teams/', include('team.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
