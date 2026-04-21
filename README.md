# OpenCare-Africa
Looking to help? Check out our [Contributing Guide](./CONTRIBUTING.md)!

A comprehensive health informatics platform backend built with Django, designed specifically for healthcare management in Africa.

---

## 🏥 Project Overview

OpenCare-Africa is a robust, scalable backend system for managing healthcare operations, patient records, health worker management, and facility operations. The system follows modern Django best practices and provides comprehensive API endpoints for seamless frontend integration.

---

## ✨ Features

### Core Functionality

* **User Management**: Role-based access and permissions for healthcare workers
* **Patient Management**: End-to-end patient lifecycle management with medical history
* **Health Facility Management**: Facility operations, services, and resources
* **Health Records**: Detailed medical records with FHIR compliance
* **Analytics & Reporting**: Disease tracking, performance metrics, and insights
* **API-First Design**: RESTful APIs with OpenAPI/Swagger documentation

### Technical Features

* **Django 4.2+**: Modern Django implementation
* **PostgreSQL**: Reliable and scalable database
* **Redis**: Caching and session management
* **Celery**: Background task processing
* **Docker**: Containerized deployment
* **JWT Authentication**: Secure API access
* **Health Checks**: System monitoring and diagnostics

---

## 🏗️ Architecture

```
OpenCare-Africa/
├── apps/
│   ├── core/
│   ├── patients/
│   ├── health_workers/
│   ├── facilities/
│   ├── records/
│   ├── analytics/
│   └── api/
├── config/
│   ├── settings/
│   ├── urls.py
│   └── celery.py
├── templates/
├── static/
├── media/
├── docs/
└── scripts/
```

---

## 🚀 Quick Start

### Prerequisites

* Docker & Docker Compose (recommended)
* Python 3.11+ (for local development)
* PostgreSQL 15+ (included in Docker)
* Redis 7+ (included in Docker)

---

## 🐳 Docker Setup (Recommended)

This is the recommended way to run OpenCare-Africa, as it ensures consistency across all environments.

### 1. Clone the repository

```bash
git clone https://github.com/bos-com/OpenCare-Africa.git
cd OpenCare-Africa
```

### 2. Set up environment variables

```bash
cp env.example .env
```

The `.env` file is already configured for Docker. No changes are needed unless you want to customize settings.

### 3. Build and start services

```bash
docker-compose build
docker-compose up -d
```

### 4. Run migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Verify installation

```bash
docker-compose ps
curl http://localhost:8000/health/
```

### 7. Access the application

* Web: [http://localhost:8000](http://localhost:8000)
* Admin: [http://localhost:8000/admin](http://localhost:8000/admin)
* API Docs: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 📘 API Documentation

* Swagger UI: `/api/docs/`
* ReDoc: `/api/redoc/`
* Schema: `/api/schema/`

### Key Endpoints

* `/api/v1/auth/`
* `/api/v1/patients/`
* `/api/v1/health-workers/`
* `/api/v1/facilities/`
* `/api/v1/records/`
* `/api/v1/analytics/`

---

## 🛠️ Local Development Setup

If you prefer to run the application locally without Docker, follow these steps:

### 1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional
```

### 3. Configure environment

```bash
cp env.example .env
```

Update DB and Redis settings for local use.

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start server

```bash
python manage.py runserver
```

SQLite is used by default for development (no additional setup required).

---

## 🗄️ Database Overview

### Core Models

* User
* Location
* HealthFacility
* AuditTrail

### Patient Models

* Patient
* PatientVisit
* PatientMedicalHistory

### Healthcare Models

* HealthWorkerProfile
* ProfessionalQualification
* WorkSchedule

### Records Models

* HealthRecord
* VitalSigns
* Medication
* LaboratoryTest

---

## 🔧 Configuration

### Environment Variables

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=opencare_africa
DB_USER=opencare_user
DB_PASSWORD=opencare_password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

---

## 🧪 Testing

```bash
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment

### Production Checklist

* Set `DEBUG=False`
* Configure production database
* Enable SSL/TLS
* Configure static files
* Set up monitoring
* Configure backups

---

## 🔒 Security Features

* JWT authentication
* Role-based access control
* Audit logging
* Input validation
* CORS configuration
* Rate limiting

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests
5. Submit a pull request

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

* Django community
* Healthcare professionals
* Open-source contributors

---

**OpenCare-Africa** — Empowering healthcare in Africa through technology.
