"""
Core serializers for OpenCare-Africa health system.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Location, HealthFacility, AuditTrail, SystemConfiguration

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    full_name = serializers.SerializerMethodField()
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'user_type_display', 'phone_number', 'date_of_birth',
            'profile_picture', 'license_number', 'specialization', 'years_of_experience',
            'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users.
    """
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password',
            'password_confirm', 'user_type', 'phone_number', 'date_of_birth'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model.
    """
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'location_type', 'location_type_display',
            'parent', 'parent_name', 'latitude', 'longitude'
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.parent:
            representation['full_location'] = f"{instance.name}, {instance.parent}"
        else:
            representation['full_location'] = instance.name
        return representation


class LocationTreeSerializer(serializers.ModelSerializer):
    """
    Serializer for hierarchical location display.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'location_type', 'children']
    
    def get_children(self, obj):
        children = Location.objects.filter(parent=obj)
        return LocationTreeSerializer(children, many=True).data


class HealthFacilitySerializer(serializers.ModelSerializer):
    """
    Serializer for HealthFacility model.
    """
    facility_type_display = serializers.CharField(source='get_facility_type_display', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    services_count = serializers.SerializerMethodField()
    
    class Meta:
        model = HealthFacility
        fields = [
            'id', 'name', 'facility_type', 'facility_type_display',
            'location', 'location_name', 'address', 'phone_number',
            'email', 'website', 'is_24_hours', 'opening_time',
            'closing_time', 'services_offered', 'contact_person_name',
            'contact_person_phone', 'services_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_services_count(self, obj):
        return len(obj.services_offered) if obj.services_offered else 0


class HealthFacilityDetailSerializer(HealthFacilitySerializer):
    """
    Detailed serializer for HealthFacility with related data.
    """
    location_detail = LocationSerializer(source='location', read_only=True)
    
    class Meta(HealthFacilitySerializer.Meta):
        fields = HealthFacilitySerializer.Meta.fields + ['location_detail']


class AuditTrailSerializer(serializers.ModelSerializer):
    """
    Serializer for AuditTrail model.
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditTrail
        fields = [
            'id', 'user', 'user_name', 'action', 'action_display',
            'model_name', 'object_id', 'changes', 'timestamp',
            'ip_address', 'user_agent'
        ]
        read_only_fields = ['id', 'timestamp']


class SystemConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for SystemConfiguration model.
    """
    class Meta:
        model = SystemConfiguration
        fields = ['id', 'key', 'value', 'description', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer for dashboard statistics.
    """
    total_patients = serializers.IntegerField()
    total_health_workers = serializers.IntegerField()
    total_facilities = serializers.IntegerField()
    total_visits_today = serializers.IntegerField()
    active_outbreaks = serializers.IntegerField()
    system_health = serializers.CharField()
    last_backup = serializers.DateTimeField()
    database_size = serializers.CharField()
    storage_usage = serializers.CharField()
