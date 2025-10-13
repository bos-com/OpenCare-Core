"""RBAC enforcement tests for API endpoints."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from apps.api.permissions import RoleRequired

User = get_user_model()


class RBACPermissionTests(TestCase):
    """Validate role-based access control wiring."""

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

        self.admin_user = User.objects.create_user(
            username="rbac-admin",
            password="testpass123",
            email="admin@example.com",
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
        )

        self.provider_user = User.objects.create_user(
            username="rbac-provider",
            password="testpass123",
            email="provider@example.com",
            role=User.Role.PROVIDER,
        )

        self.patient_user = User.objects.create_user(
            username="rbac-patient",
            password="testpass123",
            email="patient@example.com",
            role=User.Role.PATIENT,
        )

    def _client_for(self, user: User) -> APIClient:
        client = APIClient()
        client.force_authenticate(user)
        return client

    def test_patient_blocked_from_clinical_endpoints(self):
        """Patients should receive 403 when calling staff-only endpoints."""

        client = self._client_for(self.patient_user)
        url = reverse("api:patients-list")
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_provider_blocked_from_admin_only_metrics(self):
        """Providers must not access admin-only statistics endpoints."""

        client = self._client_for(self.provider_user)
        url = reverse("api:api_stats")
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_admin_only_endpoints(self):
        """Admins should be able to call restricted endpoints."""

        client = self._client_for(self.admin_user)
        stats_url = reverse("api:api_stats")
        export_url = reverse("api:export_data")

        stats_response = client.get(stats_url)
        self.assertEqual(stats_response.status_code, 200)

        export_response = client.post(export_url, {"format": "csv", "type": "patients"}, format="json")
        self.assertEqual(export_response.status_code, 200)
        self.assertEqual(export_response.data["format"], "csv")

    def test_role_required_allows_provider_role(self):
        """RoleRequired should allow users whose role matches the requirement."""

        permission = RoleRequired()

        class DummyView:
            required_roles = frozenset({User.Role.PROVIDER})

        request = self.factory.get("/dummy")
        request.user = self.provider_user

        self.assertTrue(permission.has_permission(request, DummyView()))

        request.user = self.patient_user
        self.assertFalse(permission.has_permission(request, DummyView()))

        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, DummyView()))
