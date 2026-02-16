#!/bin/bash

# Simple script to test Beaconcha.in API v2 endpoint availability
# This performs a basic request to verify the API endpoint exists
# Note: A valid API key is required for actual queries

echo "Testing Beaconcha.in API v2 endpoint..."
echo "Endpoint: https://beaconcha.in/api/v2/ethereum/validators/rewards-list"
echo ""
echo "Note: This endpoint requires:"
echo "  - POST method"
echo "  - Authorization header with Bearer token"
echo "  - Content-Type: application/json"
echo "  - Valid API key from Beaconcha.in"
echo ""
echo "Testing endpoint availability (without authentication)..."
echo ""

# Test basic connectivity (will likely return 401 Unauthorized, which is expected)
response=$(curl -s -X POST https://beaconcha.in/api/v2/ethereum/validators/rewards-list \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}" \
  -d '{}')

echo "$response"
echo ""
echo ""
echo "Expected response: 401 Unauthorized (API key required)"
echo "If you received a 401 or similar authentication error, the endpoint is available."
echo ""
echo "For actual queries with authentication, use:"
echo "  ./query-validator-rewards.sh --apikey YOUR_API_KEY"
echo "  ./query-validator-rewards.py --apikey YOUR_API_KEY"
echo "  node query-validator-rewards.js --apikey YOUR_API_KEY"
echo ""
echo "See VALIDATOR_REWARDS.md for complete examples and documentation."
