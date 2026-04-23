"""
API tests validating patient health record CRUD flows.
"""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import HealthFacility, Location
from apps.patients.models import Patient
from apps.records.models import HealthRecord


User = get_user_model()


class HealthRecordAPITests(APITestCase):
    """
    Exercise the records endpoint to ensure role enforcement and functionality.
    """

    def setUp(self):
        """
        Create reusable fixtures for each test case.
        """

        self.clinical_user = User.objects.create_user(
            username="doctor1",
            password="testpass123",
            user_type="doctor",
            first_name="Dana",
            last_name="Doctor",
        )
        self.non_clinical_user = User.objects.create_user(
            username="community1",
            password="testpass123",
            user_type="community_worker",
            first_name="Case",
            last_name="Worker",
        )
        self.location = Location.objects.create(
            name="Central Region",
            location_type="region",
        )
        self.facility = HealthFacility.objects.create(
            name="Central Hospital",
            facility_type="hospital",
            location=self.location,
            address="123 Main Street",
            phone_number="+256700000000",
            email="central@example.com",
            website="",
            is_24_hours=True,
            contact_person_name="Head Nurse",
            contact_person_phone="+256700000001",
            services_offered=[],
        )
        self.patient = Patient.objects.create(
            patient_id="PAT-2001",
            first_name="Jane",
            last_name="Doe",
            date_of_birth=timezone.now().date() - timedelta(days=30 * 365),
            gender="F",
            phone_number="+256700000002",
            email="jane@example.com",
            address="456 Care Road",
            location=self.location,
            emergency_contact_name="John Doe",
            emergency_contact_phone="+256700000003",
            emergency_contact_relationship="Sibling",
            registered_facility=self.facility,
        )
        self.list_url = reverse("api:records-list")
        self.client.force_authenticate(self.clinical_user)

    def _payload(self, **overrides):
        """
        Build a base payload for record creation, overriding as needed.
        """

        base = {
            "patient": self.patient.pk,
            "facility": self.facility.pk,
            "record_type": "medical",
            "record_date": timezone.now().isoformat(),
            "attending_provider": self.clinical_user.pk,
            "chief_complaint": "Mild headache",
            "assessment": "Observation required",
            "diagnosis": [],
            "treatment_plan": "Monitor symptoms",
            "follow_up_plan": "Return in one week",
            "notes": "Initial consultation",
            "is_confidential": False,
            "is_active": True,
        }
        base.update(overrides)
        return base

    def test_clinical_staff_can_create_record(self):
        """
        Clinical roles should be able to create patient records.
        """

        response = self.client.post(self.list_url, data=self._payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthRecord.objects.count(), 1)

    def test_non_clinical_user_forbidden(self):
        """
        Non-clinical roles must be denied read access.
        """

        self.client.force_authenticate(self.non_clinical_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_record(self):
        """
        Ensure updates persist and return the latest content.
        """

        record = HealthRecord.objects.create(
            patient=self.patient,
            facility=self.facility,
            record_type="medical",
            record_date=timezone.now(),
            attending_provider=self.clinical_user,
        )
        url = reverse("api:records-detail", args=[record.pk])
        response = self.client.patch(
            url,
            data={"assessment": "Condition improving"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.assessment, "Condition improving")

    def test_delete_record(self):
        """
        Deleting a record should remove it from the database.
        """

        record = HealthRecord.objects.create(
            patient=self.patient,
            facility=self.facility,
            record_type="medical",
            record_date=timezone.now(),
            attending_provider=self.clinical_user,
        )
        url = reverse("api:records-detail", args=[record.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HealthRecord.objects.filter(pk=record.pk).exists())

    def test_filter_by_record_type(self):
        """
        Verify that filter parameters narrow the result set.
        """

        HealthRecord.objects.create(
            patient=self.patient,
            facility=self.facility,
            record_type="medical",
            record_date=timezone.now(),
            attending_provider=self.clinical_user,
        )
        HealthRecord.objects.create(
            patient=self.patient,
            facility=self.facility,
            record_type="imaging",
            record_date=timezone.now(),
            attending_provider=self.clinical_user,
        )
        response = self.client.get(self.list_url, {"record_type": "imaging"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["record_type"], "imaging")

    def test_by_patient_action(self):
        """
        The by-patient helper should return records scoped by external ID.
        """

        HealthRecord.objects.create(
            patient=self.patient,
            facility=self.facility,
            record_type="medical",
            record_date=timezone.now(),
            attending_provider=self.clinical_user,
        )
        url = reverse("api:records-by-patient")
        response = self.client.get(url, {"patient_id": self.patient.patient_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
