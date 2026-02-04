#!/bin/bash

# Etherscan Address Token Balance Query Script
# This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load messages from JSON file
load_messages() {
    jq -c '.' "$SCRIPT_DIR/etherscan-messages.json" 2>/dev/null || echo '{"errors":{},"status":{},"labels":{}}'
}

MESSAGES=$(load_messages)

get_message() {
    echo "$MESSAGES" | jq -r ".$1 // \"\""
}

# Use jq and Python (single call) to load config efficiently
# shellcheck disable=SC2046
read -r ETHERSCAN_API_BASE DEFAULT_ADDRESS DEFAULT_CHAIN_ID DEFAULT_PAGE DEFAULT_OFFSET API_MODULE API_ACTION <<< \
  $(jq -r '[.apiBaseUrl, .defaultAddress, (.defaultChainId | tostring), (.defaultPage | tostring), (.defaultOffset | tostring), .module, .action] | join(" ")' "$SCRIPT_DIR/etherscan-api-config.json")

# Function to validate Ethereum address using shared Python module
validate_address() {
    # Pass address via stdin to prevent command injection
    echo "$1" | python3 -c "from etherscan_common import validate_ethereum_address; import sys; address = sys.stdin.read().strip(); sys.exit(0 if validate_ethereum_address(address) else 1)"
}

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Query ERC-20 token balances for an Ethereum address using Etherscan API v2"
    echo ""
    echo "Options:"
    echo "  -a, --address ADDRESS    Ethereum address to query (default: $DEFAULT_ADDRESS)"
    echo "  -k, --apikey APIKEY      Etherscan API key (required)"
    echo "  -c, --chainid CHAINID    Chain ID (default: $DEFAULT_CHAIN_ID for Ethereum mainnet)"
    echo "  -p, --page PAGE          Page number for pagination (default: $DEFAULT_PAGE)"
    echo "  -o, --offset OFFSET      Results per page (default: $DEFAULT_OFFSET, max: 10000)"
    echo "  -h, --help               Display this help message"
    echo ""
    echo "Example:"
    echo "  $0 --apikey YOUR_API_KEY"
    echo "  $0 --address 0x123... --apikey YOUR_API_KEY --page 1 --offset 50"
    exit 1
}

# Initialize variables
ADDRESS="$DEFAULT_ADDRESS"
CHAIN_ID="$DEFAULT_CHAIN_ID"
PAGE="$DEFAULT_PAGE"
OFFSET="$DEFAULT_OFFSET"
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
        -p|--page)
            PAGE="$2"
            shift 2
            ;;
        -o|--offset)
            OFFSET="$2"
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
    get_message 'errors.apiKeyRequired'
    echo ""
    usage
fi

# Validate address format using shared validation function
if ! validate_address "$ADDRESS"; then
    get_message 'errors.invalidAddress'
    get_message 'errors.expectedAddressFormat'
    exit 1
fi

# Build the API URL
API_URL="${ETHERSCAN_API_BASE}?chainid=${CHAIN_ID}&module=${API_MODULE}&action=${API_ACTION}&address=${ADDRESS}&page=${PAGE}&offset=${OFFSET}&apikey=${API_KEY}"

# Display query information
get_message 'status.querying'
echo "$(get_message 'labels.address'): $ADDRESS"
echo "$(get_message 'labels.chainId'): $CHAIN_ID"
echo "$(get_message 'labels.page'): $PAGE"
echo "$(get_message 'labels.offset'): $OFFSET"
echo ""

# Make the API request
if ! response=$(curl -s "$API_URL"); then
    get_message 'errors.apiFailed'
    exit 1
fi

# Display the response
echo "$(get_message 'labels.response'):"
echo "$response" | jq '.' 2>/dev/null || echo "$response"

# Check response status using jq
status=$(echo "$response" | jq -r '.status // ""')
if [ "$status" = "1" ]; then
    echo ""
    get_message 'status.success'
else
    echo ""
    get_message 'status.failed'
    message=$(echo "$response" | jq -r '.message // ""')
    echo "$(get_message 'labels.message'): $message"
fi
