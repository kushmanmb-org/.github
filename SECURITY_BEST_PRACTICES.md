# Security Best Practices for Private Data

This document outlines best practices for handling sensitive data in this repository.

## 🔒 Protecting API Keys and Credentials

### Never Commit Secrets
**NEVER** commit the following to version control:
- API keys (Etherscan, Infura, Alchemy, etc.)
- Private keys or mnemonics
- Passwords or authentication tokens
- Database credentials
- Session secrets
- Any sensitive configuration

### Recommended Approaches

#### 1. Environment Variables (Recommended)
Store sensitive data in environment variables:

```bash
# Set environment variable
export ETHERSCAN_API_KEY="your-api-key-here"

# Use in scripts
node query-token-balance.js --apikey "$ETHERSCAN_API_KEY"
```

Create a `.env` file for local development (already in .gitignore):
```bash
# .env (this file is gitignored)
ETHERSCAN_API_KEY=your-api-key-here
INFURA_PROJECT_ID=your-project-id
```

#### 2. Command-Line Arguments
Pass secrets as command-line arguments:
```bash
node query-token-balance.js --apikey YOUR_API_KEY_HERE
```

#### 3. Local Configuration Files
Use the provided example configuration files and add your API keys locally:

**For Etherscan API:**
```bash
# The etherscan-api-config.json file is gitignored to protect your API key
# Use it to store your actual API key (never commit this file)
# The example file shows the expected format without sensitive data
cat etherscan-api-config.example.json

# You can also create additional local config files (gitignored by *.local.json pattern)
cp etherscan-api-config.json etherscan-api-config.local.json
# Edit the file to add your API key
```

**Important:** The `etherscan-api-config.json` file is now gitignored to prevent accidental commits of API keys. Always use environment variables or command-line arguments when possible.

## 📋 .gitignore Protection

Our `.gitignore` file protects the following types of sensitive data:

### Environment Files
- `.env`, `.env.*`, `.env.local`, `.env.development`, `.env.production`, etc.
- `*.local.json`, `*.local.config`, `config.local.*`

### API Keys and Credentials
- `*.apikey`, `*.api-key`, `*apikey*`, `*api-key*`
- `api-keys.*`, `apikeys.*`
- `*credentials*`, `*.credentials`
- `secrets.*`, `*secrets.json`, `*secrets.yml`
- `etherscan-api-config.json`, `*-api-config.json` (API configuration files)

### Private Keys and Certificates
- `*.key`, `*.pem`, `*.p12`, `*.pfx`, `*.cer`, `*.crt`
- `private-key*`, `*private-key*`, `privatekey*`

### Blockchain Wallets
- `keystore/`, `*keystore*`
- `wallet.dat`, `*.wallet`
- `mnemonic.*`, `*mnemonic*`
- `seed.*`, `*seed.txt`

### Tokens and Sessions
- `*.token`, `*token.txt`, `auth-token*`
- `session.*`, `*.session`

### CI/CD Secrets
- `.secrets/`, `secrets/`, `*secret.env`

### Database and Backup Files
- `*.db`, `*.sqlite`, `*.sqlite3`
- `*.backup`, `*.bak`, `*.old`, `*-backup.*`

## 🛡️ Security Checklist

Before committing code, verify:

- [ ] No hardcoded API keys in source files
- [ ] No private keys or mnemonics in code or comments
- [ ] No passwords or credentials in configuration files
- [ ] All sensitive files match .gitignore patterns
- [ ] Example files use placeholders (e.g., "YourApiKeyToken")
- [ ] Documentation references environment variables for secrets

## 🔍 Checking for Exposed Secrets

### Before Committing
```bash
# Check what files will be committed
git status

# Review changes for secrets
git diff

# Verify .gitignore is working
git check-ignore -v <filename>
```

### After Committing (if you accidentally committed a secret)
1. **Revoke the exposed secret immediately** (regenerate API key, rotate credentials)
2. Remove the secret from Git history using `git filter-branch` or BFG Repo-Cleaner
3. Force push the cleaned history
4. Update the secret everywhere it's used

## 📚 Additional Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [12-Factor App: Config](https://12factor.net/config)

## 🎯 Quick Reference

### ✅ Good Practices
```javascript
// Use environment variable
const apiKey = process.env.ETHERSCAN_API_KEY;

// Load from gitignored local config
const config = require('./config.local.json');

// Pass as CLI argument
// node script.js --apikey $ETHERSCAN_API_KEY
```

### ❌ Bad Practices
```javascript
// NEVER hardcode API keys
const apiKey = "ZITG8EMXRFSWU2CDTNT4XEI7GDYB2JBMGD"; // ❌ DON'T DO THIS

// NEVER commit config with real keys
const config = {
  apikey: "real-api-key-here" // ❌ DON'T DO THIS
};
```

## 🚨 If You Find a Committed Secret

If you discover a committed secret:
1. **Report it immediately** via GitHub Security Advisory
2. **Do not share** the secret in issues or pull requests
3. **Revoke** the exposed credential immediately
4. **Follow** the cleanup process above

---

*Last Updated: 2026-02-12*
