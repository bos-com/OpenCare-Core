"""
Health Workers models for OpenCare-Africa health system.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User, HealthFacility, Location


class HealthWorkerProfile(models.Model):
    """
    Extended profile for health workers with additional professional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_worker_profile')
    
    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=100, blank=True)
    sub_specialization = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    # Employment Details
    primary_facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='primary_staff')
    secondary_facilities = models.ManyToManyField(HealthFacility, blank=True, related_name='secondary_staff')
    
    # Professional Status
    is_licensed = models.BooleanField(default=True)
    license_expiry_date = models.DateField(null=True, blank=True)
    is_active_practitioner = models.BooleanField(default=True)
    
    # Contact Information
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Additional Information
    bio = models.TextField(blank=True)
    languages_spoken = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Health Worker Profile')
        verbose_name_plural = _('Health Worker Profiles')
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"


class ProfessionalQualification(models.Model):
    """
    Model for storing professional qualifications and certifications.
    """
    health_worker = models.ForeignKey(HealthWorkerProfile, on_delete=models.CASCADE, related_name='qualifications')
    
    # Qualification Details
    qualification_type = models.CharField(max_length=100, choices=[
        ('degree', _('Academic Degree')),
        ('diploma', _('Diploma')),
        ('certification', _('Professional Certification')),
        ('license', _('Professional License')),
        ('training', _('Training Program')),
    ])
    
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    
    # Dates
    start_date = models.DateField()
    completion_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # Additional Information
    grade = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    certificate_file = models.FileField(upload_to='qualifications/', null=True, blank=True)
    
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verification_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Professional Qualification')
        verbose_name_plural = _('Professional Qualifications')
        ordering = ['-completion_date']
    
    def __str__(self):
        return f"{self.title} - {self.health_worker.user.get_full_name()}"


class WorkSchedule(models.Model):
    """
    Model for managing health worker work schedules.
    """
    health_worker = models.ForeignKey(HealthWorkerProfile, on_delete=models.CASCADE, related_name='work_schedules')
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE)
    
    # Schedule Details
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
    
    # Schedule Type
    schedule_type = models.CharField(max_length=20, choices=[
        ('regular', _('Regular Schedule')),
        ('on_call', _('On-Call')),
        ('overtime', _('Overtime')),
        ('emergency', _('Emergency Coverage')),
    ], default='regular')
    
    # Availability
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Work Schedule')
        verbose_name_plural = _('Work Schedules')
        unique_together = ['health_worker', 'facility', 'day_of_week', 'start_time']
        ordering = ['health_worker', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.health_worker.user.get_full_name()} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class ProfessionalDevelopment(models.Model):
    """
    Model for tracking professional development activities.
    """
    health_worker = models.ForeignKey(HealthWorkerProfile, on_delete=models.CASCADE, related_name='professional_development')
    
    # Activity Details
    activity_type = models.CharField(max_length=50, choices=[
        ('training', _('Training Program')),
        ('conference', _('Conference/Workshop')),
        ('seminar', _('Seminar')),
        ('online_course', _('Online Course')),
        ('research', _('Research Project')),
        ('publication', _('Publication')),
        ('presentation', _('Presentation')),
    ])
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.CharField(max_length=200)
    
    # Dates and Duration
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.PositiveIntegerField(null=True, blank=True)
    
    # Outcomes
    certificate_received = models.BooleanField(default=False)
    certificate_file = models.FileField(upload_to='professional_development/', null=True, blank=True)
    credits_earned = models.PositiveIntegerField(null=True, blank=True)
    
    # Cost and Funding
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    funding_source = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Professional Development')
        verbose_name_plural = _('Professional Development')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} - {self.health_worker.user.get_full_name()}"


class PerformanceEvaluation(models.Model):
    """
    Model for tracking health worker performance evaluations.
    """
    health_worker = models.ForeignKey(HealthWorkerProfile, on_delete=models.CASCADE, related_name='performance_evaluations')
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_given')
    
    # Evaluation Details
    evaluation_date = models.DateField()
    evaluation_period_start = models.DateField()
    evaluation_period_end = models.DateField()
    
    # Performance Ratings (1-5 scale)
    clinical_skills = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    communication_skills = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    teamwork = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    professionalism = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    productivity = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    
    # Overall Rating
    overall_rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    
    # Feedback
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals = models.TextField()
    
    # Action Items
    action_items = models.JSONField(default=list)
    follow_up_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Performance Evaluation')
        verbose_name_plural = _('Performance Evaluations')
        ordering = ['-evaluation_date']
    
    def __str__(self):
        return f"Performance Evaluation - {self.health_worker.user.get_full_name()} ({self.evaluation_date})"
    
    def save(self, *args, **kwargs):
        # Calculate overall rating as average of individual ratings
        ratings = [
            self.clinical_skills, self.communication_skills, self.teamwork,
            self.professionalism, self.productivity
        ]
        self.overall_rating = sum(ratings) // len(ratings)
        super().save(*args, **kwargs)
