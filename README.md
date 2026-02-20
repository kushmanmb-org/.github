# .github Repository

This repository contains organization-wide configuration, templates, and utilities for blockchain-related operations.

> 📖 **[View Documentation Site](https://kushmanmb-org.github.io/.github/)** - Browse the full documentation on GitHub Pages

## 🔒 Security and Privacy

This repository implements industry-standard security practices following guidance from the Linux Foundation, GitHub Security Lab, and OpenSSF. Key security features include:

- **Automated Dependency Updates**: Dependabot monitors and updates dependencies
- **Security Scanning**: CodeQL and secret scanning workflows detect vulnerabilities
- **Branch Protection**: Required reviews and status checks on main branch
- **Workflow Security**: Script injection prevention and minimal permissions
- **Commit Signing**: GPG verification for all commits (recommended)
- **Secret Management**: Comprehensive .gitignore patterns and environment variable usage

**📚 Security Documentation:**
- [Security Policy](SECURITY.md) - Vulnerability reporting and disclosure
- [Security Best Practices](SECURITY_BEST_PRACTICES.md) - Protecting API keys and sensitive data
- [Workflow Security](WORKFLOW_SECURITY.md) - GitHub Actions security guidelines
- [Branch Protection](BRANCH_PROTECTION.md) - Repository security configuration

## Contents

### GitHub Documentation

- **[Git Key-Pairs Guide](GIT_KEY_PAIRS.md)** - Comprehensive overview of SSH and GPG key-pairs for Git authentication and commit signing
- **[Connecting to GitHub with SSH](CONNECTING_TO_GITHUB_WITH_SSH.md)** - Complete guide for setting up SSH authentication with GitHub
- **[GPG Key Management](GPG_KEY_MANAGEMENT.md)** - Comprehensive guide for managing GPG keys, signing commits, and refreshing keys from keyservers
- **[Git POW Verification](GIT_POW_VERIFICATION.md)** - Verify Git commit signatures using GPG with secure practices

### Blockchain Documentation

- **[ENS Creator Verification](ENS_VERIFICATION.md)** - Verify and announce kushmanmb.base.eth creator status on Base network
- **[Cryptocurrency Consolidation](CRYPTO_CONSOLIDATION.md)** - Automated workflows for safely consolidating crypto assets to kushmanmb.base.eth
- **[Transaction Hash Verification](TX_HASH_VERIFICATION.md)** - Verify blockchain transaction hashes with private data protection using .gitignore
- **[Address Labels Configuration](ADDRESS_LABELS.md)** - Best practices for configuring blockchain address labels and metadata
- **[Blockchain JSON-RPC Server](BLOCKCHAIN_RPC.md)** - JSON-RPC 2.0 server for blockchain transaction operations (Electrum protocol)
- **[Multisig Wallet ABI](MULTISIG_WALLET_README.md)** - Documentation for Ethereum multisignature wallet smart contract
- **[Etherscan Token Balance API](ETHERSCAN_TOKEN_BALANCE.md)** - Guide for querying ERC-20 token balances using Etherscan API v2
- **[Validator Rewards API](VALIDATOR_REWARDS.md)** - Query Ethereum validator rewards using Beaconcha.in API v2
- **[Bitcoin Difficulty Adjustment API](MEMPOOL_DIFFICULTY.md)** - Example HTML page for fetching Bitcoin difficulty adjustment data using mempool.space API
- **[Solscan API](SOLSCAN_API.md)** - Query Solana account transfer history using Solscan API v2.0

### Development Tools

- **[Database Frontend (Go)](db/frontend.go)** - Secure database operations with SQL injection prevention, input validation, and proper error handling
- **[Bash Configuration](BASHRC.md)** - Custom bash functions including foundryup (Foundry installer), cwhois (bgp.tools whois wrapper), and lastcall (Ethereum address transaction query)

### Utility Scripts

- **[verify_ens_creator.py](verify_ens_creator.py)** - Verify ENS creator status on Base network (kushmanmb.base.eth)
- **[git_pow_verifier.py](git_pow_verifier.py)** - Verify Git commit signatures using GPG (Proof of Work verification)
- **[verify_tx_hash.py](verify_tx_hash.py)** - Verify blockchain transaction hashes (Ethereum and Bitcoin formats)
- **[blockchain_rpc_server.py](blockchain_rpc_server.py)** - JSON-RPC server for blockchain.transaction.get_merkle
- **[blockchain_rpc_client.py](blockchain_rpc_client.py)** - Client for testing the JSON-RPC server
- **[api-test.sh](api-test.sh)** - Simple script to test Etherscan API v2 endpoint connectivity
- **[validator-rewards-test.sh](validator-rewards-test.sh)** - Simple script to test Beaconcha.in API v2 endpoint connectivity
- **[query-token-balance.sh](query-token-balance.sh)** - Bash script for querying token balances
- **[query-token-balance.py](query-token-balance.py)** - Python script for querying token balances
- **[query-token-balance.js](query-token-balance.js)** - JavaScript/Node.js script for querying token balances
- **[query-validator-rewards.sh](query-validator-rewards.sh)** - Bash script for querying validator rewards
- **[query-validator-rewards.py](query-validator-rewards.py)** - Python script for querying validator rewards
- **[query-validator-rewards.js](query-validator-rewards.js)** - JavaScript/Node.js script for querying validator rewards
- **[query-solana-transfers.js](query-solana-transfers.js)** - JavaScript/Node.js script for querying Solana account transfers via Solscan API
- **[test-verify.js](test-verify.js)** - JavaScript verification utilities for transaction hashes and ENS names
- **[verify-contract.js](verify-contract.js)** - JavaScript smart contract verification utilities for Ethereum addresses and ABI handling
- **[validate-address-labels.py](validate-address-labels.py)** - Python script for validating address labels configuration

### Blockchain Resources

- **[address-labels.json](address-labels.json)** - Address labeling configuration with metadata
- **[address-labels.example.json](address-labels.example.json)** - Example address labels configuration with multiple entries
- **[address-labels.schema.json](address-labels.schema.json)** - JSON schema for address labels validation
- **[blockchain-address.json](blockchain-address.json)** - Blockchain address information
- **[multisig-wallet.abi.json](multisig-wallet.abi.json)** - ABI definition for multisig wallet contract
- **[mempool-difficulty-adjustment.html](mempool-difficulty-adjustment.html)** - HTML example for fetching Bitcoin difficulty adjustment data
- **[solscan-api-config.example.json](solscan-api-config.example.json)** - Configuration template for Solscan API queries
- **[solscan-example.js](solscan-example.js)** - Example usage of Solscan API with axios

## Quick Start

> **⚠️ Security Warning**: Never commit API keys, private keys, or sensitive credentials to version control.
> Use environment variables or gitignored local configuration files.
> See [Security Best Practices](SECURITY_BEST_PRACTICES.md) for detailed guidance.

### ENS Creator Verification

Verify and announce kushmanmb.base.eth creator status on Base network:

```bash
# Verify ENS creator status
./verify_ens_creator.py --name kushmanmb.base.eth

# Display official creator status announcement
./verify_ens_creator.py --announce

# Output as JSON with details
./verify_ens_creator.py --json --pretty
```

**Official ENS Name**: `kushmanmb.base.eth` (Base Mainnet, Chain ID: 8453)

This ENS name is the official primary consolidation address for the kushmanmb-org organization. The verification script uses only public blockchain data and requires no API keys or private information.

For detailed usage and integration examples, see [ENS_VERIFICATION.md](ENS_VERIFICATION.md).

### Git POW Verification

Verify Git commit signatures using GPG to ensure commit authenticity:

```bash
# Verify a single commit (current HEAD)
./git_pow_verifier.py --commit HEAD

# Verify a specific commit by SHA
./git_pow_verifier.py --commit abc123def456

# Verify multiple commits from a file
./git_pow_verifier.py --file commits-example.json

# Output as JSON with details
./git_pow_verifier.py --commit HEAD --json --pretty --info
```

**Private Data Protection**: Verification configuration files are automatically excluded from version control using `.gitignore` patterns. Store sensitive verification policies in:
- `verification-data/` directory
- `commits.json` files (not example files)
- `verification-config.*` files

For detailed usage and GPG setup, see [GIT_POW_VERIFICATION.md](GIT_POW_VERIFICATION.md).

### Transaction Hash Verification

Verify blockchain transaction hashes with automatic protection for private data:

```bash
# Verify a single transaction hash (Ethereum format)
./verify_tx_hash.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000

# Verify a Bitcoin transaction hash
./verify_tx_hash.py --hash 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898

# Verify multiple hashes from a file
./verify_tx_hash.py --file tx-hashes-example.json

# Output as JSON
./verify_tx_hash.py --hash 0x000...000 --json --pretty
```

**Private Data Protection**: Transaction data files are automatically excluded from version control using `.gitignore` patterns. Store sensitive transaction data in:
- `tx-data/` directory
- `tx-hashes.json` files (not example files)
- `transaction-data.*` files

For detailed usage and examples, see [TX_HASH_VERIFICATION.md](TX_HASH_VERIFICATION.md).

### Blockchain JSON-RPC Server

Start a JSON-RPC server for blockchain transaction operations:

```bash
# Start the server (default: 127.0.0.1:8332)
python3 blockchain_rpc_server.py

# Test with the client
python3 blockchain_rpc_client.py \
  --tx 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898 \
  --height 172165 \
  --pretty

# Or test with curl
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "blockchain.transaction.get_merkle",
    "params": ["08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898", 172165]
  }'
```

For detailed usage and API documentation, see [BLOCKCHAIN_RPC.md](BLOCKCHAIN_RPC.md).

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

#### Using JavaScript/Node.js Script

```bash
node query-token-balance.js --apikey YOUR_API_KEY --pretty
```

#### Using cURL

##### Test API Endpoint (Basic GET)

```bash
curl --request GET \
  --url https://api.etherscan.io/v2/api
```

Or use the provided test script:

```bash
./api-test.sh
```

##### Query Token Balance (Full Example)

```bash
curl "https://api.etherscan.io/v2/api?chainid=1&module=account&action=addresstokenbalance&address=0x983e3660c0bE01991785F80f266A84B911ab59b0&page=1&offset=100&apikey=YourApiKeyToken"
```

For detailed usage and examples, see [ETHERSCAN_TOKEN_BALANCE.md](ETHERSCAN_TOKEN_BALANCE.md).

### Query Validator Rewards

You can query Ethereum validator rewards using the Beaconcha.in API v2 with the provided scripts.

#### Using Bash Script

```bash
./query-validator-rewards.sh --apikey YOUR_API_KEY
```

#### Using Python Script

```bash
./query-validator-rewards.py --apikey YOUR_API_KEY --pretty
```

#### Using JavaScript/Node.js Script

```bash
node query-validator-rewards.js --apikey YOUR_API_KEY --pretty
```

#### Using cURL

##### Test API Endpoint

```bash
./validator-rewards-test.sh
```

##### Query Validator Rewards (Full Example)

```bash
curl -X POST 'https://beaconcha.in/api/v2/ethereum/validators/rewards-list' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "validators": [1, 2, 3],
    "limit": 10
  }'
```

For detailed usage and examples, see [VALIDATOR_REWARDS.md](VALIDATOR_REWARDS.md).

### Address Labels Configuration

Manage and validate blockchain address labels with metadata:

```bash
# Validate address labels configuration
python3 validate-address-labels.py address-labels.json

# Use the example configuration as a template
cp address-labels.example.json my-labels.json
# Edit my-labels.json with your addresses
python3 validate-address-labels.py my-labels.json
```

The address labels configuration follows Etherscan API response format and supports:
- Address identification and categorization
- Custom labels and reputation scores
- URL associations for projects and organizations
- JSON schema validation

For detailed documentation, see [ADDRESS_LABELS.md](ADDRESS_LABELS.md).

### Bitcoin Difficulty Adjustment

View Bitcoin network difficulty adjustment data using the mempool.space API:

```bash
# Open the HTML file in your browser
open mempool-difficulty-adjustment.html
# Or on Linux:
xdg-open mempool-difficulty-adjustment.html
```

The page will automatically fetch and display current Bitcoin difficulty adjustment information including progress percentage, difficulty change, estimated retarget date, and remaining blocks.

For detailed usage and API documentation, see [MEMPOOL_DIFFICULTY.md](MEMPOOL_DIFFICULTY.md).

### Query Solana Transfers

Query Solana account transfer history using the Solscan API v2.0:

#### Using JavaScript/Node.js Script

```bash
node query-solana-transfers.js --token YOUR_API_TOKEN --pretty
```

#### Using the Example Module

```bash
node solscan-example.js
```

#### Using axios Directly

```javascript
import axios from 'axios'

const requestOptions = {
  method: "get",
  url: "https://pro-api.solscan.io/v2.0/account/transfer",
  params: {
    page: "1",
    page_size: "10",
    sort_by: "block_time",
    sort_order: "desc",
  },
  headers: {
    token: process.env.SOLSCAN_API_TOKEN
  },
}

axios
  .request(requestOptions)
  .then(response => console.log(response.data))
  .catch(err => console.error(err));
```

**Security Note**: Never commit your API token to version control. Use environment variables (`SOLSCAN_API_TOKEN`) or pass the token via command-line arguments.

For detailed usage and examples, see [SOLSCAN_API.md](SOLSCAN_API.md).

### Cryptocurrency Consolidation

Automated workflows for safely consolidating crypto assets across multiple chains:

```bash
# Monitor balances across all chains
gh workflow run balance-monitor.yml

# Consolidate funds (dry run first)
gh workflow run crypto-consolidation.yml \
  --field sourceChain=base \
  --field amount=1.0 \
  --field dryRun=true

# Verify a transaction after consolidation
gh workflow run tx-verification.yml \
  --field txHash=0x... \
  --field chain=base
```

**Target Consolidation Address**: `kushmanmb.base.eth`

The consolidation system supports:
- Multi-chain balance monitoring (Ethereum, Base, Polygon, Arbitrum, Optimism)
- Secure transaction workflows with multi-signature approval
- Automated verification and audit trails
- Gas optimization strategies

For detailed setup and usage instructions, see [CRYPTO_CONSOLIDATION.md](CRYPTO_CONSOLIDATION.md).

## Addresses

- **Primary Consolidation Address**: `kushmanmb.base.eth`
- **Token Balance Query Address**: `0x983e3660c0bE01991785F80f266A84B911ab59b0`
- **Multisig Wallet Owner**: `0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7`
- **Labeled Address (kushmanmb10)**: `0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43`

## Community Files

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Security Policy](SECURITY.md)
- [Security Best Practices](SECURITY_BEST_PRACTICES.md) - Guidelines for protecting API keys and sensitive data
- [Workflow Security](WORKFLOW_SECURITY.md) - GitHub Actions security best practices
- [Branch Protection](BRANCH_PROTECTION.md) - Repository security configuration guide
- [Funding Information](FUNDING.yml)

## Workflow Templates

The `workflow-templates/` directory contains GitHub Actions workflow templates for:

- **JavaScript/TypeScript Projects**: Build, lint, and test workflows (Node.js)
- **Go Projects**: Build, lint, and test workflows with Makefile support (for repositories like ethpandaops/eth-beacon-genesis)
- **Ruby Projects**: Build, lint, and test workflows with Bundler support
- **Cryptocurrency Operations**: Balance monitoring and consolidation workflows
- Release creation and publishing

## License

See individual files for licensing information.
