OpenCare-AfricaA comprehensive health informatics platform backend built with Django, designed specifically for healthcare management in Africa.Project OverviewOpenCare-Africa is a robust, scalable backend system for managing healthcare operations, patient records, health worker management, and health facility operations. The system is built with modern Django practices and includes comprehensive API endpoints for integration with frontend applications.FeaturesCore FunctionalityUser Management: Comprehensive user roles and permissions for healthcare workers.Patient Management: Complete patient lifecycle management with medical history.Health Facility Management: Facility operations, services, and resource management.Health Records: Comprehensive medical records with FHIR compliance.Analytics & Reporting: Health metrics, disease outbreak tracking, and performance analytics.API-First Design: RESTful API with OpenAPI/Swagger documentation.Technical FeaturesDjango 4.2+: Modern Django with best practices.PostgreSQL: Robust database with healthcare-optimized schemas.Redis: Caching and session management.Celery: Background task processing.Docker: Containerized deployment.JWT Authentication: Secure API authentication.Health Checks: System monitoring and diagnostics.ArchitectureOpenCare-Africa/
├── apps/                   # Django applications
│   ├── core/               # Core models and utilities
│   ├── patients/           # Patient management
│   ├── health_workers/     # Healthcare personnel management
│   ├── facilities/         # Health facility operations
│   ├── records/            # Medical records management
│   ├── analytics/          # Health analytics and reporting
│   └── api/                # API endpoints and viewsets
├── config/                 # Project configuration
│   ├── settings/           # Environment-specific settings
│   ├── urls.py             # Main URL configuration
│   └── celery.py           # Celery configuration
├── templates/              # HTML templates
├── static/                 # Static files
├── media/                  # User-uploaded files
├── docs/                   # Documentation
└── scripts/                # Database and deployment scripts
Quick StartPrerequisitesDocker & Docker Compose (recommended)Python 3.11+ (for local development without Docker)PostgreSQL 15+Redis 7+Docker Setup (Recommended)Clone the repositoryBashgit clone https://github.com/bos-com/OpenCare-Africa.git
cd OpenCare-Africa
Set up environment variablesBashcp env.example .env
Build and start all servicesBashdocker-compose build
docker-compose up -d
Run database migrationsBashdocker-compose exec web python manage.py migrate
Create superuserBashdocker-compose exec web python manage.py createsuperuser
Access the applicationWeb Interface: http://localhost:8000Admin Panel: http://localhost:8000/adminAPI Documentation: http://localhost:8000/api/docs/Health Check: http://localhost:8000/health/Viewing API DocsBrowse to http://localhost:8000/api/docs/ for interactive OpenAPI documentation.Review sanitized response expectations and logging rules in docs/error-handling.md before exposing new endpoints.Extend automated tests to cover both success and error scenarios when updating API behavior.Docker Services OverviewServicePortPurposeweb8000Django web applicationdb5432PostgreSQL databaseredis6379Redis cache and Celery brokercelery-Background task processorcelery-beat-Scheduled task schedulernginx80Reverse proxy (production)metabase3000Analytics dashboardsuperset8088Business intelligence platformLocal Development Setup (Alternative)Clone and Enter DirectoryBashgit clone https://github.com/bos-com/OpenCare-Africa.git
cd OpenCare-Africa
Set up Virtual EnvironmentBashpython3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
Install DependenciesBashpip install -r requirements.txt
pip install -r requirements-dev.txt # Optional
Database & MigrationsBashpython manage.py migrate
python manage.py createsuperuser
Run ServerBashpython manage.py runserver
Database SchemaCore ModelsUser: Extended model with healthcare worker profiles.Location: Hierarchical geographic location management.HealthFacility: Facility information and services.AuditTrail: Comprehensive audit logging for security.Records & HealthcareHealthRecord: Comprehensive medical records.VitalSigns: Patient measurements tracking.Medication: Prescription and medication management.LaboratoryTest: Lab results and interpretation.TestingBash# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
Deployment Checklist[ ] Set DEBUG=False[ ] Configure production database[ ] Set up SSL/TLS certificates[ ] Configure static file serving[ ] Set up Sentry for monitoring[ ] Configure backup strategiesContributingFork the repository.Create a feature branch.Add tests for new functionality.Ensure all tests pass.Submit a pull request.LicenseThis project is licensed under the MIT License - see the LICENSE file for details.