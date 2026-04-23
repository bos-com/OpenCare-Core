# Patient Records API

The patient records API provides secure CRUD access to clinical history across
OpenCare-Africa. Only authenticated clinical roles (doctor, nurse, midwife,
lab technician, pharmacist) and superusers may interact with these endpoints.

## Endpoints

- `GET /api/v1/records/` — List records with pagination. Supports filtering on
  `record_type`, `facility`, `attending_provider`, `patient`, `patient_id`, and
  `record_date` ranges (`record_date_after`, `record_date_before`).
- `POST /api/v1/records/` — Create a new record entry.
- `GET /api/v1/records/{id}/` — Retrieve full clinical details.
- `PATCH /api/v1/records/{id}/` — Update selected fields.
- `DELETE /api/v1/records/{id}/` — Remove a record.
- `GET /api/v1/records/by-patient/?patient_id=PAT-123` — Convenience helper
  for pulling a patient's entire history by external identifier.

## Roles & Security

- Endpoints require JWT authentication (or a valid session).
- Only users with clinical roles or superuser privileges pass the permission
  check enforced by `apps.api.permissions.IsClinicalStaff`.
- Each response omits sensitive attachments unless requested through the
  detailed view, helping to balance usability and confidentiality.

## Example Payload

```json
{
  "patient": 1,
  "facility": 3,
  "record_type": "medical",
  "record_date": "2025-01-15T10:00:00Z",
  "attending_provider": 7,
  "chief_complaint": "Headache",
  "assessment": "Observation required",
  "diagnosis": ["tension_headache"],
  "treatment_plan": "Hydration and rest",
  "follow_up_plan": "Return if symptoms persist",
  "notes": "No contraindications noted",
  "is_confidential": false
}
```

## Testing

Automated tests covering create, read, update, delete, filtering, and access
control live in `apps/api/tests/test_health_records_api.py`. Run them with:

```bash
python manage.py test apps.api.tests.test_health_records_api
```
