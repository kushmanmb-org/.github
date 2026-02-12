# GPG Key Management for GitHub

This guide walks you through setting up and managing GPG keys for signing commits and tags on GitHub, ensuring authenticity and integrity of your contributions.

## Overview

GPG (GNU Privacy Guard) allows you to cryptographically sign your Git commits and tags. This proves that commits come from a trusted source and haven't been tampered with.

## Prerequisites

- Git installed on your computer
- GPG installed (`gpg` or `gpg2`)
- A GitHub account
- Terminal/Command Prompt access

## Table of Contents

1. [Checking for Existing GPG Keys](#checking-for-existing-gpg-keys)
2. [Generating a New GPG Key](#generating-a-new-gpg-key)
3. [Adding GPG Key to GitHub](#adding-gpg-key-to-github)
4. [Configuring Git to Use GPG](#configuring-git-to-use-gpg)
5. [Signing Commits and Tags](#signing-commits-and-tags)
6. [Refreshing GPG Keys](#refreshing-gpg-keys)
7. [Managing GPG Keys](#managing-gpg-keys)
8. [Troubleshooting](#troubleshooting)

## Checking for Existing GPG Keys

Before generating a new GPG key, check if you already have one:

```bash
# List existing GPG keys
gpg --list-secret-keys --keyid-format=long
```

If you see output like this, you already have GPG keys:

```text
/home/user/.gnupg/pubring.kbx
-----------------------------
sec   rsa4096/3AA5C34371567BD2 2021-01-01 [SC]
uid                 [ultimate] Your Name <your_email@example.com>
ssb   rsa4096/42B317FD4BA89E7A 2021-01-01 [E]
```

The key ID in this example is `3AA5C34371567BD2`.

## Generating a New GPG Key

### Step 1: Generate the Key

Generate a new GPG key with appropriate algorithms:

```bash
gpg --full-generate-key
```

### Step 2: Select Key Type

When prompted, select:

1. Key type: **RSA and RSA** (option 1)
2. Key size: **4096** bits
3. Expiration: Choose an expiration period (recommended: 1-2 years)
   - Press **Enter** for no expiration (not recommended)
   - Or enter `1y` for 1 year, `2y` for 2 years, etc.

### Step 3: Enter User Information

Provide the following information:

- **Real name**: Your name (matches your GitHub profile)
- **Email address**: The verified email address associated with your GitHub account
- **Comment**: Optional description (can leave blank)

### Step 4: Set Passphrase

Enter a strong passphrase to protect your GPG key. **This is critical for security.**

**Example session:**

```text
gpg (GnuPG) 2.2.27; Copyright (C) 2021 Free Software Foundation, Inc.
Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection? 1
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Please specify how long the key should be valid.
Key is valid for? (0) 1y
Is this correct? (y/N) y
```

## Adding GPG Key to GitHub

### Step 1: List Your Keys

```bash
gpg --list-secret-keys --keyid-format=long
```

Note your GPG key ID (the part after `rsa4096/`).

### Step 2: Export Your Public Key

Export the public key in ASCII armor format:

```bash
gpg --armor --export YOUR_KEY_ID
```

Example:

```bash
gpg --armor --export 3AA5C34371567BD2
```

This outputs your public key starting with `-----BEGIN PGP PUBLIC KEY BLOCK-----`.

### Step 3: Copy the Public Key

Copy the entire public key output, including the BEGIN and END lines:

```bash
# On Linux/macOS, pipe to clipboard (if xclip/pbcopy available)
gpg --armor --export YOUR_KEY_ID | pbcopy  # macOS
gpg --armor --export YOUR_KEY_ID | xclip -selection clipboard  # Linux

# Or manually copy from terminal output
gpg --armor --export YOUR_KEY_ID
```

### Step 4: Add to GitHub

1. Go to [GitHub.com](https://github.com)
2. Click your profile picture → **Settings**
3. In the left sidebar, click **SSH and GPG keys**
4. Click **New GPG key**
5. In the "Title" field, add a descriptive label (e.g., "Personal Laptop GPG Key")
6. Paste your GPG public key into the "Key" field
7. Click **Add GPG key**
8. Confirm with your GitHub password if prompted

## Configuring Git to Use GPG

### Set Your GPG Key in Git

Configure Git to use your GPG key for signing:

```bash
# Set the GPG key for signing
git config --global user.signingkey YOUR_KEY_ID

# Example
git config --global user.signingkey 3AA5C34371567BD2
```

### Configure Git to Use gpg2 (if needed)

If you're using `gpg2`:

```bash
git config --global gpg.program gpg2
```

### Set Git Email to Match GPG Key

Ensure your Git email matches the email in your GPG key:

```bash
git config --global user.email "your_email@example.com"
```

## Signing Commits and Tags

### Sign Individual Commits

Sign a single commit with the `-S` flag:

```bash
git commit -S -m "Your commit message"
```

### Enable Automatic Commit Signing

Configure Git to automatically sign all commits:

```bash
git config --global commit.gpgsign true
```

Now all commits will be signed automatically:

```bash
git commit -m "Your commit message"  # Automatically signed
```

### Sign Tags

Create a signed tag:

```bash
git tag -s v1.0.0 -m "Release version 1.0.0"
```

### Verify Signed Commits

Verify commit signatures:

```bash
# Verify the last commit
git verify-commit HEAD

# View commit signature information
git log --show-signature -1
```

## Refreshing GPG Keys

GPG keys can expire or be updated. Regularly refresh your keys from keyservers to ensure you have the latest versions.

### Refresh All Keys from Keyserver

Refresh all keys in your keyring from the OpenPGP keyserver:

```bash
gpg --keyserver hkps://keys.openpgp.org --refresh-keys
```

This command:

- Connects to the secure keyserver at `keys.openpgp.org` over HTTPS (hkps)
- Updates all keys in your local keyring
- Retrieves any revocations or updates to existing keys

### Refresh a Specific Key

Refresh a specific key by its ID:

```bash
gpg --keyserver hkps://keys.openpgp.org --recv-keys YOUR_KEY_ID
```

### Using Alternative Keyservers

You can use different keyservers if needed:

```bash
# Ubuntu keyserver
gpg --keyserver hkps://keyserver.ubuntu.com --refresh-keys

# MIT keyserver
gpg --keyserver hkps://pgp.mit.edu --refresh-keys
```

### Set Default Keyserver

Configure your default keyserver in `~/.gnupg/gpg.conf`:

```bash
# Edit GPG configuration
echo "keyserver hkps://keys.openpgp.org" >> ~/.gnupg/gpg.conf
```

Now you can refresh keys without specifying the keyserver:

```bash
gpg --refresh-keys
```

## Managing GPG Keys

### List All Keys

```bash
# List public keys
gpg --list-keys

# List secret (private) keys
gpg --list-secret-keys --keyid-format=long
```

### Export Keys for Backup

**Public key:**

```bash
gpg --armor --export YOUR_KEY_ID > public-key.asc
```

**Private key (keep secure!):**

```bash
gpg --armor --export-secret-keys YOUR_KEY_ID > private-key.asc
```

⚠️ **Security Warning**: Keep your private key backup in a secure location. Anyone with access to your private key can impersonate you.

### Import Keys

Import keys from a file:

```bash
# Import public key
gpg --import public-key.asc

# Import private key
gpg --import private-key.asc
```

### Delete Keys

**Delete public key:**

```bash
gpg --delete-key YOUR_KEY_ID
```

**Delete private key:**

```bash
gpg --delete-secret-key YOUR_KEY_ID
```

### Extend Key Expiration

If your key is about to expire:

```bash
# Edit the key
gpg --edit-key YOUR_KEY_ID

# In the GPG prompt
gpg> expire
# Follow prompts to set new expiration
gpg> save
```

After extending expiration, re-export and update the key on GitHub.

### Revoke a Key

If your key is compromised:

```bash
# Generate a revocation certificate
gpg --output revoke.asc --gen-revoke YOUR_KEY_ID

# Import the revocation certificate
gpg --import revoke.asc

# Publish to keyserver
gpg --keyserver hkps://keys.openpgp.org --send-keys YOUR_KEY_ID
```

## Troubleshooting

### GPG Agent Issues

If commits fail to sign:

**Restart GPG agent:**

```bash
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**Test GPG signing:**

```bash
echo "test" | gpg --clearsign
```

### TTY Error

If you get "inappropriate ioctl for device" error:

```bash
export GPG_TTY=$(tty)
```

Add to your shell configuration file (`~/.bashrc`, `~/.zshrc`):

```bash
export GPG_TTY=$(tty)
```

### Passphrase Prompt Issues

**On Linux (using gpg-agent):**

```bash
# Install pinentry
sudo apt-get install pinentry-tty  # or pinentry-gtk, pinentry-qt

# Configure pinentry in ~/.gnupg/gpg-agent.conf
echo "pinentry-program /usr/bin/pinentry-tty" > ~/.gnupg/gpg-agent.conf

# Reload agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**On macOS:**

```bash
brew install pinentry-mac
echo "pinentry-program /opt/homebrew/bin/pinentry-mac" > ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

### Commit Not Showing as Verified on GitHub

**Check the following:**

1. **Email matches:**

   ```bash
   # Check Git email
   git config user.email
   
   # Check GPG key email
   gpg --list-secret-keys --keyid-format=long
   ```

   These must match exactly.

2. **Key added to GitHub:**

   - Verify at [GitHub GPG Keys](https://github.com/settings/keys)

3. **Key not expired:**

   ```bash
   gpg --list-keys YOUR_KEY_ID
   ```

4. **Correct key used:**

   ```bash
   git config user.signingkey
   ```

### Failed to Sign Data Error

If you see "gpg failed to sign the data":

```bash
# Check GPG version
gpg --version

# Test GPG signing
echo "test" | gpg --clearsign

# Configure Git to use correct GPG program
git config --global gpg.program gpg  # or gpg2
```

## Best Practices

### Security Recommendations

1. **Use strong passphrases** - Protect your GPG key with a strong, unique passphrase
2. **Set expiration dates** - Use 1-2 year expiration periods and renew regularly
3. **Back up keys securely** - Store encrypted backups offline
4. **Use hardware tokens** - Consider YubiKey or other hardware security keys
5. **Revoke compromised keys immediately** - Have a revocation certificate ready
6. **One key per device** - Consider separate keys for different machines
7. **Regularly refresh keys** - Run `gpg --refresh-keys` periodically to get updates

### Recommended GPG Configuration

Create or edit `~/.gnupg/gpg.conf`:

```text
# Use the secure keyserver
keyserver hkps://keys.openpgp.org

# Display long key IDs
keyid-format 0xlong

# Display fingerprints
with-fingerprint

# Use strong digest algorithms
personal-digest-preferences SHA512 SHA384 SHA256

# Use strong cipher algorithms
personal-cipher-preferences AES256 AES192 AES

# Disable weak algorithms
disable-cipher-algo 3DES
weak-digest SHA1
```

### Git GPG Configuration

Recommended Git GPG settings:

```bash
# Sign all commits by default
git config --global commit.gpgsign true

# Sign all tags by default
git config --global tag.gpgsign true

# Set your GPG key
git config --global user.signingkey YOUR_KEY_ID

# Use correct email
git config --global user.email "your_email@example.com"
```

## Additional Resources

### Official Documentation

- [GitHub GPG Documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)
- [Git Tools - Signing Your Work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)

### Keyserver Resources

- [keys.openpgp.org](https://keys.openpgp.org/) - Modern OpenPGP keyserver
- [Keyserver Best Practices](https://keys.openpgp.org/about/usage)

### Related Topics

- [GitHub SSH Documentation](CONNECTING_TO_GITHUB_WITH_SSH.md)
- [Signed Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Security Best Practices](SECURITY_BEST_PRACTICES.md)

## Summary

You've successfully set up GPG key management for GitHub! You can now:

- ✅ Generate and manage GPG keys
- ✅ Sign commits and tags cryptographically
- ✅ Verify commit authenticity on GitHub
- ✅ Refresh and update keys from keyservers
- ✅ Maintain secure key management practices

For issues or questions, refer to the [Troubleshooting](#troubleshooting) section or consult [GitHub's official documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification).
