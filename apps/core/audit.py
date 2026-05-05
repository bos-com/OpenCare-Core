"""
Utility helpers for writing sanitized audit trail entries.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from django.db import transaction
from .models import AuditTrail

ALLOWED_CHANGE_KEYS = {"fields", "summary", "count", "filters", "metadata"}


def _get_client_ip(request) -> Optional[str]:
    """
    Extract the originating client IP address from request headers.
    """
    if request is None:
        return None
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        # X-Forwarded-For may contain multiple comma-separated values.
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _get_user_agent(request) -> str:
    """
    Return a truncated user agent string from the request.
    """
    if request is None:
        return ""
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    # Prevent oversized headers from being stored.
    return user_agent[:512]


def sanitize_change_payload(changes: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ensure the change payload only contains whitelisted keys and simple values.
    """
    if not isinstance(changes, dict):
        return {}
    sanitized: Dict[str, Any] = {}
    for key, value in changes.items():
        if key not in ALLOWED_CHANGE_KEYS:
            continue
        if key in {"fields", "filters"} and isinstance(value, Iterable):
            sanitized[key] = sorted({str(item) for item in value})
        elif key in {"summary", "metadata"}:
            sanitized[key] = str(value)
        elif key == "count":
            try:
                sanitized[key] = int(value)
            except (TypeError, ValueError):
                sanitized[key] = 0
    return sanitized


def log_audit_event(
    *,
    user,
    action: str,
    model_name: str,
    object_id: str,
    request=None,
    changes: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Persist a sanitized audit trail entry.
    """
    if not model_name:
        raise ValueError("model_name is required for audit logging")

    sanitized_changes = sanitize_change_payload(changes)
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)
    actor = user if getattr(user, "is_authenticated", False) else None

    def _create_entry():
        AuditTrail.objects.create(
            user=actor,
            action=action,
            model_name=model_name,
            object_id=str(object_id) if object_id is not None else "",
            changes=sanitized_changes,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    if transaction.get_connection().in_atomic_block:
        transaction.on_commit(_create_entry)
    else:
        _create_entry()
