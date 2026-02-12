#!/usr/bin/env python3

"""
Etherscan Address Balance Query Script
This script queries ETH balance for an Ethereum address using the Etherscan API v2
"""

import argparse
import json
import sys
import requests
from etherscan_common import (
    validate_ethereum_address,
    load_config,
    load_messages,
    is_response_successful,
    format_response
)

# Load shared configuration and messages
shared_config = load_config()
messages = load_messages()


def build_balance_params(config, address, api_key, chain_id, tag):
    """
    Build API request parameters for balance query.
    
    Args:
        config (dict): Shared configuration
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        chain_id (int): Chain ID
        tag (str): Block parameter (latest, earliest, or block number)
        
    Returns:
        dict: API request parameters
    """
    return {
        "chainid": chain_id,
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": tag,
        "apikey": api_key
    }


def format_balance(balance_wei):
    """
    Format balance from wei to ETH.
    
    Args:
        balance_wei (str): Balance in wei
        
    Returns:
        str: Balance in ETH formatted to 18 decimal places
    """
    balance_eth = float(balance_wei) / 1e18
    return f"{balance_eth:.18f}"


def query_balance(address, api_key, chain_id=None, tag='latest'):
    """
    Query ETH balance for an Ethereum address.
    
    Args:
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        chain_id (int, optional): Chain ID (defaults to config value)
        tag (str, optional): Block parameter (default: 'latest')
        
    Returns:
        dict: API response data
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    if chain_id is None:
        chain_id = shared_config['defaultChainId']
    
    params = build_balance_params(shared_config, address, api_key, chain_id, tag)
    
    try:
        response = requests.get(shared_config['apiBaseUrl'], params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{messages['errors']['apiFailed']}: {e}", file=sys.stderr)
        raise


def main():
    """Main function to handle command-line interface and execute query."""
    parser = argparse.ArgumentParser(
        description="Query ETH balance for an Ethereum address using Etherscan API v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --apikey YOUR_API_KEY
  %(prog)s --address 0x123... --apikey YOUR_API_KEY --tag latest
        """
    )
    
    parser.add_argument(
        "-a", "--address",
        default=shared_config['defaultAddress'],
        help=f"Ethereum address to query (default: {shared_config['defaultAddress']})"
    )
    parser.add_argument(
        "-k", "--apikey",
        required=True,
        help="Etherscan API key (required)"
    )
    parser.add_argument(
        "-c", "--chainid",
        type=int,
        default=shared_config['defaultChainId'],
        help=f"Chain ID (default: {shared_config['defaultChainId']} for Ethereum mainnet)"
    )
    parser.add_argument(
        "-t", "--tag",
        default="latest",
        help="Block parameter: latest, earliest, or block number in hex (default: latest)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print balance information"
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
    print(f"Tag: {args.tag}")
    print()
    
    # Execute query
    try:
        response_data = query_balance(
            args.address,
            args.apikey,
            args.chainid,
            args.tag
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
                    balance_wei = response_data["result"]
                    balance_eth = format_balance(balance_wei)
                    print(f"\nBalance Information:")
                    print(f"  Address: {args.address}")
                    print(f"  Balance (wei): {balance_wei}")
                    print(f"  Balance (ETH): {balance_eth} ETH")
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
