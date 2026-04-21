# Security Policy

Thank you for helping keep OpenCare-Core secure.

## Supported Security Scope

Security reports are welcome for:
- authentication and authorization flaws,
- sensitive data exposure,
- insecure defaults or configuration,
- dependency vulnerabilities,
- API endpoint abuse paths.

## Reporting a Vulnerability

Please do **not** open public issues for sensitive vulnerabilities.

Instead:
1. Email project maintainers with a clear report.
2. Include:
   - affected component,
   - reproduction steps,
   - impact assessment,
   - suggested remediation (if known).

## Response Expectations

Maintainers should aim to:
- acknowledge receipt promptly,
- triage severity,
- coordinate remediation,
- publish a fix and advisory when appropriate.

## Disclosure Guidelines

- Practice responsible disclosure.
- Allow maintainers reasonable time to patch before public disclosure.
- Avoid sharing exploit details publicly until remediation is available.

## Contributor Security Rules

- Never commit real secrets (keys, passwords, tokens).
- Use environment templates (`env.example`, `.env.example`) for examples.
- Prefer least-privilege defaults in config and code.
