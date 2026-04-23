"""
Patient serializers for OpenCare-Africa health system.
"""

from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import Patient, PatientVisit, PatientMedicalHistory
from apps.core.serializers import LocationSerializer, HealthFacilitySerializer, UserSerializer


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
    Serializer for creating new patients.
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
