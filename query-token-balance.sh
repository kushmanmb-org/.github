#!/bin/bash

# Etherscan Address Token Balance Query Script
# This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2

# Load configuration from etherscan-config.json
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/etherscan-config.json"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: etherscan-config.json not found"
    echo "Expected location: $CONFIG_FILE"
    exit 1
fi

# Parse configuration using jq or python if available
if command -v jq &> /dev/null; then
    ETHERSCAN_API_BASE=$(jq -r '.etherscan_api.base_url' "$CONFIG_FILE")
    DEFAULT_ADDRESS=$(jq -r '.etherscan_api.example_address' "$CONFIG_FILE")
    DEFAULT_CHAIN_ID=$(jq -r '.etherscan_api.default_chain_id' "$CONFIG_FILE")
    DEFAULT_PAGE=$(jq -r '.etherscan_api.default_pagination.page' "$CONFIG_FILE")
    DEFAULT_OFFSET=$(jq -r '.etherscan_api.default_pagination.offset' "$CONFIG_FILE")
    ADDRESS_PATTERN=$(jq -r '.etherscan_api.address_validation_pattern' "$CONFIG_FILE")
    API_MODULE=$(jq -r '.etherscan_api.endpoints.addresstokenbalance.module' "$CONFIG_FILE")
    API_ACTION=$(jq -r '.etherscan_api.endpoints.addresstokenbalance.action' "$CONFIG_FILE")
elif command -v python3 &> /dev/null; then
    # Load JSON once and extract all values - pass config file path as argument
    read -r ETHERSCAN_API_BASE DEFAULT_ADDRESS DEFAULT_CHAIN_ID DEFAULT_PAGE DEFAULT_OFFSET ADDRESS_PATTERN API_MODULE API_ACTION < <(python3 - "$CONFIG_FILE" <<'EOF'
import json
import sys
try:
    with open(sys.argv[1]) as f:
        config = json.load(f)
    api = config['etherscan_api']
    endpoint = api['endpoints']['addresstokenbalance']
    print(api['base_url'], api['example_address'], api['default_chain_id'], 
          api['default_pagination']['page'], api['default_pagination']['offset'],
          api['address_validation_pattern'], endpoint['module'], endpoint['action'])
except Exception as e:
    print(f"Error loading config: {e}", file=sys.stderr)
    sys.exit(1)
EOF
)
    if [ $? -ne 0 ]; then
        echo "Error: Failed to parse etherscan-config.json"
        exit 1
    fi
else
    echo "Error: Neither jq nor python3 is available. Please install one of them to parse the config file."
    exit 1
fi

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
    echo "Error: API key is required"
    echo ""
    usage
fi

# Validate address format (basic check)
if [[ ! "$ADDRESS" =~ $ADDRESS_PATTERN ]]; then
    echo "Error: Invalid Ethereum address format"
    echo "Expected format: 0x followed by 40 hexadecimal characters"
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
