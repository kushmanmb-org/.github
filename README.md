# .github Repository

This repository contains organization-wide configuration, templates, and utilities for blockchain-related operations.

## Contents

### GitHub Documentation

- **[Connecting to GitHub with SSH](CONNECTING_TO_GITHUB_WITH_SSH.md)** - Complete guide for setting up SSH authentication with GitHub

### Blockchain Documentation

- **[Blockchain JSON-RPC Server](BLOCKCHAIN_RPC.md)** - JSON-RPC 2.0 server for blockchain transaction operations (Electrum protocol)
- **[Multisig Wallet ABI](MULTISIG_WALLET_README.md)** - Documentation for Ethereum multisignature wallet smart contract
- **[Etherscan Token Balance API](ETHERSCAN_TOKEN_BALANCE.md)** - Guide for querying ERC-20 token balances using Etherscan API v2
- **[Bitcoin Difficulty Adjustment API](MEMPOOL_DIFFICULTY.md)** - Example HTML page for fetching Bitcoin difficulty adjustment data using mempool.space API

### Development Tools

- **[Bash Configuration](BASHRC.md)** - Custom bash functions including foundryup (Foundry installer) and cwhois (bgp.tools whois wrapper)

### Utility Scripts

- **[blockchain_rpc_server.py](blockchain_rpc_server.py)** - JSON-RPC server for blockchain.transaction.get_merkle
- **[blockchain_rpc_client.py](blockchain_rpc_client.py)** - Client for testing the JSON-RPC server
- **[api-test.sh](api-test.sh)** - Simple script to test Etherscan API v2 endpoint connectivity
- **[query-token-balance.sh](query-token-balance.sh)** - Bash script for querying token balances
- **[query-token-balance.py](query-token-balance.py)** - Python script for querying token balances
- **[query-token-balance.js](query-token-balance.js)** - JavaScript/Node.js script for querying token balances

### Blockchain Resources

- **[blockchain-address.json](blockchain-address.json)** - Blockchain address information
- **[multisig-wallet.abi.json](multisig-wallet.abi.json)** - ABI definition for multisig wallet contract
- **[mempool-difficulty-adjustment.html](mempool-difficulty-adjustment.html)** - HTML example for fetching Bitcoin difficulty adjustment data

## Quick Start

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

- **Token Balance Query Address**: `0x983e3660c0bE01991785F80f266A84B911ab59b0`
- **Multisig Wallet Owner**: `0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7`

## Community Files

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Funding Information](FUNDING.yml)

## Workflow Templates

The `workflow-templates/` directory contains GitHub Actions workflow templates for:

- **JavaScript/TypeScript Projects**: Build, lint, and test workflows (Node.js)
- **Go Projects**: Build, lint, and test workflows with Makefile support (for repositories like ethpandaops/eth-beacon-genesis)
- **Ruby Projects**: Build, lint, and test workflows with Bundler support
- Release creation and publishing

## License

See individual files for licensing information.
