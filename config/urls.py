"""
URL configuration for opencare-africa project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Admin site customization
admin.site.site_header = 'OpenCare-Africa Administration'
admin.site.site_title = 'OpenCare-Africa Admin'
admin.site.index_title = 'Welcome to OpenCare-Africa Admin'

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Health Check
    path('health/', include('health_check.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/v1/', include('apps.api.urls')),
    
    # Core App URLs
    path('', include('apps.core.urls')),
    
    # Patient Management
    path('patients/', include('apps.patients.urls')),
    
    # Health Workers - temporarily commented out
    # path('health-workers/', include('apps.health_workers.urls')),
    
    # Facilities - temporarily commented out
    # path('facilities/', include('apps.facilities.urls')),
    
    # Health Records - temporarily commented out
    # path('records/', include('apps.records.urls')),
    
    # Analytics - temporarily commented out
    # path('analytics/', include('apps.analytics.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
