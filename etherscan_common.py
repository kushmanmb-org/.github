"""
Shared validation and utility functions for Etherscan token balance queries.
This module provides common functionality used across multiple implementations.
"""

import re
import json
import os
from urllib.parse import urlencode

# Ethereum address validation pattern
ETHEREUM_ADDRESS_PATTERN = re.compile(r'^0x[a-fA-F0-9]{40}$')

# Messages cache
_MESSAGES = None


def load_messages():
    """
    Load shared messages from JSON file.
    
    Returns:
        dict: Messages data
    """
    global _MESSAGES
    if _MESSAGES is None:
        messages_path = os.path.join(os.path.dirname(__file__), 'etherscan-messages.json')
        try:
            with open(messages_path, 'r') as f:
                _MESSAGES = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback to empty dict if messages file not found
            _MESSAGES = {"errors": {}, "status": {}, "labels": {}}
    return _MESSAGES


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


def build_api_url(config, params):
    """
    Build full API URL with parameters.
    
    Args:
        config (dict): Shared configuration
        params (dict): API request parameters
        
    Returns:
        str: Full API URL with query parameters
    """
    base_url = config['apiBaseUrl']
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"


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


def is_response_successful(response):
    """
    Check if API response indicates success.
    
    Args:
        response (dict): API response data
        
    Returns:
        bool: True if successful, False otherwise
    """
    return response and response.get("status") == "1"


def format_response(response, pretty=False):
    """
    Format API response output.
    
    Args:
        response (dict): API response data
        pretty (bool): Whether to pretty-print the JSON
        
    Returns:
        str: Formatted JSON string
    """
    indent = 2 if pretty else None
    return json.dumps(response, indent=indent)
