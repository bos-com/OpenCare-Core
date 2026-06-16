# OpenCare-Core

OpenCare-Core is a Django backend for healthcare operations, patient records,
health worker management, facilities, appointments, audit logging, and API-first
integration work.

## Current Module Status

The repository includes models and scaffolding for several healthcare domains,
but not every module is exposed through `config/urls.py` yet.

| Module | Status | Notes |
| --- | --- | --- |
| Core pages and API hub | Available | Root routes and `/api/v1/` are enabled. |
| Patients | Available | `apps.patients.urls` is included in the main URL configuration. |
| Appointments | Available through API | The appointments app and tests are present under `apps/appointments/`. |
| Health workers | In progress | App code exists, but routes are not yet enabled in `config/urls.py`. |
| Facilities | In progress | Models exist, but the public route include remains disabled. |
| Records | In progress | Record models and serializers exist, but routes are not yet wired. |
| Analytics | In progress | App scaffolding exists, but the dedicated route include remains disabled. |

## Features

- Django and Django REST Framework backend
- JWT authentication and role-based access controls
- Patient, appointment, health record, and audit logging foundations
- PostgreSQL, Redis, Celery, and Docker Compose support
- OpenAPI schema, Swagger UI, and ReDoc documentation
- Development, test, and production settings modules

## Project Structure

```text
OpenCare-Core/
├── apps/                 # Django applications
├── config/               # Project URLs, WSGI/ASGI, Celery, and settings
├── docs/                 # Feature and API behavior guides
├── scripts/              # Database initialization assets
├── templates/            # HTML templates
├── docker-compose.yml    # Local service orchestration
├── Dockerfile            # Application container image
├── manage.py             # Django management entry point
└── requirements.txt      # Python dependencies
```

## Prerequisites

- Docker and Docker Compose for the recommended setup
- Python 3.11+ for local development without Docker
- PostgreSQL and Redis if you are not using Docker

## Docker Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/bos-com/OpenCare-Core.git
   cd OpenCare-Core
   ```

2. Copy the environment template:

   ```bash
   cp env.example .env
   ```

3. Build and start the services:

   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. Run migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create an admin user if needed:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Open the application:

   - Web interface: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin/`
   - Swagger UI: `http://localhost:8000/api/docs/`
   - ReDoc: `http://localhost:8000/api/redoc/`
   - Health check: `http://localhost:8000/health/`

## Local Development

```bash
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cp env.example .env
python manage.py migrate
python manage.py runserver
```

On macOS or Linux, activate the virtual environment with
`source venv/bin/activate`.

## Testing

```bash
python manage.py test
```

For targeted checks, run a specific app test module:

```bash
python manage.py test apps.api.tests
python manage.py test apps.appointments.tests
```

## API Documentation

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI schema: `/api/schema/`

Review [`docs/error-handling.md`](docs/error-handling.md) before adding or
changing endpoints so API errors remain sanitized and consistent.

## Documentation Index

- [`docs/appointments.md`](docs/appointments.md)
- [`docs/audit-logs.md`](docs/audit-logs.md)
- [`docs/error-handling.md`](docs/error-handling.md)
- [`docs/patient-records.md`](docs/patient-records.md)
- [`docs/rbac.md`](docs/rbac.md)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the contributor workflow. In
general, open or pick an issue, keep pull requests focused, add tests for
behavior changes, and document API or setup changes.

## License

This project is licensed under the terms in [`LICENSE`](LICENSE).
