#!/bin/bash

# Etherscan Address Balance Query Script
# This script queries ETH balance for an Ethereum address using the Etherscan API v2

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load messages from JSON file
load_messages() {
    python3 -c "import json, os; messages = json.load(open(os.path.join('$SCRIPT_DIR', 'etherscan-messages.json'))); print(json.dumps(messages))"
}

MESSAGES=$(load_messages)

get_message() {
    echo "$MESSAGES" | python3 -c "
import json
import sys

data = json.load(sys.stdin)
keys = '$1'.split('.')
result = data
for k in keys:
    result = result.get(k, '')
print(result)
"
}

# Use Python to load config and validate address (shared functionality)
# shellcheck disable=SC2046
read -r ETHERSCAN_API_BASE DEFAULT_ADDRESS DEFAULT_CHAIN_ID <<< \
  $(python3 -c "from etherscan_common import load_config; config = load_config(); print(config['apiBaseUrl'], config['defaultAddress'], config['defaultChainId'])")

# Function to validate Ethereum address using shared Python module
validate_address() {
    # Pass address via stdin to prevent command injection
    echo "$1" | python3 -c "from etherscan_common import validate_ethereum_address; import sys; address = sys.stdin.read().strip(); sys.exit(0 if validate_ethereum_address(address) else 1)"
}

# Function to format balance from wei to ETH
format_balance() {
    python3 -c "print(f'{float($1) / 1e18:.18f}')"
}

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Query ETH balance for an Ethereum address using Etherscan API v2"
    echo ""
    echo "Options:"
    echo "  -a, --address ADDRESS    Ethereum address to query (default: $DEFAULT_ADDRESS)"
    echo "  -k, --apikey APIKEY      Etherscan API key (required)"
    echo "  -c, --chainid CHAINID    Chain ID (default: $DEFAULT_CHAIN_ID for Ethereum mainnet)"
    echo "  -t, --tag TAG            Block parameter: latest, earliest, or block number (default: latest)"
    echo "  -h, --help               Display this help message"
    echo ""
    echo "Example:"
    echo "  $0 --apikey YOUR_API_KEY"
    echo "  $0 --address 0x123... --apikey YOUR_API_KEY --tag latest"
    exit 1
}

# Initialize variables
ADDRESS="$DEFAULT_ADDRESS"
CHAIN_ID="$DEFAULT_CHAIN_ID"
TAG="latest"
API_KEY=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--address)
            ADDRESS="$2"
            shift 2
            ;;
        -k|--apikey)
            API_KEY="$2"
            shift 2
            ;;
        -c|--chainid)
            CHAIN_ID="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
done

# Validate required parameters
if [ -z "$API_KEY" ]; then
    echo "$(get_message 'errors.apiKeyRequired')"
    echo ""
    usage
fi

# Validate address format using shared validation function
if ! validate_address "$ADDRESS"; then
    echo "$(get_message 'errors.invalidAddress')"
    echo "$(get_message 'errors.expectedAddressFormat')"
    exit 1
fi

# Build the API URL for balance query
API_URL="${ETHERSCAN_API_BASE}?chainid=${CHAIN_ID}&module=account&action=balance&address=${ADDRESS}&tag=${TAG}&apikey=${API_KEY}"

# Display query information
echo "$(get_message 'status.querying')"
echo "$(get_message 'labels.address'): $ADDRESS"
echo "$(get_message 'labels.chainId'): $CHAIN_ID"
echo "Tag: $TAG"
echo ""

# Make the API request with timeout
if ! response=$(curl -s --max-time 30 "$API_URL"); then
    echo "$(get_message 'errors.apiFailed')"
    exit 1
fi

# Display the response
echo "$(get_message 'labels.response'):"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

# Check response status and display balance information
status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$status" = "1" ]; then
    echo ""
    echo "$(get_message 'status.success')"
    
    # Extract and format balance
    balance_wei=$(echo "$response" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
    if [ -n "$balance_wei" ]; then
        balance_eth=$(format_balance "$balance_wei")
        echo ""
        echo "Balance Information:"
        echo "  Address: $ADDRESS"
        echo "  Balance (wei): $balance_wei"
        echo "  Balance (ETH): $balance_eth ETH"
    fi
else
    echo ""
    echo "$(get_message 'status.failed')"
    message=$(echo "$response" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    echo "$(get_message 'labels.message'): $message"
fi
