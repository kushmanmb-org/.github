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
    format_token_balance,
    load_messages,
    is_response_successful,
    format_response
)

# Load shared configuration and messages
shared_config = load_config()
messages = load_messages()


def query_token_balance(address, api_key, chain_id=None, 
                       page=None, offset=None):
    """
    Query ERC-20 token balances for an Ethereum address.
    
    Args:
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        chain_id (int, optional): Chain ID (defaults to config value)
        page (int, optional): Page number for pagination (defaults to config value)
        offset (int, optional): Results per page (defaults to config value)
        
    Returns:
        dict: API response data
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    params = build_api_params(shared_config, address, api_key, chain_id, page, offset)
    
    try:
        response = requests.get(shared_config['apiBaseUrl'], params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
<<<<<<< HEAD
        print(f"{shared_config['errorMessages']['apiRequestFailed']}: {e}", file=sys.stderr)
=======
        print(f"{messages['errors']['apiFailed']}: {e}", file=sys.stderr)
>>>>>>> origin/main
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
<<<<<<< HEAD
        default=DEFAULT_ADDRESS,
        help=f"{help_options.get('address', 'Ethereum address to query')} (default: {DEFAULT_ADDRESS})"
=======
        default=shared_config['defaultAddress'],
        help=f"Ethereum address to query (default: {shared_config['defaultAddress']})"
>>>>>>> origin/main
    )
    parser.add_argument(
        "-k", "--apikey",
        default=os.environ.get('ETHERSCAN_API_KEY'),
        help=help_options.get('apikey', 'Etherscan API key (required)')
    )
    parser.add_argument(
        "-c", "--chainid",
        type=int,
<<<<<<< HEAD
        default=DEFAULT_CHAIN_ID,
        help=f"{help_options.get('chainid', 'Chain ID')} (default: {DEFAULT_CHAIN_ID})"
=======
        default=shared_config['defaultChainId'],
        help=f"Chain ID (default: {shared_config['defaultChainId']} for Ethereum mainnet)"
>>>>>>> origin/main
    )
    parser.add_argument(
        "-p", "--page",
        type=int,
<<<<<<< HEAD
        default=DEFAULT_PAGE,
        help=f"{help_options.get('page', 'Page number for pagination')} (default: {DEFAULT_PAGE})"
=======
        default=shared_config['defaultPage'],
        help=f"Page number for pagination (default: {shared_config['defaultPage']})"
>>>>>>> origin/main
    )
    parser.add_argument(
        "-o", "--offset",
        type=int,
<<<<<<< HEAD
        default=DEFAULT_OFFSET,
        help=f"{help_options.get('offset', 'Results per page')} (default: {DEFAULT_OFFSET})"
=======
        default=shared_config['defaultOffset'],
        help=f"Results per page (default: {shared_config['defaultOffset']}, max: 10000)"
>>>>>>> origin/main
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
        print(shared_config['errorMessages']['apiKeyRequired'], file=sys.stderr)
        sys.exit(1)
    
    # Validate address
    if not validate_ethereum_address(args.address):
<<<<<<< HEAD
        print(shared_config['errorMessages']['invalidAddress'], file=sys.stderr)
        print(shared_config['errorMessages']['invalidAddressFormat'], file=sys.stderr)
=======
        print(messages['errors']['invalidAddress'], file=sys.stderr)
        print(messages['errors']['expectedAddressFormat'], file=sys.stderr)
>>>>>>> origin/main
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
            print(format_response(response_data, pretty=True))
        else:
            print(f"{messages['labels']['response']}:")
            print(format_response(response_data, pretty=True))
            
            # Check status
            if is_response_successful(response_data):
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
