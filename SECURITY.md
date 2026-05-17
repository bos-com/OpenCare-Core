# Security Policy

OpenCare-Core handles sensitive protected health information (PHI) for patients and healthcare workers across Africa. We take security vulnerabilities extremely seriously and appreciate responsible disclosure from the community.

---

##  Supported Versions

We actively maintain and release security patches for the following versions:

| Version | Supported |
|---------|-----------|
| Latest (main branch) | ✅ Actively supported |
| Previous release | ✅ Critical fixes only |
| Older versions | ❌ Not supported |

---

##  Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Public disclosure before a fix is available puts patients, healthcare workers, and facilities at risk.

### How to Report

Send your vulnerability report by email to:

 **kmuwanga@bugemauniv.ac.ug**

Please include the subject line: `[SECURITY] OpenCare-Core Vulnerability Report`

### What to Include in Your Report

To help us triage and fix the issue quickly, please provide:

1. **Description** — A clear description of the vulnerability
2. **Affected component** — Which module, endpoint, or feature is affected (e.g., `apps/patients`, `/api/v1/records/`)
3. **Steps to reproduce** — A minimal, reproducible example or proof-of-concept
4. **Impact assessment** — What data or functionality could be compromised
5. **Suggested fix** (optional) — If you have a proposed solution, we welcome it
6. **Your contact details** — So we can follow up with you

---

##  Response Timeline

| Stage | Timeframe |
|-------|-----------|
| Acknowledgement of report | Within 48 hours |
| Initial assessment | Within 5 business days |
| Fix development begins | Within 10 business days (critical) |
| Patch released | Within 30 days where possible |
| Public disclosure | After patch is released |

We will keep you informed at each stage. If you do not hear back within 48 hours, please follow up to ensure your report was received.

---

##  Scope

### In Scope

The following are within scope for vulnerability reports:

- Authentication and authorisation bypass (JWT, session handling, RBAC)
- Patient data exposure or PHI leakage through API endpoints
- SQL injection or other injection vulnerabilities
- Insecure direct object references (IDOR) allowing access to another user's records
- Sensitive data exposure in error messages or logs
- Broken access control on healthcare worker or facility management endpoints
- Server-side request forgery (SSRF)
- Cross-site scripting (XSS) in any frontend-facing components
- Insecure deserialization

### Out of Scope

The following are **not** considered valid vulnerability reports:

- Theoretical vulnerabilities without a proof of concept
- Issues requiring physical access to the server
- Social engineering attacks
- Denial of service (DoS) via intentional flooding
- Vulnerabilities in third-party dependencies that are already publicly disclosed and have no available fix
- Self-XSS or issues that require the victim to take unlikely actions

---

##  Healthcare Data Considerations

Because OpenCare-Core processes PHI (Protected Health Information), we treat any vulnerability that could expose patient data as **Critical Priority**, regardless of the technical CVSS score. This includes:

- Unauthorised access to patient records, medical history, or visit data
- Exposure of health worker identity linked to patient care
- Leakage of facility-level data that could identify specific patients

---

##  Recognition

We are grateful to security researchers who responsibly disclose vulnerabilities. With your permission, we will acknowledge your contribution in our release notes when the vulnerability is patched.

We do not currently offer a monetary bug bounty, but we deeply appreciate the effort and responsibility shown by ethical security researchers.

---

##  Additional Resources

- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute to the project
- [docs/audit-logs.md](docs/audit-logs.md) — PHI access tracking requirements
- [docs/patient-records.md](docs/patient-records.md) — Patient data handling guidelines
