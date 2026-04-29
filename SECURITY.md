# Security Policy

OpenCare-Core handles healthcare workflows and may process sensitive operational
or patient-related information. Please report security concerns responsibly so
maintainers can investigate before details are shared publicly.

## Supported Versions

The `main` branch is the active development line and receives security fixes.
If release branches are introduced later, this section should be updated with a
version support table.

## Reporting a Vulnerability

Do not open a public GitHub issue for a suspected vulnerability.

Instead, contact the maintainers through the project support channel listed in
the README or use a private disclosure method provided by the repository owners.
Include as much detail as possible:

- Affected endpoint, module, or configuration.
- Steps to reproduce.
- Expected and actual behavior.
- Potential impact.
- Suggested mitigation, if known.

## Handling Expectations

Maintainers should acknowledge reports, assess severity, prepare a fix, and
publish remediation notes once users have a safe upgrade path.

## Security Review Areas

Contributors should pay special attention to:

- Authentication and authorization checks.
- Patient data access controls.
- Input validation and file uploads.
- Audit logging for sensitive data changes.
- Error responses that might expose private data.
- Environment variables and secret handling.
