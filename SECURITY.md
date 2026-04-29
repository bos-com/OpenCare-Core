# Security Policy

OpenCare-Core handles healthcare workflows, so security reports should be
treated with care even when the repository is still under active development.

## Reporting a Vulnerability

Do not open a public issue for suspected vulnerabilities, exposed credentials,
or patient-identifiable data. Instead, contact the maintainers privately through
the repository owner or the communication channel listed by the BOS-COM project.

Please include:

- A clear description of the vulnerability
- Steps to reproduce the issue
- Affected endpoints, models, settings, or deployment modes
- Any logs or screenshots with secrets and patient data removed
- Suggested mitigation, if known

## Handling Sensitive Data

- Do not commit real patient, staff, facility, credential, or token data.
- Use synthetic test fixtures for examples and automated tests.
- Redact request bodies, headers, cookies, and environment values before sharing
  logs in issues or pull requests.
- Keep error responses sanitized; see
  [`docs/error-handling.md`](docs/error-handling.md).

## Maintainer Triage

Maintainers should acknowledge private vulnerability reports, reproduce the
issue in a safe environment, prepare a focused fix, and publish remediation notes
after a patch is available.
