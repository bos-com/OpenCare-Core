"""
Admin configuration for patient models.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Patient, PatientVisit, PatientMedicalHistory


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin interface for Patient model.
    """
    list_display = [
        'patient_id', 'first_name', 'last_name', 'gender', 'age',
        'phone_number', 'location', 'registered_facility', 'is_active',
        'registration_date'
    ]
    list_filter = [
        'gender', 'marital_status', 'blood_type', 'is_active',
        'location', 'registered_facility', 'registration_date'
    ]
    search_fields = [
        'patient_id', 'first_name', 'last_name', 'phone_number',
        'email', 'emergency_contact_name'
    ]
    ordering = ['-registration_date']
    list_per_page = 25
    
    fieldsets = (
        (_('Patient Information'), {
            'fields': (
                'patient_id', 'first_name', 'last_name', 'middle_name',
                'date_of_birth', 'gender', 'marital_status'
            )
        }),
        (_('Contact Information'), {
            'fields': (
                'phone_number', 'email', 'address', 'location'
            )
        }),
        (_('Emergency Contact'), {
            'fields': (
                'emergency_contact_name', 'emergency_contact_phone',
                'emergency_contact_relationship'
            )
        }),
        (_('Medical Information'), {
            'fields': (
                'blood_type', 'allergies', 'chronic_conditions',
                'current_medications'
            )
        }),
        (_('Registration'), {
            'fields': (
                'registered_facility', 'is_active', 'registration_date'
            )
        }),
        (_('Additional Information'), {
            'fields': (
                'occupation', 'education_level', 'religion', 'ethnicity'
            ),
            'classes': ('collapse',)
        }),
        (_('Insurance & Payment'), {
            'fields': (
                'insurance_provider', 'insurance_number', 'payment_method'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['patient_id', 'registration_date', 'created_at', 'updated_at']
    
    def age(self, obj):
        return obj.get_age()
    age.short_description = _('Age')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('location', 'registered_facility')


@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    """
    Admin interface for PatientVisit model.
    """
    list_display = [
        'patient', 'facility', 'visit_type', 'status', 'scheduled_date',
        'attending_provider', 'payment_status'
    ]
    list_filter = [
        'visit_type', 'status', 'facility', 'scheduled_date',
        'payment_status', 'created_at'
    ]
    search_fields = [
        'patient__first_name', 'patient__last_name', 'patient__patient_id',
        'facility__name', 'attending_provider__username'
    ]
    ordering = ['-scheduled_date']
    list_per_page = 25
    
    fieldsets = (
        (_('Visit Information'), {
            'fields': (
                'patient', 'facility', 'visit_type', 'status'
            )
        }),
        (_('Schedule'), {
            'fields': ('scheduled_date', 'actual_date')
        }),
        (_('Clinical Information'), {
            'fields': (
                'chief_complaint', 'diagnosis', 'treatment_plan',
                'prescription'
            )
        }),
        (_('Healthcare Provider'), {
            'fields': ('attending_provider',)
        }),
        (_('Financial'), {
            'fields': (
                'consultation_fee', 'total_cost', 'payment_status'
            )
        }),
        (_('Notes'), {
            'fields': ('notes',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'patient', 'facility', 'attending_provider'
        )


@admin.register(PatientMedicalHistory)
class PatientMedicalHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for PatientMedicalHistory model.
    """
    list_display = [
        'patient', 'condition', 'diagnosis_date', 'severity',
        'is_active', 'facility', 'diagnosed_by'
    ]
    list_filter = [
        'severity', 'is_active', 'facility', 'diagnosis_date',
        'created_at'
    ]
    search_fields = [
        'patient__first_name', 'patient__last_name', 'patient__patient_id',
        'condition', 'facility__name', 'diagnosed_by__username'
    ]
    ordering = ['-diagnosis_date']
    list_per_page = 25
    
    fieldsets = (
        (_('Patient & Condition'), {
            'fields': (
                'patient', 'condition', 'diagnosis_date', 'severity',
                'is_active'
            )
        }),
        (_('Treatment Information'), {
            'fields': (
                'treatment', 'medications', 'outcomes'
            )
        }),
        (_('Healthcare Provider'), {
            'fields': ('diagnosed_by', 'facility')
        }),
        (_('Notes'), {
            'fields': ('notes',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'patient', 'facility', 'diagnosed_by'
        )


# Inline admin for related models
class PatientVisitInline(admin.TabularInline):
    """
    Inline admin for PatientVisit in Patient admin.
    """
    model = PatientVisit
    extra = 0
    readonly_fields = ['created_at']
    fields = ['visit_type', 'status', 'scheduled_date', 'facility', 'attending_provider']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('facility', 'attending_provider')


class PatientMedicalHistoryInline(admin.TabularInline):
    """
    Inline admin for PatientMedicalHistory in Patient admin.
    """
    model = PatientMedicalHistory
    extra = 0
    readonly_fields = ['created_at']
    fields = ['condition', 'diagnosis_date', 'severity', 'is_active', 'facility']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('facility')


# Add inlines to Patient admin
PatientAdmin.inlines = [PatientVisitInline, PatientMedicalHistoryInline]
