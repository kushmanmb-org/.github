# Git POW (Proof of Work) Verification

Verify Git commit signatures using GPG, ensuring commits are properly signed and authenticated. This utility follows security best practices for handling cryptographic verification data.

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Security Best Practices](#security-best-practices)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)
10. [Related Documentation](#related-documentation)

## Overview

The Git POW verification utility provides a secure way to verify that Git commits are properly signed with GPG keys. This helps ensure:

- **Authenticity**: Commits are from the claimed author
- **Integrity**: Commit content hasn't been tampered with
- **Trust**: Commits are signed with trusted keys
- **Accountability**: Clear audit trail of verified commits

### What is "POW" in this context?

POW (Proof of Work) in Git verification refers to the cryptographic proof that a commit was created by someone who possesses the private key corresponding to a trusted public key. This is analogous to blockchain proof-of-work but uses GPG signatures instead of computational puzzles.

## Requirements

- **Python 3.6+**
- **Git** (with GPG support)
- **GPG** (GnuPG) installed and configured

### Checking Requirements

```bash
# Check Python version
python3 --version

# Check Git version
git --version

# Check GPG version
gpg --version
```

## Installation

The utility is ready to use without installation. Simply ensure you have the required dependencies and the script has execute permissions:

```bash
# Make executable
chmod +x git_pow_verifier.py

# Verify it works
./git_pow_verifier.py --help
```

## Quick Start

### 1. Verify a Single Commit

```bash
# Verify current HEAD commit
./git_pow_verifier.py --commit HEAD

# Verify a specific commit by SHA
./git_pow_verifier.py --commit abc123def456

# Verify with full details
./git_pow_verifier.py --commit HEAD --verbose --info
```

### 2. Verify Multiple Commits

Create a `commits.json` file (or use the example):

```json
[
  "HEAD",
  "HEAD~1",
  "abc123def456"
]
```

Then verify:

```bash
./git_pow_verifier.py --file commits.json
```

### 3. Check Results as JSON

```bash
# Single commit as JSON
./git_pow_verifier.py --commit HEAD --json --pretty

# Multiple commits as JSON
./git_pow_verifier.py --file commits.json --json --pretty
```

## Usage

### Command-Line Options

```
usage: git_pow_verifier.py [-h] [--commit COMMIT] [--file FILE] [--repo REPO]
                           [--json] [--pretty] [--verbose] [--info]

options:
  -h, --help       Show help message and exit
  --commit COMMIT  Single commit SHA to verify (can be full or short SHA, or HEAD)
  --file FILE      JSON file containing commit SHAs to verify
  --repo REPO      Path to Git repository (default: current directory)
  --json           Output results as JSON
  --pretty         Pretty-print JSON output (requires --json)
  --verbose        Show verbose output including raw GPG output
  --info           Include commit information (author, subject)
```

### Commit File Format

The verification utility supports two JSON formats:

**Format 1: Simple List**
```json
[
  "HEAD",
  "abc123def456",
  "1234567"
]
```

**Format 2: Object with Metadata**
```json
{
  "commits": [
    {"sha": "HEAD"},
    {"commit": "abc123def456"},
    {"sha": "1234567"}
  ]
}
```

## Configuration

### Setting Up GPG for Commit Signing

Before using the verification utility, ensure your Git commits are signed. See the following guides:

- [GPG Key Management](GPG_KEY_MANAGEMENT.md) - Complete GPG setup guide
- [Git Key-Pairs Guide](GIT_KEY_PAIRS.md) - Understanding SSH and GPG keys

### Configuring Git to Sign Commits

```bash
# Configure Git to use your GPG key
git config --global user.signingkey YOUR_GPG_KEY_ID

# Enable commit signing by default
git config --global commit.gpgsign true

# Verify configuration
git config --get user.signingkey
git config --get commit.gpgsign
```

### Importing Public Keys for Verification

To verify commits signed by others, import their public keys:

```bash
# Import from keyserver
gpg --keyserver keyserver.ubuntu.com --recv-keys KEY_ID

# Import from file
gpg --import public-key.asc

# List imported keys
gpg --list-keys
```

## Security Best Practices

### Private Data Protection

The verification utility follows strict security practices:

✅ **DO:**
- Store verification policies in `.gitignore`-protected files
- Use environment variables for sensitive configuration
- Keep GPG private keys secure and encrypted
- Use strong passphrases for GPG keys
- Regularly rotate and update GPG keys
- Verify commits before merging critical changes

❌ **DON'T:**
- Commit GPG private keys to version control
- Share passphrases in commit messages or documentation
- Store verification secrets in public repositories
- Trust unverified commits in production deployments
- Use weak or compromised GPG keys

### .gitignore Protection

The following patterns are automatically excluded from version control:

```
# Git verification data
verification-data/
gpg-verification.*
*verification-config*
*commits*.json          # Except *commits*example*.json
verification-policy.*
```

**Safe to commit:**
- `commits-example.json`
- `verification-config.example.json`
- Documentation and README files

**Never commit:**
- `commits.json`
- `verification-config.json`
- `gpg-verification.key`
- Private keys or passphrases

### Security Checklist

Before using the verification utility:

- [ ] GPG is properly installed and configured
- [ ] Git is configured to sign commits
- [ ] Your GPG key is backed up securely
- [ ] Public keys of trusted contributors are imported
- [ ] .gitignore patterns are in place
- [ ] No private keys are in the repository
- [ ] Verification policies are documented (in protected files)

## Examples

### Example 1: Verify Recent Commits

Verify the last 5 commits in your repository:

```bash
# Get the last 5 commit SHAs
git log -5 --format="%H" > /tmp/recent-commits.txt

# Create JSON file
python3 -c "import json; commits = open('/tmp/recent-commits.txt').read().split(); print(json.dumps(commits, indent=2))" > /tmp/commits.json

# Verify them
./git_pow_verifier.py --file /tmp/commits.json --info
```

### Example 2: Verify PR Commits

Verify all commits in a pull request:

```bash
# Get PR commits (assuming PR branch is 'feature-branch')
git log main..feature-branch --format="%H" > /tmp/pr-commits.txt

# Create JSON and verify
python3 -c "import json; commits = open('/tmp/pr-commits.txt').read().split(); print(json.dumps(commits, indent=2))" > /tmp/pr-commits.json
./git_pow_verifier.py --file /tmp/pr-commits.json --verbose
```

### Example 3: Automated Verification in CI/CD

```bash
#!/bin/bash
# verify-commits.sh - Use in CI/CD pipeline

# Verify HEAD commit
./git_pow_verifier.py --commit HEAD --json > verification-result.json

# Check if verification passed
if python3 -c "import json; result = json.load(open('verification-result.json')); exit(0 if result['valid'] else 1)"; then
  echo "✅ Commit verification passed"
  exit 0
else
  echo "❌ Commit verification failed"
  exit 1
fi
```

### Example 4: Check Verification Status

```bash
# Quick check with minimal output
./git_pow_verifier.py --commit HEAD

# Detailed check with all information
./git_pow_verifier.py --commit HEAD --verbose --info

# Export as JSON for processing
./git_pow_verifier.py --commit HEAD --json --pretty > verification.json
```

### Example 5: Verify Tagged Releases

```bash
# Verify a specific tag
./git_pow_verifier.py --commit v1.0.0

# Verify all recent tags
for tag in $(git tag -l | tail -5); do
  echo "Verifying tag: $tag"
  ./git_pow_verifier.py --commit $tag --info
  echo ""
done
```

## Troubleshooting

### Issue: "Commit is not signed"

**Problem:** The commit doesn't have a GPG signature.

**Solution:**
```bash
# Check if commit signing is enabled
git config --get commit.gpgsign

# Enable commit signing
git config --global commit.gpgsign true

# Amend the last commit with a signature
git commit --amend --no-edit -S
```

### Issue: "Cannot check signature: GPG key not found in keyring"

**Problem:** The public key used to sign the commit is not in your GPG keyring.

**Solution:**
```bash
# Get the key ID from the error message
# Then import the key from a keyserver
gpg --keyserver keyserver.ubuntu.com --recv-keys KEY_ID

# Or import from a file
gpg --import contributor-public-key.asc

# Verify the key was imported
gpg --list-keys KEY_ID
```

### Issue: "Bad signature: Signature verification failed"

**Problem:** The signature is invalid (commit content was modified after signing).

**Solution:**
This is a serious security issue. The commit has been tampered with after signing.
- **DO NOT** merge or use this commit
- Investigate why the signature is invalid
- Contact the commit author
- Re-sign the commit if you're the author and the change was intentional

### Issue: "Not a Git repository"

**Problem:** The command is not being run in a Git repository.

**Solution:**
```bash
# Navigate to your Git repository
cd /path/to/your/repo

# Or specify the repository path
./git_pow_verifier.py --commit HEAD --repo /path/to/your/repo
```

### Issue: "Git command not found"

**Problem:** Git is not installed or not in PATH.

**Solution:**
```bash
# On Ubuntu/Debian
sudo apt-get install git

# On macOS
brew install git

# On RHEL/CentOS
sudo yum install git

# Verify installation
git --version
```

### Issue: Trust Level "unknown"

**Problem:** The GPG key is not trusted in your keyring.

**Solution:**
```bash
# List the key
gpg --list-keys KEY_ID

# Edit the key to set trust level
gpg --edit-key KEY_ID
# In the GPG prompt, type: trust
# Select trust level (usually 5 for ultimate if it's your own key)
# Type: quit
```

## Related Documentation

- **[GPG Key Management](GPG_KEY_MANAGEMENT.md)** - Complete guide to managing GPG keys
- **[Git Key-Pairs Guide](GIT_KEY_PAIRS.md)** - Understanding SSH and GPG keys for Git
- **[Security Best Practices](SECURITY_BEST_PRACTICES.md)** - Guidelines for protecting sensitive data
- **[Connecting to GitHub with SSH](CONNECTING_TO_GITHUB_WITH_SSH.md)** - SSH authentication guide
- **[Transaction Hash Verification](TX_HASH_VERIFICATION.md)** - Similar verification utility for blockchain transactions

## Output Format

### Standard Output

```
Commit: abc123def456
  Author: John Doe <john@example.com>
  Subject: Add new feature
  Status: ✅ VALID
  Signed: Yes
  Signer: John Doe <john@example.com>
  Key ID: ABCD1234EF567890
  Trust: ultimate
```

### JSON Output

```json
{
  "commit": "abc123def456",
  "signed": true,
  "valid": true,
  "key_id": "ABCD1234EF567890",
  "signer": "John Doe <john@example.com>",
  "fingerprint": "ABCD 1234 EF56 7890 ABCD 1234 EF56 7890 ABCD 1234",
  "trust_level": "ultimate",
  "error": null,
  "raw_output": "gpg: Signature made..."
}
```

## Exit Codes

- `0` - All commits verified successfully
- `1` - One or more commits failed verification

## Performance Considerations

- **Single Commit**: ~100ms per verification
- **Batch Verification**: ~100ms per commit (parallelizable)
- **Large Files**: Verification time is independent of commit size

For large batches (100+ commits), consider splitting into multiple files and processing in parallel.

## License

See individual files for licensing information.

---

**Security Note:** This utility helps verify commit authenticity but should be part of a comprehensive security strategy. Always follow security best practices and keep your GPG keys secure.

*Last Updated: 2026-02-13*
