#!/usr/bin/env python3

"""
Etherscan Address Token Balance Query Script
This script queries ERC-20 token balances for an Ethereum address using the Etherscan API v2
"""

import argparse
import json
import re
import sys
import requests


# Configuration
ETHERSCAN_API_BASE = "https://api.etherscan.io/v2/api"
DEFAULT_ADDRESS = "0x983e3660c0bE01991785F80f266A84B911ab59b0"
DEFAULT_CHAIN_ID = 1
DEFAULT_PAGE = 1
DEFAULT_OFFSET = 100


def validate_ethereum_address(address):
    """
    Validate Ethereum address format.
    
    Args:
        address (str): Ethereum address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
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
    params = {
        "chainid": chain_id,
        "module": "account",
        "action": "addresstokenbalance",
        "address": address,
        "page": page,
        "offset": offset,
        "apikey": api_key
    }
    
    try:
        response = requests.get(ETHERSCAN_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as api_error:
        print(f"Error: Failed to connect to Etherscan API: {api_error}", file=sys.stderr)
        raise


def format_token_balance(token_data):
    """
    Format token balance data for display.
    
    Args:
        token_data (dict): Token data from API response
        
    Returns:
        str: Formatted token information
    """
    formatted_lines = []
    formatted_lines.append(f"  Token: {token_data.get('TokenName', 'Unknown')}")
    formatted_lines.append(f"  Symbol: {token_data.get('TokenSymbol', 'N/A')}")
    formatted_lines.append(f"  Address: {token_data.get('TokenAddress', 'N/A')}")
    formatted_lines.append(f"  Quantity: {token_data.get('TokenQuantity', '0')}")
    formatted_lines.append(f"  Divisor: {token_data.get('TokenDivisor', '18')}")
    return "\n".join(formatted_lines)


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
                        for token_index, token in enumerate(results, 1):
                            print(f"Token #{token_index}:")
                            print(format_token_balance(token))
                            print()
                    else:
                        print("\nNo tokens found for this address")
            else:
                print("\n✗ Query failed")
                message = response_data.get("message", "Unknown error")
                print(f"Message: {message}")
                sys.exit(1)
                
    except Exception as unexpected_error:
        print(f"Error: {unexpected_error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
