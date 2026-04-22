# Development Setup Guide

This guide provides detailed instructions for setting up a local development environment for OpenCare-Core.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.11+**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads)
- **PostgreSQL 15+**: Download from [postgresql.org](https://www.postgresql.org/download/)
- **Redis 7+**: Download from [redis.io](https://redis.io/download)
- **Docker & Docker Compose** (optional but recommended): Download from [docker.com](https://www.docker.com/products/docker-desktop)

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/bos-com/OpenCare-Core.git
cd OpenCare-Core
```

## Step 2: Set Up Virtual Environment

A virtual environment isolates your project dependencies from your system Python.

### Creating the Virtual Environment

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv
```

### Activating the Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

### Verifying Virtual Environment

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

```bash
# Check Python version
python --version  # Should show Python 3.11+

# Check pip version
pip --version
```

## Step 3: Upgrade pip and Install Dependencies

```bash
# Upgrade pip to the latest version
pip install --upgrade pip

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (includes testing tools)
pip install -r requirements-dev.txt
```

### Understanding the Dependencies

**Production Dependencies (requirements.txt):**
- Django 4.2.7 - Web framework
- Django REST Framework - API toolkit
- PostgreSQL adapter - Database connectivity
- Redis client - Caching and task queue
- JWT libraries - Authentication
- FHIR/HL7 libraries - Healthcare data standards

**Development Dependencies (requirements-dev.txt):**
- pytest - Testing framework
- pytest-django - Django testing integration
- pytest-cov - Code coverage
- black - Code formatter
- flake8 - Code linter
- isort - Import sorter
- factory-boy - Test data generation

## Step 4: Configure Environment Variables

```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file with your preferred editor
nano .env  # or vim .env, or code .env
```

### Required Environment Variables

Edit `.env` and configure the following:

```bash
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here-generate-a-secure-random-string
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=opencare_africa
DB_USER=opencare_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-different-from-django-secret
JWT_ACCESS_TOKEN_LIFETIME=5  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1  # days
```

### Generating Secure Keys

For production, generate secure random keys:

```bash
# Generate Django SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Generate JWT secret
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

## Step 5: Set Up PostgreSQL Database

### Create Database and User

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE opencare_africa;
CREATE USER opencare_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE opencare_africa TO opencare_user;
\q
```

### Alternative: Using Docker for Database

If you prefer using Docker for the database:

```bash
# Start PostgreSQL container
docker run --name opencare-postgres \
  -e POSTGRES_DB=opencare_africa \
  -e POSTGRES_USER=opencare_user \
  -e POSTGRES_PASSWORD=your-secure-password \
  -p 5432:5432 \
  -d postgres:15

# Update .env with DB_HOST=localhost
```

## Step 6: Set Up Redis

### Install and Start Redis

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**On macOS (with Homebrew):**
```bash
brew install redis
brew services start redis
```

**On Windows:**
Download Redis for Windows from [GitHub releases](https://github.com/microsoftarchive/redis/releases)

### Verify Redis is Running

```bash
# Test Redis connection
redis-cli ping
# Should return: PONG
```

### Alternative: Using Docker for Redis

```bash
# Start Redis container
docker run --name opencare-redis -p 6379:6379 -d redis:7
```

## Step 7: Run Database Migrations

Migrations create the database schema based on your Django models.

```bash
# Show all migrations (helpful for understanding what will be applied)
python manage.py showmigrations

# Apply all migrations
python manage.py migrate

# Verify migrations were applied successfully
python manage.py showmigrations
```

### Understanding Migrations

Migrations are Django's way of propagating changes you make to your models into your database schema.

- **showmigrations**: Lists all migrations and their status
- **migrate**: Applies pending migrations
- **makemigrations**: Creates new migrations based on model changes

### Common Migration Issues

**If you encounter migration errors:**

```bash
# Check for conflicting migrations
python manage.py showmigrations

# Fake initial migration if needed
python manage.py migrate --fake-initial

# Reset database (WARNING: This deletes all data!)
python manage.py flush
```

## Step 8: Create Superuser Account

Create an admin account to access the Django admin panel.

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email address
- Password (entered twice)

## Step 9: Run Development Server

Start the Django development server.

```bash
# Start the development server
python manage.py runserver

# Or specify a different port
python manage.py runserver 8001
```

The server will start at `http://127.0.0.1:8000/`

### Accessing the Application

- **Web Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **Health Check**: http://127.0.0.1:8000/health/

## Step 10: Run Tests

Verify everything is working by running the test suite.

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report in htmlcov/

# Run specific app tests
python manage.py test apps.patients
python manage.py test apps.core

# Run specific test
python manage.py test apps.patients.tests.test_models
```

### Understanding Test Output

- **OK**: All tests passed
- **FAILED**: One or more tests failed
- **ERROR**: Test setup/teardown failed
- **Coverage report**: Shows percentage of code covered by tests

## Step 11: Code Quality Checks

Run code quality tools to ensure your code meets project standards.

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .

# Run all checks together
black . && isort . && flake8 .
```

## Step 12: Load Sample Data (Optional)

Load sample data for development and testing.

```bash
# Load sample data fixtures
python manage.py loaddata sample_data.json

# Or use Django's built-in data loading
python manage.py shell
# Then in the shell:
from apps.patients.models import Patient
# Create sample patients...
```

## Common Development Tasks

### Creating a New Django App

```bash
python manage.py startapp new_app_name
```

### Creating Database Migrations

```bash
# After modifying models
python manage.py makemigrations
python manage.py migrate
```

### Using Django Shell

```bash
# Interactive Python shell with Django environment loaded
python manage.py shell

# Or with IPython (if installed)
python manage.py shell_plus
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: Virtual environment not activating
```bash
# Solution: Ensure you're in the correct directory
cd OpenCare-Core
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

**Problem**: Wrong Python version
```bash
# Solution: Check Python version
python --version
# If not 3.11+, install correct version and recreate venv
```

### Database Issues

**Problem**: Cannot connect to database
```bash
# Solution: Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l

# Check connection settings in .env
cat .env | grep DB_
```

**Problem**: Migration errors
```bash
# Solution: Check migration status
python manage.py showmigrations

# Reset migrations (WARNING: Deletes data!)
python manage.py migrate --fake zero
python manage.py migrate
```

### Redis Issues

**Problem**: Cannot connect to Redis
```bash
# Solution: Check Redis is running
redis-cli ping

# Check Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

### Dependency Issues

**Problem**: Package installation fails
```bash
# Solution: Upgrade pip and retry
pip install --upgrade pip
pip install -r requirements.txt

# If specific package fails, try installing separately
pip install package-name
```

### Port Already in Use

**Problem**: Port 8000 already in use
```bash
# Solution: Use different port
python manage.py runserver 8001

# Or kill process using port 8000
lsof -ti:8000 | xargs kill -9  # Linux/macOS
netstat -ano | findstr :8000  # Windows
```

## Development Workflow

### Typical Development Cycle

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes to code**

3. **Run tests**
   ```bash
   python manage.py test
   ```

4. **Run code quality checks**
   ```bash
   black . && isort . && flake8 .
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Useful Git Commands

```bash
# View current branch
git branch

# View changes
git status
git diff

# Stash changes
git stash
git stash pop

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View commit history
git log --oneline
```

## Next Steps

- Read the [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Explore the [API documentation](http://127.0.0.1:8000/api/docs/)
- Check the [docs/](docs/) directory for additional documentation
- Join the community discussions on GitHub

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting section](#troubleshooting) in README.md
2. Search existing [GitHub Issues](https://github.com/bos-com/OpenCare-Core/issues)
3. Ask questions in [GitHub Discussions](https://github.com/bos-com/OpenCare-Core/discussions)
4. Contact the development team

---

**Happy Coding!** 🚀
