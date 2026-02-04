#!/usr/bin/env python3

"""
Etherscan Address Token Balance Query Script
This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2
"""

import argparse
import json
import sys
import requests
from etherscan_common import (
    validate_ethereum_address,
    load_config,
    build_api_params,
    format_token_balance,
    load_messages
)

# Load shared configuration and messages
shared_config = load_config()
messages = load_messages()

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
        print(f"{messages['errors']['apiFailed']}: {e}", file=sys.stderr)
        raise


def main():
    """Main function to handle command-line interface and execute query."""
    parser = argparse.ArgumentParser(
        description="Query ERC-20 token balances for an Ethereum address using Etherscan API v2",
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
        help=f"Ethereum address to query (default: {DEFAULT_ADDRESS})"
    )
    parser.add_argument(
        "-k", "--apikey",
        required=True,
        help="Etherscan API key (required)"
    )
    parser.add_argument(
        "-c", "--chainid",
        type=int,
        default=DEFAULT_CHAIN_ID,
        help=f"Chain ID (default: {DEFAULT_CHAIN_ID} for Ethereum mainnet)"
    )
    parser.add_argument(
        "-p", "--page",
        type=int,
        default=DEFAULT_PAGE,
        help=f"Page number for pagination (default: {DEFAULT_PAGE})"
    )
    parser.add_argument(
        "-o", "--offset",
        type=int,
        default=DEFAULT_OFFSET,
        help=f"Results per page (default: {DEFAULT_OFFSET}, max: 10000)"
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
    
    # Validate address
    if not validate_ethereum_address(args.address):
        print(messages['errors']['invalidAddress'], file=sys.stderr)
        print(messages['errors']['expectedAddressFormat'], file=sys.stderr)
        sys.exit(1)
    
    # Display query information
    print(messages['status']['querying'])
    print(f"{messages['labels']['address']}: {args.address}")
    print(f"{messages['labels']['chainId']}: {args.chainid}")
    print(f"{messages['labels']['page']}: {args.page}")
    print(f"{messages['labels']['offset']}: {args.offset}")
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
            print(f"{messages['labels']['response']}:")
            print(json.dumps(response_data, indent=2))
            
            # Check status
            status = response_data.get("status", "0")
            if status == "1":
                print(f"\n{messages['status']['success']}")
                
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
                print(f"\n{messages['status']['failed']}")
                message = response_data.get("message", "Unknown error")
                print(f"{messages['labels']['message']}: {message}")
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
