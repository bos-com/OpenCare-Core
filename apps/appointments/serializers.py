"""
Serializers for appointment scheduling.
"""

from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core.models import HealthFacility, User
from apps.patients.models import Patient

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing appointments.
    """

    patient_name = serializers.CharField(source="patient.get_full_name", read_only=True)
    provider_name = serializers.CharField(source="provider.get_full_name", read_only=True)
    facility_name = serializers.CharField(source="facility.name", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "patient_name",
            "provider",
            "provider_name",
            "facility",
            "facility_name",
            "appointment_type",
            "reason",
            "status",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AppointmentDetailSerializer(AppointmentSerializer):
    """
    Detailed serializer that includes notification metadata.
    """

    class Meta(AppointmentSerializer.Meta):
        fields = AppointmentSerializer.Meta.fields + ["notifications_sent"]
        read_only_fields = AppointmentSerializer.Meta.read_only_fields + ["notifications_sent"]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating appointments with conflict detection.
    """

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "provider",
            "facility",
            "appointment_type",
            "reason",
            "status",
            "start_time",
            "end_time",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        start = attrs.get("start_time") or getattr(self.instance, "start_time", None)
        end = attrs.get("end_time") or getattr(self.instance, "end_time", None)
        if start is None or end is None:
            raise serializers.ValidationError(_("Start and end times are required."))
        if start >= end:
            raise serializers.ValidationError(_("End time must be after start time."))
        if end - start < timedelta(minutes=5):
            raise serializers.ValidationError(_("Appointment must be at least 5 minutes long."))

        provider = attrs.get("provider") or getattr(self.instance, "provider", None)
        patient = attrs.get("patient") or getattr(self.instance, "patient", None)
        facility = attrs.get("facility") or getattr(self.instance, "facility", None)

        if provider and provider.user_type not in {"doctor", "nurse", "midwife", "community_worker"}:
            raise serializers.ValidationError(_("Selected provider is not eligible for appointments."))

        active_statuses = [Appointment.Status.SCHEDULED, Appointment.Status.NO_SHOW]
        query_kwargs = {"status__in": active_statuses, "start_time__lt": end, "end_time__gt": start}
        appointments = Appointment.objects.filter(**query_kwargs)
        if self.instance:
            appointments = appointments.exclude(pk=self.instance.pk)

        if provider and appointments.filter(provider=provider).exists():
            raise serializers.ValidationError({"provider": _("Provider already has an appointment in this window.")})
        if patient and appointments.filter(patient=patient).exists():
            raise serializers.ValidationError({"patient": _("Patient already has an appointment in this window.")})
        if facility and appointments.filter(facility=facility).exists():
            raise serializers.ValidationError({"facility": _("Facility already has an appointment in this window.")})

        return attrs

    def validate_provider(self, value):
        if not value.is_active:
            raise serializers.ValidationError(_("Provider account is inactive."))
        return value

    def validate_patient(self, value):
        if not value.is_active:
            raise serializers.ValidationError(_("Patient profile is inactive."))
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.setdefault("created_by", getattr(request, "user", None))
        return super().create(validated_data)
