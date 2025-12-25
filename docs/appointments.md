# Appointment Scheduling API

The Appointment Scheduling API provides comprehensive endpoints for managing appointments between patients and healthcare providers. It includes conflict detection, notification hooks, and role-based access control.

## Overview

The appointment system ensures:
- **No double booking**: Prevents overlapping appointments for providers, patients, and facilities
- **Automatic notifications**: Sends email and SMS notifications for appointment events
- **Role-based access**: Only admins and providers can manage appointments
- **Status management**: Track appointment lifecycle (scheduled, completed, cancelled, no-show)

## Endpoints

### Base URL
All appointment endpoints are under `/api/v1/appointments/`

### CRUD Operations

#### List Appointments
```
GET /api/v1/appointments/
```
Returns paginated list of appointments with filtering and search support.

**Query Parameters:**
- `provider` - Filter by provider ID
- `patient` - Filter by patient ID
- `facility` - Filter by facility ID
- `status` - Filter by status (scheduled, completed, cancelled, no_show)
- `appointment_type` - Filter by appointment type
- `search` - Search by patient ID, patient name, or provider name
- `ordering` - Order by `start_time` or `created_at` (default: `start_time`)

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "John Doe",
      "provider": 5,
      "provider_name": "Dr. Jane Smith",
      "facility": 3,
      "facility_name": "Hope Clinic",
      "appointment_type": "consultation",
      "reason": "Routine checkup",
      "status": "scheduled",
      "start_time": "2025-01-15T10:00:00Z",
      "end_time": "2025-01-15T10:30:00Z",
      "created_at": "2025-01-10T08:00:00Z",
      "updated_at": "2025-01-10T08:00:00Z"
    }
  ]
}
```

#### Create Appointment
```
POST /api/v1/appointments/
```
Creates a new appointment with automatic conflict detection and notifications.

**Request Body:**
```json
{
  "patient": 1,
  "provider": 5,
  "facility": 3,
  "appointment_type": "consultation",
  "reason": "Routine checkup",
  "start_time": "2025-01-15T10:00:00Z",
  "end_time": "2025-01-15T10:30:00Z"
}
```

**Validation Rules:**
- `start_time` must be in the future
- `end_time` must be after `start_time`
- Minimum duration: 5 minutes
- No overlapping appointments for provider, patient, or facility
- Provider must be active and eligible (doctor, nurse, midwife, community_worker)
- Patient must be active

**Response:** `201 Created` with appointment details

**Error Responses:**
- `400 Bad Request` - Validation errors or conflicts
  ```json
  {
    "provider": ["Provider already has an appointment in this window."],
    "patient": ["Patient already has an appointment in this window."],
    "facility": ["Facility already has an appointment in this window."]
  }
  ```

#### Retrieve Appointment
```
GET /api/v1/appointments/{id}/
```
Returns detailed appointment information including notification history.

**Response:**
```json
{
  "id": 1,
  "patient": 1,
  "patient_name": "John Doe",
  "provider": 5,
  "provider_name": "Dr. Jane Smith",
  "facility": 3,
  "facility_name": "Hope Clinic",
  "appointment_type": "consultation",
  "reason": "Routine checkup",
  "status": "scheduled",
  "start_time": "2025-01-15T10:00:00Z",
  "end_time": "2025-01-15T10:30:00Z",
  "notifications_sent": [
    {
      "type": "email",
      "recipient": "patient",
      "method": "email",
      "sent_at": "2025-01-10T08:00:00Z"
    }
  ],
  "created_at": "2025-01-10T08:00:00Z",
  "updated_at": "2025-01-10T08:00:00Z"
}
```

#### Update Appointment
```
PATCH /api/v1/appointments/{id}/
PUT /api/v1/appointments/{id}/
```
Updates appointment details. Triggers conflict detection and notifications.

**Request Body:** (same as create, all fields optional)

**Response:** `200 OK` with updated appointment

#### Delete Appointment
```
DELETE /api/v1/appointments/{id}/
```
Cancels and deletes an appointment. Sends cancellation notifications.

**Response:** `204 No Content`

### Custom Actions

#### Upcoming Appointments
```
GET /api/v1/appointments/upcoming/
```
Returns all scheduled appointments in the future.

**Response:** Same format as list endpoint, filtered to future scheduled appointments only.

#### Appointments by Provider
```
GET /api/v1/appointments/by-provider/{provider_id}/
```
Returns all appointments for a specific provider.

**Response:** Same format as list endpoint.

#### Appointments by Patient
```
GET /api/v1/appointments/by-patient/{patient_id}/
```
Returns all appointments for a specific patient.

**Response:** Same format as list endpoint.

#### Check Conflicts
```
POST /api/v1/appointments/{id}/check-conflicts/
```
Manually check for scheduling conflicts for an appointment.

**Response:**
```json
{
  "has_conflicts": true,
  "conflicts": {
    "provider": [
      {
        "id": 2,
        "start_time": "2025-01-15T10:15:00Z",
        "end_time": "2025-01-15T10:45:00Z",
        "patient__first_name": "Jane",
        "patient__last_name": "Doe"
      }
    ]
  }
}
```

#### Cancel Appointment
```
POST /api/v1/appointments/{id}/cancel/
```
Marks an appointment as cancelled and sends notifications.

**Response:** `200 OK` with updated appointment (status: "cancelled")

#### Complete Appointment
```
POST /api/v1/appointments/{id}/complete/
```
Marks an appointment as completed.

**Response:** `200 OK` with updated appointment (status: "completed")

#### Mark No-Show
```
POST /api/v1/appointments/{id}/mark-no-show/
```
Marks an appointment as no-show.

**Response:** `200 OK` with updated appointment (status: "no_show")

## Conflict Detection

The system prevents double booking by checking for overlapping appointments:

1. **Provider conflicts**: A provider cannot have two appointments at the same time
2. **Patient conflicts**: A patient cannot have two appointments at the same time
3. **Facility conflicts**: A facility cannot have two appointments at the same time

**Conflict Detection Logic:**
- Only considers appointments with status `scheduled` or `no_show`
- Checks for time overlap: `start_time < other.end_time AND end_time > other.start_time`
- Validates during create and update operations
- Can be manually checked using the `check-conflicts` endpoint

## Notifications

The system automatically sends notifications for appointment events:

### Events
- **created**: When a new appointment is scheduled
- **updated**: When appointment details are changed
- **cancelled**: When an appointment is cancelled
- **reminder**: (Future) For appointment reminders

### Notification Methods

#### Email Notifications
- Sent to both patient and provider email addresses
- Includes appointment details, date/time, facility, and reason
- Subject line includes event type and appointment date

#### SMS Notifications
- Sent to both patient and provider phone numbers
- Shorter format optimized for SMS
- Includes key details: date, time, provider/facility name

### Notification Hooks

The notification system is designed to integrate with:
- **Email**: Django's `send_mail` (configurable via `DEFAULT_FROM_EMAIL`)
- **SMS**: Hook ready for integration with:
  - Twilio
  - AWS SNS
  - Africa's Talking
  - Other SMS gateway services

**Current Implementation:**
- Email notifications are fully functional
- SMS notifications are logged (ready for provider integration)

**Notification History:**
All sent notifications are tracked in the `notifications_sent` field of each appointment.

## Roles & Permissions

- **Admin** (`admin` role): Full access to all appointment operations
- **Provider** (`provider` role): Can create, view, update, and cancel appointments
- **Patient** (`patient` role): Currently blocked (future: may view own appointments)

All endpoints require authentication and appropriate role permissions.

## Status Management

Appointments can have the following statuses:

- **scheduled**: Appointment is confirmed and upcoming
- **completed**: Appointment was successfully completed
- **cancelled**: Appointment was cancelled
- **no_show**: Patient did not show up for the appointment

Status transitions:
- `scheduled` → `completed` (via `complete` action)
- `scheduled` → `cancelled` (via `cancel` action or delete)
- `scheduled` → `no_show` (via `mark-no-show` action)

## Model Properties

The Appointment model includes helpful properties:

- `duration_minutes`: Calculates appointment duration in minutes
- `is_upcoming`: Returns `True` if appointment is in the future and scheduled
- `check_conflicts()`: Method to manually check for scheduling conflicts

## Example Usage

### Create an Appointment
```bash
curl -X POST https://api.opencare-africa.com/api/v1/appointments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "provider": 5,
    "facility": 3,
    "appointment_type": "consultation",
    "reason": "Annual checkup",
    "start_time": "2025-01-15T10:00:00Z",
    "end_time": "2025-01-15T10:30:00Z"
  }'
```

### List Upcoming Appointments
```bash
curl -X GET https://api.opencare-africa.com/api/v1/appointments/upcoming/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Cancel an Appointment
```bash
curl -X POST https://api.opencare-africa.com/api/v1/appointments/1/cancel/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing

Comprehensive test coverage includes:
- CRUD operations
- Conflict detection (provider, patient, facility)
- Validation rules (past dates, minimum duration)
- Custom actions (upcoming, by-provider, by-patient)
- Status management (cancel, complete, no-show)
- RBAC enforcement
- Notification triggers

Run tests with:
```bash
python manage.py test apps.appointments.tests.test_appointments_api
```

## Future Enhancements

- Patient portal access to view own appointments
- Appointment reminders (24 hours before)
- Recurring appointments
- Waitlist management
- Integration with calendar systems (Google Calendar, Outlook)
- Video consultation links
- Appointment ratings and feedback
