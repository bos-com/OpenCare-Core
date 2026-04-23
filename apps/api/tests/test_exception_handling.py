"""Tests for sanitized API exception handling."""

from __future__ import annotations

from django.test import TestCase, override_settings
from django.urls import path
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient


@api_view(["GET"])
def explode(request):
    """Endpoint that raises an unhandled exception."""

    raise ValueError("super secret stack trace")


@api_view(["GET"])
def invalid(request):
    """Endpoint that raises a validation error."""

    raise ValidationError({"field": ["This value is invalid."]})


urlpatterns = [
    path("boom/", explode, name="boom"),
    path("invalid/", invalid, name="invalid"),
]


class ExceptionHandlingTests(TestCase):
    """Validate the custom exception handler behaviour."""

    def setUp(self):
        self.client = APIClient()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="handler-tester",
            password="testpass123",
            email="tester@example.com",
        )
        self.client.force_authenticate(self.user)

    @override_settings(ROOT_URLCONF=__name__)
    def test_unhandled_exception_returns_generic_message(self):
        """Unhandled exceptions should produce sanitized 500 responses."""

        response = self.client.get("/boom/")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["code"], "server_error")
        self.assertNotIn("secret", response.data["message"].lower())

    @override_settings(ROOT_URLCONF=__name__)
    def test_validation_error_returns_structured_payload(self):
        """Validation errors should include a generic message plus field errors."""

        response = self.client.get("/invalid/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "invalid")
        self.assertEqual(response.data["message"], "Request validation failed.")
        self.assertIn("field", response.data["errors"])
        self.assertEqual(response.data["errors"]["field"][0], "This value is invalid.")
