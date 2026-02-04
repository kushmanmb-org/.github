#!/bin/bash

# Simple script to test Etherscan API v2 endpoint availability
# This performs a basic GET request to verify the API is accessible

echo "Testing Etherscan API v2 endpoint..."
echo "Endpoint: https://api.etherscan.io/v2/api"
echo ""

curl --request GET \
  --url https://api.etherscan.io/v2/api

echo ""
echo ""
echo "Note: The API requires parameters for actual queries."
echo "See ETHERSCAN_TOKEN_BALANCE.md for complete examples with parameters."
