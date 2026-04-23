"""
URL configuration for patients app.
"""

from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Patient management
    path('', views.patient_list, name='patient_list'),
    path('create/', views.patient_create, name='patient_create'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    
    # Patient search
    path('search/', views.patient_search, name='patient_search'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    
    # Patient visits
    path('<int:patient_pk>/visits/', views.patient_visits, name='patient_visits'),
    path('<int:patient_pk>/visits/create/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/edit/', views.visit_edit, name='visit_edit'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    
    # Patient medical history
    path('<int:patient_pk>/medical-history/', views.medical_history, name='medical_history'),
    path('<int:patient_pk>/medical-history/create/', views.medical_history_create, name='medical_history_create'),
    path('medical-history/<int:pk>/', views.medical_history_detail, name='medical_history_detail'),
    path('medical-history/<int:pk>/edit/', views.medical_history_edit, name='medical_history_edit'),
    path('medical-history/<int:pk>/delete/', views.medical_history_delete, name='medical_history_delete'),
    
    # Patient statistics and reports
    path('statistics/', views.patient_statistics, name='patient_statistics'),
    path('reports/', views.patient_reports, name='patient_reports'),
    path('export/', views.export_patients, name='export_patients'),
    
    # Bulk operations
    path('bulk-import/', views.bulk_import, name='bulk_import'),
    path('bulk-export/', views.bulk_export, name='bulk_export'),
    
    # Patient dashboard
    path('<int:pk>/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('<int:pk>/timeline/', views.patient_timeline, name='patient_timeline'),
]
