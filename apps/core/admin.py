"""
Admin configuration for core models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Location, HealthFacility, AuditTrail, SystemConfiguration

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'role', 'user_type',
        'phone_number', 'is_active', 'date_joined', 'last_login'
    ]
    list_filter = [
        'role', 'user_type', 'is_active', 'is_staff', 'is_superuser',
        'date_joined', 'last_login'
    ]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number',
                'date_of_birth', 'profile_picture'
            )
        }),
        (_('Professional info'), {
            'fields': (
                'role', 'user_type', 'license_number', 'specialization',
                'years_of_experience'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'role', 'user_type'
            ),
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin interface for Location model.
    """
    list_display = [
        'name', 'location_type', 'parent', 'latitude', 'longitude',
        'get_full_location'
    ]
    list_filter = ['location_type', 'parent']
    search_fields = ['name', 'parent__name']
    ordering = ['location_type', 'name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'location_type', 'parent')
        }),
        (_('Geographic Information'), {
            'fields': ('latitude', 'longitude')
        }),
    )
    
    def get_full_location(self, obj):
        if obj.parent:
            return f"{obj.name}, {obj.parent}"
        return obj.name
    get_full_location.short_description = _('Full Location')


@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):
    """
    Admin interface for HealthFacility model.
    """
    list_display = [
        'name', 'facility_type', 'location', 'phone_number',
        'is_24_hours', 'contact_person_name', 'created_at'
    ]
    list_filter = [
        'facility_type', 'is_24_hours', 'location', 'created_at'
    ]
    search_fields = ['name', 'address', 'contact_person_name', 'phone_number']
    ordering = ['name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'facility_type', 'location', 'address')
        }),
        (_('Contact Information'), {
            'fields': (
                'phone_number', 'email', 'website', 'contact_person_name',
                'contact_person_phone'
            )
        }),
        (_('Operating Hours'), {
            'fields': ('is_24_hours', 'opening_time', 'closing_time')
        }),
        (_('Services'), {
            'fields': ('services_offered',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    """
    Admin interface for AuditTrail model.
    """
    list_display = [
        'user', 'action', 'model_name', 'object_id', 'timestamp',
        'ip_address'
    ]
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'model_name']
    ordering = ['-timestamp']
    
    fieldsets = (
        (_('Action Details'), {
            'fields': ('user', 'action', 'model_name', 'object_id')
        }),
        (_('Changes'), {
            'fields': ('changes',)
        }),
        (_('Context'), {
            'fields': ('ip_address', 'user_agent', 'timestamp')
        }),
    )
    
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    """
    Admin interface for SystemConfiguration model.
    """
    list_display = ['key', 'value', 'is_public', 'created_at', 'updated_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['key', 'description']
    ordering = ['key']
    
    fieldsets = (
        (_('Configuration'), {
            'fields': ('key', 'value', 'description', 'is_public')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


# Customize admin site
admin.site.site_header = _('OpenCare-Africa Administration')
admin.site.site_title = _('OpenCare-Africa Admin')
admin.site.index_title = _('Welcome to OpenCare-Africa Admin')
