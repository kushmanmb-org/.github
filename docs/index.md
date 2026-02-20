---
layout: default
title: Home
---

# .github Repository

Welcome to the kushmanmb-org/.github repository documentation. This repository contains organization-wide configuration, templates, and utilities for blockchain-related operations.

## 🔒 Security and Privacy

This repository implements industry-standard security practices following guidance from the Linux Foundation, GitHub Security Lab, and OpenSSF.

### Key Security Features

- **Automated Dependency Updates**: Dependabot monitors and updates dependencies
- **Security Scanning**: CodeQL and secret scanning workflows detect vulnerabilities
- **Branch Protection**: Required reviews and status checks on main branch
- **Workflow Security**: Script injection prevention and minimal permissions
- **Commit Signing**: GPG verification for all commits (recommended)
- **Secret Management**: Comprehensive .gitignore patterns and environment variable usage

## 📚 Documentation

### GitHub Documentation

- [Git Key-Pairs Guide](../GIT_KEY_PAIRS.md) - SSH and GPG key-pairs for Git
- [Connecting to GitHub with SSH](../CONNECTING_TO_GITHUB_WITH_SSH.md) - SSH authentication setup
- [GPG Key Management](../GPG_KEY_MANAGEMENT.md) - Managing GPG keys and signing commits
- [Git POW Verification](../GIT_POW_VERIFICATION.md) - Verify Git commit signatures

### Blockchain Documentation

- [ENS Creator Verification](../ENS_VERIFICATION.md) - Verify kushmanmb.base.eth creator status
- [Cryptocurrency Consolidation](../CRYPTO_CONSOLIDATION.md) - Automated crypto asset consolidation
- [Transaction Hash Verification](../TX_HASH_VERIFICATION.md) - Verify blockchain transaction hashes
- [Address Labels Configuration](../ADDRESS_LABELS.md) - Blockchain address labels and metadata
- [Blockchain JSON-RPC Server](../BLOCKCHAIN_RPC.md) - JSON-RPC 2.0 server for blockchain operations
- [Multisig Wallet ABI](../MULTISIG_WALLET_README.md) - Ethereum multisignature wallet documentation
- [Etherscan Token Balance API](../ETHERSCAN_TOKEN_BALANCE.md) - Query ERC-20 token balances
- [Validator Rewards API](../VALIDATOR_REWARDS.md) - Query Ethereum validator rewards
- [Bitcoin Difficulty Adjustment API](../MEMPOOL_DIFFICULTY.md) - Bitcoin difficulty data
- [Solscan API](../SOLSCAN_API.md) - Query Solana account transfer history

### Security Documentation

- [Security Policy](security.md) - Vulnerability reporting and disclosure
- [Security Best Practices](../SECURITY_BEST_PRACTICES.md) - Protecting API keys and sensitive data
- [Workflow Security](../WORKFLOW_SECURITY.md) - GitHub Actions security guidelines
- [Branch Protection](../BRANCH_PROTECTION.md) - Repository security configuration

## 🚀 Quick Start

### ENS Creator Verification

Verify and announce kushmanmb.base.eth creator status on Base network:

```bash
./verify_ens_creator.py --name kushmanmb.base.eth
./verify_ens_creator.py --announce
./verify_ens_creator.py --json --pretty
```

### Git POW Verification

Verify Git commit signatures using GPG:

```bash
./git_pow_verifier.py --commit HEAD
./git_pow_verifier.py --commit abc123def456
./git_pow_verifier.py --file commits-example.json
```

### Transaction Hash Verification

Verify blockchain transaction hashes:

```bash
./verify_tx_hash.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000
./verify_tx_hash.py --file tx-hashes-example.json
```

## 🌐 Addresses

- **Primary Consolidation Address**: `kushmanmb.base.eth`
- **Token Balance Query Address**: `0x983e3660c0bE01991785F80f266A84B911ab59b0`
- **Multisig Wallet Owner**: `0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7`
- **Labeled Address (kushmanmb10)**: `0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43`

## 🤝 Community

- [Code of Conduct](../CODE_OF_CONDUCT.md)
- [Contributing Guide](contributing.md)
- [Support](../SUPPORT.md)
- [Funding Information](../FUNDING.yml)

## 📦 Workflow Templates

The `workflow-templates/` directory contains GitHub Actions workflow templates for:

- JavaScript/TypeScript Projects
- Go Projects  
- Ruby Projects
- Cryptocurrency Operations
- Release creation and publishing

## 📄 License

See individual files for licensing information.
