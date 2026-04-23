"""
Patient models for OpenCare-Africa health system.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from apps.core.models import Location, HealthFacility


class Patient(models.Model):
    """
    Patient model for storing patient information.
    """
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', _('Single')),
        ('married', _('Married')),
        ('divorced', _('Divorced')),
        ('widowed', _('Widowed')),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Basic Information
    patient_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    
    # Contact Information
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Phone number must be entered in the format: +999999999. Up to 15 digits allowed.')
            )
        ]
    )
    email = models.EmailField(blank=True)
    address = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relationship = models.CharField(max_length=50)
    
    # Medical Information
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    allergies = models.JSONField(default=list)
    chronic_conditions = models.JSONField(default=list)
    current_medications = models.JSONField(default=list)
    
    # Insurance & Financial
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Registration
    registered_facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Additional Information
    occupation = models.CharField(max_length=100, blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    ethnicity = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"
    
    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class PatientVisit(models.Model):
    """
    Model for tracking patient visits to health facilities.
    """
    VISIT_TYPE_CHOICES = [
        ('consultation', _('Consultation')),
        ('emergency', _('Emergency')),
        ('follow_up', _('Follow-up')),
        ('vaccination', _('Vaccination')),
        ('laboratory', _('Laboratory Test')),
        ('pharmacy', _('Pharmacy')),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', _('Scheduled')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('no_show', _('No Show')),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Visit Details
    scheduled_date = models.DateTimeField()
    actual_date = models.DateTimeField(null=True, blank=True)
    chief_complaint = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    prescription = models.JSONField(default=list)
    
    # Healthcare Provider
    attending_provider = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Financial
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Patient Visit')
        verbose_name_plural = _('Patient Visits')
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.patient} - {self.get_visit_type_display()} at {self.facility}"


class PatientMedicalHistory(models.Model):
    """
    Model for storing patient medical history.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition = models.CharField(max_length=200)
    diagnosis_date = models.DateField()
    is_active = models.BooleanField(default=True)
    severity = models.CharField(max_length=20, choices=[
        ('mild', _('Mild')),
        ('moderate', _('Moderate')),
        ('severe', _('Severe')),
    ])
    
    # Treatment Information
    treatment = models.TextField(blank=True)
    medications = models.JSONField(default=list)
    outcomes = models.TextField(blank=True)
    
    # Healthcare Provider
    diagnosed_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Patient Medical History')
        verbose_name_plural = _('Patient Medical Histories')
        ordering = ['-diagnosis_date']
    
    def __str__(self):
        return f"{self.patient} - {self.condition} ({self.diagnosis_date})"
