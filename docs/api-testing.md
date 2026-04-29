# API Testing Guide

This guide describes how contributors should test OpenCare-Core API changes
before opening a pull request.

## Test Scope

API changes should include tests for:

- Successful requests with valid input.
- Validation failures for missing or malformed input.
- Permission failures for unauthorized or underprivileged users.
- Error responses that should be sanitized.
- Pagination, filtering, and ordering where supported.

## Running Tests

Install development dependencies, then run the API test suite:

```bash
pip install -r requirements-dev.txt
pytest apps/api/tests
```

To run a focused test file:

```bash
pytest apps/api/tests/test_health_records_api.py
```

## Writing API Tests

When adding or updating endpoints:

1. Create test data with factories, fixtures, or explicit model setup.
2. Authenticate as the minimum role needed for the request.
3. Assert the HTTP status code.
4. Assert the response body shape and important fields.
5. Add negative tests for authorization and validation behavior.

## Error Handling Checks

API tests should confirm that client-facing errors are useful without exposing
private implementation details. For behavior expectations, review
[`docs/error-handling.md`](error-handling.md).

## Pull Request Checklist

Before submitting an API pull request:

- Run the relevant API tests.
- Add or update tests for changed behavior.
- Confirm API documentation or serializers match the response.
- Note any tests that could not be run and why.
