# API Testing Guide

This guide describes a practical baseline for testing OpenCare-Core APIs before opening a pull request.

## 1. Test Environments

- **Local development** (`python manage.py runserver`)
- **Docker stack** (`docker-compose up -d`)

Use whichever environment matches your contribution scope.

## 2. Pre-test Checklist

1. Dependencies are installed.
2. Migrations are up to date.
3. Required environment variables are present.
4. Application starts without traceback errors.

## 3. Baseline Verification Steps

### 3.1 Health and availability
- Verify service is reachable.
- Verify health endpoint response is expected.

### 3.2 Authentication flow
- Validate login/token endpoint behavior for:
  - valid credentials,
  - invalid credentials,
  - missing fields.

### 3.3 Core CRUD endpoints
For each modified module, test:
- Create
- Read/list
- Update/partial update
- Delete (or expected restriction behavior)

### 3.4 Error handling
Validate:
- proper status codes,
- sanitized error responses,
- no sensitive information leakage.

## 4. Recommended Command Examples

```bash
# Run unit/integration tests
python manage.py test

# Optional coverage run
coverage run --source='.' manage.py test
coverage report
```

## 5. PR Evidence Expectations

Include in your PR:
- test commands you ran,
- high-level results,
- any intentionally skipped tests and why.

This keeps reviews efficient and traceable.
