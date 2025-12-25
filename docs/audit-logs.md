# Audit Logs for Health Data Access

OpenCare-Africa maintains a complete, tamper-evident record of access to
protected health information (PHI). Use this guide when designing new features,
reviewing incidents, or validating regulatory compliance.

## What to Capture

- **Who**: Record the authenticated user or service account ID. For anonymous
  requests, capture the device fingerprint or session identifier.
- **What**: Log the model, primary key, and action (`read`, `update`, `delete`,
  `export`, etc.). Avoid storing entire payloads; reference summarized fields
  or hashes when necessary.
- **When**: Use timezone-aware UTC timestamps with millisecond precision.
- **Where**: Persist the source IP and, when available, facility or device
  metadata to support forensic traces.
- **Why**: Include a concise justification (e.g., care team access, billing
  reconciliation) supplied by workflows that require explicit reasons.

## Storage and Retention

- **Immutable store**: Append entries to the dedicated audit trail tables. Do
  not allow in-place updates; use write-once semantics with versioning.
- **Retention**: Retain PHI access logs for the regulatory minimum (typically
  6+ years) or longer if policy requires. Provide scripts to export archives to
  long-term storage.
- **Integrity**: Sign batches or use database-level checksum columns to detect
  tampering. Prefer cryptographically verifiable chains for high-assurance
  deployments.

## Access Controls

- **Restricted visibility**: Grant read access only to compliance officers and
  authorized auditors. Application users must not see audit entries unless the
  feature explicitly supports it (e.g., patient access reports).
- **Least privilege**: segregate audit writers from readers; the application
  process writes entries, while reporting jobs run with read-only credentials.
- **Alerting**: Integrate with SIEM tooling to trigger alerts on suspicious
  patterns, such as repeated failed access or off-hours bulk exports.

## Testing and Validation

- **Unit tests**: Assert that high-risk endpoints emit audit entries with the
  correct actor, action, and object identifiers.
- **Integration tests**: Simulate representative API flows (patient lookups,
  record edits, data exports) and confirm the audit trail captures them without
  exposing PHI content.
- **Performance checks**: Verify that logging does not materially degrade
  request latency. Use asynchronous tasks or buffered writes when necessary.
- **Compliance review**: Include audit log coverage in release checklists and
  periodic HIPAA/GDPR assessments.

## Reviewing Logs

- Administrative users can access the read-only endpoint at `/api/v1/audit-logs/`
  to review and filter audit events.
- Use query parameters such as `?model_name=patients.Patient` or `?action=view`
  to narrow down entries when investigating incidents.

Following these practices ensures every access to PHI is discoverable, auditable,
and compliant with healthcare regulations.
