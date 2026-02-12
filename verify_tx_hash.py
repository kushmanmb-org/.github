#!/usr/bin/env python3
"""
Transaction Hash Verification Utility

This utility verifies blockchain transaction hashes, ensuring they are properly
formatted and validated. It supports both Ethereum (0x-prefixed) and Bitcoin
(non-prefixed) transaction hash formats.

Private transaction data should be stored in files that are excluded by .gitignore
patterns (e.g., tx-data/, *tx-hashes*, transaction-data.*, etc.)
"""

import re
import sys
import json
import argparse
from typing import Optional, Dict, Any, List


class TransactionHashValidator:
    """Validates blockchain transaction hashes."""
    
    # Ethereum transaction hash pattern (with 0x prefix)
    ETH_TX_HASH_PATTERN = re.compile(r'^0x[0-9a-fA-F]{64}$')
    
    # Bitcoin transaction hash pattern (without prefix)
    BTC_TX_HASH_PATTERN = re.compile(r'^[0-9a-fA-F]{64}$')
    
    # Null/zero transaction hash (Ethereum format)
    NULL_TX_HASH_ETH = "0x0000000000000000000000000000000000000000000000000000000000000000"
    
    # Null/zero transaction hash (Bitcoin format)
    NULL_TX_HASH_BTC = "0000000000000000000000000000000000000000000000000000000000000000"
    
    @staticmethod
    def validate_hash(tx_hash: str, allow_null: bool = True) -> Dict[str, Any]:
        """
        Validate a transaction hash.
        
        Args:
            tx_hash: The transaction hash to validate
            allow_null: Whether to allow null/zero hashes (default: True)
            
        Returns:
            Dictionary with validation results:
            {
                "valid": bool,
                "format": str ("ethereum" | "bitcoin" | "invalid"),
                "is_null": bool,
                "normalized": str,
                "error": Optional[str]
            }
        """
        if not tx_hash or not isinstance(tx_hash, str):
            return {
                "valid": False,
                "format": "invalid",
                "is_null": False,
                "normalized": "",
                "error": "Transaction hash must be a non-empty string"
            }
        
        # Strip whitespace
        tx_hash = tx_hash.strip()
        
        # Check for Ethereum format (with 0x prefix)
        if TransactionHashValidator.ETH_TX_HASH_PATTERN.match(tx_hash):
            is_null = (tx_hash.lower() == TransactionHashValidator.NULL_TX_HASH_ETH.lower())
            
            if is_null and not allow_null:
                return {
                    "valid": False,
                    "format": "ethereum",
                    "is_null": True,
                    "normalized": TransactionHashValidator.NULL_TX_HASH_ETH,
                    "error": "Null transaction hash is not allowed"
                }
            
            return {
                "valid": True,
                "format": "ethereum",
                "is_null": is_null,
                "normalized": tx_hash.lower(),
                "error": None
            }
        
        # Check for Bitcoin format (without prefix)
        if TransactionHashValidator.BTC_TX_HASH_PATTERN.match(tx_hash):
            is_null = (tx_hash.lower() == TransactionHashValidator.NULL_TX_HASH_BTC.lower())
            
            if is_null and not allow_null:
                return {
                    "valid": False,
                    "format": "bitcoin",
                    "is_null": True,
                    "normalized": TransactionHashValidator.NULL_TX_HASH_BTC,
                    "error": "Null transaction hash is not allowed"
                }
            
            return {
                "valid": True,
                "format": "bitcoin",
                "is_null": is_null,
                "normalized": tx_hash.lower(),
                "error": None
            }
        
        return {
            "valid": False,
            "format": "invalid",
            "is_null": False,
            "normalized": "",
            "error": "Invalid transaction hash format. Expected 64 hex characters (optionally prefixed with 0x)"
        }
    
    @staticmethod
    def validate_batch(tx_hashes: List[str], allow_null: bool = True) -> Dict[str, Any]:
        """
        Validate multiple transaction hashes.
        
        Args:
            tx_hashes: List of transaction hashes to validate
            allow_null: Whether to allow null/zero hashes (default: True)
            
        Returns:
            Dictionary with batch validation results
        """
        results = []
        valid_count = 0
        invalid_count = 0
        null_count = 0
        
        for i, tx_hash in enumerate(tx_hashes):
            result = TransactionHashValidator.validate_hash(tx_hash, allow_null)
            result["index"] = i
            result["input"] = tx_hash
            results.append(result)
            
            if result["valid"]:
                valid_count += 1
                if result["is_null"]:
                    null_count += 1
            else:
                invalid_count += 1
        
        return {
            "total": len(tx_hashes),
            "valid": valid_count,
            "invalid": invalid_count,
            "null": null_count,
            "results": results
        }


def load_tx_hashes_from_file(filepath: str) -> List[str]:
    """
    Load transaction hashes from a file.
    
    Supports:
    - Plain text files (one hash per line)
    - JSON files (array of strings or objects with 'hash' or 'tx_hash' field)
    
    Args:
        filepath: Path to the file containing transaction hashes
        
    Returns:
        List of transaction hash strings
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
            
            # Try to parse as JSON
            try:
                data = json.loads(content)
                
                # Handle array of strings
                if isinstance(data, list):
                    if all(isinstance(item, str) for item in data):
                        return data
                    
                    # Handle array of objects
                    hashes = []
                    for item in data:
                        if isinstance(item, dict):
                            # Try common field names
                            if 'hash' in item:
                                hashes.append(item['hash'])
                            elif 'tx_hash' in item:
                                hashes.append(item['tx_hash'])
                            elif 'txHash' in item:
                                hashes.append(item['txHash'])
                            elif 'transaction_hash' in item:
                                hashes.append(item['transaction_hash'])
                    return hashes
                
                # Handle single hash object
                if isinstance(data, dict):
                    if 'hash' in data:
                        return [data['hash']]
                    elif 'tx_hash' in data:
                        return [data['tx_hash']]
                    elif 'txHash' in data:
                        return [data['txHash']]
                    elif 'transaction_hash' in data:
                        return [data['transaction_hash']]
                
            except json.JSONDecodeError:
                # Not JSON, treat as plain text
                pass
            
            # Parse as plain text (one hash per line)
            lines = content.split('\n')
            hashes = [line.strip() for line in lines if line.strip()]
            return hashes
            
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the transaction hash verification utility."""
    parser = argparse.ArgumentParser(
        description="Verify blockchain transaction hashes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify a single transaction hash
  %(prog)s --hash 0x0000000000000000000000000000000000000000000000000000000000000000

  # Verify multiple hashes
  %(prog)s --hash 0xabc123... --hash 0xdef456...

  # Verify hashes from a file
  %(prog)s --file tx-hashes.txt

  # Disallow null hashes
  %(prog)s --hash 0x00...00 --no-null

  # Output as JSON
  %(prog)s --hash 0xabc123... --json

Note: Private transaction data should be stored in gitignored locations
such as tx-data/, *tx-hashes*, transaction-data.*, etc.
"""
    )
    
    parser.add_argument(
        '--hash',
        action='append',
        dest='hashes',
        help='Transaction hash to verify (can be specified multiple times)'
    )
    
    parser.add_argument(
        '--file',
        dest='file',
        help='File containing transaction hashes (one per line or JSON)'
    )
    
    parser.add_argument(
        '--no-null',
        action='store_true',
        help='Disallow null/zero transaction hashes'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output (requires --json)'
    )
    
    args = parser.parse_args()
    
    # Collect transaction hashes
    tx_hashes = []
    
    if args.hashes:
        tx_hashes.extend(args.hashes)
    
    if args.file:
        tx_hashes.extend(load_tx_hashes_from_file(args.file))
    
    if not tx_hashes:
        parser.print_help()
        sys.exit(1)
    
    # Validate hashes
    allow_null = not args.no_null
    
    if len(tx_hashes) == 1:
        # Single hash validation
        result = TransactionHashValidator.validate_hash(tx_hashes[0], allow_null)
        
        if args.json:
            if args.pretty:
                print(json.dumps(result, indent=2))
            else:
                print(json.dumps(result))
        else:
            print(f"Transaction Hash: {tx_hashes[0]}")
            print(f"Valid: {result['valid']}")
            print(f"Format: {result['format']}")
            print(f"Is Null: {result['is_null']}")
            if result['normalized']:
                print(f"Normalized: {result['normalized']}")
            if result['error']:
                print(f"Error: {result['error']}")
        
        sys.exit(0 if result['valid'] else 1)
    else:
        # Batch validation
        batch_result = TransactionHashValidator.validate_batch(tx_hashes, allow_null)
        
        if args.json:
            if args.pretty:
                print(json.dumps(batch_result, indent=2))
            else:
                print(json.dumps(batch_result))
        else:
            print(f"Total: {batch_result['total']}")
            print(f"Valid: {batch_result['valid']}")
            print(f"Invalid: {batch_result['invalid']}")
            print(f"Null: {batch_result['null']}")
            print()
            
            for result in batch_result['results']:
                status = "✓" if result['valid'] else "✗"
                print(f"{status} [{result['index']}] {result['input']}")
                if result['error']:
                    print(f"   Error: {result['error']}")
        
        sys.exit(0 if batch_result['invalid'] == 0 else 1)


if __name__ == "__main__":
    main()
