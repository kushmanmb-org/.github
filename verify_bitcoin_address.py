#!/usr/bin/env python3
"""
Bitcoin Address Verification Utility

This utility verifies Bitcoin addresses using cryptographic validation,
ensuring they are properly formatted and have valid checksums.
Follows security best practices for handling blockchain data.

Key Features:
- Base58Check validation (P2PKH and P2SH addresses)
- Checksum verification using double SHA-256
- Secure error handling without exposing sensitive data
- Support for mainnet and testnet addresses

Private address data should be stored in files that are excluded by
.gitignore patterns (e.g., address-data/, *addresses*, blockchain-address.*, etc.)
"""

import hashlib
import json
import sys
import argparse
from typing import Dict, Any, Optional, List


class BitcoinAddressValidator:
    """Validates Bitcoin addresses using Base58Check encoding."""
    
    # Bitcoin address version bytes
    MAINNET_P2PKH = 0x00  # Pay-to-PubKey-Hash (starts with '1')
    MAINNET_P2SH = 0x05   # Pay-to-Script-Hash (starts with '3')
    TESTNET_P2PKH = 0x6F  # Testnet P2PKH (starts with 'm' or 'n')
    TESTNET_P2SH = 0xC4   # Testnet P2SH (starts with '2')
    
    # Base58 character set used by Bitcoin
    BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    @staticmethod
    def base58_decode(address: str) -> Optional[bytes]:
        """
        Decode a Base58 encoded string to bytes.
        
        Args:
            address: Base58 encoded address string
            
        Returns:
            Decoded bytes or None if invalid
        """
        try:
            # Convert Base58 string to integer
            decoded_int = 0
            for char in address:
                if char not in BitcoinAddressValidator.BASE58_ALPHABET:
                    return None
                decoded_int = decoded_int * 58 + BitcoinAddressValidator.BASE58_ALPHABET.index(char)
            
            # Convert integer to bytes
            decoded_bytes = decoded_int.to_bytes(25, byteorder='big')
            
            # Handle leading zeros (represented as '1' in Base58)
            num_leading_zeros = len(address) - len(address.lstrip('1'))
            if num_leading_zeros > 0:
                decoded_bytes = b'\x00' * num_leading_zeros + decoded_bytes[num_leading_zeros:]
            
            return decoded_bytes
        except (ValueError, OverflowError):
            return None
    
    @staticmethod
    def verify_checksum(address_bytes: bytes) -> bool:
        """
        Verify the checksum of a Bitcoin address.
        
        Args:
            address_bytes: Decoded address bytes (should be 25 bytes)
            
        Returns:
            True if checksum is valid, False otherwise
        """
        if len(address_bytes) != 25:
            return False
        
        # Split payload and checksum
        payload = address_bytes[:-4]
        checksum = address_bytes[-4:]
        
        # Calculate expected checksum using double SHA-256
        hash_result = hashlib.sha256(hashlib.sha256(payload).digest()).digest()
        expected_checksum = hash_result[:4]
        
        return checksum == expected_checksum
    
    @staticmethod
    def get_address_type(version_byte: int) -> str:
        """
        Get the address type from version byte.
        
        Args:
            version_byte: First byte of decoded address
            
        Returns:
            Human-readable address type
        """
        if version_byte == BitcoinAddressValidator.MAINNET_P2PKH:
            return "mainnet_p2pkh"
        elif version_byte == BitcoinAddressValidator.MAINNET_P2SH:
            return "mainnet_p2sh"
        elif version_byte == BitcoinAddressValidator.TESTNET_P2PKH:
            return "testnet_p2pkh"
        elif version_byte == BitcoinAddressValidator.TESTNET_P2SH:
            return "testnet_p2sh"
        else:
            return f"unknown_0x{version_byte:02x}"
    
    @classmethod
    def validate_address(cls, address: str) -> Dict[str, Any]:
        """
        Validate a Bitcoin address.
        
        Args:
            address: The Bitcoin address to validate
            
        Returns:
            Dictionary with validation results:
            {
                "valid": bool,
                "address": str,
                "type": str,
                "network": str ("mainnet" | "testnet" | "unknown"),
                "format": str ("p2pkh" | "p2sh" | "unknown"),
                "error": str (if not valid)
            }
        """
        result = {
            "valid": False,
            "address": address,
            "type": "unknown",
            "network": "unknown",
            "format": "unknown"
        }
        
        # Basic validation
        if not address or not isinstance(address, str):
            result["error"] = "Address must be a non-empty string"
            return result
        
        # Check length (Bitcoin addresses are typically 26-35 characters)
        if len(address) < 26 or len(address) > 35:
            result["error"] = f"Invalid address length: {len(address)} (expected 26-35 characters)"
            return result
        
        # Decode Base58
        decoded = cls.base58_decode(address)
        if decoded is None:
            result["error"] = "Failed to decode Base58 address"
            return result
        
        # Verify checksum
        if not cls.verify_checksum(decoded):
            result["error"] = "Invalid checksum"
            return result
        
        # Get version byte and determine address type
        version_byte = decoded[0]
        address_type = cls.get_address_type(version_byte)
        result["type"] = address_type
        
        # Determine network and format
        if version_byte == cls.MAINNET_P2PKH:
            result["network"] = "mainnet"
            result["format"] = "p2pkh"
            result["valid"] = True
        elif version_byte == cls.MAINNET_P2SH:
            result["network"] = "mainnet"
            result["format"] = "p2sh"
            result["valid"] = True
        elif version_byte == cls.TESTNET_P2PKH:
            result["network"] = "testnet"
            result["format"] = "p2pkh"
            result["valid"] = True
        elif version_byte == cls.TESTNET_P2SH:
            result["network"] = "testnet"
            result["format"] = "p2sh"
            result["valid"] = True
        else:
            result["error"] = f"Unknown address version byte: 0x{version_byte:02x}"
        
        return result


def validate_file(filepath: str, pretty: bool = False) -> Dict[str, Any]:
    """
    Validate Bitcoin addresses from a JSON file.
    
    Args:
        filepath: Path to JSON file containing address data
        pretty: Pretty print JSON output
        
    Returns:
        Dictionary with validation results
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        addresses_to_validate = []
        
        if isinstance(data, dict):
            # Single address object
            if 'address' in data:
                addresses_to_validate.append(data['address'])
            # List of addresses
            elif 'addresses' in data:
                addresses_to_validate = data['addresses']
        elif isinstance(data, list):
            # List of address objects
            for item in data:
                if isinstance(item, dict) and 'address' in item:
                    addresses_to_validate.append(item['address'])
                elif isinstance(item, str):
                    addresses_to_validate.append(item)
        
        if not addresses_to_validate:
            return {
                "error": "No addresses found in file",
                "file": filepath
            }
        
        # Validate all addresses
        results = []
        for addr in addresses_to_validate:
            validation = BitcoinAddressValidator.validate_address(addr)
            results.append(validation)
        
        return {
            "file": filepath,
            "total_addresses": len(results),
            "valid_addresses": sum(1 for r in results if r["valid"]),
            "invalid_addresses": sum(1 for r in results if not r["valid"]),
            "results": results
        }
    
    except FileNotFoundError:
        return {"error": f"File not found: {filepath}"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def main():
    """Main entry point for the Bitcoin address verification utility."""
    parser = argparse.ArgumentParser(
        description='Bitcoin Address Verification Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify a single Bitcoin address
  %(prog)s --address 1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv
  
  # Verify addresses from a JSON file
  %(prog)s --file blockchain-address.json
  
  # Output as pretty-printed JSON
  %(prog)s --address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa --json --pretty
  
  # Verify multiple addresses
  %(prog)s --address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa --address 3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy
        """
    )
    
    parser.add_argument(
        '--address',
        action='append',
        help='Bitcoin address to validate (can be specified multiple times)'
    )
    parser.add_argument(
        '--file',
        help='JSON file containing Bitcoin address(es) to validate'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output'
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.address and not args.file:
        parser.error('Either --address or --file must be specified')
    
    results = []
    
    # Validate addresses from command line
    if args.address:
        for addr in args.address:
            result = BitcoinAddressValidator.validate_address(addr)
            results.append(result)
    
    # Validate addresses from file
    if args.file:
        file_result = validate_file(args.file, args.pretty)
        if args.address:
            # Combine results
            results = {
                "command_line_addresses": results,
                "file_validation": file_result
            }
        else:
            results = file_result
    elif len(results) == 1:
        results = results[0]
    
    # Output results
    if args.json:
        if args.pretty:
            print(json.dumps(results, indent=2))
        else:
            print(json.dumps(results))
    else:
        # Human-readable output
        if isinstance(results, dict):
            if 'file' in results:
                # File validation results
                print(f"\nFile: {results['file']}")
                if 'error' in results:
                    print(f"Error: {results['error']}")
                    return 1
                print(f"Total addresses: {results['total_addresses']}")
                print(f"Valid addresses: {results['valid_addresses']}")
                print(f"Invalid addresses: {results['invalid_addresses']}")
                print("\nDetails:")
                for r in results['results']:
                    status = "✓ VALID" if r['valid'] else "✗ INVALID"
                    print(f"  {status}: {r['address']}")
                    if r['valid']:
                        print(f"    Network: {r['network']}")
                        print(f"    Format: {r['format']}")
                        print(f"    Type: {r['type']}")
                    else:
                        print(f"    Error: {r.get('error', 'Unknown error')}")
            elif 'command_line_addresses' in results:
                # Combined results
                print("\nCommand Line Addresses:")
                for r in results['command_line_addresses']:
                    status = "✓ VALID" if r['valid'] else "✗ INVALID"
                    print(f"  {status}: {r['address']}")
                    if not r['valid']:
                        print(f"    Error: {r.get('error', 'Unknown error')}")
                
                print("\nFile Validation:")
                file_res = results['file_validation']
                if 'error' in file_res:
                    print(f"  Error: {file_res['error']}")
                else:
                    print(f"  Total: {file_res['total_addresses']}")
                    print(f"  Valid: {file_res['valid_addresses']}")
                    print(f"  Invalid: {file_res['invalid_addresses']}")
            else:
                # Single address validation
                status = "✓ VALID" if results['valid'] else "✗ INVALID"
                print(f"\n{status}: {results['address']}")
                if results['valid']:
                    print(f"Network: {results['network']}")
                    print(f"Format: {results['format']}")
                    print(f"Type: {results['type']}")
                else:
                    print(f"Error: {results.get('error', 'Unknown error')}")
        elif isinstance(results, list):
            # Multiple addresses from command line
            print()
            for r in results:
                status = "✓ VALID" if r['valid'] else "✗ INVALID"
                print(f"{status}: {r['address']}")
                if r['valid']:
                    print(f"  Network: {r['network']}")
                    print(f"  Format: {r['format']}")
                    print(f"  Type: {r['type']}")
                else:
                    print(f"  Error: {r.get('error', 'Unknown error')}")
                print()
    
    # Return exit code based on validation results
    if isinstance(results, dict):
        if 'valid' in results:
            return 0 if results['valid'] else 1
        elif 'invalid_addresses' in results:
            return 0 if results['invalid_addresses'] == 0 else 1
        elif 'error' in results:
            return 1
    elif isinstance(results, list):
        return 0 if all(r['valid'] for r in results) else 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
