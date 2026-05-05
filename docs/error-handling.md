# Error Handling Guidelines

OpenCare-Africa must protect sensitive health information at every layer.
These guidelines describe how to return helpful but safe API responses,
capture actionable diagnostics via logging, and verify everything with tests.

## Sanitized Error Responses

- **Prefer structured payloads**: Use Django REST Framework's `Response` with a
  consistent schema (`code`, `message`, `errors`). Include only the context
  clients need to proceed; never echo raw exception strings or database fields.
- **Centralized handler**: The custom exception handler at
  `apps.api.exceptions.sanitized_exception_handler` enforces the standard shape
  and replaces 5xx messages with a generic placeholder.
- **Remove sensitive values**: Strip patient identifiers, authentication
  tokens, secrets, and raw query parameters from direct responses. When the
  original error contains sensitive values, replace them with neutral language
  (for example, `"message": "Unable to process request"`).
- **Map internal errors**: Convert uncaught exceptions to `HTTP_500_INTERNAL_SERVER_ERROR`
  with a generic message. Record the exception details in logs instead of the
  response body.
- **Validation errors**: Provide field-level messages while ensuring protected
  data (e.g., partial SSNs, lab results) is masked or omitted.

## Logging Policy

- **Log at the boundary**: Capture errors in Django middleware, DRF exception
  handlers, Celery tasks, and management commands. Use structured logging where
  possible to enable filtering and redaction.
- **Separate concerns**: Application logs may contain sensitive context, so
  restrict access to trusted operators. Route audit events to the configured
  secure sink (e.g., STDOUT in production for centralized collection).
- **Redact secrets**: Before logging request data, remove passwords, tokens,
  patient identifiers, and any HIPAA-protected information. Prefer
  `extra={"user_id": user.pk}` over embedding full objects.
- **Include correlation IDs**: Attach `request.id` or another correlation value
  to logs to help trace issues without exposing raw inputs.
- **Avoid duplicate noise**: Log exceptions once at the highest useful level to
  prevent flooding alerting systems.

## Tests and Verification

- **Unit tests**: For custom exception handlers, assert that sensitive fields do
  not appear in serialized responses and that HTTP status codes match the
  contract.
- **Integration tests**: Use API tests to trigger representative errors (e.g.,
  invalid payloads, missing authentication) and validate that responses are
  sanitized JSON structures.
- **Logging assertions**: When feasible, patch loggers to confirm redaction
  logic strips secrets before log emission.
- **Security review**: Include error-handling verification in release and
  incident postmortem checklists to prevent regressions.

Following these practices keeps patient data secure while giving clients enough
information to recover from errors and operators the diagnostics required to fix
the underlying issues.
