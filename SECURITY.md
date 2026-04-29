# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: yes |

## Reporting a Vulnerability

If you discover a security vulnerability in OpenCare-Core, please **DO NOT** create a public GitHub issue. Instead, follow this responsible disclosure process:

### How to Report

1. **Email**: Send an email to security@opencare-africa.org
2. **Subject Line**: Use the format `[Security] Vulnerability Report - [Brief Description]`
3. **Include**:
   - Detailed description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Any proof-of-concept code or screenshots (if applicable)
   - Your contact information for follow-up

### What to Expect

- **Response Time**: We will acknowledge your report within 48 hours
- **Investigation**: We will investigate the vulnerability and determine its severity
- **Resolution**: We will work on a fix and coordinate a release timeline
- **Disclosure**: We will publicly disclose the vulnerability after a fix is released
- **Credit**: With your permission, we will credit you in the security advisory

### Security Best Practices for Contributors

When contributing to OpenCare-Core, please follow these security guidelines:

#### Code Security

- Never commit sensitive information (API keys, passwords, tokens)
- Use environment variables for configuration
- Implement proper input validation and sanitization
- Follow OWASP security guidelines
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Use HTTPS for all external communications
- Validate and sanitize all user inputs

#### Dependencies

- Keep dependencies up to date
- Review security advisories for dependencies
- Use tools like `pip-audit` or `safety` to check for vulnerable packages
- Document any security-related dependency changes

#### Testing

- Write security tests for authentication and authorization
- Test for common vulnerabilities (XSS, SQL injection, CSRF)
- Use security scanning tools in CI/CD pipeline
- Perform regular security audits

#### Healthcare Data Protection

- Follow HIPAA and local healthcare data protection regulations
- Implement proper encryption for sensitive data at rest and in transit
- Log all access to patient health information (PHI)
- Implement proper audit trails
- Follow FHIR security guidelines for healthcare data exchange

### Security Features in OpenCare-Core

OpenCare-Core includes several security features:

- **Authentication**: JWT-based authentication with secure token handling
- **Authorization**: Role-based access control (RBAC)
- **Audit Logging**: Comprehensive audit trails for PHI access
- **Data Encryption**: Encryption for sensitive data at rest and in transit
- **Input Validation**: Comprehensive input validation and sanitization
- **CORS Configuration**: Proper CORS configuration for API security
- **Rate Limiting**: Configurable rate limiting to prevent abuse
- **Security Headers**: Implementation of security best practice headers

### Common Security Considerations

#### Authentication & Authorization

- All API endpoints require proper authentication
- Role-based access control ensures users can only access authorized resources
- Session management follows security best practices
- Password policies enforce strong passwords

#### Data Protection

- Patient health information (PHI) is encrypted at rest
- All data in transit is encrypted using TLS/SSL
- Audit logs track all access to sensitive data
- Data retention policies comply with healthcare regulations

#### API Security

- API documentation includes authentication requirements
- Rate limiting prevents API abuse
- Input validation prevents injection attacks
- Proper error handling doesn't expose sensitive information

### Security Tools Used

We use several tools to maintain security:

- **pip-audit**: Checks for vulnerable dependencies
- **bandit**: Security linter for Python code
- **safety**: Checks for known security vulnerabilities
- **OWASP ZAP**: Web application security scanner
- **pytest**: Security-focused testing

### Incident Response

In the event of a security incident:

1. **Immediate Response**: Contain the incident and prevent further damage
2. **Investigation**: Determine the scope and impact of the incident
3. **Communication**: Notify affected stakeholders as required
4. **Remediation**: Fix vulnerabilities and prevent recurrence
5. **Documentation**: Document the incident and lessons learned

### Compliance

OpenCare-Core is designed to comply with:

- **HIPAA**: Health Insurance Portability and Accountability Act
- **GDPR**: General Data Protection Regulation (where applicable)
- **Local Regulations**: African healthcare data protection laws
- **FHIR Security**: Fast Healthcare Interoperability Resources security standards

### Contact Information

For security-related inquiries:

- **Security Issues**: security@opencare-africa.org
- **General Security Questions**: support@opencare-africa.org
- **Emergency Security Contact**: [Available to registered security researchers]

### Acknowledgments

We thank all security researchers who responsibly disclose vulnerabilities to help make OpenCare-Core more secure.

---

**Last Updated**: April 22, 2026

**Version**: 1.0.0
