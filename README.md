# .github Repository

This repository contains organization-wide configuration, templates, and utilities for blockchain-related operations.

## Contents

### Blockchain Documentation
- **[Multisig Wallet ABI](MULTISIG_WALLET_README.md)** - Documentation for Ethereum multisignature wallet smart contract
- **[Etherscan Token Balance API](ETHERSCAN_TOKEN_BALANCE.md)** - Guide for querying ERC-20 token balances using Etherscan API v2

### Utility Scripts
- **[query-token-balance.sh](query-token-balance.sh)** - Bash script for querying token balances
- **[query-token-balance.py](query-token-balance.py)** - Python script for querying token balances

### Blockchain Resources
- **[blockchain-address.json](blockchain-address.json)** - Blockchain address information
- **[multisig-wallet.abi.json](multisig-wallet.abi.json)** - ABI definition for multisig wallet contract

## Quick Start

### Query Token Balances

You can query ERC-20 token balances for any Ethereum address using the provided scripts.

#### Using Bash Script
```bash
./query-token-balance.sh --apikey YOUR_API_KEY
```

#### Using Python Script
```bash
./query-token-balance.py --apikey YOUR_API_KEY --pretty
```

#### Using cURL
```bash
curl "https://api.etherscan.io/v2/api?chainid=1&module=account&action=addresstokenbalance&address=0x983e3660c0bE01991785F80f266A84B911ab59b0&page=1&offset=100&apikey=YourApiKeyToken"
```

For detailed usage and examples, see [ETHERSCAN_TOKEN_BALANCE.md](ETHERSCAN_TOKEN_BALANCE.md).

## Addresses

- **Token Balance Query Address**: `0x983e3660c0bE01991785F80f266A84B911ab59b0`
- **Multisig Wallet Owner**: `0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7`

## Community Files

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Funding Information](FUNDING.yml)

## Workflow Templates

The `workflow-templates/` directory contains GitHub Actions workflow templates for:
- Build, lint, and test workflows
- Release creation and publishing

## License

See individual files for licensing information.
