# .github Repository

This repository contains organization-wide configuration, templates, and utilities for blockchain-related operations.

## Contents

### GitHub Documentation

- **[Git Key-Pairs Guide](GIT_KEY_PAIRS.md)** - Comprehensive overview of SSH and GPG key-pairs for Git authentication and commit signing
- **[Connecting to GitHub with SSH](CONNECTING_TO_GITHUB_WITH_SSH.md)** - Complete guide for setting up SSH authentication with GitHub
- **[GPG Key Management](GPG_KEY_MANAGEMENT.md)** - Comprehensive guide for managing GPG keys, signing commits, and refreshing keys from keyservers

### Blockchain Documentation

- **[Transaction Hash Verification](TX_HASH_VERIFICATION.md)** - Verify blockchain transaction hashes with private data protection using .gitignore
- **[Address Labels Configuration](ADDRESS_LABELS.md)** - Best practices for configuring blockchain address labels and metadata
- **[Blockchain JSON-RPC Server](BLOCKCHAIN_RPC.md)** - JSON-RPC 2.0 server for blockchain transaction operations (Electrum protocol)
- **[Multisig Wallet ABI](MULTISIG_WALLET_README.md)** - Documentation for Ethereum multisignature wallet smart contract
- **[Etherscan Balance API](ETHERSCAN_BALANCE.md)** - Guide for querying native ETH balance using Etherscan API v2
- **[Etherscan Token Balance API](ETHERSCAN_TOKEN_BALANCE.md)** - Guide for querying ERC-20 token balances using Etherscan API v2
- **[Bitcoin Difficulty Adjustment API](MEMPOOL_DIFFICULTY.md)** - Example HTML page for fetching Bitcoin difficulty adjustment data using mempool.space API

### Development Tools

- **[Bash Configuration](BASHRC.md)** - Custom bash functions including foundryup (Foundry installer) and cwhois (bgp.tools whois wrapper)

### Utility Scripts

- **[verify_tx_hash.py](verify_tx_hash.py)** - Verify blockchain transaction hashes (Ethereum and Bitcoin formats)
- **[blockchain_rpc_server.py](blockchain_rpc_server.py)** - JSON-RPC server for blockchain.transaction.get_merkle
- **[blockchain_rpc_client.py](blockchain_rpc_client.py)** - Client for testing the JSON-RPC server
- **[api-test.sh](api-test.sh)** - Simple script to test Etherscan API v2 endpoint connectivity
- **[query-balance.sh](query-balance.sh)** - Bash script for querying ETH balance
- **[query-balance.py](query-balance.py)** - Python script for querying ETH balance
- **[query-balance.js](query-balance.js)** - JavaScript/Node.js script for querying ETH balance
- **[query-token-balance.sh](query-token-balance.sh)** - Bash script for querying token balances
- **[query-token-balance.py](query-token-balance.py)** - Python script for querying token balances
- **[query-token-balance.js](query-token-balance.js)** - JavaScript/Node.js script for querying token balances
- **[validate-address-labels.py](validate-address-labels.py)** - Python script for validating address labels configuration

### Blockchain Resources

- **[address-labels.json](address-labels.json)** - Address labeling configuration with metadata
- **[address-labels.example.json](address-labels.example.json)** - Example address labels configuration with multiple entries
- **[address-labels.schema.json](address-labels.schema.json)** - JSON schema for address labels validation
- **[blockchain-address.json](blockchain-address.json)** - Blockchain address information
- **[multisig-wallet.abi.json](multisig-wallet.abi.json)** - ABI definition for multisig wallet contract
- **[mempool-difficulty-adjustment.html](mempool-difficulty-adjustment.html)** - HTML example for fetching Bitcoin difficulty adjustment data

## Quick Start

> **⚠️ Security Warning**: Never commit API keys, private keys, or sensitive credentials to version control.
> Use environment variables or gitignored local configuration files.
> See [Security Best Practices](SECURITY_BEST_PRACTICES.md) for detailed guidance.

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

### Query ETH Balance

You can query native ETH balance for any Ethereum address using the provided scripts.

#### Using Bash Script

```bash
./query-balance.sh --apikey YOUR_API_KEY
```

#### Using Python Script

```bash
./query-balance.py --apikey YOUR_API_KEY --pretty
```

#### Using JavaScript/Node.js Script

```bash
node query-balance.js --apikey YOUR_API_KEY --pretty
```

#### Using cURL

```bash
curl "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=0x983e3660c0bE01991785F80f266A84B911ab59b0&tag=latest&apikey=YourApiKeyToken"
```

For detailed usage and examples, see [ETHERSCAN_BALANCE.md](ETHERSCAN_BALANCE.md).

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

## Addresses

- **Balance Query Address**: `0x983e3660c0bE01991785F80f266A84B911ab59b0` (for both ETH and token balance queries)
- **Multisig Wallet Owner**: `0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7`
- **Labeled Address (kushmanmb10)**: `0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43`

## Community Files

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Security Policy](SECURITY.md)
- [Security Best Practices](SECURITY_BEST_PRACTICES.md) - Guidelines for protecting API keys and sensitive data
- [Funding Information](FUNDING.yml)

## Workflow Templates

The `workflow-templates/` directory contains GitHub Actions workflow templates for:

- **JavaScript/TypeScript Projects**: Build, lint, and test workflows (Node.js)
- **Go Projects**: Build, lint, and test workflows with Makefile support (for repositories like ethpandaops/eth-beacon-genesis)
- **Ruby Projects**: Build, lint, and test workflows with Bundler support
- Release creation and publishing

## License

See individual files for licensing information.
