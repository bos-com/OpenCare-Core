"""
URL configuration for API app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'patients', views.PatientViewSet, basename='patients')
router.register(r'health-workers', views.HealthWorkerViewSet, basename='health-workers')
router.register(r'facilities', views.FacilityViewSet, basename='facilities')
router.register(r'visits', views.PatientVisitViewSet, basename='visits')
router.register(r'records', views.HealthRecordViewSet, basename='records')
router.register(r'audit-logs', views.AuditTrailViewSet, basename='audit-logs')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')

urlpatterns = [
    # API v1 endpoints
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # Custom endpoints
    path('stats/', views.api_stats, name='api_stats'),
    path('export/', views.export_data, name='export_data'),
]