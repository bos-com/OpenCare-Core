"""
Custom permission classes for API access control.
"""

from __future__ import annotations

from typing import Iterable, Set

from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


def _normalize_roles(roles: Iterable[str]) -> frozenset[str]:
    """Normalize role values to strings."""
    normalized: Set[str] = set()
    for role in roles:
        if hasattr(role, "value"):
            normalized.add(str(role.value))
        else:
            normalized.add(str(role))
    return frozenset(normalized)


class IsClinicalStaff(BasePermission):
    """
    Allow requests from authenticated clinical staff or superusers.

    Clinical staff is defined as any user whose `user_type` is in
    `CLINICAL_ROLES`. Read and write operations are blocked for other roles,
    ensuring sensitive health records are only modified by qualified users.
    """

    CLINICAL_ROLES: Iterable[str] = (
        "doctor",
        "nurse",
        "midwife",
        "pharmacist",
        "lab_technician",
    )

    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return getattr(user, "user_type", None) in self.CLINICAL_ROLES

    def has_object_permission(self, request, view, obj) -> bool:  # noqa: D401
        """
        Mirror `has_permission` so object-level checks follow the same rule.
        """
        return self.has_permission(request, view)


class RoleRequired(BasePermission):
    """DRF permission enforcing role membership based on ``view.required_roles``."""

    message = _("You do not have permission to perform this action.")

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        required = getattr(view, "required_roles", None)
        if required is None and hasattr(view, "cls"):
            required = getattr(view.cls, "required_roles", None)

        if not required:
            return True

        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return False

        if getattr(user, "is_admin_role", False) or getattr(user, "is_superuser", False):
            return True

        return getattr(user, "role", None) in required


def require_roles(*roles: str):
    """Decorator to attach required roles metadata to API views."""

    normalized = _normalize_roles(roles)

    def decorator(view):
        setattr(view, "required_roles", normalized)
        if hasattr(view, "cls"):
            setattr(view.cls, "required_roles", normalized)
        return view

    return decorator
