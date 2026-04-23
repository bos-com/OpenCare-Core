"""
URL configuration for core app.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Home page
    path('home/', views.home, name='home'),
    
    # System information
    path('system-info/', views.system_info, name='system_info'),
    path('health-status/', views.health_status, name='health_status'),
    
    # User management
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Location management
    path('locations/', views.location_list, name='location_list'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    
    # Facility management
    path('facilities/', views.facility_list, name='facility_list'),
    path('facilities/<int:pk>/', views.facility_detail, name='facility_detail'),
    
    # Reports and analytics
    path('reports/', views.reports, name='reports'),
    path('analytics/', views.analytics, name='analytics'),
    
    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/system/', views.system_settings, name='system_settings'),
]
