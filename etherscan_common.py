"""
Shared validation and utility functions for Etherscan token balance queries.
This module provides common functionality used across multiple implementations.
"""

import re
import json
import os

# Ethereum address validation pattern
ETHEREUM_ADDRESS_PATTERN = re.compile(r'^0x[a-fA-F0-9]{40}$')


def validate_ethereum_address(address):
    """
    Validate Ethereum address format.
    
    Args:
        address (str): Ethereum address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return bool(ETHEREUM_ADDRESS_PATTERN.match(address))


def load_config(config_path=None):
    """
    Load shared configuration from JSON file.
    
    Args:
        config_path (str, optional): Path to config file. If None, uses default location.
        
    Returns:
        dict: Configuration data
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is not valid JSON
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'etherscan-api-config.json')
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            "Please ensure etherscan-api-config.json exists in the script directory."
        )
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in configuration file: {config_path}",
            e.doc, e.pos
        )


def build_api_params(config, address, api_key, chain_id=None, page=None, offset=None):
    """
    Build API request parameters from config and user inputs.
    
    Args:
        config (dict): Shared configuration
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        chain_id (int, optional): Chain ID
        page (int, optional): Page number
        offset (int, optional): Results per page
        
    Returns:
        dict: API request parameters
    """
    params = {
        "chainid": chain_id or config['defaultChainId'],
        "module": config['module'],
        "action": config['action'],
        "address": address,
        "page": page or config['defaultPage'],
        "offset": offset or config['defaultOffset'],
        "apikey": api_key
    }
    return params


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
