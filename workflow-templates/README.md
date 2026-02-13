# Workflow Templates

This directory contains reusable GitHub Actions workflow templates.

## Workflows and Permissions

### build-lint-test.yml

**Purpose**: Runs build, lint, and test processes for pull requests and main branch pushes (JavaScript/TypeScript).

**Permissions**:

- `contents: read` - Read-only access to repository contents (explicit for security best practice)

This workflow does not modify the repository, so it only requires read access.

### go-build-lint-test.yml

**Purpose**: Runs build, lint, and test processes for Go projects with support for multiple Go versions and Makefile-based builds.

**Permissions**:

- `contents: read` - Read-only access to repository contents (explicit for security best practice)

This workflow does not modify the repository, so it only requires read access.

### ruby-build-lint-test.yml

**Purpose**: Runs build, lint, and test processes for Ruby projects with support for multiple Ruby versions and Bundler.

**Permissions**:

- `contents: read` - Read-only access to repository contents (explicit for security best practice)

This workflow does not modify the repository, so it only requires read access.

### balance-monitor.yml

**Purpose**: Monitors cryptocurrency balances across multiple chains (Ethereum, Base, Polygon, Arbitrum, Optimism).

**Permissions**:

- `contents: read` - Read-only access to repository contents (explicit for security best practice)

This workflow monitors balances and generates reports but does not modify the repository.

### crypto-consolidation.yml

**Purpose**: Safely consolidates cryptocurrency assets to kushmanmb.base.eth with manual approval gates.

**Permissions**:

- `contents: read` - Read-only access to repository contents
- `issues: write` - Required for tracking approval requests

This workflow requires write access to issues for the approval tracking system, but maintains read-only access to repository contents for security.

### create-release-pr.yml

**Purpose**: Creates a release pull request with version bumps.

**Permissions**:

- `contents: write` - Required to create branches and commits
- `pull-requests: write` - Required to create pull requests

These write permissions are necessary for the workflow to function. Cannot be set to read-only.

### publish-release.yml

**Purpose**: Publishes a release when a release PR is merged.

**Permissions**:

- `contents: write` - Required to create releases and tags

This write permission is necessary for the workflow to function. Cannot be set to read-only.

## Security Best Practices

Following GitHub Actions security best practices:

1. Workflows that don't need write access have explicit `contents: read` permissions
2. Workflows that require write access have only the minimum permissions needed
3. All permissions are explicitly declared for clarity and security

## Can I Remove Read-Only Permissions?

**Answer**: It depends on the workflow:

- **build-lint-test.yml**: Has explicit read-only permissions (`contents: read`) for security. You could remove this line to use default permissions, but explicit read-only is more secure.
  
- **create-release-pr.yml** and **publish-release.yml**: Cannot be set to read-only as they need write permissions to create PRs and releases. Removing these permissions would break the workflows.
