"""
Facility models for OpenCare-Africa health system.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import HealthFacility, Location, User


class FacilityService(models.Model):
    """
    Model for managing services offered by health facilities.
    """
    SERVICE_CATEGORY_CHOICES = [
        ('primary_care', _('Primary Care')),
        ('emergency_care', _('Emergency Care')),
        ('specialized_care', _('Specialized Care')),
        ('diagnostic', _('Diagnostic Services')),
        ('pharmacy', _('Pharmacy Services')),
        ('laboratory', _('Laboratory Services')),
        ('maternity', _('Maternity Services')),
        ('pediatric', _('Pediatric Services')),
        ('mental_health', _('Mental Health Services')),
        ('rehabilitation', _('Rehabilitation Services')),
    ]
    
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=SERVICE_CATEGORY_CHOICES)
    description = models.TextField()
    
    # Service availability
    is_available = models.BooleanField(default=True)
    availability_schedule = models.JSONField(default=dict)  # Store schedule as JSON
    
    # Service details
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    requirements = models.TextField(blank=True)
    
    # Staff requirements
    required_staff_count = models.PositiveIntegerField(default=1)
    required_qualifications = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Facility Service')
        verbose_name_plural = _('Facility Services')
        unique_together = ['facility', 'name']
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} at {self.facility}"


class FacilityStaff(models.Model):
    """
    Model for managing staff at health facilities.
    """
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE)
    
    # Employment details
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(max_length=20, choices=[
        ('full_time', _('Full Time')),
        ('part_time', _('Part Time')),
        ('contract', _('Contract')),
        ('volunteer', _('Volunteer')),
    ])
    
    # Work schedule
    work_schedule = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    # Employment dates
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    
    # Additional information
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Facility Staff')
        verbose_name_plural = _('Facility Staff')
        unique_together = ['staff', 'facility']
        ordering = ['facility', 'department', 'position']
    
    def __str__(self):
        return f"{self.staff} - {self.position} at {self.facility}"


class FacilityEquipment(models.Model):
    """
    Model for managing medical equipment and resources at facilities.
    """
    EQUIPMENT_STATUS_CHOICES = [
        ('operational', _('Operational')),
        ('maintenance', _('Under Maintenance')),
        ('repair', _('Under Repair')),
        ('out_of_order', _('Out of Order')),
        ('retired', _('Retired')),
    ]
    
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    # Equipment details
    category = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    
    # Status and maintenance
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS_CHOICES, default='operational')
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    
    # Location within facility
    location_in_facility = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(FacilityStaff, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Cost information
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Facility Equipment')
        verbose_name_plural = _('Facility Equipment')
        ordering = ['facility', 'category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()}) at {self.facility}"


class FacilityInventory(models.Model):
    """
    Model for managing medical supplies and inventory at facilities.
    """
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    
    # Quantity and units
    current_quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=20)
    
    # Stock information
    supplier = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Cost information
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Storage location
    storage_location = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Facility Inventory')
        verbose_name_plural = _('Facility Inventory')
        unique_together = ['facility', 'item_name', 'batch_number']
        ordering = ['facility', 'category', 'item_name']
    
    def __str__(self):
        return f"{self.item_name} ({self.current_quantity} {self.unit}) at {self.facility}"
    
    def save(self, *args, **kwargs):
        # Calculate total value
        if self.unit_cost and self.current_quantity:
            self.total_value = self.unit_cost * self.current_quantity
        super().save(*args, **kwargs)


class FacilitySchedule(models.Model):
    """
    Model for managing facility operating schedules and appointments.
    """
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='schedules')
    service = models.ForeignKey(FacilityService, on_delete=models.CASCADE, null=True, blank=True)
    
    # Schedule details
    day_of_week = models.PositiveIntegerField(choices=[
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Availability
    is_available = models.BooleanField(default=True)
    max_appointments = models.PositiveIntegerField(null=True, blank=True)
    current_appointments = models.PositiveIntegerField(default=0)
    
    # Staff assignment
    assigned_staff = models.ManyToManyField(FacilityStaff, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Facility Schedule')
        verbose_name_plural = _('Facility Schedules')
        unique_together = ['facility', 'day_of_week', 'start_time']
        ordering = ['facility', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.facility} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
