#!/bin/bash

# Etherscan Address Token Balance Query Script
# This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2

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
read -r ETHERSCAN_API_BASE DEFAULT_ADDRESS DEFAULT_CHAIN_ID DEFAULT_PAGE DEFAULT_OFFSET API_MODULE API_ACTION HELP_DESC <<< \
  $(python3 -c "from etherscan_common import load_config; config = load_config(); print(config['apiBaseUrl'], config['defaultAddress'], config['defaultChainId'], config['defaultPage'], config['defaultOffset'], config['module'], config['action'], config['helpText']['description'])")

# Load error messages once during initialization
ERR_API_KEY=$(python3 -c "from etherscan_common import get_config; print(get_config()['errorMessages']['apiKeyRequired'])")
ERR_INVALID_ADDR=$(python3 -c "from etherscan_common import get_config; print(get_config()['errorMessages']['invalidAddress'])")
ERR_INVALID_FORMAT=$(python3 -c "from etherscan_common import get_config; print(get_config()['errorMessages']['invalidAddressFormat'])")

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
<<<<<<< HEAD
    echo "$ERR_API_KEY"
=======
    echo "$(get_message 'errors.apiKeyRequired')"
>>>>>>> origin/main
    echo ""
    usage
fi

# Validate address format using shared validation function
if ! validate_address "$ADDRESS"; then
<<<<<<< HEAD
    echo "$ERR_INVALID_ADDR"
    echo "$ERR_INVALID_FORMAT"
=======
    echo "$(get_message 'errors.invalidAddress')"
    echo "$(get_message 'errors.expectedAddressFormat')"
>>>>>>> origin/main
    exit 1
fi

# Build the API URL
API_URL="${ETHERSCAN_API_BASE}?chainid=${CHAIN_ID}&module=${API_MODULE}&action=${API_ACTION}&address=${ADDRESS}&page=${PAGE}&offset=${OFFSET}&apikey=${API_KEY}"

# Display query information
echo "$(get_message 'status.querying')"
echo "$(get_message 'labels.address'): $ADDRESS"
echo "$(get_message 'labels.chainId'): $CHAIN_ID"
echo "$(get_message 'labels.page'): $PAGE"
echo "$(get_message 'labels.offset'): $OFFSET"
echo ""

# Make the API request
if ! response=$(curl -s "$API_URL"); then
    echo "$(get_message 'errors.apiFailed')"
    exit 1
fi

# Display the response
echo "$(get_message 'labels.response'):"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

# Check response status
status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$status" = "1" ]; then
    echo ""
    echo "$(get_message 'status.success')"
else
    echo ""
    echo "$(get_message 'status.failed')"
    message=$(echo "$response" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    echo "$(get_message 'labels.message'): $message"
fi
