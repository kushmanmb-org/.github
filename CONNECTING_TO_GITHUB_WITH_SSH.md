# Connecting to GitHub with SSH

This guide walks you through setting up SSH authentication for GitHub, allowing you to securely connect and authenticate without entering your username and password each time.

## Overview

SSH (Secure Shell) keys provide a secure way to authenticate with GitHub. Once set up, you can push, pull, and interact with GitHub repositories without entering credentials repeatedly.

## Prerequisites

- Git installed on your computer
- A GitHub account
- Terminal/Command Prompt access

## Table of Contents

1. [Checking for Existing SSH Keys](#checking-for-existing-ssh-keys)
2. [Generating a New SSH Key](#generating-a-new-ssh-key)
3. [Adding SSH Key to SSH Agent](#adding-ssh-key-to-ssh-agent)
4. [Adding SSH Key to GitHub](#adding-ssh-key-to-github)
5. [Testing Your SSH Connection](#testing-your-ssh-connection)
6. [Using SSH with Git](#using-ssh-with-git)
7. [Troubleshooting](#troubleshooting)

## Checking for Existing SSH Keys

Before generating a new SSH key, check if you already have one:

```bash
# List existing SSH keys
ls -al ~/.ssh
```

Look for files named:
- `id_rsa.pub`
- `id_ecdsa.pub`
- `id_ed25519.pub`

If you see any of these files, you already have SSH keys and can skip to [Adding SSH Key to GitHub](#adding-ssh-key-to-github).

## Generating a New SSH Key

### Using ED25519 (Recommended)

ED25519 is the recommended algorithm for new SSH keys due to its security and performance:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### Using RSA (Legacy Systems)

If your system doesn't support ED25519, use RSA with 4096 bits:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### Key Generation Steps

1. When prompted with "Enter a file in which to save the key", press **Enter** to accept the default location
2. At the passphrase prompt, enter a secure passphrase (recommended) or press **Enter** for no passphrase
3. Confirm the passphrase

**Example output:**
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/user/.ssh/id_ed25519
Your public key has been saved in /home/user/.ssh/id_ed25519.pub
```

## Adding SSH Key to SSH Agent

### Start the SSH Agent

**On Linux/macOS:**
```bash
eval "$(ssh-agent -s)"
```

**On Windows (Git Bash):**
```bash
eval "$(ssh-agent -s)"
```

**On Windows (PowerShell):**
```powershell
# Run as Administrator
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
```

### Add Your SSH Key

**For ED25519:**
```bash
ssh-add ~/.ssh/id_ed25519
```

**For RSA:**
```bash
ssh-add ~/.ssh/id_rsa
```

### macOS Keychain Integration

On macOS, add your SSH key to the keychain:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

For older macOS versions:
```bash
ssh-add -K ~/.ssh/id_ed25519
```

## Adding SSH Key to GitHub

### Copy Your Public Key

**On Linux/macOS:**
```bash
# For ED25519
cat ~/.ssh/id_ed25519.pub

# For RSA
cat ~/.ssh/id_rsa.pub
```

**On Windows (Git Bash):**
```bash
# For ED25519
cat ~/.ssh/id_ed25519.pub

# For RSA
cat ~/.ssh/id_rsa.pub
```

**On Windows (PowerShell):**
```powershell
# For ED25519
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard

# For RSA
Get-Content ~/.ssh/id_rsa.pub | Set-Clipboard
```

### Add to GitHub

1. Go to [GitHub.com](https://github.com)
2. Click your profile picture → **Settings**
3. In the left sidebar, click **SSH and GPG keys**
4. Click **New SSH key** or **Add SSH key**
5. In the "Title" field, add a descriptive label (e.g., "Personal Laptop")
6. Select **Authentication Key** as the key type
7. Paste your public key into the "Key" field
8. Click **Add SSH key**
9. Confirm with your GitHub password if prompted

## Testing Your SSH Connection

Test your SSH connection to GitHub:

```bash
ssh -T git@github.com
```

You should see a message like:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see this message, your SSH key is properly configured!

## Using SSH with Git

### Cloning a Repository with SSH

```bash
git clone git@github.com:username/repository.git
```

### Converting HTTPS to SSH for Existing Repositories

If you have a repository cloned with HTTPS, convert it to SSH:

```bash
# Check current remote URL
git remote -v

# Change to SSH
git remote set-url origin git@github.com:username/repository.git

# Verify the change
git remote -v
```

### SSH URL Format

GitHub SSH URLs follow this format:
```
git@github.com:owner/repository.git
```

Examples:
- `git@github.com:kushmanmb-org/.github.git`
- `git@github.com:octocat/Hello-World.git`

## Troubleshooting

### Permission Denied (publickey)

If you get this error:
```
Permission denied (publickey).
```

**Solutions:**

1. **Verify SSH key is added to GitHub:**
   - Check your [SSH keys on GitHub](https://github.com/settings/keys)
   - Ensure you copied the entire public key including `ssh-ed25519` or `ssh-rsa` prefix

2. **Ensure SSH agent has your key:**
   ```bash
   ssh-add -l
   ```
   If empty, add your key:
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Check SSH key file permissions:**
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   ```

### Could Not Open a Connection to Your Authentication Agent

**Solution:**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Bad Permissions Error

If you see "permissions are too open":

```bash
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 700 ~/.ssh
```

### Testing with Verbose Output

For detailed debugging information:

```bash
ssh -vT git@github.com
```

Use `-vvv` for maximum verbosity:
```bash
ssh -vvv -T git@github.com
```

### Multiple SSH Keys

If you have multiple SSH keys for different GitHub accounts:

1. Create an SSH config file:
   ```bash
   nano ~/.ssh/config
   ```

2. Add configuration:
   ```
   # Personal GitHub account
   Host github.com
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519

   # Work GitHub account
   Host github-work
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519_work
   ```

3. Clone using the appropriate host:
   ```bash
   # Personal
   git clone git@github.com:username/repo.git
   
   # Work
   git clone git@github-work:workusername/repo.git
   ```

### SSH Key Already in Use

If GitHub says your SSH key is already associated with another account:
- Each SSH key can only be associated with one GitHub account
- Generate a new SSH key for the second account
- Use SSH config to manage multiple keys (see above)

## Best Practices

### Security Recommendations

1. **Use a passphrase** - Always protect your SSH key with a strong passphrase
2. **Use ED25519** - Prefer ED25519 over RSA for new keys
3. **One key per device** - Generate unique SSH keys for each device
4. **Regular rotation** - Rotate SSH keys periodically (e.g., annually)
5. **Remove old keys** - Delete SSH keys from GitHub when you no longer use a device

### SSH Config Example

Create `~/.ssh/config` for better management:

**On macOS:**
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  AddKeysToAgent yes
  UseKeychain yes
```

**On Linux/Windows:**
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  AddKeysToAgent yes
```

## Additional Resources

### GitHub Documentation
- [GitHub SSH Documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Troubleshooting SSH](https://docs.github.com/en/authentication/troubleshooting-ssh)

### OpenSSH Documentation
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [ssh-keygen Man Page](https://man.openbsd.org/ssh-keygen)

### Related Topics
- [Using SSH over HTTPS port](https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)
- [GitHub Deploy Keys](https://docs.github.com/en/developers/overview/managing-deploy-keys)
- [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager)

## Summary

You've successfully set up SSH authentication for GitHub! You can now:
- ✅ Clone repositories using SSH URLs
- ✅ Push and pull without entering passwords
- ✅ Securely authenticate with GitHub
- ✅ Manage multiple SSH keys if needed

For issues or questions, refer to the [Troubleshooting](#troubleshooting) section or consult [GitHub's official documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
