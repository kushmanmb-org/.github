#!/usr/bin/env python3

"""
Etherscan Address Token Balance Query Script
This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2
"""

import argparse
import json
import sys
import os
import requests
from etherscan_common import (
    validate_ethereum_address,
    load_config,
    build_api_params,
    format_token_balance
)

# Load shared configuration
shared_config = load_config()

# Configuration
ETHERSCAN_API_BASE = shared_config['apiBaseUrl']
DEFAULT_ADDRESS = shared_config['defaultAddress']
DEFAULT_CHAIN_ID = shared_config['defaultChainId']
DEFAULT_PAGE = shared_config['defaultPage']
DEFAULT_OFFSET = shared_config['defaultOffset']


def query_token_balance(address, api_key, chain_id=DEFAULT_CHAIN_ID, 
                       page=DEFAULT_PAGE, offset=DEFAULT_OFFSET):
    """
    Query ERC-20 token balances for an Ethereum address.
    
    Args:
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        chain_id (int): Chain ID (1 for Ethereum mainnet)
        page (int): Page number for pagination
        offset (int): Results per page
        
    Returns:
        dict: API response data
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    params = build_api_params(shared_config, address, api_key, chain_id, page, offset)
    
    try:
        response = requests.get(ETHERSCAN_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to Etherscan API: {e}", file=sys.stderr)
        raise


def main():
    """Main function to handle command-line interface and execute query."""
    help_config = shared_config.get('helpText', {})
    help_options = help_config.get('options', {})
    
    parser = argparse.ArgumentParser(
        description=help_config.get('description', 'Query ERC-20 token balances using Etherscan API v2'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --apikey YOUR_API_KEY
  %(prog)s --address 0x123... --apikey YOUR_API_KEY --page 1 --offset 50
        """
    )
    
    parser.add_argument(
        "-a", "--address",
        default=DEFAULT_ADDRESS,
        help=f"{help_options.get('address', 'Ethereum address to query')} (default: {DEFAULT_ADDRESS})"
    )
    parser.add_argument(
        "-k", "--apikey",
        default=os.environ.get('ETHERSCAN_API_KEY'),
        help=help_options.get('apikey', 'Etherscan API key (required)')
    )
    parser.add_argument(
        "-c", "--chainid",
        type=int,
        default=DEFAULT_CHAIN_ID,
        help=f"{help_options.get('chainid', 'Chain ID')} (default: {DEFAULT_CHAIN_ID})"
    )
    parser.add_argument(
        "-p", "--page",
        type=int,
        default=DEFAULT_PAGE,
        help=f"{help_options.get('page', 'Page number for pagination')} (default: {DEFAULT_PAGE})"
    )
    parser.add_argument(
        "-o", "--offset",
        type=int,
        default=DEFAULT_OFFSET,
        help=f"{help_options.get('offset', 'Results per page')} (default: {DEFAULT_OFFSET})"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print token information"
    )
    
    args = parser.parse_args()
    
    # Check if API key is provided either as argument or environment variable
    if not args.apikey:
        print("Error: API key is required. Use --apikey option or set ETHERSCAN_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    
    # Validate address
    if not validate_ethereum_address(args.address):
        print("Error: Invalid Ethereum address format", file=sys.stderr)
        print("Expected format: 0x followed by 40 hexadecimal characters", file=sys.stderr)
        sys.exit(1)
    
    # Display query information
    print("Querying Etherscan API...")
    print(f"Address: {args.address}")
    print(f"Chain ID: {args.chainid}")
    print(f"Page: {args.page}")
    print(f"Offset: {args.offset}")
    print()
    
    # Execute query
    try:
        response_data = query_token_balance(
            args.address,
            args.apikey,
            args.chainid,
            args.page,
            args.offset
        )
        
        # Output results
        if args.json:
            print(json.dumps(response_data, indent=2))
        else:
            print("Response:")
            print(json.dumps(response_data, indent=2))
            
            # Check status
            status = response_data.get("status", "0")
            if status == "1":
                print("\n✓ Query successful")
                
                # Pretty print if requested
                if args.pretty and "result" in response_data:
                    results = response_data["result"]
                    if isinstance(results, list) and results:
                        print(f"\nFound {len(results)} token(s):\n")
                        for i, token in enumerate(results, 1):
                            print(f"Token #{i}:")
                            print(format_token_balance(token))
                            print()
                    else:
                        print("\nNo tokens found for this address")
            else:
                print("\n✗ Query failed")
                message = response_data.get("message", "Unknown error")
                print(f"Message: {message}")
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
