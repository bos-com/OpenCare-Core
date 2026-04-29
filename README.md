# OpenCare-Africa (OpenCare-Core)

OpenCare-Core is a Django-based health informatics backend designed for
healthcare management in Africa. It provides APIs, admin workflows, background
tasks, and supporting documentation for patient, facility, staff, record, and
appointment management.

## Highlights

- Django 4.2 backend with Django REST Framework
- PostgreSQL, Redis, Celery, and Docker support
- JWT authentication via SimpleJWT
- OpenAPI documentation through drf-spectacular
- Health checks, audit logging, and domain-specific docs

## Repository Layout

| Path | Purpose |
| --- | --- |
| `apps/` | Django applications such as core, patients, API, analytics, and appointments |
| `config/` | Django settings, URL routing, ASGI/WSGI, and Celery config |
| `docs/` | Focused documentation for API behavior and domain workflows |
| `templates/` | Server-rendered HTML templates |
| `docker-compose.yml` | Multi-service development stack |
| `requirements*.txt` | Python dependencies |

## Choose a Setup Path

| Path | Best for | Main command |
| --- | --- | --- |
| Docker | Recommended full-stack development | `docker-compose up --build -d` |
| Local | App-only Django development | `python manage.py runserver` |

## Docker Setup

Use Docker when you want the web app, database, Redis, and worker services to
start together with the repository defaults.

1. Clone the repository:

   ```bash
   git clone https://github.com/bos-com/OpenCare-Core.git
   cd OpenCare-Core
   ```

2. Copy the environment template:

   ```bash
   cp env.example .env
   ```

   PowerShell equivalent:

   ```powershell
   Copy-Item env.example .env
   ```

3. Build and start the stack:

   ```bash
   docker-compose up --build -d
   ```

4. Apply migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Optionally create a superuser:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Verify the installation:

   ```bash
   docker-compose ps
   curl http://localhost:8000/health/
   ```

### Docker Access Points

- Web app: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Health check: `http://localhost:8000/health/`

## Local Development

Use this mode when you want to run the Django app directly without the full
container stack.

1. Clone the repository:

   ```bash
   git clone https://github.com/bos-com/OpenCare-Core.git
   cd OpenCare-Core
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   Linux or macOS:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Copy the environment template:

   ```bash
   cp env.example .env
   ```

   Update `.env` if you are pointing at non-Docker PostgreSQL or Redis
   services.

5. Apply migrations and optionally create a superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the dev server:

   ```bash
   python manage.py runserver
   ```

7. Verify the installation:

   ```bash
   curl http://localhost:8000/health/
   ```

## API Documentation and Testing

Interactive API docs are available after startup:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI schema: `/api/schema/`

Use these companion docs for day-to-day development:

- [`docs/api-testing.md`](docs/api-testing.md) for curl-based smoke tests
- [`docs/error-handling.md`](docs/error-handling.md) for sanitized API error guidance
- [`docs/patient-records.md`](docs/patient-records.md) for records workflow details
- [`docs/appointments.md`](docs/appointments.md) for appointment behavior
- [`docs/audit-logs.md`](docs/audit-logs.md) for audit trail expectations
- [`docs/rbac.md`](docs/rbac.md) for role and permission behavior

### Key API Areas

- Authentication: `/api/v1/auth/`
- Patients: `/api/v1/patients/`
- Health workers: `/api/v1/health-workers/`
- Facilities: `/api/v1/facilities/`
- Records: `/api/v1/records/`
- Audit logs: `/api/v1/audit-logs/`
- Appointments: `/api/v1/appointments/`
- API health: `/api/v1/health/`

## Configuration

Primary configuration entry points:

- `env.example`
- `config/settings/base.py`
- `config/settings/development.py`
- `config/settings/production.py`
- `config/settings/test.py`

## Testing

Run the full suite:

```bash
python manage.py test
```

Run focused API suites:

```bash
python manage.py test apps.api.tests
python manage.py test apps.appointments.tests
```

Run with coverage:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Contributing

Contribution workflow, coding standards, and pull request expectations are
documented in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

This project is distributed under the terms described in [`LICENSE`](LICENSE).
