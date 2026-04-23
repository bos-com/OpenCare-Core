"""
Health Records models for OpenCare-Africa health system.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import User, HealthFacility
from apps.patients.models import Patient


class HealthRecord(models.Model):
    """
    Main model for patient health records.
    """
    RECORD_TYPE_CHOICES = [
        ('medical', _('Medical Record')),
        ('dental', _('Dental Record')),
        ('mental_health', _('Mental Health Record')),
        ('maternity', _('Maternity Record')),
        ('pediatric', _('Pediatric Record')),
        ('emergency', _('Emergency Record')),
        ('laboratory', _('Laboratory Record')),
        ('imaging', _('Imaging Record')),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    
    # Record Details
    record_date = models.DateTimeField()
    attending_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Clinical Information
    chief_complaint = models.TextField(blank=True)
    history_of_present_illness = models.TextField(blank=True)
    past_medical_history = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    social_history = models.TextField(blank=True)
    
    # Physical Examination
    vital_signs = models.JSONField(default=dict)
    physical_examination = models.TextField(blank=True)
    
    # Assessment and Plan
    assessment = models.TextField(blank=True)
    diagnosis = models.JSONField(default=list)
    treatment_plan = models.TextField(blank=True)
    follow_up_plan = models.TextField(blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    attachments = models.JSONField(default=list)  # Store file paths
    
    # Record Status
    is_active = models.BooleanField(default=True)
    is_confidential = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Health Record')
        verbose_name_plural = _('Health Records')
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.patient} - {self.get_record_type_display()} ({self.record_date})"


class VitalSigns(models.Model):
    """
    Model for storing patient vital signs.
    """
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='vital_signs_detail')
    
    # Vital Signs
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)  # Celsius
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)  # mmHg
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)  # mmHg
    heart_rate = models.PositiveIntegerField(null=True, blank=True)  # bpm
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)  # breaths/min
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True)  # %
    
    # Additional Measurements
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # kg
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Pain Assessment
    pain_scale = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(11)], null=True, blank=True)
    
    # Measurement Context
    measurement_position = models.CharField(max_length=50, blank=True)  # sitting, standing, lying
    measurement_notes = models.TextField(blank=True)
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Vital Signs')
        verbose_name_plural = _('Vital Signs')
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"Vital Signs for {self.health_record.patient} at {self.recorded_at}"
    
    def save(self, *args, **kwargs):
        # Calculate BMI if height and weight are provided
        if self.height and self.weight:
            height_m = self.height / 100  # Convert cm to meters
            self.bmi = round(self.weight / (height_m ** 2), 2)
        super().save(*args, **kwargs)


class Medication(models.Model):
    """
    Model for managing patient medications and prescriptions.
    """
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='medications')
    
    # Medication Details
    medication_name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    dosage_form = models.CharField(max_length=50)  # tablet, capsule, liquid, injection, etc.
    strength = models.CharField(max_length=50)  # 500mg, 10mg/ml, etc.
    
    # Prescription Details
    dosage = models.CharField(max_length=100)  # 1 tablet, 2ml, etc.
    frequency = models.CharField(max_length=100)  # twice daily, every 8 hours, etc.
    route = models.CharField(max_length=50)  # oral, intravenous, topical, etc.
    duration = models.CharField(max_length=100, blank=True)  # 7 days, until finished, etc.
    
    # Prescribing Information
    prescribed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prescription_date = models.DateTimeField(auto_now_add=True)
    
    # Instructions
    instructions = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Adverse Effects
    adverse_effects = models.TextField(blank=True)
    is_discontinued = models.BooleanField(default=False)
    discontinuation_reason = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Medication')
        verbose_name_plural = _('Medications')
        ordering = ['-prescription_date']
    
    def __str__(self):
        return f"{self.medication_name} - {self.dosage} {self.frequency} for {self.health_record.patient}"


class LaboratoryTest(models.Model):
    """
    Model for laboratory test results.
    """
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='laboratory_tests')
    
    # Test Information
    test_name = models.CharField(max_length=200)
    test_category = models.CharField(max_length=100)  # blood, urine, stool, etc.
    test_code = models.CharField(max_length=50, blank=True)
    
    # Test Details
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    collection_date = models.DateTimeField(null=True, blank=True)
    result_date = models.DateTimeField(null=True, blank=True)
    
    # Test Results
    results = models.JSONField(default=dict)  # Store test parameters and values
    reference_range = models.JSONField(default=dict)  # Store normal ranges
    units = models.JSONField(default=dict)  # Store units for each parameter
    
    # Result Interpretation
    is_abnormal = models.BooleanField(default=False)
    interpretation = models.TextField(blank=True)
    clinical_significance = models.TextField(blank=True)
    
    # Quality Control
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tests')
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    specimen_quality = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    attachments = models.JSONField(default=list)  # Store result files
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Laboratory Test')
        verbose_name_plural = _('Laboratory Tests')
        ordering = ['-ordered_date']
    
    def __str__(self):
        return f"{self.test_name} for {self.health_record.patient} ({self.ordered_date})"


class ImagingStudy(models.Model):
    """
    Model for imaging study results (X-rays, CT scans, MRI, etc.).
    """
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='imaging_studies')
    
    # Study Information
    study_type = models.CharField(max_length=100)  # X-ray, CT, MRI, ultrasound, etc.
    body_part = models.CharField(max_length=100)  # chest, abdomen, head, etc.
    study_description = models.TextField()
    
    # Study Details
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    performed_date = models.DateTimeField(null=True, blank=True)
    reported_date = models.DateTimeField(null=True, blank=True)
    
    # Technical Details
    technique = models.TextField(blank=True)
    contrast_used = models.BooleanField(default=False)
    contrast_type = models.CharField(max_length=100, blank=True)
    
    # Results
    findings = models.TextField(blank=True)
    impression = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    # Radiologist
    radiologist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_studies')
    
    # Quality and Safety
    radiation_dose = models.CharField(max_length=100, blank=True)
    safety_checks = models.JSONField(default=list)
    
    # Files and Attachments
    image_files = models.JSONField(default=list)  # Store image file paths
    report_file = models.FileField(upload_to='imaging_reports/', null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Imaging Study')
        verbose_name_plural = _('Imaging Studies')
        ordering = ['-ordered_date']
    
    def __str__(self):
        return f"{self.study_type} - {self.body_part} for {self.health_record.patient}"


class TreatmentPlan(models.Model):
    """
    Model for comprehensive treatment plans.
    """
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='treatment_plans')
    
    # Plan Details
    plan_name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=50, choices=[
        ('acute', _('Acute Care')),
        ('chronic', _('Chronic Disease Management')),
        ('preventive', _('Preventive Care')),
        ('rehabilitation', _('Rehabilitation')),
        ('palliative', _('Palliative Care')),
    ])
    
    # Plan Components
    goals = models.JSONField(default=list)
    interventions = models.JSONField(default=list)
    expected_outcomes = models.TextField()
    timeline = models.CharField(max_length=100, blank=True)
    
    # Care Team
    primary_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    care_team = models.ManyToManyField(User, blank=True, related_name='care_plans')
    
    # Plan Status
    status = models.CharField(max_length=20, choices=[
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('discontinued', _('Discontinued')),
        ('on_hold', _('On Hold')),
    ], default='active')
    
    # Progress Tracking
    progress_notes = models.JSONField(default=list)
    milestones = models.JSONField(default=list)
    
    # Evaluation
    effectiveness_rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    patient_satisfaction = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Treatment Plan')
        verbose_name_plural = _('Treatment Plans')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.plan_name} for {self.health_record.patient} ({self.get_status_display()})"
