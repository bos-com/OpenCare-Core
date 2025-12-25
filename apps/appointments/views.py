"""
ViewSet for appointment scheduling.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.mixins import AuditLogMixin
from .models import Appointment
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
    AppointmentSerializer,
)
from .notifications import send_notification


class AppointmentViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    Manage patient-provider appointments with conflict detection.
    """

    queryset = (
        Appointment.objects.select_related("patient", "provider", "facility")
        .all()
    )
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    filterset_fields = [
        "provider",
        "patient",
        "facility",
        "status",
        "appointment_type",
    ]
    search_fields = [
        "patient__patient_id",
        "patient__first_name",
        "patient__last_name",
        "provider__first_name",
        "provider__last_name",
    ]
    ordering_fields = ["start_time", "created_at"]
    ordering = ["start_time"]

    serializer_action_map = {
        "list": AppointmentSerializer,
        "retrieve": AppointmentDetailSerializer,
        "create": AppointmentCreateSerializer,
        "update": AppointmentCreateSerializer,
        "partial_update": AppointmentCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        appointment = super().perform_create(serializer)
        send_notification(appointment, "created")
        return appointment

    def perform_update(self, serializer):
        appointment = super().perform_update(serializer)
        send_notification(appointment, "updated")
        return appointment

    def perform_destroy(self, instance):
        send_notification(instance, "cancelled")
        super().perform_destroy(instance)
