# Git Key-Pairs Guide

A comprehensive guide to understanding and managing key-pairs for Git and GitHub authentication.

## Overview

When working with Git and GitHub, you'll encounter two main types of cryptographic key-pairs:

1. **SSH Keys** - For authentication and secure communication with GitHub
2. **GPG Keys** - For signing commits and tags to verify authenticity

This guide provides an overview of both types and when to use each.

## Table of Contents

1. [Understanding Key-Pairs](#understanding-key-pairs)
2. [SSH Keys vs GPG Keys](#ssh-keys-vs-gpg-keys)
3. [Quick Start Guide](#quick-start-guide)
4. [SSH Keys for Authentication](#ssh-keys-for-authentication)
5. [GPG Keys for Signing](#gpg-keys-for-signing)
6. [Best Practices](#best-practices)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

## Understanding Key-Pairs

A key-pair consists of two mathematically related keys:

- **Public Key** - Shared openly (added to GitHub, keyservers, etc.)
- **Private Key** - Kept secret and secure (never shared)

### How Key-Pairs Work

1. You generate a key-pair on your local machine
2. The public key is uploaded to GitHub
3. Your private key stays on your machine
4. When you connect to GitHub, the keys verify your identity
5. Only someone with the private key can prove ownership of the public key

### Key Types and Algorithms

**SSH Key Algorithms:**
- **ED25519** (Recommended) - Modern, secure, fast
- **RSA 4096** - Legacy support, widely compatible

**GPG Key Algorithms:**
- **RSA 4096** (Standard) - Widely used for signing
- **Curve25519** - Modern alternative (ECC)

## SSH Keys vs GPG Keys

| Feature | SSH Keys | GPG Keys |
|---------|----------|----------|
| **Primary Purpose** | Authentication | Signing & Encryption |
| **Use Case** | Authenticate to GitHub without passwords | Sign commits and tags |
| **Verifies** | Who is connecting | Who authored the code |
| **Required For** | Push/Pull operations via SSH | Verified commits badge |
| **Algorithm Choice** | ED25519 or RSA | RSA 4096 |
| **Key Location** | `~/.ssh/` | `~/.gnupg/` |
| **GitHub Setup** | Settings → SSH and GPG keys → SSH keys | Settings → SSH and GPG keys → GPG keys |

### When to Use Each

**Use SSH Keys When:**
- You want to clone, push, or pull from GitHub without entering passwords
- You're setting up authentication for Git operations
- You need to automate Git workflows
- You're working with deploy keys

**Use GPG Keys When:**
- You want verified commit badges on GitHub
- You need to prove commit authorship
- You're working on security-sensitive projects
- You want to sign releases and tags
- Your organization requires signed commits

**Use Both When:**
- You want complete security (authentication + verification)
- You're working on open-source projects
- You're a maintainer who needs to prove identity
- You want maximum trust and security

## Quick Start Guide

### Setting Up SSH Keys (5 minutes)

**1. Generate SSH Key:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**2. Start SSH Agent and Add Key:**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**3. Copy Public Key:**
```bash
cat ~/.ssh/id_ed25519.pub
```

**4. Add to GitHub:**
- Go to [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys)
- Click "New SSH key"
- Paste your public key

**5. Test Connection:**
```bash
ssh -T git@github.com
```

✅ **Success:** You should see "Hi username! You've successfully authenticated..."

**For detailed instructions:** See [CONNECTING_TO_GITHUB_WITH_SSH.md](CONNECTING_TO_GITHUB_WITH_SSH.md)

### Setting Up GPG Keys (10 minutes)

**1. Generate GPG Key:**
```bash
gpg --full-generate-key
# Select: (1) RSA and RSA
# Key size: 4096
# Expiration: 1y (recommended)
# Enter your name and email
```

**2. List Keys and Get Key ID:**
```bash
gpg --list-secret-keys --keyid-format=long
# Note the key ID (e.g., 3AA5C34371567BD2)
```

**3. Export Public Key:**
```bash
gpg --armor --export YOUR_KEY_ID
```

**4. Add to GitHub:**
- Go to [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys)
- Click "New GPG key"
- Paste your public key

**5. Configure Git:**
```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
```

✅ **Success:** Your commits will now be automatically signed!

**For detailed instructions:** See [GPG_KEY_MANAGEMENT.md](GPG_KEY_MANAGEMENT.md)

## SSH Keys for Authentication

### What SSH Keys Do

SSH keys authenticate your identity when:
- Cloning private repositories
- Pushing commits to repositories
- Pulling from repositories
- Using Git operations via SSH protocol

### SSH Key Workflow

```
Your Computer                     GitHub
--------------                    --------
1. Generate SSH key-pair
   (public + private)

2. Add public key ─────────────> Store public key
                                 in your account

3. Git operation ───────────────> Verify using
   (signed with private key)      public key

4. Access granted <─────────────  Authentication
                                 successful
```

### Common SSH Commands

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# List loaded keys
ssh-add -l

# Test GitHub connection
ssh -T git@github.com

# Clone with SSH
git clone git@github.com:username/repo.git

# Convert HTTPS repo to SSH
git remote set-url origin git@github.com:username/repo.git
```

### Managing Multiple SSH Keys

If you have multiple GitHub accounts or keys:

**1. Create SSH config file:**
```bash
nano ~/.ssh/config
```

**2. Add configuration:**
```
# Personal account
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519

# Work account
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
```

**3. Clone using appropriate host:**
```bash
# Personal
git clone git@github.com:personal/repo.git

# Work
git clone git@github-work:company/repo.git
```

## GPG Keys for Signing

### What GPG Keys Do

GPG keys cryptographically sign your commits to:
- Prove you authored the commit
- Show commits haven't been tampered with
- Display "Verified" badge on GitHub
- Build trust in your contributions

### GPG Key Workflow

```
Your Computer                     GitHub
--------------                    --------
1. Generate GPG key-pair
   (public + private)

2. Add public key ─────────────> Store public key
                                 in your account

3. Make commit ───────────────> Verify signature
   (signed with private key)    using public key

4. Commit displayed <──────────  Show "Verified"
                                badge
```

### Common GPG Commands

```bash
# Generate new GPG key
gpg --full-generate-key

# List GPG keys
gpg --list-secret-keys --keyid-format=long

# Export public key for GitHub
gpg --armor --export YOUR_KEY_ID

# Configure Git to sign commits
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Sign a specific commit
git commit -S -m "Your commit message"

# Sign a tag
git tag -s v1.0.0 -m "Version 1.0.0"

# Verify a commit signature
git verify-commit HEAD

# View signature in log
git log --show-signature -1

# Refresh keys from keyserver
gpg --keyserver hkps://keys.openpgp.org --refresh-keys
```

### Verified Commits on GitHub

When you sign commits with GPG, GitHub shows verification status:

- **✅ Verified** - Signature valid, key in your GitHub account
- **⚠️ Unverified** - Signature valid, but key not in your account
- **❌ Invalid** - Signature verification failed
- **No status** - Commit not signed

## Best Practices

### SSH Key Best Practices

1. **Use ED25519 keys** - Modern, secure, and fast
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Use passphrases** - Always protect SSH keys with strong passphrases
   ```bash
   # When prompted, enter a strong passphrase
   ```

3. **One key per device** - Generate unique keys for each machine
   ```bash
   # On laptop
   ssh-keygen -t ed25519 -C "laptop@example.com"
   # On desktop
   ssh-keygen -t ed25519 -C "desktop@example.com"
   ```

4. **Name keys descriptively** - Add meaningful comments
   ```bash
   ssh-keygen -t ed25519 -C "work-laptop-2026"
   ```

5. **Remove old keys** - Delete unused keys from GitHub settings

6. **Use SSH agent** - Avoid typing passphrases repeatedly
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

### GPG Key Best Practices

1. **Set expiration dates** - Use 1-2 year expiration
   ```bash
   # During key generation, set expiration: 1y or 2y
   ```

2. **Use strong passphrases** - Protect GPG keys with complex passphrases

3. **Back up keys securely** - Store encrypted backups offline
   ```bash
   gpg --armor --export-secret-keys YOUR_KEY_ID > gpg-backup.asc
   # Store this file securely (encrypted USB drive, password manager)
   ```

4. **Sign all commits** - Enable automatic commit signing
   ```bash
   git config --global commit.gpgsign true
   ```

5. **Sign important tags** - Always sign release tags
   ```bash
   git tag -s v1.0.0 -m "Release 1.0.0"
   ```

6. **Refresh keys regularly** - Update from keyservers monthly
   ```bash
   gpg --keyserver hkps://keys.openpgp.org --refresh-keys
   ```

7. **Extend before expiration** - Renew keys before they expire
   ```bash
   gpg --edit-key YOUR_KEY_ID
   gpg> expire
   ```

### Universal Best Practices

1. **Match email addresses** - Git, SSH comments, and GPG UIDs should use same email
   ```bash
   # Check Git email
   git config user.email
   
   # Should match GitHub email and GPG key email
   ```

2. **Use verified emails** - Only use verified email addresses from GitHub

3. **Keep keys private** - Never share private keys or commit them to Git

4. **Regular security audits** - Review keys in GitHub settings quarterly

5. **Revoke compromised keys** - Immediately revoke if compromised
   ```bash
   # For SSH: Delete from GitHub settings
   # For GPG: Generate and publish revocation certificate
   ```

6. **Document your keys** - Keep a secure record of which keys are where

## Security Considerations

### Protecting Private Keys

**SSH Private Keys:**
- Location: `~/.ssh/id_ed25519` (or `id_rsa`)
- Permissions: `chmod 600 ~/.ssh/id_ed25519`
- Never share or commit to repositories
- Use passphrases to encrypt the key file

**GPG Private Keys:**
- Location: `~/.gnupg/` directory
- Access: Only readable by your user account
- Never share or commit to repositories
- Use strong passphrases to protect

### Passphrase Guidelines

A strong passphrase should be:
- **At least 20 characters** for high security
- **Combination of words** (e.g., "correct horse battery staple")
- **Unique** - Don't reuse passwords
- **Memorable** - You'll need to type it regularly

Consider using a **password manager** to generate and store passphrases.

### Key Rotation

**When to rotate keys:**
- Annually as a best practice
- When a device is lost or stolen
- When a key may have been compromised
- When leaving an organization
- When an employee with access leaves

**How to rotate:**

**SSH Keys:**
1. Generate new key on your device
2. Add new key to GitHub
3. Test with new key: `ssh -T git@github.com`
4. Remove old key from GitHub
5. Delete old key from device: `rm ~/.ssh/old_key*`

**GPG Keys:**
1. Generate new GPG key
2. Add new key to GitHub
3. Update Git config: `git config --global user.signingkey NEW_KEY_ID`
4. Revoke old key (if necessary)
5. Publish revocation to keyservers

### Compromised Keys

**If you suspect a key is compromised:**

**SSH Key:**
1. Immediately remove from GitHub (Settings → SSH and GPG keys)
2. Delete from local machine
3. Generate new key
4. Add new key to GitHub
5. Update any automated systems using the old key

**GPG Key:**
1. Generate revocation certificate
   ```bash
   gpg --output revoke.asc --gen-revoke YOUR_KEY_ID
   ```
2. Import revocation
   ```bash
   gpg --import revoke.asc
   ```
3. Publish to keyservers
   ```bash
   gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_KEY_ID
   ```
4. Remove from GitHub
5. Generate new key
6. Update Git configuration

## Troubleshooting

### Common SSH Issues

**Permission Denied (publickey)**
```bash
# Verify key is loaded
ssh-add -l

# If empty, add your key
ssh-add ~/.ssh/id_ed25519

# Test connection
ssh -T git@github.com

# Check key permissions
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 700 ~/.ssh
```

**Could not open a connection to your authentication agent**
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519
```

**Host key verification failed**
```bash
# Update known hosts
ssh-keyscan github.com >> ~/.ssh/known_hosts

# Or remove old entry and try again
ssh-keygen -R github.com
```

### Common GPG Issues

**gpg failed to sign the data**
```bash
# Test GPG signing
echo "test" | gpg --clearsign

# Check Git GPG program
git config --global gpg.program gpg

# Restart GPG agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**inappropriate ioctl for device**
```bash
# Set GPG_TTY environment variable
export GPG_TTY=$(tty)

# Add to ~/.bashrc or ~/.zshrc
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
```

**Commits not showing as verified on GitHub**
```bash
# Check email matches
git config user.email
gpg --list-secret-keys --keyid-format=long

# Check signing key is configured
git config user.signingkey

# Check key is on GitHub
# Visit: https://github.com/settings/keys

# Check key hasn't expired
gpg --list-keys YOUR_KEY_ID
```

### Debug Mode

**SSH verbose output:**
```bash
ssh -vvv -T git@github.com
```

**Git verbose output:**
```bash
GIT_TRACE=1 GIT_SSH_COMMAND="ssh -vvv" git clone git@github.com:user/repo.git
```

**GPG verbose output:**
```bash
git commit -S -m "Test" --verbose
```

## Complete Setup Example

Here's a complete example of setting up both SSH and GPG keys:

```bash
# ============================================
# PART 1: SSH Key Setup
# ============================================

# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter for default location
# Enter a strong passphrase

# 2. Start SSH agent and add key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Display public key
cat ~/.ssh/id_ed25519.pub
# Copy this output

# 4. Add to GitHub
# - Go to https://github.com/settings/keys
# - Click "New SSH key"
# - Paste the public key
# - Click "Add SSH key"

# 5. Test connection
ssh -T git@github.com
# Should show: "Hi username! You've successfully authenticated..."

# ============================================
# PART 2: GPG Key Setup
# ============================================

# 1. Generate GPG key
gpg --full-generate-key
# Select: (1) RSA and RSA
# Key size: 4096
# Expiration: 1y
# Enter your name and verified GitHub email
# Enter a strong passphrase

# 2. List keys and get key ID
gpg --list-secret-keys --keyid-format=long
# Look for the line like: rsa4096/3AA5C34371567BD2
# The key ID is: 3AA5C34371567BD2

# 3. Export public key
gpg --armor --export 3AA5C34371567BD2
# Copy this output (from BEGIN to END PGP PUBLIC KEY BLOCK)

# 4. Add to GitHub
# - Go to https://github.com/settings/keys
# - Click "New GPG key"
# - Paste the public key
# - Click "Add GPG key"

# 5. Configure Git to use GPG key
git config --global user.signingkey 3AA5C34371567BD2
git config --global commit.gpgsign true

# 6. Test by making a signed commit
echo "test" > test.txt
git add test.txt
git commit -m "Test signed commit"
# Should sign automatically

# Verify the signature
git verify-commit HEAD
# Should show: "Good signature from..."

# ============================================
# VERIFICATION
# ============================================

# Verify SSH setup
echo "SSH Test:"
ssh -T git@github.com

# Verify GPG setup
echo "GPG Test:"
git log --show-signature -1

# Verify configurations
echo "Git Config:"
git config user.email
git config user.signingkey
git config commit.gpgsign

echo "Setup complete! ✅"
```

## Additional Resources

### Official Documentation

**SSH Keys:**
- [GitHub SSH Documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [ssh-keygen Man Page](https://man.openbsd.org/ssh-keygen)

**GPG Keys:**
- [GitHub GPG Documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)
- [Git Signing Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)

### Related Documentation in This Repository

- **[Connecting to GitHub with SSH](CONNECTING_TO_GITHUB_WITH_SSH.md)** - Detailed SSH setup guide
- **[GPG Key Management](GPG_KEY_MANAGEMENT.md)** - Comprehensive GPG guide
- **[Security Best Practices](SECURITY_BEST_PRACTICES.md)** - Security guidelines
- **[Contributing Guide](CONTRIBUTING.md)** - Contribution guidelines

### Tools and Utilities

- **SSH Key Generation:** `ssh-keygen`
- **SSH Agent:** `ssh-agent`, `ssh-add`
- **GPG:** `gpg` or `gpg2`
- **Git:** Native Git signing support

### Community Resources

- [GitHub Community Forum](https://github.community/)
- [Git Mailing List](https://git-scm.com/community)
- [GnuPG Users List](https://gnupg.org/documentation/mailing-lists.html)

## Summary Checklist

Use this checklist to ensure you have everything set up correctly:

### SSH Keys ✅
- [ ] SSH key-pair generated (ED25519 or RSA 4096)
- [ ] Private key protected with passphrase
- [ ] Public key added to GitHub account
- [ ] SSH agent running with key loaded
- [ ] Connection tested: `ssh -T git@github.com`
- [ ] Repositories using SSH URLs
- [ ] SSH config created (if using multiple keys)

### GPG Keys ✅
- [ ] GPG key-pair generated (RSA 4096)
- [ ] Private key protected with passphrase
- [ ] Key expiration set (1-2 years)
- [ ] Public key exported and added to GitHub
- [ ] Git configured with signing key
- [ ] Automatic commit signing enabled
- [ ] Test commit signed and verified
- [ ] Commits showing "Verified" badge on GitHub
- [ ] Key backed up securely

### Configuration ✅
- [ ] Git email matches GitHub verified email
- [ ] Git email matches GPG key email
- [ ] SSH permissions correct (600 for private, 644 for public)
- [ ] GPG_TTY set in shell configuration
- [ ] Keys documented in secure location

### Security ✅
- [ ] Both keys protected with strong passphrases
- [ ] Private keys never shared or committed
- [ ] Key rotation schedule established
- [ ] Backup strategy in place
- [ ] Old keys removed from unused devices

## Conclusion

You now have a comprehensive understanding of Git key-pairs! With both SSH and GPG keys configured, you have:

✅ **Secure authentication** to GitHub via SSH keys
✅ **Verified commits** with GPG signatures
✅ **Enhanced security** for your development workflow
✅ **Trust and transparency** in your contributions

Remember:
- Keep your private keys secure
- Use strong passphrases
- Rotate keys regularly
- Monitor your GitHub security settings

For detailed information, refer to:
- [CONNECTING_TO_GITHUB_WITH_SSH.md](CONNECTING_TO_GITHUB_WITH_SSH.md) for SSH details
- [GPG_KEY_MANAGEMENT.md](GPG_KEY_MANAGEMENT.md) for GPG details

Happy coding! 🚀
