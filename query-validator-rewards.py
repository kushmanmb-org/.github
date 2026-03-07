#!/usr/bin/env python3

"""
Beaconcha.in Validator Rewards Query Script
This script queries Ethereum validator rewards using the Beaconcha.in API v2
"""

import argparse
import json
import sys
import os
import requests

# Default configuration
API_ENDPOINT = "https://beaconcha.in/api/v2/ethereum/validators/rewards-list"
DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0


def query_validator_rewards(api_key, validators=None, epoch=None, 
                            limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
    """
    Query Ethereum validator rewards from Beaconcha.in API.
    
    Args:
        api_key (str): Beaconcha.in API key
        validators (list, optional): List of validator indices
        epoch (int, optional): Specific epoch to query
        limit (int): Number of results to return
        offset (int): Pagination offset
        
    Returns:
        dict: API response data
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build request body
    body = {
        "limit": limit,
        "offset": offset
    }
    
    if validators is not None and len(validators) > 0:
        body["validators"] = validators
    
    if epoch is not None:
        body["epoch"] = epoch
    
    try:
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=body,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        if e.response.text:
            try:
                error_data = e.response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"Response: {e.response.text}", file=sys.stderr)
        raise
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        raise


def format_response(data, pretty=False):
    """
    Format API response data as JSON string.
    Redacts sensitive fields to prevent accidental exposure.
    
    Args:
        data: Response data to format
        pretty: Whether to pretty-print the JSON
        
    Returns:
        str: Formatted JSON string with sensitive fields redacted
    """
    import copy
    
    # List of sensitive field names to redact
    sensitive_fields = ['apikey', 'api_key', 'apiKey', 'token', 'access_token', 'secret', 'password', 'authorization']
    
    # Create a deep copy and redact sensitive fields
    sanitized = copy.deepcopy(data)
    
    def redact_sensitive_fields(obj):
        """Recursively redact sensitive fields in nested structures."""
        if not isinstance(obj, dict):
            return
        
        for key in list(obj.keys()):
            # Check if this is a sensitive field
            if any(field.lower() in key.lower() for field in sensitive_fields):
                obj[key] = '[REDACTED]'
            elif isinstance(obj[key], dict):
                # Recursively redact nested objects
                redact_sensitive_fields(obj[key])
            elif isinstance(obj[key], list):
                # Redact items in lists
                for item in obj[key]:
                    if isinstance(item, dict):
                        redact_sensitive_fields(item)
    
    redact_sensitive_fields(sanitized)
    
    if pretty:
        return json.dumps(sanitized, indent=2, sort_keys=False)
    return json.dumps(sanitized)


def format_reward_record(record):
    """Format a single reward record for display."""
    lines = []
    lines.append(f"  Validator Index: {record.get('validatorindex', 'N/A')}")
    lines.append(f"  Epoch: {record.get('epoch', 'N/A')}")
    
    if record.get('attesterslot') is not None:
        lines.append(f"  Attester Slot: {record['attesterslot']}")
    
    if record.get('attestation_source') is not None:
        lines.append(f"  Attestation Source: {record['attestation_source']}")
    
    if record.get('attestation_target') is not None:
        lines.append(f"  Attestation Target: {record['attestation_target']}")
    
    if record.get('attestation_head') is not None:
        lines.append(f"  Attestation Head: {record['attestation_head']}")
    
    if record.get('proposerslot') is not None:
        lines.append(f"  Proposer Slot: {record['proposerslot']}")
    
    if record.get('deposits') is not None:
        lines.append(f"  Deposits: {record['deposits']}")
    
    if record.get('withdrawals') is not None:
        lines.append(f"  Withdrawals: {record['withdrawals']}")
    
    return "\n".join(lines)


def main():
    """Main function to handle command-line interface and execute query."""
    parser = argparse.ArgumentParser(
        description="Query Ethereum validator rewards using Beaconcha.in API v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --apikey YOUR_API_KEY
  %(prog)s --apikey YOUR_API_KEY --validators 1 2 3 --pretty
  %(prog)s --apikey YOUR_API_KEY --epoch 123456 --limit 50

Environment Variables:
  BEACONCHAIN_API_KEY    API key for Beaconcha.in (alternative to --apikey)

Security Note:
  Never commit API keys to version control. Use environment variables or
  gitignored configuration files. See SECURITY_BEST_PRACTICES.md for details.
        """
    )
    
    parser.add_argument(
        "-k", "--apikey",
        default=os.environ.get('BEACONCHAIN_API_KEY'),
        help="Beaconcha.in API key (required)"
    )
    parser.add_argument(
        "-v", "--validators",
        nargs='+',
        type=int,
        help="List of validator indices (e.g., 1 2 3)"
    )
    parser.add_argument(
        "-e", "--epoch",
        type=int,
        help="Specific epoch to query rewards for"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Number of results to return (default: {DEFAULT_LIMIT})"
    )
    parser.add_argument(
        "-o", "--offset",
        type=int,
        default=DEFAULT_OFFSET,
        help=f"Pagination offset (default: {DEFAULT_OFFSET})"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print output"
    )
    
    args = parser.parse_args()
    
    # Check if API key is provided
    if not args.apikey:
        print("Error: API key is required.", file=sys.stderr)
        print("Provide it via --apikey option or set BEACONCHAIN_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    
    # Display query information
    print("Querying Beaconcha.in Validator Rewards API...")
    print(f"Endpoint: {API_ENDPOINT}")
    if args.validators:
        print(f"Validators: {', '.join(map(str, args.validators))}")
    if args.epoch is not None:
        print(f"Epoch: {args.epoch}")
    print(f"Limit: {args.limit}")
    print(f"Offset: {args.offset}")
    print()
    
    # Execute query
    try:
        response_data = query_validator_rewards(
            args.apikey,
            validators=args.validators,
            epoch=args.epoch,
            limit=args.limit,
            offset=args.offset
        )
        
        # Output results
        print("Response:")
        if args.json or not args.pretty:
            print(format_response(response_data, pretty=args.pretty))
        else:
            print(format_response(response_data, pretty=True))
        
        # Check status
        status = response_data.get("status", "unknown")
        if status == "success":
            print()
            print("✓ Query successful")
            
            # Display summary if pretty output requested
            if args.pretty and "data" in response_data:
                results = response_data["data"]
                if isinstance(results, list):
                    print(f"Results: {len(results)} record(s)")
                    
                    if results and len(results) <= 10:
                        print()
                        print("Details:")
                        for i, record in enumerate(results, 1):
                            print(f"\nRecord #{i}:")
                            print(format_reward_record(record))
                    elif results:
                        print(f"(showing first 10 of {len(results)} records)")
                        print()
                        print("Details:")
                        for i, record in enumerate(results[:10], 1):
                            print(f"\nRecord #{i}:")
                            print(format_reward_record(record))
        elif status == "error":
            print()
            print("✗ Query failed")
            error_msg = response_data.get("error", "Unknown error")
            print(f"Error: {error_msg}")
            sys.exit(1)
        else:
            print()
            print("⚠ Unknown response status")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
