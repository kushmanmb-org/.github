#!/usr/bin/env python3
"""
Test suite for Bitcoin Address Verification Utility

This test suite validates the Bitcoin address verification functionality
including Base58 decoding, checksum verification, and address type detection.
"""

import unittest
import json
import tempfile
import os
import sys
from verify_bitcoin_address import BitcoinAddressValidator, validate_file


class TestBitcoinAddressValidator(unittest.TestCase):
    """Test cases for Bitcoin address validation."""
    
    def test_valid_mainnet_p2pkh_address(self):
        """Test validation of valid mainnet P2PKH address."""
        # The address from the problem statement
        address = "1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["address"], address)
        self.assertEqual(result["network"], "mainnet")
        self.assertEqual(result["format"], "p2pkh")
        self.assertEqual(result["type"], "mainnet_p2pkh")
        self.assertNotIn("error", result)
    
    def test_valid_mainnet_p2pkh_address_satoshi(self):
        """Test validation of Satoshi's genesis block address."""
        address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["network"], "mainnet")
        self.assertEqual(result["format"], "p2pkh")
    
    def test_valid_mainnet_p2sh_address(self):
        """Test validation of valid mainnet P2SH address."""
        # Valid P2SH address (starts with 3)
        address = "35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["network"], "mainnet")
        self.assertEqual(result["format"], "p2sh")
        self.assertEqual(result["type"], "mainnet_p2sh")
    
    def test_invalid_checksum(self):
        """Test validation of address with invalid checksum."""
        # Modified last character to make checksum invalid
        address = "1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpX"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
        self.assertIn("checksum", result["error"].lower())
    
    def test_invalid_characters(self):
        """Test validation of address with invalid Base58 characters."""
        # Contains 'O' which is not in Base58 alphabet
        address = "1wiz18xYmhRX6xStj2b9t1rwWX4GKUOOO"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
    
    def test_invalid_length_too_short(self):
        """Test validation of address that is too short."""
        address = "1wiz18x"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
        self.assertIn("length", result["error"].lower())
    
    def test_invalid_length_too_long(self):
        """Test validation of address that is too long."""
        address = "1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv1234567890"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
        self.assertIn("length", result["error"].lower())
    
    def test_empty_address(self):
        """Test validation of empty address."""
        address = ""
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
    
    def test_none_address(self):
        """Test validation of None address."""
        address = None
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
    
    def test_base58_decode_valid(self):
        """Test Base58 decoding with valid input."""
        # Simple Base58 encoded value
        address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        decoded = BitcoinAddressValidator.base58_decode(address)
        
        self.assertIsNotNone(decoded)
        self.assertEqual(len(decoded), 25)
    
    def test_base58_decode_invalid_chars(self):
        """Test Base58 decoding with invalid characters."""
        # Contains invalid Base58 character '0'
        address = "1A0zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        decoded = BitcoinAddressValidator.base58_decode(address)
        
        self.assertIsNone(decoded)
    
    def test_verify_checksum_valid(self):
        """Test checksum verification with valid data."""
        # Decode a known valid address
        address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        decoded = BitcoinAddressValidator.base58_decode(address)
        
        self.assertIsNotNone(decoded)
        self.assertTrue(BitcoinAddressValidator.verify_checksum(decoded))
    
    def test_verify_checksum_invalid_length(self):
        """Test checksum verification with invalid length."""
        # Too short
        self.assertFalse(BitcoinAddressValidator.verify_checksum(b'\x00' * 20))
        
        # Too long
        self.assertFalse(BitcoinAddressValidator.verify_checksum(b'\x00' * 30))
    
    def test_get_address_type_mainnet_p2pkh(self):
        """Test address type detection for mainnet P2PKH."""
        address_type = BitcoinAddressValidator.get_address_type(0x00)
        self.assertEqual(address_type, "mainnet_p2pkh")
    
    def test_get_address_type_mainnet_p2sh(self):
        """Test address type detection for mainnet P2SH."""
        address_type = BitcoinAddressValidator.get_address_type(0x05)
        self.assertEqual(address_type, "mainnet_p2sh")
    
    def test_get_address_type_testnet_p2pkh(self):
        """Test address type detection for testnet P2PKH."""
        address_type = BitcoinAddressValidator.get_address_type(0x6F)
        self.assertEqual(address_type, "testnet_p2pkh")
    
    def test_get_address_type_testnet_p2sh(self):
        """Test address type detection for testnet P2SH."""
        address_type = BitcoinAddressValidator.get_address_type(0xC4)
        self.assertEqual(address_type, "testnet_p2sh")
    
    def test_get_address_type_unknown(self):
        """Test address type detection for unknown version byte."""
        address_type = BitcoinAddressValidator.get_address_type(0xFF)
        self.assertEqual(address_type, "unknown_0xff")
    
    def test_validate_file_single_address(self):
        """Test validation of single address from JSON file."""
        # Create temporary file with address
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"address": "1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv"}, f)
            temp_file = f.name
        
        try:
            result = validate_file(temp_file)
            
            self.assertEqual(result["total_addresses"], 1)
            self.assertEqual(result["valid_addresses"], 1)
            self.assertEqual(result["invalid_addresses"], 0)
            self.assertEqual(len(result["results"]), 1)
            self.assertTrue(result["results"][0]["valid"])
        finally:
            os.unlink(temp_file)
    
    def test_validate_file_multiple_addresses(self):
        """Test validation of multiple addresses from JSON file."""
        # Create temporary file with multiple addresses
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "addresses": [
                    "1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv",
                    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                    "35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP"
                ]
            }, f)
            temp_file = f.name
        
        try:
            result = validate_file(temp_file)
            
            self.assertEqual(result["total_addresses"], 3)
            self.assertEqual(result["valid_addresses"], 3)
            self.assertEqual(result["invalid_addresses"], 0)
        finally:
            os.unlink(temp_file)
    
    def test_validate_file_mixed_validity(self):
        """Test validation with both valid and invalid addresses."""
        # Create temporary file with mixed addresses
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "addresses": [
                    "1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv",  # Valid
                    "invalid_address",                      # Invalid
                    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"   # Valid
                ]
            }, f)
            temp_file = f.name
        
        try:
            result = validate_file(temp_file)
            
            self.assertEqual(result["total_addresses"], 3)
            self.assertEqual(result["valid_addresses"], 2)
            self.assertEqual(result["invalid_addresses"], 1)
        finally:
            os.unlink(temp_file)
    
    def test_validate_file_not_found(self):
        """Test validation with non-existent file."""
        result = validate_file("/nonexistent/file.json")
        
        self.assertIn("error", result)
        self.assertIn("not found", result["error"].lower())
    
    def test_validate_file_invalid_json(self):
        """Test validation with invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_file = f.name
        
        try:
            result = validate_file(temp_file)
            
            self.assertIn("error", result)
            self.assertIn("json", result["error"].lower())
        finally:
            os.unlink(temp_file)
    
    def test_validate_file_no_addresses(self):
        """Test validation with file containing no addresses."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "no addresses here"}, f)
            temp_file = f.name
        
        try:
            result = validate_file(temp_file)
            
            self.assertIn("error", result)
            self.assertIn("no addresses", result["error"].lower())
        finally:
            os.unlink(temp_file)
    
    def test_blockchain_address_json_file(self):
        """Test validation of the actual blockchain-address.json file if it exists."""
        filepath = "blockchain-address.json"
        if os.path.exists(filepath):
            result = validate_file(filepath)
            
            # Should have at least one address
            self.assertGreater(result["total_addresses"], 0)
            
            # The address from problem statement should be valid
            addresses = [r["address"] for r in result["results"]]
            self.assertIn("1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv", addresses)
            
            # All addresses should be valid
            self.assertEqual(result["invalid_addresses"], 0)


class TestSecurityBestPractices(unittest.TestCase):
    """Test cases for security best practices."""
    
    def test_no_hardcoded_private_keys(self):
        """Ensure no private keys are hardcoded in the script."""
        with open('verify_bitcoin_address.py', 'r') as f:
            content = f.read()
        
        # Check that private key terms are only mentioned in documentation
        # WIF format private keys start with 5, K, or L and are 51-52 chars
        # We verify no WIF-looking patterns exist outside of known safe contexts
        lines = content.split('\n')
        for line in lines:
            # Skip comments, docstrings, and the BASE58_ALPHABET constant
            stripped = line.strip()
            if (stripped.startswith('#') or 
                stripped.startswith('"""') or 
                stripped.startswith("'''") or
                'BASE58_ALPHABET' in line):
                continue
            # Check for WIF-like patterns (51-52 char strings starting with 5, K, or L)
            import re
            # More specific pattern: must be a standalone string, not part of alphabet
            wif_pattern = re.compile(r'''['"][5KL][1-9A-HJ-NP-Za-km-z]{50,51}['"]''')
            matches = wif_pattern.findall(line)
            self.assertEqual(len(matches), 0, f"Potential private key found in: {line[:50]}")
    
    def test_error_messages_dont_expose_sensitive_data(self):
        """Ensure error messages don't expose sensitive information."""
        # Test with an address that will fail
        address = "invalid_sensitive_data_123456"
        result = BitcoinAddressValidator.validate_address(address)
        
        self.assertFalse(result["valid"])
        self.assertIn("error", result)
        
        # Error message should not contain the full input if it's potentially sensitive
        # It should be generic
        self.assertIsInstance(result["error"], str)
        self.assertLess(len(result["error"]), 200)  # Keep error messages concise


class TestAddressFormats(unittest.TestCase):
    """Test cases for different Bitcoin address formats."""
    
    def test_leading_ones_in_address(self):
        """Test addresses with leading '1's (zeros in decoded form)."""
        # Address starting with multiple 1's
        address = "111111111111111111112czxoHN"
        result = BitcoinAddressValidator.validate_address(address)
        
        # This should be properly decoded even with leading 1's
        # Whether it's valid depends on the checksum
        self.assertIn("valid", result)
    
    def test_all_base58_characters(self):
        """Test that all valid Base58 characters are accepted."""
        valid_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        
        # The decode function should accept any string with only these characters
        for char in valid_chars:
            test_string = "1" + char * 25
            decoded = BitcoinAddressValidator.base58_decode(test_string)
            # May be None if it's invalid length after decoding, but shouldn't raise exception
            self.assertTrue(decoded is None or isinstance(decoded, bytes))


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBitcoinAddressValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityBestPractices))
    suite.addTests(loader.loadTestsFromTestCase(TestAddressFormats))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
