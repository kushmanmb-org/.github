#!/usr/bin/env python3

"""
Etherscan Address Token Balance Query Script
This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2
"""

import argparse
import json
import os
import re
import sys
import requests


# Load configuration from etherscan-config.json
config_path = os.path.join(os.path.dirname(__file__), 'etherscan-config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Configuration from JSON
ETHERSCAN_API_BASE = config['etherscan_api']['base_url']
DEFAULT_ADDRESS = config['etherscan_api']['example_address']
DEFAULT_CHAIN_ID = config['etherscan_api']['default_chain_id']
DEFAULT_PAGE = config['etherscan_api']['default_pagination']['page']
DEFAULT_OFFSET = config['etherscan_api']['default_pagination']['offset']
ADDRESS_PATTERN = config['etherscan_api']['address_validation_pattern']


def validate_ethereum_address(address):
    """
    Validate Ethereum address format.
    
    Args:
        address (str): Ethereum address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = re.compile(ADDRESS_PATTERN)
    return bool(pattern.match(address))


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
    endpoint = config['etherscan_api']['endpoints']['addresstokenbalance']
    params = {
        "chainid": chain_id,
        "module": endpoint['module'],
        "action": endpoint['action'],
        "address": address,
        "page": page,
        "offset": offset,
        "apikey": api_key
    }
    
    try:
        response = requests.get(ETHERSCAN_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to Etherscan API: {e}", file=sys.stderr)
        raise


def format_token_balance(token_data):
    """
    Format token balance data for display.
    
    Args:
        token_data (dict): Token data from API response
        
    Returns:
        str: Formatted token information
    """
    lines = []
    lines.append(f"  Token: {token_data.get('TokenName', 'Unknown')}")
    lines.append(f"  Symbol: {token_data.get('TokenSymbol', 'N/A')}")
    lines.append(f"  Address: {token_data.get('TokenAddress', 'N/A')}")
    lines.append(f"  Quantity: {token_data.get('TokenQuantity', '0')}")
    lines.append(f"  Divisor: {token_data.get('TokenDivisor', '18')}")
    return "\n".join(lines)


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
