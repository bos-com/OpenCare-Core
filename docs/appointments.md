# Appointment Scheduling API

The appointment scheduling endpoints coordinate visits between patients and
healthcare providers. This guide summarizes the request flow and safeguards.

## Endpoints

- `GET /api/v1/appointments/`: List upcoming appointments (filterable by patient,
  provider, facility, status, or type).
- `POST /api/v1/appointments/`: Create a new appointment.
- `GET /api/v1/appointments/{id}/`: Retrieve appointment details.
- `PATCH /api/v1/appointments/{id}/`: Update status, timing, or metadata.
- `DELETE /api/v1/appointments/{id}/`: Cancel an appointment (audit logged).

All endpoints require authentication. CRUD operations are audit logged through
the shared `AuditLogMixin`.

## Conflict Detection

- Provider, patient, and facility calendars are checked for overlapping time
  ranges before saving.
- Appointments shorter than five minutes or with `start_time >= end_time` are
  rejected.
- Only active clinical user types (doctor, nurse, midwife, community_worker)
  may be assigned as the provider.

## Notifications

- Each create/update/delete action triggers `apps.appointments.notifications.send_notification`.
- The current implementation logs to the application logger and records the
  emitted events on the appointment record.
- Integrate email/SMS by replacing the logger call inside the notification helper.

## Testing

Unit tests cover conflict detection for providers, patients, and facilities, and
verify that API responses behave as expected (`apps/appointments/tests/test_appointments_api.py`).
