"""
Comprehensive tests for the appointment scheduling API.
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
    """Test appointment CRUD operations and conflict detection."""

    def setUp(self):
        self.location = Location.objects.create(
            name="Central Region",
            location_type="region"
        )
        self.facility = HealthFacility.objects.create(
            name="Hope Clinic",
            facility_type="clinic",
            location=self.location,
            address="456 Care Street",
            phone_number="+256701000002",
            email="clinic@example.com",
            website="",
            is_24_hours=False,
            contact_person_name="Admin",
            contact_person_phone="+256701000003",
            services_offered=[],
        )
        
        self.provider = User.objects.create_user(
            username="provider1",
            password="password123",
            user_type="doctor",
            role=User.Role.PROVIDER,
            first_name="Provider",
            last_name="One",
            email="provider@example.com",
            phone_number="+256701000100",
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
            location=self.location,
            emergency_contact_name="Emergency Contact",
            emergency_contact_phone="+256701000001",
            emergency_contact_relationship="Sibling",
            registered_facility=self.facility,
        )
        
        self.client.force_authenticate(self.provider)
        self.list_url = reverse("api:appointment-list")

    def _appointment_payload(self, **kwargs):
        """Helper to create appointment payload."""
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
        """Test creating a new appointment."""
        response = self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.provider, self.provider)
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.status, Appointment.Status.SCHEDULED)

    def test_list_appointments(self):
        """Test listing appointments."""
        Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_appointment(self):
        """Test retrieving a single appointment."""
        appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
        )
        url = reverse("api:appointment-detail", args=[appointment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], appointment.pk)

    def test_update_appointment(self):
        """Test updating an appointment."""
        appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
        )
        url = reverse("api:appointment-detail", args=[appointment.pk])
        new_reason = "Follow-up consultation"
        response = self.client.patch(url, {"reason": new_reason}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.reason, new_reason)

    def test_delete_appointment(self):
        """Test deleting an appointment."""
        appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
        )
        url = reverse("api:appointment-detail", args=[appointment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Appointment.objects.filter(pk=appointment.pk).exists())

    def test_provider_conflict_detection(self):
        """Test that provider cannot have overlapping appointments."""
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        # Try to create another appointment with same provider at overlapping time
        start = timezone.now() + timedelta(hours=1, minutes=15)
        end = start + timedelta(minutes=30)
        payload = self._appointment_payload(
            start_time=start.isoformat(),
            end_time=end.isoformat()
        )
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("provider", response.data)

    def test_patient_conflict_detection(self):
        """Test that patient cannot have overlapping appointments."""
        another_provider = User.objects.create_user(
            username="provider2",
            password="password123",
            user_type="doctor",
            role=User.Role.PROVIDER,
            first_name="Provider",
            last_name="Two",
        )
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        # Try to create another appointment with same patient at overlapping time
        start = timezone.now() + timedelta(hours=1, minutes=15)
        end = start + timedelta(minutes=30)
        payload = self._appointment_payload(
            provider=another_provider.pk,
            start_time=start.isoformat(),
            end_time=end.isoformat()
        )
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("patient", response.data)

    def test_facility_conflict_detection(self):
        """Test that facility cannot have overlapping appointments."""
        another_patient = Patient.objects.create(
            patient_id="PAT-000101",
            first_name="Patient",
            last_name="Two",
            date_of_birth=datetime(1992, 1, 1).date(),
            gender="F",
            phone_number="+256701000010",
            email="patient2@example.com",
            address="789 Health Road",
            location=self.location,
            emergency_contact_name="Emergency2",
            emergency_contact_phone="+256701000011",
            emergency_contact_relationship="Parent",
            registered_facility=self.facility,
        )
        self.client.post(self.list_url, data=self._appointment_payload(), format="json")
        # Try to create another appointment at same facility at overlapping time
        start = timezone.now() + timedelta(hours=1, minutes=15)
        end = start + timedelta(minutes=30)
        payload = self._appointment_payload(
            patient=another_patient.pk,
            start_time=start.isoformat(),
            end_time=end.isoformat()
        )
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("facility", response.data)

    def test_cannot_schedule_in_past(self):
        """Test that appointments cannot be scheduled in the past."""
        past_time = timezone.now() - timedelta(hours=1)
        payload = self._appointment_payload(
            start_time=past_time.isoformat(),
            end_time=(past_time + timedelta(minutes=30)).isoformat()
        )
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_time", response.data)

    def test_minimum_duration_validation(self):
        """Test that appointments must be at least 5 minutes long."""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(minutes=3)  # Too short
        payload = self._appointment_payload(
            start_time=start.isoformat(),
            end_time=end.isoformat()
        )
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upcoming_appointments_action(self):
        """Test the upcoming appointments endpoint."""
        # Create past appointment
        Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() - timedelta(minutes=30),
            status=Appointment.Status.SCHEDULED,
        )
        # Create future appointment
        future_appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
            status=Appointment.Status.SCHEDULED,
        )
        url = reverse("api:appointment-upcoming")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], future_appointment.pk)

    def test_by_provider_action(self):
        """Test filtering appointments by provider."""
        another_provider = User.objects.create_user(
            username="provider2",
            password="password123",
            user_type="nurse",
            role=User.Role.PROVIDER,
        )
        appointment1 = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
        )
        Appointment.objects.create(
            patient=self.patient,
            provider=another_provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=2),
            end_time=timezone.now() + timedelta(hours=2, minutes=30),
        )
        url = reverse("api:appointment-by-provider", args=[self.provider.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], appointment1.pk)

    def test_by_patient_action(self):
        """Test filtering appointments by patient."""
        another_patient = Patient.objects.create(
            patient_id="PAT-000102",
            first_name="Patient",
            last_name="Three",
            date_of_birth=datetime(1993, 1, 1).date(),
            gender="F",
            phone_number="+256701000020",
            email="patient3@example.com",
            address="999 Health Road",
            location=self.location,
            emergency_contact_name="Emergency3",
            emergency_contact_phone="+256701000021",
            emergency_contact_relationship="Spouse",
            registered_facility=self.facility,
        )
        appointment1 = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
        )
        Appointment.objects.create(
            patient=another_patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=2),
            end_time=timezone.now() + timedelta(hours=2, minutes=30),
        )
        url = reverse("api:appointment-by-patient", args=[self.patient.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], appointment1.pk)

    def test_cancel_appointment_action(self):
        """Test cancelling an appointment."""
        appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
            status=Appointment.Status.SCHEDULED,
        )
        url = reverse("api:appointment-cancel", args=[appointment.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, Appointment.Status.CANCELLED)

    def test_complete_appointment_action(self):
        """Test marking an appointment as completed."""
        appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() - timedelta(minutes=30),
            status=Appointment.Status.SCHEDULED,
        )
        url = reverse("api:appointment-complete", args=[appointment.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, Appointment.Status.COMPLETED)

    def test_mark_no_show_action(self):
        """Test marking an appointment as no-show."""
        appointment = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() - timedelta(minutes=30),
            status=Appointment.Status.SCHEDULED,
        )
        url = reverse("api:appointment-mark-no-show", args=[appointment.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, Appointment.Status.NO_SHOW)

    def test_check_conflicts_action(self):
        """Test the check conflicts endpoint."""
        appointment1 = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=30),
            status=Appointment.Status.SCHEDULED,
        )
        # Create overlapping appointment
        appointment2 = Appointment.objects.create(
            patient=self.patient,
            provider=self.provider,
            facility=self.facility,
            start_time=timezone.now() + timedelta(hours=1, minutes=15),
            end_time=timezone.now() + timedelta(hours=1, minutes=45),
            status=Appointment.Status.SCHEDULED,
        )
        url = reverse("api:appointment-check-conflicts", args=[appointment2.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["has_conflicts"])

    def test_rbac_patient_blocked(self):
        """Test that patients cannot access appointment endpoints."""
        patient_user = User.objects.create_user(
            username="patient_user",
            password="password123",
            role=User.Role.PATIENT,
            email="patient_user@example.com",
        )
        self.client.force_authenticate(patient_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rbac_admin_can_access(self):
        """Test that admins can access appointment endpoints."""
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
            role=User.Role.ADMIN,
        )
        self.client.force_authenticate(admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
