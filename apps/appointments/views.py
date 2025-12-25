"""
ViewSet for appointment scheduling.
"""

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.mixins import AuditLogMixin
from apps.api.permissions import RoleRequired
from django.contrib.auth import get_user_model
from .models import Appointment
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
    AppointmentSerializer,
)
from .notifications import send_notification

User = get_user_model()


class AppointmentViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    Manage patient-provider appointments with conflict detection.
    """

    queryset = (
        Appointment.objects.select_related("patient", "provider", "facility", "created_by")
        .all()
    )
    permission_classes = [IsAuthenticated, RoleRequired]
    required_roles = frozenset({User.Role.ADMIN, User.Role.PROVIDER})
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

    @action(detail=False, methods=["get"], url_path="upcoming")
    def upcoming(self, request):
        """Get all upcoming appointments."""
        now = timezone.now()
        queryset = self.get_queryset().filter(
            start_time__gt=now,
            status=Appointment.Status.SCHEDULED
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-provider/(?P<provider_id>[^/.]+)")
    def by_provider(self, request, provider_id=None):
        """Get appointments for a specific provider."""
        queryset = self.get_queryset().filter(provider_id=provider_id)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-patient/(?P<patient_id>[^/.]+)")
    def by_patient(self, request, patient_id=None):
        """Get appointments for a specific patient."""
        queryset = self.get_queryset().filter(patient_id=patient_id)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="check-conflicts")
    def check_conflicts(self, request, pk=None):
        """Check for scheduling conflicts for this appointment."""
        appointment = self.get_object()
        conflicts = appointment.check_conflicts(exclude_pk=appointment.pk)
        return Response({
            "has_conflicts": conflicts is not None,
            "conflicts": conflicts or {}
        })

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        """Cancel an appointment."""
        appointment = self.get_object()
        if appointment.status == Appointment.Status.CANCELLED:
            return Response(
                {"error": "Appointment is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
        send_notification(appointment, "cancelled")
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        """Mark an appointment as completed."""
        appointment = self.get_object()
        if appointment.status == Appointment.Status.COMPLETED:
            return Response(
                {"error": "Appointment is already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        send_notification(appointment, "updated")
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="mark-no-show")
    def mark_no_show(self, request, pk=None):
        """Mark an appointment as no-show."""
        appointment = self.get_object()
        if appointment.status == Appointment.Status.NO_SHOW:
            return Response(
                {"error": "Appointment is already marked as no-show."},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = Appointment.Status.NO_SHOW
        appointment.save()
        send_notification(appointment, "updated")
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
