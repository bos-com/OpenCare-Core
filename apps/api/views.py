"""
API views for OpenCare-Africa health system.
"""

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.api.mixins import AuditLogMixin
from apps.core.models import AuditTrail, HealthFacility
from apps.core.serializers import (
    AuditTrailSerializer,
    HealthFacilitySerializer,
    UserSerializer,
)
from apps.patients.models import Patient, PatientVisit
from apps.patients.serializers import (
    PatientCreateSerializer,
    PatientDetailSerializer,
    PatientSerializer,
    PatientVisitCreateSerializer,
    PatientVisitDetailSerializer,
    PatientVisitSerializer,
    PatientSearchSerializer,
)
from apps.records.models import HealthRecord
from apps.records.serializers import (
    HealthRecordCreateSerializer,
    HealthRecordDetailSerializer,
    HealthRecordSerializer,
)
from apps.core.audit import log_audit_event
from apps.api.permissions import IsClinicalStaff
from apps.records.filters import HealthRecordFilter

User = get_user_model()


class PatientViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    ViewSet for patient management with audit logging.
    """

    permission_classes = [IsAuthenticated]
    queryset = (
        Patient.objects.select_related("location", "registered_facility")
        .prefetch_related("patientvisit_set")
        .all()
    )
    serializer_class = PatientSerializer
    filterset_fields = ["registered_facility", "gender", "is_active"]
    search_fields = ["patient_id", "first_name", "last_name", "phone_number"]
    ordering_fields = ["registration_date", "last_name"]

    serializer_action_map = {
        "list": PatientSerializer,
        "retrieve": PatientDetailSerializer,
        "create": PatientCreateSerializer,
        "update": PatientCreateSerializer,
        "partial_update": PatientCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, self.serializer_class)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Search patients by name, ID, or other criteria.
        """
        serializer = PatientSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]
        search_type = serializer.validated_data["search_type"]

        queryset = self.get_queryset()
        if search_type == "name":
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        elif search_type == "patient_id":
            queryset = queryset.filter(patient_id__icontains=query)
        elif search_type == "phone":
            queryset = queryset.filter(phone_number__icontains=query)
        elif search_type == "location":
            queryset = queryset.filter(location__name__icontains=query)
        elif search_type == "facility":
            queryset = queryset.filter(registered_facility__name__icontains=query)

        results = PatientSerializer(queryset[: serializer.validated_data["limit"]], many=True).data

        log_audit_event(
            user=request.user,
            action="view",
            model_name=self.get_audit_model_name(),
            object_id=self.get_audit_object_id(None),
            request=request,
            changes={
                "summary": "patient search executed",
                "filters": [search_type],
            },
        )

        return Response({"results": results, "count": len(results)})


class HealthWorkerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for health worker management.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(
        user_type__in=["doctor", "nurse", "midwife", "community_worker"]
    )
    serializer_class = UserSerializer
    search_fields = ["first_name", "last_name", "specialization"]
    ordering_fields = ["last_name", "date_joined"]


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for health facility management.
    """

    permission_classes = [IsAuthenticated]
    queryset = HealthFacility.objects.select_related("location").all()
    serializer_class = HealthFacilitySerializer
    filterset_fields = ["facility_type", "location"]
    search_fields = ["name", "address"]
    ordering_fields = ["name"]


class PatientVisitViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    ViewSet for patient visit management with audit logging.
    """

    permission_classes = [IsAuthenticated]
    queryset = (
        PatientVisit.objects.select_related("patient", "facility", "attending_provider")
        .all()
    )
    serializer_class = PatientVisitSerializer
    filterset_fields = ["visit_type", "status", "facility", "patient"]
    search_fields = ["patient__patient_id", "patient__first_name", "patient__last_name"]
    ordering_fields = ["scheduled_date", "created_at"]

    serializer_action_map = {
        "list": PatientVisitSerializer,
        "retrieve": PatientVisitDetailSerializer,
        "create": PatientVisitCreateSerializer,
        "update": PatientVisitCreateSerializer,
        "partial_update": PatientVisitCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, self.serializer_class)

    @action(detail=False, methods=["get"], url_path="today")
    def today(self, request):
        """
        Return visits scheduled for today.
        """
        from django.utils import timezone

        today = timezone.now().date()
        visits = self.get_queryset().filter(scheduled_date__date=today)
        results = PatientVisitSerializer(visits, many=True).data
        log_audit_event(
            user=request.user,
            action="view",
            model_name=self.get_audit_model_name(),
            object_id=self.get_audit_object_id(None),
            request=request,
            changes={"summary": "today visit report generated"},
        )
        return Response({"results": results, "count": len(results)})


class HealthRecordViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    Provide CRUD operations for patient health records with audit logging.

    Access is limited to authenticated clinical staff or superusers. Collections
    support filtering by patient, provider, facility, record type, and date
    ranges to keep browsing focused on relevant medical history.
    """

    permission_classes = [IsClinicalStaff]
    queryset = (
        HealthRecord.objects.select_related("patient", "facility", "attending_provider")
        .prefetch_related("medications", "laboratory_tests")
        .all()
    )
    serializer_class = HealthRecordSerializer
    filterset_class = HealthRecordFilter
    search_fields = [
        "patient__patient_id",
        "patient__first_name",
        "patient__last_name",
        "facility__name",
        "attending_provider__first_name",
        "attending_provider__last_name",
    ]
    ordering_fields = ["record_date", "created_at"]
    ordering = ["-record_date"]

    serializer_action_map = {
        "list": HealthRecordSerializer,
        "retrieve": HealthRecordDetailSerializer,
        "create": HealthRecordCreateSerializer,
        "update": HealthRecordCreateSerializer,
        "partial_update": HealthRecordCreateSerializer,
    }

    def get_serializer_class(self):
        """
        Return the serializer configured for the current action.
        """
        return self.serializer_action_map.get(self.action, self.serializer_class)

    @action(detail=False, methods=["get"], url_path="by-patient")
    def by_patient(self, request):
        """
        List health records for a patient identifier.

        This helper allows clinicians to quickly pull a patient's timeline by
        passing their external `patient_id` as a query parameter.
        """
        patient_identifier = request.query_params.get("patient_id")
        if not patient_identifier:
            return Response({"results": []})

        queryset = self.filter_queryset(
            self.get_queryset().filter(patient__patient_id=patient_identifier)
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        
        log_audit_event(
            user=request.user,
            action="view",
            model_name=self.get_audit_model_name(),
            object_id=self.get_audit_object_id(None),
            request=request,
            changes={"summary": "records fetched by patient identifier"},
        )
        
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response({"results": serializer.data})


class AuditTrailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only access to audit trail entries for administrative users.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = AuditTrail.objects.select_related("user").all().order_by("-timestamp")
    serializer_class = AuditTrailSerializer
    filterset_fields = ["action", "model_name", "user"]
    search_fields = ["object_id", "changes"]
    ordering_fields = ["timestamp", "model_name"]
    ordering = ["-timestamp"]


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for API monitoring."""
    return JsonResponse(
        {
            "status": "healthy",
            "service": "OpenCare-Africa API",
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "endpoints": {
                "patients": "/api/v1/patients/",
                "health_workers": "/api/v1/health-workers/",
                "facilities": "/api/v1/facilities/",
                "visits": "/api/v1/visits/",
                "records": "/api/v1/records/",
            },
        }
    )


@require_http_methods(["GET"])
def api_stats(request):
    """Get API usage statistics."""
    return JsonResponse(
        {
            "total_requests": 0,
            "active_users": 0,
            "popular_endpoints": [],
            "response_times": {"average": 0, "p95": 0, "p99": 0},
        }
    )


@require_http_methods(["POST"])
def export_data(request):
    """Export data in various formats."""
    format_type = request.POST.get("format", "json")
    data_type = request.POST.get("type", "patients")

    return JsonResponse(
        {
            "message": "Data export endpoint",
            "format": format_type,
            "type": data_type,
            "download_url": None,
        }
    )
