"""
Tests for health data audit logging.
"""

from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import AuditTrail, HealthFacility, Location
from apps.patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditLoggingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor1",
            password="password123",
            user_type="doctor",
            first_name="Doc",
            last_name="Tor",
        )
        self.client.force_authenticate(self.user)

        self.location = Location.objects.create(
            name="Central District",
            location_type="district",
        )
        self.facility = HealthFacility.objects.create(
            name="Central Clinic",
            facility_type="hospital",
            location=self.location,
            address="123 Main Street",
            phone_number="+256700000010",
            email="clinic@example.com",
            website="",
            is_24_hours=True,
            contact_person_name="Chief Admin",
            contact_person_phone="+256700000011",
            services_offered=[],
        )
        self.patient = Patient.objects.create(
            patient_id="PAT-000001",
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            gender="F",
            phone_number="+256700000012",
            email="jane@example.com",
            address="45 Health Avenue",
            location=self.location,
            emergency_contact_name="John Doe",
            emergency_contact_phone="+256700000013",
            emergency_contact_relationship="Spouse",
            registered_facility=self.facility,
        )

    def test_patient_detail_access_creates_audit_log(self):
        AuditTrail.objects.all().delete()
        url = reverse("api:patient-detail", args=[self.patient.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_entry = AuditTrail.objects.filter(
            action="view",
            model_name="patients.Patient",
            object_id=str(self.patient.pk),
        ).first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.user, self.user)

    def test_patient_list_access_logs_view(self):
        AuditTrail.objects.all().delete()
        url = reverse("api:patient-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_entry = AuditTrail.objects.filter(
            action="view",
            model_name="patients.Patient",
            object_id="list",
        ).first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.user, self.user)
        self.assertIn("summary", log_entry.changes)

    def test_patient_creation_logs_action(self):
        AuditTrail.objects.all().delete()
        url = reverse("api:patient-list")
        payload = {
            "first_name": "Alice",
            "last_name": "Smith",
            "date_of_birth": "1985-05-05",
            "gender": "F",
            "phone_number": "+256700000099",
            "email": "alice@example.com",
            "address": "78 Care Road",
            "location": self.location.pk,
            "emergency_contact_name": "Bob Smith",
            "emergency_contact_phone": "+256700000098",
            "emergency_contact_relationship": "Sibling",
            "registered_facility": self.facility.pk,
        }
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        log_entry = AuditTrail.objects.filter(
            action="create", model_name="patients.Patient"
        ).order_by("-timestamp").first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.user, self.user)
        self.assertIn("fields", log_entry.changes)
        self.assertNotIn("first_name", str(log_entry.changes))

    def test_audit_log_endpoint_requires_admin(self):
        url = reverse("api:audit-logs-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        admin_user = User.objects.create_superuser(
            username="admin1",
            email="admin@example.com",
            password="password123",
        )
        self.client.force_authenticate(admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
