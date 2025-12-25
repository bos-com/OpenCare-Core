"""
Appointment scheduling models.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Appointment(models.Model):
    """
    Represents a scheduled interaction between a patient and provider.
    """

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", _("Scheduled")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")
        NO_SHOW = "no_show", _("No Show")

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    facility = models.ForeignKey(
        "core.HealthFacility",
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    appointment_type = models.CharField(max_length=50, blank=True)
    reason = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notifications_sent = models.JSONField(default=list, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="appointments_created",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["provider", "start_time"]),
            models.Index(fields=["patient", "start_time"]),
            models.Index(fields=["facility", "start_time"]),
        ]

    def __str__(self):
        return f"{self.patient} with {self.provider} on {self.start_time:%Y-%m-%d %H:%M}"

    def check_conflicts(self, exclude_pk=None):
        """
        Check for scheduling conflicts with existing appointments.
        
        Returns a dict with conflict information if conflicts exist.
        """
        from django.db.models import Q
        
        active_statuses = [self.Status.SCHEDULED, self.Status.NO_SHOW]
        query = Q(
            status__in=active_statuses,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        
        if exclude_pk:
            query &= ~Q(pk=exclude_pk)
        
        conflicts = Appointment.objects.filter(query)
        
        provider_conflicts = conflicts.filter(provider=self.provider)
        patient_conflicts = conflicts.filter(patient=self.patient)
        facility_conflicts = conflicts.filter(facility=self.facility)
        
        result = {}
        if provider_conflicts.exists():
            result['provider'] = list(provider_conflicts.values('id', 'start_time', 'end_time', 'patient__first_name', 'patient__last_name'))
        if patient_conflicts.exists():
            result['patient'] = list(patient_conflicts.values('id', 'start_time', 'end_time', 'provider__first_name', 'provider__last_name'))
        if facility_conflicts.exists():
            result['facility'] = list(facility_conflicts.values('id', 'start_time', 'end_time', 'patient__first_name', 'provider__first_name'))
        
        return result if result else None

    @property
    def duration_minutes(self):
        """Calculate appointment duration in minutes."""
        if self.start_time and self.end_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return 0

    @property
    def is_upcoming(self):
        """Check if appointment is in the future."""
        from django.utils import timezone
        return self.start_time > timezone.now() and self.status == self.Status.SCHEDULED
