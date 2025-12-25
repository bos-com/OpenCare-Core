"""
Serializers for patient health record APIs.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.core.models import User
from apps.patients.models import Patient

from .models import HealthRecord, VitalSigns, Medication, LaboratoryTest


class HealthRecordSerializer(serializers.ModelSerializer):
    """
    Lightweight representation of a health record for list views.
    """

    record_type_display = serializers.CharField(source="get_record_type_display", read_only=True)
    patient_name = serializers.CharField(source="patient.get_full_name", read_only=True)
    facility_name = serializers.CharField(source="facility.name", read_only=True)
    provider_name = serializers.CharField(
        source="attending_provider.get_full_name", read_only=True
    )

    class Meta:
        model = HealthRecord
        fields = [
            "id",
            "patient",
            "patient_name",
            "facility",
            "facility_name",
            "record_type",
            "record_type_display",
            "record_date",
            "attending_provider",
            "provider_name",
            "chief_complaint",
            "assessment",
            "diagnosis",
            "treatment_plan",
            "follow_up_plan",
            "is_active",
            "is_confidential",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class HealthRecordDetailSerializer(HealthRecordSerializer):
    """
    Extend the base health record serializer with full clinical context.
    """

    class Meta(HealthRecordSerializer.Meta):
        fields = HealthRecordSerializer.Meta.fields + [
            "history_of_present_illness",
            "past_medical_history",
            "family_history",
            "social_history",
            "vital_signs",
            "physical_examination",
            "notes",
            "attachments",
        ]


class HealthRecordCreateSerializer(serializers.ModelSerializer):
    """
    Handle creation and updates while validating related foreign keys.
    """

    class Meta:
        model = HealthRecord
        fields = [
            "patient",
            "facility",
            "record_type",
            "record_date",
            "attending_provider",
            "chief_complaint",
            "history_of_present_illness",
            "past_medical_history",
            "family_history",
            "social_history",
            "vital_signs",
            "physical_examination",
            "assessment",
            "diagnosis",
            "treatment_plan",
            "follow_up_plan",
            "notes",
            "attachments",
            "is_confidential",
            "is_active",
        ]

    def validate(self, attrs):
        """
        Ensure the referenced patient, provider, and facility are active entries.
        """
        patient: Patient = attrs.get("patient")
        provider: User | None = attrs.get("attending_provider")
        if patient and not patient.is_active:
            raise serializers.ValidationError("Patient profile is inactive.")

        if provider and not provider.is_active:
            raise serializers.ValidationError("Attending provider account is inactive.")

        return attrs


class VitalSignsSerializer(serializers.ModelSerializer):
    """
    Serializer for VitalSigns associated with a health record.
    """

    recorded_by_name = serializers.CharField(source="recorded_by.get_full_name", read_only=True)

    class Meta:
        model = VitalSigns
        fields = [
            "id",
            "health_record",
            "temperature",
            "blood_pressure_systolic",
            "blood_pressure_diastolic",
            "heart_rate",
            "respiratory_rate",
            "oxygen_saturation",
            "height",
            "weight",
            "bmi",
            "pain_scale",
            "measurement_position",
            "measurement_notes",
            "recorded_at",
            "recorded_by",
            "recorded_by_name",
        ]
        read_only_fields = ["id", "recorded_at", "bmi"]


class MedicationSerializer(serializers.ModelSerializer):
    """
    Serializer for Medication entries on a health record.
    """

    prescribed_by_name = serializers.CharField(source="prescribed_by.get_full_name", read_only=True)

    class Meta:
        model = Medication
        fields = [
            "id",
            "health_record",
            "medication_name",
            "dosage_form",
            "strength",
            "dosage",
            "frequency",
            "route",
            "duration",
            "prescribed_by",
            "prescribed_by_name",
            "instructions",
            "special_instructions",
            "is_active",
            "start_date",
            "end_date",
            "notes",
            "is_discontinued",
            "discontinuation_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class LaboratoryTestSerializer(serializers.ModelSerializer):
    """
    Serializer for laboratory test results linked to a health record.
    """

    ordered_by_name = serializers.CharField(source="ordered_by.get_full_name", read_only=True)
    verified_by_name = serializers.CharField(source="verified_by.get_full_name", read_only=True)

    class Meta:
        model = LaboratoryTest
        fields = [
            "id",
            "health_record",
            "test_name",
            "test_category",
            "test_code",
            "ordered_by",
            "ordered_by_name",
            "ordered_date",
            "collection_date",
            "result_date",
            "results",
            "reference_range",
            "units",
            "is_abnormal",
            "interpretation",
            "clinical_significance",
            "is_verified",
            "verified_by",
            "verified_by_name",
            "verification_date",
            "specimen_quality",
            "notes",
            "attachments",
        ]
        read_only_fields = ["id", "ordered_date", "verification_date"]
