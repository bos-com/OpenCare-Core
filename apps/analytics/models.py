"""
Analytics models for OpenCare-Africa health system.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User, HealthFacility, Location
from apps.patients.models import Patient


class HealthMetrics(models.Model):
    """
    Model for storing health metrics and KPIs.
    """
    METRIC_TYPE_CHOICES = [
        ('patient_count', _('Patient Count')),
        ('visit_count', _('Visit Count')),
        ('disease_prevalence', _('Disease Prevalence')),
        ('mortality_rate', _('Mortality Rate')),
        ('birth_rate', _('Birth Rate')),
        ('vaccination_rate', _('Vaccination Rate')),
        ('treatment_success', _('Treatment Success Rate')),
        ('wait_time', _('Average Wait Time')),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    period = models.CharField(max_length=20, choices=[
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('yearly', _('Yearly')),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Health Metric')
        verbose_name_plural = _('Health Metrics')
        unique_together = ['metric_type', 'location', 'facility', 'date', 'period']
        ordering = ['-date', 'metric_type']
    
    def __str__(self):
        location_str = f" at {self.location}" if self.location else ""
        facility_str = f" at {self.facility}" if self.facility else ""
        return f"{self.get_metric_type_display()}: {self.value} {self.unit}{location_str}{facility_str}"


class DiseaseOutbreak(models.Model):
    """
    Model for tracking disease outbreaks and epidemics.
    """
    SEVERITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ]
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('contained', _('Contained')),
        ('resolved', _('Resolved')),
    ]
    
    disease_name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Case counts
    total_cases = models.PositiveIntegerField(default=0)
    active_cases = models.PositiveIntegerField(default=0)
    recovered_cases = models.PositiveIntegerField(default=0)
    fatal_cases = models.PositiveIntegerField(default=0)
    
    # Response information
    response_measures = models.JSONField(default=list)
    affected_facilities = models.ManyToManyField(HealthFacility)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Disease Outbreak')
        verbose_name_plural = _('Disease Outbreaks')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.disease_name} outbreak in {self.location} ({self.get_status_display()})"


class HealthReport(models.Model):
    """
    Model for generating and storing health reports.
    """
    REPORT_TYPE_CHOICES = [
        ('daily', _('Daily Report')),
        ('weekly', _('Weekly Report')),
        ('monthly', _('Monthly Report')),
        ('quarterly', _('Quarterly Report')),
        ('annual', _('Annual Report')),
        ('incident', _('Incident Report')),
        ('outbreak', _('Outbreak Report')),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    
    # Report period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Report content
    content = models.JSONField(default=dict)
    summary = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    # File attachments
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Health Report')
        verbose_name_plural = _('Health Reports')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"


class PatientAnalytics(models.Model):
    """
    Model for patient-specific analytics and insights.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    analysis_date = models.DateField()
    
    # Health indicators
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    health_trend = models.CharField(max_length=20, choices=[
        ('improving', _('Improving')),
        ('stable', _('Stable')),
        ('declining', _('Declining')),
        ('critical', _('Critical')),
    ], blank=True)
    
    # Visit patterns
    visit_frequency = models.PositiveIntegerField(default=0)
    last_visit_date = models.DateField(null=True, blank=True)
    next_scheduled_visit = models.DateField(null=True, blank=True)
    
    # Treatment effectiveness
    treatment_compliance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    medication_adherence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Predictive analytics
    predicted_health_issues = models.JSONField(default=list)
    recommended_actions = models.JSONField(default=list)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Patient Analytics')
        verbose_name_plural = _('Patient Analytics')
        unique_together = ['patient', 'analysis_date']
        ordering = ['-analysis_date']
    
    def __str__(self):
        return f"Analytics for {self.patient} on {self.analysis_date}"
