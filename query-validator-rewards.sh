#!/bin/bash

# Beaconcha.in Validator Rewards Query Script
# This script queries Ethereum validator rewards using the Beaconcha.in API v2

set -euo pipefail

# Default configuration
API_ENDPOINT="https://beaconcha.in/api/v2/ethereum/validators/rewards-list"
DEFAULT_LIMIT=100
DEFAULT_OFFSET=0

# Function to display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Description: Query Ethereum validator rewards using Beaconcha.in API v2

Options:
  -k, --apikey APIKEY          Beaconcha.in API key (required, can also be set via BEACONCHAIN_API_KEY environment variable)
  -v, --validators IDS         Comma-separated list of validator indices (e.g., "1,2,3")
  -e, --epoch EPOCH            Specific epoch to query rewards for
  -l, --limit LIMIT            Number of results to return (default: $DEFAULT_LIMIT)
  -o, --offset OFFSET          Pagination offset (default: $DEFAULT_OFFSET)
  -p, --pretty                 Pretty print JSON output
  -h, --help                   Display this help message

Examples:
  $0 --apikey YOUR_API_KEY
  $0 --apikey YOUR_API_KEY --validators "1,2,3"
  $0 --apikey YOUR_API_KEY --epoch 123456 --limit 50 --pretty

Environment Variables:
  BEACONCHAIN_API_KEY          API key for Beaconcha.in (alternative to --apikey)

Security Note:
  Never commit API keys to version control. Use environment variables or
  gitignored configuration files. See SECURITY_BEST_PRACTICES.md for details.
EOF
    exit 1
}

# Initialize variables
API_KEY="${BEACONCHAIN_API_KEY:-}"
VALIDATORS=""
EPOCH=""
LIMIT="$DEFAULT_LIMIT"
OFFSET="$DEFAULT_OFFSET"
PRETTY=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -k|--apikey)
            API_KEY="$2"
            shift 2
            ;;
        -v|--validators)
            VALIDATORS="$2"
            shift 2
            ;;
        -e|--epoch)
            EPOCH="$2"
            shift 2
            ;;
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -o|--offset)
            OFFSET="$2"
            shift 2
            ;;
        -p|--pretty)
            PRETTY=true
            shift
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
    echo "Error: API key is required."
    echo "Provide it via --apikey option or set BEACONCHAIN_API_KEY environment variable."
    echo ""
    usage
fi

# Build JSON request body
build_json_body() {
    local json="{"
    local first=true

    # Add validators if provided
    if [ -n "$VALIDATORS" ]; then
        # Convert comma-separated string to JSON array
        local validator_array=$(echo "$VALIDATORS" | awk '{gsub(/[^0-9,]/,""); split($0,a,","); printf "["; for(i=1;i<=length(a);i++){printf "%s%d", (i>1?",":""), a[i]}; printf "]"}')
        if [ "$first" = true ]; then
            first=false
        else
            json+=","
        fi
        json+="\"validators\":$validator_array"
    fi

    # Add epoch if provided
    if [ -n "$EPOCH" ]; then
        if [ "$first" = true ]; then
            first=false
        else
            json+=","
        fi
        json+="\"epoch\":$EPOCH"
    fi

    # Add limit
    if [ "$first" = true ]; then
        first=false
    else
        json+=","
    fi
    json+="\"limit\":$LIMIT"

    # Add offset
    json+=",\"offset\":$OFFSET"

    json+="}"
    echo "$json"
}

# Build request body
REQUEST_BODY=$(build_json_body)

# Display query information
echo "Querying Beaconcha.in Validator Rewards API..."
echo "Endpoint: $API_ENDPOINT"
if [ -n "$VALIDATORS" ]; then
    echo "Validators: $VALIDATORS"
fi
if [ -n "$EPOCH" ]; then
    echo "Epoch: $EPOCH"
fi
echo "Limit: $LIMIT"
echo "Offset: $OFFSET"
echo ""

# Make the API request
if ! response=$(curl -s -X POST "$API_ENDPOINT" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$REQUEST_BODY"); then
    echo "Error: API request failed"
    exit 1
fi

# Display the response
echo "Response:"
if [ "$PRETTY" = true ]; then
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo "$response"
fi

# Check response status
status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
if [ "$status" = "success" ]; then
    echo ""
    echo "✓ Query successful"
    
    # Count results if possible
    result_count=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', [])))" 2>/dev/null || echo "")
    if [ -n "$result_count" ]; then
        echo "Results: $result_count record(s)"
    fi
elif [ "$status" = "error" ]; then
    echo ""
    echo "✗ Query failed"
    error_msg=$(echo "$response" | grep -o '"error":"[^"]*"' | cut -d'"' -f4 || echo "Unknown error")
    echo "Error: $error_msg"
    exit 1
else
    echo ""
    echo "⚠ Unknown response status"
fi
