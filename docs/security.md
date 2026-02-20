---
layout: default
title: Security Policy
---

# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this repository, please report it to us privately.

**Please do not report security vulnerabilities through public GitHub issues.**

### Reporting Process

1. **Email**: Send details to the repository maintainers (check the repository for contact information)
2. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Assessment**: We'll assess the vulnerability and determine severity
- **Fix**: We'll work on a fix and coordinate disclosure timing with you
- **Credit**: We'll credit you in the security advisory (unless you prefer anonymity)

## Supported Versions

We support security updates for the latest version of the main branch.

## Security Best Practices

This repository follows security best practices including:

- **Dependency Scanning**: Automated with Dependabot
- **Secret Scanning**: Automated detection of accidentally committed secrets
- **Code Scanning**: CodeQL analysis for vulnerability detection
- **Workflow Security**: Minimal permissions and script injection prevention

For detailed security guidelines, see:
- [Security Best Practices](../SECURITY_BEST_PRACTICES.md)
- [Workflow Security](../WORKFLOW_SECURITY.md)
- [Branch Protection](../BRANCH_PROTECTION.md)

## Security Tools Used

- **CodeQL**: Static code analysis
- **Dependabot**: Automated dependency updates
- **Secret Scanning**: Credential leak detection
- **Branch Protection**: Required reviews and status checks

## Responsible Disclosure

We follow responsible disclosure practices:

1. Report received and acknowledged
2. Vulnerability assessed and validated
3. Fix developed and tested
4. Security advisory published
5. Credits given to reporter

Thank you for helping keep our repository secure!
