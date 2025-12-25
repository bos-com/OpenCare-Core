# OpenCare-Africa

A comprehensive health informatics platform backend built with Django, designed specifically for healthcare management in Africa.

## 🏥 Project Overview

OpenCare-Africa is a robust, scalable backend system for managing healthcare operations, patient records, health worker management, and health facility operations. The system is built with modern Django practices and includes comprehensive API endpoints for integration with frontend applications.

## ✨ Features

### Core Functionality
- **User Management**: Comprehensive user roles and permissions for healthcare workers
- **Patient Management**: Complete patient lifecycle management with medical history
- **Health Facility Management**: Facility operations, services, and resource management
- **Health Records**: Comprehensive medical records with FHIR compliance
- **Analytics & Reporting**: Health metrics, disease outbreak tracking, and performance analytics
- **API-First Design**: RESTful API with OpenAPI/Swagger documentation

### Technical Features
- **Django 4.2+**: Modern Django with best practices
- **PostgreSQL**: Robust database with healthcare-optimized schemas
- **Redis**: Caching and session management
- **Celery**: Background task processing
- **Docker**: Containerized deployment
- **JWT Authentication**: Secure API authentication
- **Health Checks**: System monitoring and diagnostics

## 🏗️ Architecture

```
OpenCare-Africa/
├── apps/                    # Django applications
│   ├── core/               # Core models and utilities
│   ├── patients/           # Patient management
│   ├── health_workers/     # Healthcare personnel management
│   ├── facilities/         # Health facility operations
│   ├── records/            # Medical records management
│   ├── analytics/          # Health analytics and reporting
│   └── api/                # API endpoints and viewsets
├── config/                 # Project configuration
│   ├── settings/           # Environment-specific settings
│   ├── urls.py            # Main URL configuration
│   └── celery.py          # Celery configuration
├── templates/              # HTML templates
├── static/                 # Static files
├── media/                  # User-uploaded files
├── docs/                   # Documentation
└── scripts/                # Database and deployment scripts
```

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended for all environments)
- Python 3.11+ (only needed for local development without Docker)
- PostgreSQL 15+ (included in Docker setup)
- Redis 7+ (included in Docker setup)

### 🐳 Docker Setup (Recommended)

This is the **recommended** way to run OpenCare-Africa as it ensures consistency across all environments.

1. **Clone the repository**
   ```bash
   git clone https://github.com/bos-com/OpenCare-Africa.git
   cd OpenCare-Africa
   ```

2. **Set up environment variables**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # The .env file is already configured for Docker
   # No changes needed unless you want to customize settings
   ```

3. **Build and start all services**
   ```bash
   # Build Docker images
   docker-compose build
   
   # Start all services (database, Redis, web app, Celery)
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Verify the installation**
   ```bash
   # Check service status
   docker-compose ps
   
   # Test the health endpoint
   curl http://localhost:8000/health/
   
   # Test the web interface
   open http://localhost:8000/
   ```

7. **Access the application**
   - **Web Interface**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin
   - **API Documentation**: http://localhost:8000/api/docs/
   - **Health Check**: http://localhost:8000/health/

## 📘 Viewing API Docs

- Start the stack via Docker or local development, then browse to http://localhost:8000/api/docs/ for interactive OpenAPI documentation.
- Review sanitized response expectations and logging rules in [`docs/error-handling.md`](docs/error-handling.md) before exposing new endpoints.
- Extend automated tests to cover both happy-path and error scenarios when updating API behavior; see the error-handling guide for recommendations.

### 🐳 Docker Services Overview

The Docker setup includes the following services:

| Service | Port | Purpose |
|---------|------|---------|
| **web** | 8000 | Django web application |
| **db** | 5432 | PostgreSQL database |
| **redis** | 6379 | Redis cache and Celery broker |
| **celery** | - | Background task processor |
| **celery-beat** | - | Scheduled task scheduler |
| **nginx** | 80 | Reverse proxy (production) |
| **metabase** | 3000 | Analytics dashboard |
| **superset** | 8088 | Business intelligence platform |

### 🚀 Quick Docker Commands

```bash
# Start all services
docker-compose up -d

# View service status
docker-compose ps

# View logs
docker-compose logs -f web

# Stop all services
docker-compose down

# Restart a specific service
docker-compose restart web

# Execute Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
```

### 🛠️ Local Development Setup (Alternative)

If you prefer to run the application locally without Docker:

1. **Clone the repository**
   ```bash
   git clone https://github.com/bos-com/OpenCare-Africa.git
   cd OpenCare-Africa
   ```

2. **Set up Python virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Upgrade pip
   pip install --upgrade pip
   ```

3. **Set up environment variables**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Update .env for local development
   # Change DB_HOST=localhost and REDIS_HOST=localhost
   ```

4. **Install dependencies**
   ```bash
   # Install production dependencies
   pip install -r requirements.txt
   
   # Install development dependencies (optional)
   pip install -r requirements-dev.txt
   ```

5. **Set up the database**
   ```bash
   # For development, SQLite is used by default
   # No additional database setup required
   
   # Run migrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Verify the installation**
   ```bash
   # Test the API health endpoint
   curl http://localhost:8000/health/
   
   # Test the web interface
   open http://localhost:8000/
   ```

## 📊 API Documentation

The API is fully documented using OpenAPI/Swagger:

- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

### Key API Endpoints

- **Authentication**: `/api/v1/auth/`
- **Patients**: `/api/v1/patients/`
- **Health Workers**: `/api/v1/health-workers/`
- **Facilities**: `/api/v1/facilities/`
- **Health Records**: `/api/v1/records/`
- **Analytics**: `/api/v1/analytics/`
- **Appointments**: `/api/v1/appointments/`

## 🗄️ Database Schema

### Core Models
- **User**: Extended user model with healthcare worker profiles
- **Location**: Hierarchical geographic location management
- **HealthFacility**: Health facility information and services
- **AuditTrail**: Comprehensive audit logging

### Patient Models
- **Patient**: Complete patient information and demographics
- **PatientVisit**: Patient visit tracking and scheduling
- **PatientMedicalHistory**: Medical history and conditions

### Healthcare Models
- **HealthWorkerProfile**: Extended healthcare worker profiles
- **ProfessionalQualification**: Qualifications and certifications
- **WorkSchedule**: Work schedules and availability
- **PerformanceEvaluation**: Performance tracking and reviews

### Facility Models
- **FacilityService**: Services offered by health facilities
- **FacilityStaff**: Staff management and assignments
- **FacilityEquipment**: Medical equipment tracking
- **FacilityInventory**: Medical supplies and inventory

### Records Models
- **HealthRecord**: Comprehensive medical records
- **VitalSigns**: Patient vital signs and measurements
- **Medication**: Prescription and medication management
- **LaboratoryTest**: Lab test results and interpretation
- **ImagingStudy**: Medical imaging results

### Analytics Models
- **HealthMetrics**: Health KPIs and metrics
- **DiseaseOutbreak**: Disease outbreak tracking
- **HealthReport**: Automated health reports
- **PatientAnalytics**: Patient-specific analytics

## 🔧 Configuration

### Environment Variables

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=opencare_africa
DB_USER=opencare_user
DB_PASSWORD=opencare_password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

### Settings Files

- `config/settings/base.py`: Base configuration
- `config/settings/development.py`: Development environment
- `config/settings/production.py`: Production environment
- `config/settings/test.py`: Testing environment

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run specific app tests
python manage.py test apps.patients
python manage.py test apps.core
```

## 📈 Performance & Monitoring

### Health Checks
- Database connectivity
- Redis connectivity
- Storage availability
- System resources

### Monitoring
- Django Debug Toolbar (development)
- Sentry integration (production)
- Custom health metrics
- Performance analytics

### Caching
- Redis-based caching
- Database query optimization
- Static file caching
- API response caching

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up SSL/TLS certificates
- [ ] Configure static file serving
- [ ] Set up monitoring and logging
- [ ] Configure backup strategies
- [ ] Set up CI/CD pipelines

### Docker Production
```bash
# Build production image
docker build -t opencare-africa:latest .

# Run with production settings
docker run -e DJANGO_SETTINGS_MODULE=config.settings.production opencare-africa:latest
```

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Comprehensive audit logging
- Input validation and sanitization
- CORS configuration
- Rate limiting (configurable)
- Secure password policies

## 📚 Documentation

- **API Documentation**: Built-in Swagger/OpenAPI docs
- **Code Documentation**: Comprehensive docstrings
- **Admin Interface**: Django admin for data management
- **User Guides**: Available in `/docs/` directory
- **Patient Records**: See [`docs/patient-records.md`](docs/patient-records.md) for CRUD usage and security notes
- **Audit Logging**: See [`docs/audit-logs.md`](docs/audit-logs.md) for PHI access tracking requirements
- **Appointments**: See [`docs/appointments.md`](docs/appointments.md) for scheduling API usage and safeguards

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Include tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Troubleshooting

### Docker-Specific Issues

#### 1. Docker Build Failures
**Issue**: `docker-compose build` fails with errors
**Solution**: 
```bash
# Clean up Docker cache and rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache

# Check Docker logs for specific errors
docker-compose logs web
```

#### 2. Port Conflicts
**Issue**: `Port is already allocated` or `Address already in use`
**Solution**: 
```bash
# Check what's using the port
sudo netstat -tulpn | grep :8000

# Stop conflicting services or change ports in docker-compose.yml
docker-compose down
# Edit docker-compose.yml to use different ports
docker-compose up -d
```

#### 3. Database Connection Issues
**Issue**: `django.db.utils.OperationalError: could not connect to server`
**Solution**:
```bash
# Ensure database service is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database service
docker-compose restart db

# Wait for database to be ready, then run migrations
sleep 10
docker-compose exec web python manage.py migrate
```

#### 4. Redis Connection Issues
**Issue**: `redis.exceptions.ConnectionError` in Docker
**Solution**:
```bash
# Check Redis service status
docker-compose ps redis

# Restart Redis service
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

#### 5. Permission Issues
**Issue**: `Permission denied` errors in Docker containers
**Solution**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### 6. Memory Issues
**Issue**: Docker containers running out of memory
**Solution**:
```bash
# Check Docker resource usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Or add memory limits to docker-compose.yml
```

#### 7. Volume Mount Issues
**Issue**: Changes not reflecting in containers
**Solution**:
```bash
# Restart services to pick up volume changes
docker-compose restart web

# Or rebuild if needed
docker-compose down
docker-compose up -d --build
```

### Docker Commands Reference

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs web
docker-compose logs db
docker-compose logs redis

# Execute commands in containers
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Check service status
docker-compose ps

# Rebuild specific service
docker-compose build web
docker-compose up -d web

# Clean up everything
docker-compose down -v
docker system prune -f
```

### Common Issues

#### 1. Python Version Compatibility
**Issue**: `ModuleNotFoundError` or package installation failures
**Solution**: Ensure you're using Python 3.11+ and have created a virtual environment
```bash
python3 --version  # Should be 3.11+
python3 -m venv venv
source venv/bin/activate
```

#### 2. Database Migration Errors
**Issue**: `django.db.utils.OperationalError` or migration failures
**Solution**: Ensure the database is properly configured and migrations are up to date
```bash
python manage.py showmigrations
python manage.py migrate
```

#### 3. Missing Dependencies
**Issue**: `ModuleNotFoundError` for specific packages
**Solution**: Reinstall dependencies and ensure all requirements are met
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Port Already in Use
**Issue**: `Address already in use` error when starting the server
**Solution**: Use a different port or kill the existing process
```bash
python manage.py runserver 8001
# OR
pkill -f "python manage.py runserver"
```

#### 5. Static Files Warning
**Issue**: `staticfiles.W004` warning about missing static directory
**Solution**: Create the static directory (this is normal for development)
```bash
mkdir -p static
```

#### 6. Redis Connection Errors
**Issue**: `redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379`
**Solution**: Redis is not required for basic development. The health check has been configured to skip Redis checks in development mode. If you need Redis for production features, install and start it:
```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server

# macOS (with Homebrew)
brew install redis
brew services start redis
```

#### 7. Environment Variables
**Issue**: Configuration errors or missing environment variables
**Solution**: Ensure `.env` file exists and contains required variables
```bash
cp env.example .env
# Edit .env if needed for your environment
```

### Development Tips

1. **Use the development settings**: The project uses `config.settings.development` by default
2. **Check logs**: Look at the console output for detailed error messages
3. **Database**: SQLite is used by default for development (no setup required)
4. **API Testing**: Use the built-in API documentation at `/api/docs/`
5. **Admin Interface**: Access at `/admin/` after creating a superuser

### Getting Help

- **Documentation**: Check the `/docs/` directory
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the development team

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core backend infrastructure
- ✅ Patient management system
- ✅ Health worker management
- ✅ Facility management
- ✅ Basic API endpoints

### Phase 2 (Next)
- 🔄 Advanced analytics dashboard
- 🔄 Mobile API optimization
- 🔄 Integration with external systems
- 🔄 Advanced reporting features

### Phase 3 (Future)
- 📋 AI-powered health insights
- 📋 Telemedicine integration
- 📋 Advanced data visualization
- 📋 Multi-language support

## 🙏 Acknowledgments

- Django community for the excellent framework
- Healthcare professionals for domain expertise
- Open source contributors for various packages
- African healthcare workers for inspiration

---

**OpenCare-Africa** - Empowering healthcare in Africa through technology.
