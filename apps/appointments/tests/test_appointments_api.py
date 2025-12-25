"""
Tests for the appointment scheduling API.
"""

from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import HealthFacility, Location
from apps.patients.models import Patient
from apps.appointments.models import Appointment


User = get_user_model()


class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.provider = User.objects.create_user(
            username="provider1",
            password="password123",
            user_type="doctor",
            first_name="Provider",
            last_name="One",
        )
        self.patient = Patient.objects.create(
            patient_id="PAT-000100",
            first_name="Patient",
            last_name="One",
            date_of_birth=datetime(1990, 1, 1).date(),
            gender="M",
            phone_number="+256701000000",
            email="patient@example.com",
            address="123 Wellness Road",
            location=Location.objects.create(name="Region", location_type="region"),
            emergency_contact_name="Emergency Contact",
            emergency_contact_phone="+256701000001",
            emergency_contact_relationship="Sibling",
            registered_facility=HealthFacility.objects.create(
                name="Hope Clinic",
                facility_type="clinic",
                location=Location.objects.create(name="District", location_type="district"),
                address="456 Care Street",
                phone_number="+256701000002",
                email="clinic@example.com",
                website="",
                is_24_hours=False,
                contact_person_name="Admin",
                contact_person_phone="+256701000003",
                services_offered=[],
            ),
        )
        self.facility = self.patient.registered_facility
        self.client.force_authenticate(self.provider)
        self.list_url = reverse("api:appointment-list")

    def _appointment_payload(self, **kwargs):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(minutes=30)
        payload = {
            "patient": self.patient.pk,
            "provider": self.provider.pk,
            "facility": self.facility.pk,
            "appointment_type": "consultation",
            "reason": "Routine checkup",
            "status": Appointment.Status.SCHEDULED,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }
        payload.update(kwargs)
        return payload

    def test_create_appointment(self):
        response = self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.provider, self.provider)
        self.assertIn("created", appointment.notifications_sent)

    def test_provider_conflict_detection(self):
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        response = self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("provider", response.data)

    def test_patient_conflict_detection(self):
        another_provider = User.objects.create_user(
            username="provider2",
            password="password123",
            user_type="doctor",
            first_name="Provider",
            last_name="Two",
        )
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        payload = self._appointment_payload(provider=another_provider.pk)
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("patient", response.data)

    def test_facility_conflict_detection(self):
        another_patient = Patient.objects.create(
            patient_id="PAT-000101",
            first_name="Patient",
            last_name="Two",
            date_of_birth=datetime(1992, 1, 1).date(),
            gender="F",
            phone_number="+256701000010",
            email="patient2@example.com",
            address="789 Health Road",
            location=self.patient.location,
            emergency_contact_name="Emergency2",
            emergency_contact_phone="+256701000011",
            emergency_contact_relationship="Parent",
            registered_facility=self.facility,
        )
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        payload = self._appointment_payload(patient=another_patient.pk)
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("facility", response.data)

    def test_admin_can_view_audit_logs_for_appointments(self):
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
        )
        self.client.force_authenticate(admin_user)
        response = self.client.get(reverse("api:audit-logs-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
