"""
Core models for OpenCare-Africa health system.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom user model for health workers and administrators.
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        PROVIDER = 'provider', _('Healthcare Provider')
        PATIENT = 'patient', _('Patient')

    USER_TYPE_CHOICES = [
        ('admin', _('Administrator')),
        ('doctor', _('Doctor')),
        ('nurse', _('Nurse')),
        ('midwife', _('Midwife')),
        ('community_worker', _('Community Health Worker')),
        ('pharmacist', _('Pharmacist')),
        ('lab_technician', _('Laboratory Technician')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PROVIDER,
        help_text=_('High-level persona used for role-based access control.')
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='community_worker'
    )
    
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Phone number must be entered in the format: +999999999. Up to 15 digits allowed.')
            )
        ],
        blank=True
    )
    
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Health worker specific fields
    license_number = models.CharField(max_length=50, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_provider_role(self):
        return self.role == self.Role.PROVIDER

    @property
    def is_patient_role(self):
        return self.role == self.Role.PATIENT


class Location(models.Model):
    """
    Geographic location model for health facilities and patients.
    """
    LOCATION_TYPE_CHOICES = [
        ('country', _('Country')),
        ('region', _('Region')),
        ('district', _('District')),
        ('subcounty', _('Sub-county')),
        ('parish', _('Parish')),
        ('village', _('Village')),
    ]
    
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        unique_together = ['name', 'parent', 'location_type']
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
    
    def __str__(self):
        if self.parent:
            return f"{self.name}, {self.parent}"
        return self.name


class HealthFacility(models.Model):
    """
    Health facility model.
    """
    FACILITY_TYPE_CHOICES = [
        ('hospital', _('Hospital')),
        ('health_center', _('Health Center')),
        ('clinic', _('Clinic')),
        ('dispensary', _('Dispensary')),
        ('laboratory', _('Laboratory')),
        ('pharmacy', _('Pharmacy')),
    ]
    
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Operating hours
    is_24_hours = models.BooleanField(default=False)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    
    # Services offered
    services_offered = models.JSONField(default=list)
    
    # Contact person
    contact_person_name = models.CharField(max_length=100)
    contact_person_phone = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Health Facility')
        verbose_name_plural = _('Health Facilities')
    
    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()})"


class AuditTrail(models.Model):
    """
    Audit trail model for tracking changes to health records.
    """
    ACTION_CHOICES = [
        ('create', _('Create')),
        ('update', _('Update')),
        ('delete', _('Delete')),
        ('view', _('View')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    changes = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('Audit Trail')
        verbose_name_plural = _('Audit Trails')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} on {self.model_name} by {self.user} at {self.timestamp}"


class SystemConfiguration(models.Model):
    """
    System configuration model for storing application settings.
    """
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('System Configuration')
        verbose_name_plural = _('System Configurations')
    
    def __str__(self):
        return self.key
