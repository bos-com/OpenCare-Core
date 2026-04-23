# Contributing to OpenCare-Africa

Thank you for your interest in contributing to OpenCare-Africa! We welcome contributions from developers, healthcare professionals, and anyone passionate about improving healthcare systems in Africa.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Security](#security)
- [Questions or Need Help?](#questions-or-need-help)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@opencare-africa.org](mailto:conduct@opencare-africa.org).

## How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Include detailed steps to reproduce the bug
- Provide environment information (OS, Python version, Django version)
- Include error logs and screenshots if applicable

### Suggesting Enhancements

- Use the GitHub issue tracker with the "enhancement" label
- Describe the problem and proposed solution
- Consider the impact on existing functionality
- Think about backward compatibility

### Code Contributions

- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test coverage improvements

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- PostgreSQL (for production-like development)
- Redis (for caching and Celery)

### Setup Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/OpenCare-Africa.git
   cd OpenCare-Africa
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the coding standards below
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Your Changes

Use conventional commit format:

```bash
git commit -m "feat: add patient search functionality"
git commit -m "fix: resolve authentication issue in API"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for patient model"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 4. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots for UI changes
- Test results

## Code Standards

### Python/Django Standards

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Django Best Practices

- Use Django ORM efficiently
- Implement proper model relationships
- Use Django forms and serializers
- Follow Django security best practices
- Implement proper error handling

### Code Quality Tools

We use several tools to maintain code quality:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .

# Run security checks with bandit
bandit -r .

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.patients

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Writing Tests

- Write tests for all new functionality
- Aim for at least 80% code coverage
- Use descriptive test names
- Test both success and failure cases
- Use factories for test data (factory-boy)

### Test Structure

```python
class PatientModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.patient = PatientFactory()
    
    def test_patient_creation(self):
        """Test that patient can be created."""
        self.assertIsNotNone(self.patient)
        self.assertEqual(self.patient.first_name, "John")
    
    def test_patient_full_name(self):
        """Test patient full name method."""
        expected = f"{self.patient.first_name} {self.patient.last_name}"
        self.assertEqual(self.patient.get_full_name(), expected)
```

## Documentation

### Code Documentation

- Write clear docstrings for all functions and classes
- Use Google or NumPy docstring format
- Include examples for complex functions
- Document parameters, return values, and exceptions

### API Documentation

- Update API documentation when endpoints change
- Include request/response examples
- Document authentication requirements
- Provide clear error messages

### User Documentation

- Update README.md for major changes
- Maintain setup and deployment guides
- Document configuration options
- Provide troubleshooting guides

## Security

### Security Guidelines

- Never commit sensitive information (API keys, passwords)
- Use environment variables for configuration
- Implement proper authentication and authorization
- Validate all user inputs
- Use HTTPS in production
- Follow OWASP security guidelines

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **DO NOT** create a public GitHub issue
2. Email security@opencare-africa.org
3. Include detailed information about the vulnerability
4. Allow time for the security team to respond

## Questions or Need Help?

### Getting Help

- Check existing documentation
- Search existing issues and discussions
- Join our community discussions
- Contact the development team

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: support@opencare-africa.org
- **Community Forum**: [forum.opencare-africa.org](https://forum.opencare-africa.org)

### Mentorship

New contributors are welcome! We offer:

- Code review and feedback
- Pair programming sessions
- Mentorship from experienced contributors
- Regular office hours for questions

## Recognition

Contributors will be recognized in:

- Project README
- Release notes
- Contributor hall of fame
- Annual contributor acknowledgments

## Thank You!

Your contributions help make healthcare better for millions of people across Africa. Every line of code, bug report, or documentation improvement makes a difference.

---

**Together, we can build a healthier future for Africa!** 🩺🌍
