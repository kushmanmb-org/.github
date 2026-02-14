# Jest and Babel Security Configuration

This document outlines the security best practices implemented in the Jest and Babel configuration files for this repository.

## Overview

The repository has been configured with Jest for testing and Babel for JavaScript transpilation, following security and privacy best practices to prevent accidental exposure of sensitive data.

## Configuration Files

### jest.config.js

The Jest configuration includes several security-focused features:

#### Excluded Directories and Files

The following patterns are excluded from test discovery and coverage collection to prevent exposure of sensitive data:

- **Sensitive Directories:**
  - `node_modules/` - Third-party dependencies
  - `.secrets/`, `secrets/` - Secret storage directories
  - `keystore/` - Blockchain wallet keystores
  - `deployments/` - Smart contract deployment info
  - `chaindata/` - Private blockchain data

- **Sensitive File Patterns:**
  - `*.local.*` - Local configuration files
  - `*-config-private.*` - Private configuration files
  - `*credentials*` - Credential files
  - `*apikey*`, `*api-key*` - API key files
  - `*.backup`, `*.bak`, `*.old` - Backup files that may contain sensitive data

#### Security Features

1. **Mock Isolation:** `clearMocks`, `restoreMocks`, and `resetMocks` are all enabled to ensure no data leaks between tests
2. **Test Timeout:** 30-second timeout prevents hanging tests and potential resource leaks
3. **Open Handle Detection:** Warns about unclosed connections and file handles
4. **Force Exit:** Ensures Jest exits cleanly after tests complete

#### Coverage Configuration

Coverage reports are generated in the `coverage/` directory (gitignored) and exclude:
- Configuration files that might contain sensitive patterns
- Example files
- Private/local configuration files
- Sensitive directories

### babel.config.js

The Babel configuration focuses on security and preventing code exposure:

#### Environment-Specific Configuration

1. **Production Environment:**
   - Source maps are **disabled** (`sourceMaps: false`) to prevent code exposure
   - Comments are removed to reduce code size and prevent metadata leaks
   - Compact output for minimal file size

2. **Development Environment:**
   - Source maps are **inline only** (never written to separate files)
   - Function names retained for debugging

3. **Test Environment:**
   - Uses current Node.js version for optimal compatibility
   - CommonJS modules for Jest compatibility

#### Ignored Patterns

Babel will not transform files matching these security-sensitive patterns:
- Secret storage directories and files
- API key and credential files
- Local and private configuration files
- Backup files
- Keystore directories

#### Target Configuration

- Targets Node.js 18+ (matching `package.json` engines requirement)
- Uses modern JavaScript features natively supported by Node 18
- No unnecessary polyfills that could increase attack surface

### package.json

The package.json has been updated with security in mind:

#### Key Security Settings

1. **Private Package:** `"private": true` prevents accidental publishing to npm
2. **Engine Constraint:** `"node": ">=18.0.0"` ensures modern, supported Node.js versions
3. **No Hardcoded Credentials:** All API keys must come from environment variables or CLI arguments

#### Test Scripts

- `npm test` - Run tests with Jest
- `npm run test:coverage` - Run tests with coverage report
- `npm run test:watch` - Watch mode for development
- `npm run test:ci` - CI-optimized test run with coverage
- `npm run security:audit` - Check for vulnerable dependencies
- `npm run security:check` - Check for outdated packages

## Best Practices

### When Writing Tests

1. **Never hardcode sensitive data** in test files
2. **Use mock data** for API keys, addresses, and credentials
3. **Clean up after tests** (close connections, clear timers, etc.)
4. **Avoid testing with real API endpoints** - use mocks or local test servers

### Example of Secure Test Data

```javascript
// ✅ Good - Mock data
const mockApiKey = 'TEST_API_KEY_FOR_TESTING';
const mockAddress = '0x0000000000000000000000000000000000000000';

// ❌ Bad - Real credentials
const apiKey = 'ZITG8EMXRFSWU2CDTNT4XEI7GDYB2JBMGD'; // Never do this!
```

### Environment Variables in Tests

When tests need environment variables:

```javascript
// Save original value
const originalApiKey = process.env.ETHERSCAN_API_KEY;

beforeEach(() => {
  // Set test value
  process.env.ETHERSCAN_API_KEY = 'TEST_KEY';
});

afterEach(() => {
  // Restore original value
  if (originalApiKey) {
    process.env.ETHERSCAN_API_KEY = originalApiKey;
  } else {
    delete process.env.ETHERSCAN_API_KEY;
  }
});
```

## Coverage Reports

Coverage reports are generated in the `coverage/` directory and are automatically gitignored. These reports should:

1. **Never be committed** to the repository
2. **Not include sensitive files** in the coverage analysis
3. **Be reviewed locally** to identify untested code paths

## Security Checklist

Before committing:

- [ ] No hardcoded API keys or credentials in tests
- [ ] All sensitive files are in `.gitignore`
- [ ] Tests use mock data for sensitive operations
- [ ] Coverage reports are gitignored
- [ ] No real blockchain addresses or private keys in test fixtures
- [ ] Environment variables are properly mocked and restored

## CI/CD Considerations

When running tests in CI/CD:

1. **Use the `test:ci` script** for optimized CI performance
2. **Store secrets in CI environment variables**, not in code
3. **Review coverage reports** but don't commit them
4. **Run `npm audit`** regularly to check for vulnerabilities

## Updating Dependencies

When updating Jest or Babel:

1. Review the changelog for security fixes
2. Run `npm audit` to check for vulnerabilities
3. Test that security configurations still work
4. Update this documentation if needed

## Resources

- [Jest Security Best Practices](https://jestjs.io/docs/configuration)
- [Babel Security Guidelines](https://babeljs.io/docs/en/config-files)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- Repository: [SECURITY_BEST_PRACTICES.md](./SECURITY_BEST_PRACTICES.md)

---

*Last Updated: 2026-02-14*
