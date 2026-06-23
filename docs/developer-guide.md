# Contributing to OpenCare-Core

Thank you for your interest in contributing to OpenCare-Africa — a healthcare informatics platform built to empower health systems across Africa. We welcome contributions of all kinds: bug fixes, new features, documentation, and tests.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Git Workflow](#git-workflow)
- [Coding Standards](#coding-standards)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)

---

## 🤝 Code of Conduct

This project is maintained by the Bugema Open Source Community (BOSC). We are committed to providing a welcoming and respectful environment for all contributors. Please be kind, constructive, and inclusive in all interactions.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- PostgreSQL 15+ (included in Docker setup)
- Redis 7+ (included in Docker setup)
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/<your-username>/OpenCare-Core.git
cd OpenCare-Core
```

3. Add the upstream remote:

```bash
git remote add upstream https://github.com/bos-com/OpenCare-Core.git
```

---

## 🛠️ Development Setup

### Option A: Docker (Recommended)

```bash
# Copy environment variables
cp env.example .env

# Build and start all services
docker-compose build
docker-compose up -d

# Run database migrations
docker-compose exec web python manage.py migrate

# Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

Access the app at: `http://localhost:8000`
API docs at: `http://localhost:8000/api/docs/`

### Option B: Local Development

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy and configure environment
cp env.example .env

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

---

## 🔄 Git Workflow

We use a feature-branch workflow. Please follow these steps:

1. **Sync your fork** before starting:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

2. **Create a feature branch**:

```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/issue-description
# or for documentation:
git checkout -b docs/what-you-are-documenting
```

3. **Make your changes**, commit regularly with clear messages:

```bash
git add .
git commit -m "feat: add patient search endpoint with filters"
```

4. **Push to your fork**:

```bash
git push origin feature/your-feature-name
```

5. **Open a Pull Request** from your fork to `bos-com/OpenCare-Core` main.

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use for |
|--------|---------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `refactor:` | Code restructuring |
| `chore:` | Maintenance tasks |

---

## 📐 Coding Standards

### Python / Django

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use meaningful variable and function names
- Write docstrings for all classes and public methods
- Keep functions focused and small
- Use Django's ORM — avoid raw SQL unless necessary

### Project Architecture

Contributions must follow the layered architecture:
- Business logic goes in `services.py` per app
- Database access goes in `repositories.py` or via Django ORM in services
- API serialization goes in `serializers.py`
- URL routing goes in `urls.py`

### Healthcare Data Sensitivity

OpenCare-Core handles protected health information (PHI). All contributors must:

- Never log or expose patient identifiable data in error messages
- Ensure all new patient-related endpoints require authentication
- Follow the audit logging conventions described in `docs/audit-logs.md`
- Review `docs/patient-records.md` before touching patient data endpoints

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
coverage html

# Run tests for a specific app
python manage.py test apps.patients
```

All pull requests must maintain or improve test coverage. New features require new tests.

---

## 📬 Submitting a Pull Request

Before submitting, please ensure:

- [ ] Your branch is up to date with `upstream/main`
- [ ] All tests pass: `python manage.py test`
- [ ] Code follows PEP 8 standards
- [ ] You have added tests for new functionality
- [ ] Documentation is updated if behaviour changed
- [ ] Your PR description references the issue it closes (e.g., `Closes #39`)

### PR Description Template
---

## 🐛 Reporting Issues

Found a bug? Have a feature request? Please open an issue at:
https://github.com/bos-com/OpenCare-Core/issues

For **security vulnerabilities**, please read our [SECURITY.md](SECURITY.md) and do **not** open a public issue.

---

## 🙏 Thank You

Every contribution matters — whether it's fixing a typo, improving docs, or building a new feature. We appreciate your time and effort in making OpenCare-Africa better for healthcare workers and patients across the continent.
