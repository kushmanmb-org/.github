#!/bin/bash

# Etherscan Address Token Balance Query Script
# This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2

# Use Python to load config and validate address (shared functionality)
# shellcheck disable=SC2046
read -r ETHERSCAN_API_BASE DEFAULT_ADDRESS DEFAULT_CHAIN_ID DEFAULT_PAGE DEFAULT_OFFSET API_MODULE API_ACTION HELP_DESC <<< \
  $(python3 -c "from etherscan_common import load_config; config = load_config(); print(config['apiBaseUrl'], config['defaultAddress'], config['defaultChainId'], config['defaultPage'], config['defaultOffset'], config['module'], config['action'], config['helpText']['description'])")

# Helper function to get error message from config
get_error_message() {
    python3 -c "from etherscan_common import get_config; print(get_config()['errorMessages']['$1'])"
}

# Function to validate Ethereum address using shared Python module
validate_address() {
    # Pass address via stdin to prevent command injection
    echo "$1" | python3 -c "from etherscan_common import validate_ethereum_address; import sys; address = sys.stdin.read().strip(); sys.exit(0 if validate_ethereum_address(address) else 1)"
}

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Description: $HELP_DESC"
    echo ""
    echo "Options:"
    echo "  -a, --address ADDRESS    Ethereum address to query (default: $DEFAULT_ADDRESS)"
    echo "  -k, --apikey APIKEY      Etherscan API key (required, can also be set via ETHERSCAN_API_KEY environment variable)"
    echo "  -c, --chainid CHAINID    Chain ID (1 for Ethereum mainnet) (default: $DEFAULT_CHAIN_ID)"
    echo "  -p, --page PAGE          Page number for pagination (default: $DEFAULT_PAGE)"
    echo "  -o, --offset OFFSET      Results per page (max: 10000) (default: $DEFAULT_OFFSET)"
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
API_KEY="${ETHERSCAN_API_KEY:-}"

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
    get_error_message "apiKeyRequired"
    echo ""
    usage
fi

# Validate address format using shared validation function
if ! validate_address "$ADDRESS"; then
    get_error_message "invalidAddress"
    get_error_message "invalidAddressFormat"
    exit 1
fi

# Build the API URL
API_URL="${ETHERSCAN_API_BASE}?chainid=${CHAIN_ID}&module=${API_MODULE}&action=${API_ACTION}&address=${ADDRESS}&page=${PAGE}&offset=${OFFSET}&apikey=${API_KEY}"

# Display query information
echo "Querying Etherscan API..."
echo "Address: $ADDRESS"
echo "Chain ID: $CHAIN_ID"
echo "Page: $PAGE"
echo "Offset: $OFFSET"
echo ""

# Make the API request
if ! response=$(curl -s "$API_URL"); then
    echo "Error: Failed to connect to Etherscan API"
    exit 1
fi

# Display the response
echo "Response:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

# Check response status
status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$status" = "1" ]; then
    echo ""
    echo "✓ Query successful"
else
    echo ""
    echo "✗ Query failed"
    message=$(echo "$response" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    echo "Message: $message"
fi
