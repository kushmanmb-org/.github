# Contributing to kushmanmb-org

Thank you for your interest in contributing to our blockchain development tools and utilities! We welcome contributions from the community and are pleased that you're considering helping us improve our projects.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Security Vulnerabilities](#security-vulnerabilities)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** you want to contribute to
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
   cd REPOSITORY_NAME
   ```

3. **Create a new branch** for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Documentation

Documentation improvements are always welcome! This includes:

- Fixing typos or clarifying existing documentation
- Adding examples and use cases
- Improving installation or setup instructions
- Translating documentation

### Code Contributions

We accept contributions for:

- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test coverage improvements

## Development Guidelines

### General Principles

- **Security First**: Never commit API keys, private keys, or sensitive credentials to version control
- **Code Quality**: Write clean, readable, and maintainable code
- **Testing**: Include tests for new features or bug fixes when applicable
- **Documentation**: Update documentation to reflect your changes

### Language-Specific Guidelines

#### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

#### JavaScript/Node.js

- Use modern ES6+ syntax
- Follow consistent naming conventions
- Use async/await for asynchronous operations
- Add JSDoc comments for functions

#### Shell Scripts

- Use `#!/usr/bin/env bash` shebang
- Quote variables to prevent word splitting
- Use meaningful function names
- Add comments for complex logic

### Security Best Practices

Before submitting code:

- ✅ Remove any hardcoded credentials or API keys
- ✅ Use environment variables for sensitive data
- ✅ Review [Security Best Practices](SECURITY_BEST_PRACTICES.md)
- ✅ Ensure no private keys or wallet addresses are exposed
- ✅ Validate all user inputs
- ✅ Follow secure coding practices for blockchain interactions

## Submitting Changes

### Pull Request Process

1. **Update documentation** if your changes affect user-facing features
2. **Add tests** to verify your changes work as expected
3. **Ensure all tests pass** before submitting
4. **Update the README.md** with details of changes if applicable
5. **Commit your changes** with clear, descriptive commit messages:

   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** from your fork to our repository

### Commit Message Guidelines

Write clear, concise commit messages:

- Use the imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add a blank line followed by a detailed description if needed
- Reference related issues (e.g., "Fixes #123")

**Examples:**

```text
Add Etherscan API retry logic

- Implement exponential backoff for rate limiting
- Add configurable retry attempts
- Update documentation with retry examples

Fixes #456
```

### Pull Request Requirements

- Provide a clear description of the changes
- Link to any related issues
- Include screenshots for UI changes
- Ensure CI/CD checks pass
- Be responsive to review feedback

## Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title**: Briefly describe the issue
- **Description**: Detailed explanation of the bug
- **Steps to reproduce**: How to recreate the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment details**:
  - OS and version
  - Programming language version (Python, Node.js, etc.)
  - Relevant dependencies
- **Screenshots or logs**: If applicable

**Example:**

```markdown
## Bug: Token balance query returns null for valid address

**Steps to reproduce:**
1. Run `./query-token-balance.sh --apikey YOUR_KEY`
2. Use address: 0x983e3660c0bE01991785F80f266A84B911ab59b0

**Expected:** Token balance data
**Actual:** Returns null

**Environment:**
- OS: Ubuntu 22.04
- Bash: 5.1.16
- API: Etherscan v2
```

## Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:

- **Clear title**: Describe the enhancement
- **Use case**: Why this feature would be useful
- **Proposed solution**: How it could be implemented
- **Alternatives**: Other approaches you've considered
- **Additional context**: Any other relevant information

## Security Vulnerabilities

**Do not report security vulnerabilities through public GitHub issues.**

Please follow our [Security Policy](SECURITY.md) to report security issues responsibly. We take security seriously and will respond promptly to legitimate security concerns.

## Questions?

If you have questions about contributing, feel free to:

- Open a GitHub Discussion
- Create an issue with the "question" label
- Refer to our [Support Guide](SUPPORT.md)

## Recognition

Contributors who submit accepted pull requests will be recognized in our release notes and documentation. We appreciate every contribution, no matter how small!

---

Thank you for contributing to kushmanmb-org! Together, we're building better blockchain development tools for everyone.
