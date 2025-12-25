"""
Custom permission classes for API access control.
"""

from __future__ import annotations

from typing import Iterable

from rest_framework.permissions import BasePermission


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
