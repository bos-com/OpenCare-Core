"""
Filter definitions for health record queries.
"""

from __future__ import annotations

import django_filters

from .models import HealthRecord


class HealthRecordFilter(django_filters.FilterSet):
    """
    Provide rich filtering options for health record collections.

    Supports record date ranges, facility/provider scoping, and partial patient
    ID searches so clinicians can rapidly locate relevant entries.
    """

    record_date = django_filters.DateFromToRangeFilter()
    patient_id = django_filters.CharFilter(
        field_name="patient__patient_id", lookup_expr="icontains"
    )
    provider = django_filters.NumberFilter(field_name="attending_provider")
    facility = django_filters.NumberFilter(field_name="facility")
    record_type = django_filters.CharFilter(field_name="record_type")

    class Meta:
        model = HealthRecord
        fields = [
            "record_date",
            "patient",
            "patient_id",
            "provider",
            "facility",
            "record_type",
            "is_confidential",
        ]
