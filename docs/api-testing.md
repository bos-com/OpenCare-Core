# API Testing Guide

This guide provides quick manual checks for the most important public and
authenticated API routes in OpenCare-Core.

## Base URLs

- Web application: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

## Public Health Checks

### Infrastructure health

```bash
curl http://localhost:8000/health/
```

### API health

```bash
curl http://localhost:8000/api/v1/health/
```

## Obtain a JWT Access Token

Create a staff or superuser account first, then request a token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "change-me"
  }'
```

Example response:

```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

Use the `access` token in later requests:

```text
Authorization: Bearer <access_token>
```

## Patient API Smoke Tests

### List patients

```bash
curl http://localhost:8000/api/v1/patients/ \
  -H "Authorization: Bearer <access_token>"
```

### Create a patient

```bash
curl -X POST http://localhost:8000/api/v1/patients/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "date_of_birth": "1998-06-12",
    "gender": "female",
    "phone_number": "+256700000000"
  }'
```

## Appointment API Smoke Tests

### List appointments

```bash
curl http://localhost:8000/api/v1/appointments/ \
  -H "Authorization: Bearer <access_token>"
```

### View API statistics

```bash
curl http://localhost:8000/api/v1/stats/ \
  -H "Authorization: Bearer <access_token>"
```

## Token Refresh

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

## Common Failure Cases

- `400 Bad Request`: request body fails validation
- `401 Unauthorized`: missing or expired JWT token
- `403 Forbidden`: authenticated user lacks permission for the route
- `404 Not Found`: object does not exist
