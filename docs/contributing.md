---
layout: default
title: Contributing Guide
---

# Contributing to .github

Thank you for your interest in contributing to our organization-wide configuration and utilities repository!

## How to Contribute

### Reporting Issues

1. **Check Existing Issues**: Search existing issues to avoid duplicates
2. **Create New Issue**: Use issue templates when available
3. **Provide Details**: Include steps to reproduce, expected behavior, and actual behavior

### Submitting Changes

1. **Fork the Repository**: Create your own fork
2. **Create a Branch**: Use descriptive branch names (`feature/new-utility`, `fix/security-issue`)
3. **Make Changes**: Follow coding standards and best practices
4. **Test Thoroughly**: Ensure all tests pass and add new tests if needed
5. **Commit with Sign-off**: Use clear commit messages
6. **Submit Pull Request**: Reference related issues

### Pull Request Process

1. **Update Documentation**: Update README.md and relevant docs
2. **Add Tests**: Include tests for new functionality
3. **Security Review**: Ensure no secrets or sensitive data are committed
4. **Code Review**: Address feedback from maintainers
5. **Merge**: Maintainers will merge after approval

## Coding Standards

### General Guidelines

- Follow existing code style and patterns
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused

### Security Requirements

- **Never commit secrets**: Use environment variables or `.gitignore` patterns
- **Validate input**: Always validate and sanitize user input
- **Use parameterized queries**: Prevent SQL injection
- **Follow least privilege**: Use minimal necessary permissions
- **Review dependencies**: Check for known vulnerabilities

### Documentation Standards

- Update README.md for user-facing changes
- Add inline documentation for complex code
- Include usage examples
- Document API changes

## Testing

### Running Tests

```bash
# JavaScript tests
npm test

# Python tests  
python3 -m pytest

# Shell script validation
shellcheck *.sh
```

### Writing Tests

- Write tests for new features
- Ensure tests are deterministic
- Mock external dependencies
- Test edge cases and error conditions

## Code Review Guidelines

### For Contributors

- Be open to feedback
- Respond promptly to comments
- Make requested changes
- Ask questions if unclear

### For Reviewers

- Be constructive and respectful
- Focus on code quality and security
- Suggest improvements
- Approve when ready

## Community Guidelines

Please read and follow our [Code of Conduct](../CODE_OF_CONDUCT.md).

### Expected Behavior

- Be respectful and inclusive
- Collaborate constructively
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

## Getting Help

- **Documentation**: Check README.md and related docs
- **Issues**: Search existing issues or create new one
- **Discussions**: Use GitHub Discussions for questions
- **Support**: See [SUPPORT.md](../SUPPORT.md) for support channels

## License

By contributing, you agree that your contributions will be licensed under the same license as the repository.

Thank you for contributing! 🎉
