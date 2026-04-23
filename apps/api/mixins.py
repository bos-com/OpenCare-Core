# pylint: disable=too-many-branches
"""
Shared mixins for API viewsets.
"""

from __future__ import annotations

from typing import Iterable, Optional

from rest_framework.response import Response

from apps.core.audit import log_audit_event


class AuditLogMixin:
    """
    Automatically capture audit trail entries for sensitive viewsets.
    """

    audit_list_object_id = "list"

    def get_audit_model_name(self, instance=None) -> str:
        if instance is not None:
            return instance._meta.label  # type: ignore[attr-defined]
        queryset = getattr(self, "queryset", None)
        model = getattr(queryset, "model", None)
        if model is not None:
            return model._meta.label  # type: ignore[attr-defined]
        serializer_class = self.get_serializer_class()
        meta_model = getattr(getattr(serializer_class, "Meta", None), "model", None)
        if meta_model is None:
            raise ValueError("Unable to determine model name for audit logging")
        return meta_model._meta.label  # type: ignore[attr-defined]

    def get_audit_object_id(self, instance=None) -> str:
        if instance is None:
            return self.audit_list_object_id
        identifier = getattr(instance, "pk", None)
        return str(identifier) if identifier is not None else ""

    def _build_change_payload(
        self,
        *,
        fields: Optional[Iterable[str]] = None,
        summary: Optional[str] = None,
        count: Optional[int] = None,
        filters: Optional[Iterable[str]] = None,
        metadata: Optional[str] = None,
    ):
        payload = {}
        if fields:
            payload["fields"] = {str(name) for name in fields}
        if summary:
            payload["summary"] = summary
        if count is not None:
            payload["count"] = int(count)
        if filters:
            payload["filters"] = {str(name) for name in filters}
        if metadata:
            payload["metadata"] = metadata
        return payload

    # CRUD hooks ---------------------------------------------------------
    def perform_create(self, serializer):
        instance = serializer.save()
        payload = self._build_change_payload(fields=serializer.validated_data.keys())
        log_audit_event(
            user=self.request.user,
            action="create",
            model_name=self.get_audit_model_name(instance),
            object_id=self.get_audit_object_id(instance),
            request=self.request,
            changes=payload,
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        payload = self._build_change_payload(fields=serializer.validated_data.keys())
        log_audit_event(
            user=self.request.user,
            action="update",
            model_name=self.get_audit_model_name(instance),
            object_id=self.get_audit_object_id(instance),
            request=self.request,
            changes=payload,
        )
        return instance

    def perform_destroy(self, instance):
        object_id = self.get_audit_object_id(instance)
        model_name = self.get_audit_model_name(instance)
        log_audit_event(
            user=self.request.user,
            action="delete",
            model_name=model_name,
            object_id=object_id,
            request=self.request,
            changes=self._build_change_payload(summary="record deleted"),
        )
        instance.delete()

    # Read operations ----------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response: Response = super().retrieve(request, *args, **kwargs)
        if response.status_code < 400:
            log_audit_event(
                user=request.user,
                action="view",
                model_name=self.get_audit_model_name(instance),
                object_id=self.get_audit_object_id(instance),
                request=request,
                changes=self._build_change_payload(summary="record retrieved"),
            )
        return response

    def list(self, request, *args, **kwargs):
        response: Response = super().list(request, *args, **kwargs)
        if response.status_code < 400:
            count = None
            data = response.data
            if isinstance(data, dict):
                if "results" in data and isinstance(data["results"], list):
                    count = len(data["results"])
                elif isinstance(data.get("count"), int):
                    count = data["count"]
            elif isinstance(data, list):
                count = len(data)

            log_audit_event(
                user=request.user,
                action="view",
                model_name=self.get_audit_model_name(),
                object_id=self.get_audit_object_id(None),
                request=request,
                changes=self._build_change_payload(
                    summary="list retrieved",
                    count=count,
                    filters=request.query_params.keys(),
                ),
            )
        return response
