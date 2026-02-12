#!/usr/bin/env python3
"""
Address Labels Validator

This script validates address labels configuration against the JSON schema
and performs additional validation checks for Ethereum addresses, URLs, and data quality.
"""

import json
import re
import sys
import os
from typing import Dict, List, Any
from urllib.parse import urlparse

# Ethereum address pattern
ETHEREUM_ADDRESS_PATTERN = re.compile(r'^0x[a-fA-F0-9]{40}$')

def validate_ethereum_address(address: str) -> tuple[bool, str]:
    """
    Validate Ethereum address format.
    
    Args:
        address: Ethereum address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not address:
        return False, "Address cannot be empty"
    
    if not ETHEREUM_ADDRESS_PATTERN.match(address):
        return False, f"Invalid Ethereum address format: {address}"
    
    return True, ""

def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return True, ""  # URL is optional
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, f"Invalid URL format: {url}"
        if result.scheme not in ['http', 'https']:
            return False, f"URL must use http or https scheme: {url}"
        return True, ""
    except Exception as e:
        return False, f"URL parsing error: {str(e)}"

def validate_labels(labels: List[str]) -> tuple[bool, str]:
    """
    Validate labels array.
    
    Args:
        labels: List of label strings
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(labels, list):
        return False, "Labels must be an array"
    
    if not labels:
        return True, ""  # Empty labels array is allowed
    
    for label in labels:
        if not isinstance(label, str):
            return False, f"Label must be a string: {label}"
        if not label.strip():
            return False, "Label cannot be empty or whitespace only"
    
    # Check for duplicates
    if len(labels) != len(set(labels)):
        return False, "Labels array contains duplicates"
    
    return True, ""

def validate_address_entry(entry: Dict[str, Any], index: int) -> List[str]:
    """
    Validate a single address entry.
    
    Args:
        entry: Address entry dictionary
        index: Index of the entry in the result array
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    entry_prefix = f"Entry {index}"
    
    # Required fields
    if 'address' not in entry:
        errors.append(f"{entry_prefix}: Missing required field 'address'")
    else:
        is_valid, error = validate_ethereum_address(entry['address'])
        if not is_valid:
            errors.append(f"{entry_prefix}: {error}")
    
    if 'nametag' not in entry:
        errors.append(f"{entry_prefix}: Missing required field 'nametag'")
    elif not entry['nametag'].strip():
        errors.append(f"{entry_prefix}: 'nametag' cannot be empty")
    
    # Optional fields validation
    if 'url' in entry:
        is_valid, error = validate_url(entry['url'])
        if not is_valid:
            errors.append(f"{entry_prefix}: {error}")
    
    if 'labels' in entry:
        is_valid, error = validate_labels(entry['labels'])
        if not is_valid:
            errors.append(f"{entry_prefix}: {error}")
    
    if 'reputation' in entry:
        if not isinstance(entry['reputation'], int):
            errors.append(f"{entry_prefix}: 'reputation' must be an integer")
        elif entry['reputation'] < -100 or entry['reputation'] > 100:
            errors.append(f"{entry_prefix}: 'reputation' should be between -100 and 100")
    
    if 'lastUpdatedTimestamp' in entry:
        if not isinstance(entry['lastUpdatedTimestamp'], int):
            errors.append(f"{entry_prefix}: 'lastUpdatedTimestamp' must be an integer")
        elif entry['lastUpdatedTimestamp'] < 0:
            errors.append(f"{entry_prefix}: 'lastUpdatedTimestamp' cannot be negative")
    
    return errors

def validate_address_labels(config: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate the complete address labels configuration.
    
    Args:
        config: Address labels configuration dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Validate root structure
    if 'status' not in config:
        errors.append("Missing required field 'status'")
    elif config['status'] not in ['0', '1']:
        errors.append("'status' must be '0' or '1'")
    
    if 'message' not in config:
        errors.append("Missing required field 'message'")
    
    if 'result' not in config:
        errors.append("Missing required field 'result'")
    elif not isinstance(config['result'], list):
        errors.append("'result' must be an array")
    else:
        # Validate each entry
        addresses_seen = set()
        for i, entry in enumerate(config['result']):
            entry_errors = validate_address_entry(entry, i)
            errors.extend(entry_errors)
            
            # Check for duplicate addresses
            if 'address' in entry:
                addr = entry['address'].lower()
                if addr in addresses_seen:
                    errors.append(f"Entry {i}: Duplicate address {entry['address']}")
                addresses_seen.add(addr)
    
    return len(errors) == 0, errors

def main():
    """Main function to validate address labels configuration."""
    if len(sys.argv) < 2:
        print("Usage: python validate-address-labels.py <config-file>")
        print("Example: python validate-address-labels.py address-labels.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(config_file):
        print(f"Error: Configuration file not found: {config_file}")
        sys.exit(1)
    
    # Load and parse JSON
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {config_file}")
        print(f"  {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {config_file}: {str(e)}")
        sys.exit(1)
    
    # Validate configuration
    print(f"Validating {config_file}...")
    is_valid, errors = validate_address_labels(config)
    
    if is_valid:
        print("✓ Configuration is valid!")
        print(f"  Found {len(config.get('result', []))} address entries")
        sys.exit(0)
    else:
        print("✗ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
