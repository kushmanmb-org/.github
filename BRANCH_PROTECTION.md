# Branch Protection and Repository Security Configuration

This document outlines recommended branch protection rules and repository security settings to implement safe practices for security and privacy.

## Recommended Branch Protection Rules

### For `main` branch

Configure the following protections in GitHub repository settings:

#### Require Pull Request Reviews
- **Require pull request reviews before merging**: ✅ Enabled
  - Required number of approvals: **2** (for critical repositories)
  - Dismiss stale pull request approvals when new commits are pushed: ✅ Enabled
  - Require review from Code Owners: ✅ Enabled
  - Require approval of the most recent reviewable push: ✅ Enabled

#### Require Status Checks
- **Require status checks to pass before merging**: ✅ Enabled
  - Require branches to be up to date before merging: ✅ Enabled
  - Required status checks:
    - `CodeQL` - Security analysis
    - `Secret Scanning` - Detect hardcoded secrets
    - `Validation / Validate Python` - Code quality
    - `Validation / Validate JSON` - Configuration validation
    - `Validation / Validate Markdown` - Documentation quality

#### Additional Settings
- **Require conversation resolution before merging**: ✅ Enabled
- **Require signed commits**: ✅ Enabled (recommended for crypto operations)
- **Require linear history**: ⚠️ Optional (consider for simpler history)
- **Require merge queue**: ⚠️ Optional (for high-traffic repositories)
- **Do not allow bypassing the above settings**: ✅ Enabled
- **Restrict who can push to matching branches**: ✅ Enabled
  - Allow: Administrators, specific users/teams

#### Force Push and Deletion
- **Allow force pushes**: ❌ Disabled
- **Allow deletions**: ❌ Disabled

## Repository Security Settings

### Code Security and Analysis

Enable in repository Settings > Security & analysis:

#### Dependency Graph
- **Status**: ✅ Enabled
- Automatically tracks dependencies and their vulnerabilities

#### Dependabot
- **Dependabot alerts**: ✅ Enabled
  - Get notified of vulnerabilities in dependencies
- **Dependabot security updates**: ✅ Enabled
  - Automatic pull requests to fix vulnerabilities
- **Dependabot version updates**: ✅ Enabled
  - Configured via `.github/dependabot.yml`

#### Code Scanning
- **CodeQL analysis**: ✅ Enabled
  - Configured via `.github/workflows/codeql-analysis.yml`
  - Scans: Python, JavaScript, TypeScript
  - Schedule: Daily at 2 AM UTC
  - On: Push and Pull Requests to main branch

#### Secret Scanning
- **Secret scanning**: ✅ Enabled
  - Automatically detects secrets pushed to repository
- **Push protection**: ✅ Enabled (if available)
  - Prevents pushes containing secrets
- **Custom patterns**: Configure organization-specific patterns

### GitHub Actions Security

Configure in Settings > Actions > General:

#### Actions Permissions
- **Allow actions and reusable workflows**: Select one of:
  - **Option 1 (Most Secure)**: Allow [organization] actions and reusable workflows
  - **Option 2 (Recommended)**: Allow [organization] actions and select non-[organization] actions
    - ✅ Allow actions created by GitHub
    - ✅ Allow actions by Marketplace verified creators
    - Specify: List trusted action owners (e.g., `actions/*`, `github/*`)

#### Workflow Permissions
- **Default workflow token permissions**: Read repository contents
  - ❌ **Do not** grant write permissions by default
  - Workflows must explicitly request write permissions
- **Allow GitHub Actions to create and approve pull requests**: ❌ Disabled
  - Prevent automated bypass of review requirements

#### Artifact and Log Retention
- **Artifact retention**: 90 days (default)
- **Consider shorter retention** for sensitive workflows

### Required Workflows (Organization Level)

If this is an organization-wide `.github` repository, consider requiring:
- Security scanning workflows
- Dependency update workflows  
- Code quality checks

## Environment Protection Rules

For workflows that perform sensitive operations (crypto consolidation, deployments):

### Production Environment
- **Name**: `production-crypto` or `production`
- **Required reviewers**: 2 administrators
- **Wait timer**: 5 minutes (cooling-off period)
- **Deployment branches**: Only `main` branch
- **Environment secrets**: Store sensitive credentials here

### Staging Environment  
- **Name**: `staging`
- **Required reviewers**: 1 team member
- **Deployment branches**: `main`, `develop`, `staging/*`

## Access Control

### Repository Access
- **Base permissions**: Read
- **Teams with elevated access**:
  - Admins: Write + Admin
  - Maintainers: Write
  - Contributors: Triage (for issue management)

### Outside Collaborators
- Require two-factor authentication
- Review access quarterly
- Use temporary access where possible

## Commit Signature Verification

### Requirements for Crypto Operations

Given this repository handles cryptocurrency operations, **require verified commits**:

#### Why Signed Commits Matter
- Proves commits come from trusted sources
- Prevents impersonation
- Creates audit trail
- Required for compliance in some industries

#### Setup Instructions
See detailed guides:
- [GIT_KEY_PAIRS.md](GIT_KEY_PAIRS.md)
- [GPG_KEY_MANAGEMENT.md](GPG_KEY_MANAGEMENT.md)
- [CONNECTING_TO_GITHUB_WITH_SSH.md](CONNECTING_TO_GITHUB_WITH_SSH.md)

#### Enforcement
```bash
# Verify commits locally before pushing
git log --show-signature

# Verify specific commit
git verify-commit HEAD
```

Branch protection should enforce: "Require signed commits"

## Security Audit Schedule

### Weekly
- Review Dependabot alerts
- Check failed CodeQL scans
- Review secret scanning alerts

### Monthly  
- Audit repository access
- Review branch protection compliance
- Check for unmaintained dependencies

### Quarterly
- Full security audit
- Review and update security policies
- Test incident response procedures
- Review and rotate secrets/credentials

## Incident Response

### If Secrets Are Exposed
1. **Immediately revoke** the exposed credential
2. Remove from Git history (see SECURITY_BEST_PRACTICES.md)
3. Rotate all related credentials
4. Audit access logs for potential misuse
5. Create security advisory if users affected
6. Document incident and lessons learned

### If Vulnerability Discovered
1. Create **private security advisory**
2. Assess severity and impact
3. Develop and test fix
4. Coordinate disclosure timeline
5. Release fix and advisory
6. Monitor for exploitation attempts

## Compliance and Standards

This configuration aligns with:
- **OpenSSF Best Practices**: https://bestpractices.coreinfrastructure.org/
- **Linux Foundation Security**: https://www.linuxfoundation.org/resources/open-source-guides/creating-an-open-source-program
- **GitHub Security Best Practices**: https://docs.github.com/en/code-security
- **OWASP Secure Coding Practices**: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/

## Implementation Checklist

Use this checklist to verify security configuration:

### Repository Settings
- [ ] Branch protection enabled on `main`
- [ ] Require 2 pull request reviews
- [ ] Require review from Code Owners
- [ ] Require status checks to pass
- [ ] Require signed commits
- [ ] Disable force push and branch deletion
- [ ] Require conversation resolution

### Security Features
- [ ] Dependabot alerts enabled
- [ ] Dependabot security updates enabled
- [ ] Dependabot version updates configured
- [ ] CodeQL analysis workflow added
- [ ] Secret scanning enabled
- [ ] Secret scanning push protection enabled

### Access Control
- [ ] Two-factor authentication required
- [ ] Repository access reviewed
- [ ] Outside collaborators minimized
- [ ] CODEOWNERS file created
- [ ] Teams properly configured

### Workflows
- [ ] Workflows use minimal permissions
- [ ] No script injection vulnerabilities
- [ ] Secrets properly managed
- [ ] Third-party actions pinned
- [ ] Environment protection configured

### Documentation
- [ ] SECURITY.md present
- [ ] SECURITY_BEST_PRACTICES.md present
- [ ] WORKFLOW_SECURITY.md present
- [ ] BRANCH_PROTECTION.md present (this file)
- [ ] Contributing guidelines updated
- [ ] Code of conduct present

### Monitoring
- [ ] Security alerts configured
- [ ] Audit log monitoring enabled
- [ ] Regular security reviews scheduled
- [ ] Incident response plan documented

## Quick Setup Commands

```bash
# Enable branch protection via GitHub CLI (requires admin access)
gh api -X PUT /repos/{owner}/{repo}/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":["CodeQL","Secret Scanning"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":2,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
  -f restrictions=null \
  -f required_linear_history=false \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f required_signatures=true

# Enable security features
gh api -X PATCH /repos/{owner}/{repo} \
  -f has_vulnerability_alerts=true \
  -f has_automated_security_fixes=true

# Enable secret scanning (requires Advanced Security)
gh api -X PUT /repos/{owner}/{repo}/secret-scanning/push-protection
```

## Additional Resources

- [GitHub Docs: Managing security and analysis settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository)
- [GitHub Docs: About branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Security Lab](https://securitylab.github.com/)
- [OpenSSF Scorecard](https://github.com/ossf/scorecard)

---

**Last Updated**: 2026-02-13

For security concerns or questions, see [SECURITY.md](SECURITY.md).
