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
