"""
RBAC enforcement tests for API endpoints.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from apps.api.permissions import IsAdmin, IsDoctor, IsReceptionist, RoleRequired

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

        self.doctor_user = User.objects.create_user(
            username="rbac-doctor",
            password="testpass123",
            email="doctor@example.com",
            role=User.Role.DOCTOR,
            user_type="doctor",
        )

        self.receptionist_user = User.objects.create_user(
            username="rbac-receptionist",
            password="testpass123",
            email="receptionist@example.com",
            role=User.Role.RECEPTIONIST,
            user_type="receptionist",
        )

    def _client_for(self, user: User) -> APIClient:
        client = APIClient()
        client.force_authenticate(user)
        return client

    def test_receptionist_blocked_from_admin_endpoints(self):
        """Receptionists should receive 403 when calling admin-only endpoints."""
        client = self._client_for(self.receptionist_user)
        url = reverse("api:api_stats")
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_receptionist_blocked_from_doctor_only_endpoints(self):
        """Receptionists should receive 403 when calling doctor-only endpoints."""
        client = self._client_for(self.receptionist_user)
        url = reverse("api:health-workers-list")
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_doctor_blocked_from_admin_only_metrics(self):
        """Doctors must not access admin-only statistics endpoints."""
        client = self._client_for(self.doctor_user)
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

    def test_role_required_allows_doctor_role(self):
        """RoleRequired should allow users whose role matches the requirement."""
        permission = RoleRequired()

        class DummyView:
            required_roles = frozenset({User.Role.DOCTOR})

        request = self.factory.get("/dummy")
        request.user = self.doctor_user

        self.assertTrue(permission.has_permission(request, DummyView()))

        request.user = self.receptionist_user
        self.assertFalse(permission.has_permission(request, DummyView()))

        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, DummyView()))

    def test_doctor_can_access_doctor_endpoints(self):
        """Doctors should access endpoints allowed for doctors."""
        client = self._client_for(self.doctor_user)
        url = reverse("api:patients-list")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_receptionist_can_access_receptionist_endpoints(self):
        """Receptionists should access endpoints allowed for receptionists."""
        client = self._client_for(self.receptionist_user)
        url = reverse("api:patients-list")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_all_endpoints(self):
        """Admins should have access to all endpoints."""
        client = self._client_for(self.admin_user)
        
        # Test patient endpoints (all roles)
        patients_url = reverse("api:patients-list")
        response = client.get(patients_url)
        self.assertEqual(response.status_code, 200)
        
        # Test admin-only endpoints
        health_workers_url = reverse("api:health-workers-list")
        response = client.get(health_workers_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_blocked(self):
        """Unauthenticated users should be blocked from protected endpoints."""
        client = APIClient()
        url = reverse("api:patients-list")
        response = client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_health_check_public(self):
        """Health check endpoint should be publicly accessible."""
        client = APIClient()
        url = reverse("api:health_check")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "healthy")

    def test_is_admin_permission(self):
        """IsAdmin permission should only allow admin users."""
        permission = IsAdmin()
        request = self.factory.get("/dummy")

        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.doctor_user
        self.assertFalse(permission.has_permission(request, None))

        request.user = self.receptionist_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_doctor_permission(self):
        """IsDoctor permission should allow doctor and admin users."""
        permission = IsDoctor()
        request = self.factory.get("/dummy")

        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.doctor_user
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.receptionist_user
        self.assertFalse(permission.has_permission(request, None))

    def test_is_receptionist_permission(self):
        """IsReceptionist permission should allow all roles."""
        permission = IsReceptionist()
        request = self.factory.get("/dummy")

        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.doctor_user
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.receptionist_user
        self.assertTrue(permission.has_permission(request, None))

