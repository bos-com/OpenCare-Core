"""
Patient serializers for OpenCare-Africa health system.
"""

import re
from datetime import date

from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from .models import Patient, PatientVisit, PatientMedicalHistory
from apps.core.serializers import LocationSerializer, HealthFacilitySerializer, UserSerializer

# Maximum plausible patient age in years
MAX_PATIENT_AGE = 150

# Phone number regex: optional leading +, then 9-15 digits
PHONE_REGEX = re.compile(r'^\+?\d{9,15}$')


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    marital_status_display = serializers.CharField(source='get_marital_status_display', read_only=True)
    blood_type_display = serializers.CharField(source='get_blood_type_display', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    facility_name = serializers.CharField(source='registered_facility.name', read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'patient_id', 'first_name', 'last_name', 'middle_name',
            'date_of_birth', 'age', 'gender', 'gender_display', 'marital_status',
            'marital_status_display', 'phone_number', 'email', 'address',
            'location', 'location_name', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relationship',
            'blood_type', 'blood_type_display', 'allergies', 'chronic_conditions',
            'current_medications', 'insurance_provider', 'insurance_number',
            'payment_method', 'registered_facility', 'facility_name',
            'registration_date', 'is_active', 'occupation', 'education_level',
            'religion', 'ethnicity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'patient_id', 'registration_date', 'created_at', 'updated_at']
    
    def get_age(self, obj):
        return obj.get_age()


class PatientDetailSerializer(PatientSerializer):
    """
    Detailed serializer for Patient with related data.
    """
    location_detail = LocationSerializer(source='location', read_only=True)
    facility_detail = HealthFacilitySerializer(source='registered_facility', read_only=True)
    visits_count = serializers.SerializerMethodField()
    medical_history_count = serializers.SerializerMethodField()
    
    class Meta(PatientSerializer.Meta):
        fields = PatientSerializer.Meta.fields + [
            'location_detail', 'facility_detail', 'visits_count', 'medical_history_count'
        ]
    
    def get_visits_count(self, obj):
        return obj.patientvisit_set.count()
    
    def get_medical_history_count(self, obj):
        return obj.patientmedicalhistory_set.count()


class PatientCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new patients with comprehensive input validation.

    Validates:
    - first_name / last_name are not empty or whitespace-only
    - date_of_birth is not in the future and represents a plausible age (0–150)
    - phone_number matches E.164-like format (+, then 9-15 digits)
    - email is well-formed when provided
    - emergency_contact_phone matches the same phone format
    - emergency_contact_name is required when a phone is supplied
    """
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'middle_name', 'date_of_birth',
            'gender', 'marital_status', 'phone_number', 'email', 'address',
            'location', 'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'blood_type', 'allergies',
            'chronic_conditions', 'current_medications', 'insurance_provider',
            'insurance_number', 'payment_method', 'registered_facility',
            'occupation', 'education_level', 'religion', 'ethnicity'
        ]

    # ------------------------------------------------------------------
    # Field-level validators
    # ------------------------------------------------------------------

    def validate_first_name(self, value):
        """Ensure first name is not empty or whitespace-only."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("First name must not be empty.")
            )
        return value.strip()

    def validate_last_name(self, value):
        """Ensure last name is not empty or whitespace-only."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("Last name must not be empty.")
            )
        return value.strip()

    def validate_date_of_birth(self, value):
        """Ensure date of birth is not in the future and represents a
        plausible age (between 0 and MAX_PATIENT_AGE years)."""
        today = date.today()
        if value > today:
            raise serializers.ValidationError(
                _("Date of birth cannot be in the future.")
            )
        age = (
            today.year - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if age > MAX_PATIENT_AGE:
            raise serializers.ValidationError(
                _("Date of birth implies an age greater than %(max_age)d years.")
                % {"max_age": MAX_PATIENT_AGE}
            )
        return value

    def validate_phone_number(self, value):
        """Validate phone number format: optional '+' followed by 9-15 digits."""
        cleaned = value.replace(" ", "").replace("-", "")
        if not PHONE_REGEX.match(cleaned):
            raise serializers.ValidationError(
                _("Phone number must be in the format: +999999999. "
                  "Between 9 and 15 digits allowed.")
            )
        return cleaned

    def validate_email(self, value):
        """Validate email format when provided (field is optional)."""
        if value and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', value):
            raise serializers.ValidationError(
                _("Enter a valid email address.")
            )
        return value

    def validate_emergency_contact_phone(self, value):
        """Validate emergency contact phone format."""
        if value:
            cleaned = value.replace(" ", "").replace("-", "")
            if not PHONE_REGEX.match(cleaned):
                raise serializers.ValidationError(
                    _("Emergency contact phone must be in the format: "
                      "+999999999. Between 9 and 15 digits allowed.")
                )
            return cleaned
        return value

    # ------------------------------------------------------------------
    # Cross-field / object-level validation
    # ------------------------------------------------------------------

    def validate(self, attrs):
        """Cross-field validation for emergency contact consistency."""
        ec_phone = attrs.get("emergency_contact_phone")
        ec_name = attrs.get("emergency_contact_name", "").strip()

        if ec_phone and not ec_name:
            raise serializers.ValidationError({
                "emergency_contact_name": _(
                    "Emergency contact name is required when a phone number "
                    "is provided."
                )
            })

        return attrs

    # ------------------------------------------------------------------
    # Creation helper
    # ------------------------------------------------------------------

    def _generate_patient_id(self) -> str:
        prefix = "PAT"
        random_id = get_random_string(8).upper()
        return f"{prefix}-{random_id}"
    
    def create(self, validated_data):
        patient_id = self._generate_patient_id()
        while Patient.objects.filter(patient_id=patient_id).exists():
            patient_id = self._generate_patient_id()
        validated_data["patient_id"] = patient_id
        return Patient.objects.create(**validated_data)


class PatientVisitSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientVisit model.
    """
    visit_type_display = serializers.CharField(source='get_visit_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    provider_name = serializers.CharField(source='attending_provider.get_full_name', read_only=True)
    
    class Meta:
        model = PatientVisit
        fields = [
            'id', 'patient', 'patient_name', 'facility', 'facility_name',
            'visit_type', 'visit_type_display', 'status', 'status_display',
            'scheduled_date', 'actual_date', 'chief_complaint', 'diagnosis',
            'treatment_plan', 'prescription', 'attending_provider', 'provider_name',
            'consultation_fee', 'total_cost', 'payment_status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientVisitDetailSerializer(PatientVisitSerializer):
    """
    Detailed serializer for PatientVisit with related data.
    """
    patient_detail = PatientSerializer(source='patient', read_only=True)
    facility_detail = HealthFacilitySerializer(source='facility', read_only=True)
    provider_detail = UserSerializer(source='attending_provider', read_only=True)
    
    class Meta(PatientVisitSerializer.Meta):
        fields = PatientVisitSerializer.Meta.fields + [
            'patient_detail', 'facility_detail', 'provider_detail'
        ]


class PatientVisitCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new patient visits.
    """
    class Meta:
        model = PatientVisit
        fields = [
            'patient', 'facility', 'visit_type', 'scheduled_date',
            'chief_complaint', 'consultation_fee', 'notes'
        ]


class PatientMedicalHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for PatientMedicalHistory model.
    """
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    provider_name = serializers.CharField(source='diagnosed_by.get_full_name', read_only=True)
    
    class Meta:
        model = PatientMedicalHistory
        fields = [
            'id', 'patient', 'patient_name', 'condition', 'diagnosis_date',
            'is_active', 'severity', 'severity_display', 'treatment',
            'medications', 'outcomes', 'diagnosed_by', 'provider_name',
            'facility', 'facility_name', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientMedicalHistoryDetailSerializer(PatientMedicalHistorySerializer):
    """
    Detailed serializer for PatientMedicalHistory with related data.
    """
    patient_detail = PatientSerializer(source='patient', read_only=True)
    facility_detail = HealthFacilitySerializer(source='facility', read_only=True)
    provider_detail = UserSerializer(source='diagnosed_by', read_only=True)
    
    class Meta(PatientMedicalHistorySerializer.Meta):
        fields = PatientMedicalHistorySerializer.Meta.fields + [
            'patient_detail', 'facility_detail', 'provider_detail'
        ]


class PatientSearchSerializer(serializers.Serializer):
    """
    Serializer for patient search functionality.
    """
    query = serializers.CharField(max_length=100)
    search_type = serializers.ChoiceField(choices=[
        ('name', 'Name'),
        ('patient_id', 'Patient ID'),
        ('phone', 'Phone Number'),
        ('location', 'Location'),
        ('facility', 'Facility')
    ])
    limit = serializers.IntegerField(min_value=1, max_value=100, default=20)


class PatientStatsSerializer(serializers.Serializer):
    """
    Serializer for patient statistics.
    """
    total_patients = serializers.IntegerField()
    active_patients = serializers.IntegerField()
    new_patients_this_month = serializers.IntegerField()
    patients_by_gender = serializers.DictField()
    patients_by_age_group = serializers.DictField()
    patients_by_location = serializers.DictField()
    patients_by_facility = serializers.DictField()
    common_conditions = serializers.ListField()
    average_age = serializers.FloatField()
