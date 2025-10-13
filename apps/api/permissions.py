"""Shared RBAC helpers for API endpoints."""

from __future__ import annotations

from typing import Iterable, Set

from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


def _normalize_roles(roles: Iterable[str]) -> frozenset[str]:
    normalized: Set[str] = set()
    for role in roles:
        if hasattr(role, "value"):
            normalized.add(str(role.value))
        else:
            normalized.add(str(role))
    return frozenset(normalized)


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
