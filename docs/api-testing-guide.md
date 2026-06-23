# OpenCare-Core API Testing Guide

This guide walks through testing the OpenCare-Core REST API locally using
`curl`. It covers authentication, patient management, and health facility
operations.

## Prerequisites

1. **Running server** — follow the main README to start the Django development
   server on `http://localhost:8000`.
2. **Database migrations** — run `python manage.py migrate` so the schema is
   up to date.
3. **Superuser account** — create one with
   `python manage.py createsuperuser` if you haven't already.

## 1. Authentication

OpenCare-Core uses JWT (JSON Web Token) authentication. Every protected
endpoint requires an `Authorization: Bearer <token>` header.

### Obtain a Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'
```

**Success (`200 OK`)**:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

Save the `access` token — you will pass it in subsequent requests.

### Refresh an Expired Token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{ "refresh": "<your_refresh_token>" }'
```

## 2. Patient Management

### Create a Patient

```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Mukasa",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "phone_number": "+256700123456",
    "address": "Kampala, Uganda"
  }'
```

**Success (`201 Created`)**:

```json
{
  "id": 1,
  "first_name": "Alice",
  "last_name": "Mukasa",
  "date_of_birth": "1990-05-15",
  "gender": "F",
  "phone_number": "+256700123456",
  "address": "Kampala, Uganda",
  "created_at": "2025-01-20T08:00:00Z"
}
```

### List Patients

```bash
curl http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer <access_token>"
```

### Get a Single Patient

```bash
curl http://localhost:8000/api/patients/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Update a Patient

```bash
curl -X PATCH http://localhost:8000/api/patients/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{ "phone_number": "+256700999999" }'
```

## 3. Health Facility Management

### List Facilities

```bash
curl http://localhost:8000/api/facilities/ \
  -H "Authorization: Bearer <access_token>"
```

### Create a Facility

```bash
curl -X POST http://localhost:8000/api/facilities/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bugema University Health Centre",
    "facility_type": "health_centre",
    "district": "Luweero",
    "address": "Bugema, Luweero District"
  }'
```

## 4. Common Errors

| Status | Meaning                | Example Cause                     |
|--------|------------------------|-----------------------------------|
| 400    | Bad Request            | Missing required fields           |
| 401    | Unauthorized           | Missing or expired JWT token      |
| 403    | Forbidden              | Insufficient role permissions     |
| 404    | Not Found              | Patient/facility ID doesn't exist |
| 500    | Internal Server Error  | Unhandled exception in view       |

**Example error response**:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

## 5. Using Django's Test Client

For automated testing during development, use Django's built-in test framework:

```python
from django.test import TestCase
from rest_framework.test import APIClient

class PatientAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create and authenticate a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_patient(self):
        response = self.client.post('/api/patients/', {
            'first_name': 'Test',
            'last_name': 'Patient',
            'date_of_birth': '2000-01-01',
            'gender': 'M',
        })
        self.assertEqual(response.status_code, 201)
```

Run tests with:

```bash
python manage.py test
```

## 6. Troubleshooting

- **"No module named 'config.settings'"**: Ensure `DJANGO_SETTINGS_MODULE` is
  set to `config.settings.development` in your `.env` or shell.
- **Database errors**: Run `python manage.py migrate` to apply pending
  migrations.
- **CORS errors from a frontend**: Check `CORS_ALLOWED_ORIGINS` in settings.
