#!/usr/bin/env python3
"""
Tests for transaction hash verification utility.
Tests hash validation, null hash handling, and batch processing.
"""

import unittest
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verify_tx_hash import TransactionHashValidator


class TestTransactionHashValidator(unittest.TestCase):
    """Test cases for transaction hash validator."""
    
    def test_valid_ethereum_hash(self):
        """Test validation of valid Ethereum transaction hash."""
        tx_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["format"], "ethereum")
        self.assertFalse(result["is_null"])
        self.assertEqual(result["normalized"], tx_hash.lower())
        self.assertIsNone(result["error"])
    
    def test_valid_bitcoin_hash(self):
        """Test validation of valid Bitcoin transaction hash."""
        tx_hash = "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898"
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["format"], "bitcoin")
        self.assertFalse(result["is_null"])
        self.assertEqual(result["normalized"], tx_hash.lower())
        self.assertIsNone(result["error"])
    
    def test_null_ethereum_hash(self):
        """Test validation of null Ethereum transaction hash."""
        tx_hash = "0x0000000000000000000000000000000000000000000000000000000000000000"
        result = TransactionHashValidator.validate_hash(tx_hash, allow_null=True)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["format"], "ethereum")
        self.assertTrue(result["is_null"])
        self.assertEqual(result["normalized"], tx_hash.lower())
        self.assertIsNone(result["error"])
    
    def test_null_bitcoin_hash(self):
        """Test validation of null Bitcoin transaction hash."""
        tx_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        result = TransactionHashValidator.validate_hash(tx_hash, allow_null=True)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["format"], "bitcoin")
        self.assertTrue(result["is_null"])
        self.assertEqual(result["normalized"], tx_hash.lower())
        self.assertIsNone(result["error"])
    
    def test_null_hash_not_allowed(self):
        """Test validation fails when null hash is not allowed."""
        tx_hash = "0x0000000000000000000000000000000000000000000000000000000000000000"
        result = TransactionHashValidator.validate_hash(tx_hash, allow_null=False)
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["format"], "ethereum")
        self.assertTrue(result["is_null"])
        self.assertIsNotNone(result["error"])
        self.assertIn("not allowed", result["error"])
    
    def test_invalid_hash_too_short(self):
        """Test validation fails for hash that is too short."""
        tx_hash = "0x1234567890abcdef"
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["format"], "invalid")
        self.assertFalse(result["is_null"])
        self.assertIsNotNone(result["error"])
    
    def test_invalid_hash_too_long(self):
        """Test validation fails for hash that is too long."""
        tx_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef00"
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["format"], "invalid")
        self.assertFalse(result["is_null"])
        self.assertIsNotNone(result["error"])
    
    def test_invalid_hash_non_hex(self):
        """Test validation fails for hash with non-hex characters."""
        tx_hash = "0x1234567890abcdefghij567890abcdef1234567890abcdef1234567890abcdef"
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["format"], "invalid")
        self.assertIsNotNone(result["error"])
    
    def test_empty_hash(self):
        """Test validation fails for empty hash."""
        result = TransactionHashValidator.validate_hash("")
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["format"], "invalid")
        self.assertIsNotNone(result["error"])
    
    def test_none_hash(self):
        """Test validation fails for None hash."""
        result = TransactionHashValidator.validate_hash(None)
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["format"], "invalid")
        self.assertIsNotNone(result["error"])
    
    def test_case_insensitive(self):
        """Test validation is case-insensitive."""
        tx_hash_lower = "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        tx_hash_upper = "0xABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890"
        tx_hash_mixed = "0xAbCdEf1234567890aBcDeF1234567890AbCdEf1234567890aBcDeF1234567890"
        
        result_lower = TransactionHashValidator.validate_hash(tx_hash_lower)
        result_upper = TransactionHashValidator.validate_hash(tx_hash_upper)
        result_mixed = TransactionHashValidator.validate_hash(tx_hash_mixed)
        
        self.assertTrue(result_lower["valid"])
        self.assertTrue(result_upper["valid"])
        self.assertTrue(result_mixed["valid"])
        
        # All should normalize to the same lowercase value
        self.assertEqual(result_lower["normalized"], result_upper["normalized"])
        self.assertEqual(result_lower["normalized"], result_mixed["normalized"])
    
    def test_hash_with_whitespace(self):
        """Test validation strips whitespace."""
        tx_hash = "  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef  "
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["format"], "ethereum")
    
    def test_batch_validation_all_valid(self):
        """Test batch validation with all valid hashes."""
        tx_hashes = [
            "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
            "0x0000000000000000000000000000000000000000000000000000000000000000"
        ]
        
        result = TransactionHashValidator.validate_batch(tx_hashes)
        
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["valid"], 3)
        self.assertEqual(result["invalid"], 0)
        self.assertEqual(result["null"], 1)
    
    def test_batch_validation_mixed(self):
        """Test batch validation with mixed valid and invalid hashes."""
        tx_hashes = [
            "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "invalid_hash",
            "0x0000000000000000000000000000000000000000000000000000000000000000",
            "too_short"
        ]
        
        result = TransactionHashValidator.validate_batch(tx_hashes)
        
        self.assertEqual(result["total"], 4)
        self.assertEqual(result["valid"], 2)
        self.assertEqual(result["invalid"], 2)
        self.assertEqual(result["null"], 1)
    
    def test_batch_validation_no_null_allowed(self):
        """Test batch validation with null hashes not allowed."""
        tx_hashes = [
            "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "0x0000000000000000000000000000000000000000000000000000000000000000"
        ]
        
        result = TransactionHashValidator.validate_batch(tx_hashes, allow_null=False)
        
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["valid"], 1)
        self.assertEqual(result["invalid"], 1)
        self.assertEqual(result["null"], 0)
    
    def test_problem_statement_hash(self):
        """Test the exact hash from the problem statement."""
        tx_hash = "0x0000000000000000000000000000000000000000000000000000000000000000"
        result = TransactionHashValidator.validate_hash(tx_hash)
        
        # Verify it's recognized as a valid null hash
        self.assertTrue(result["valid"])
        self.assertEqual(result["format"], "ethereum")
        self.assertTrue(result["is_null"])
        self.assertEqual(
            result["normalized"],
            "0x0000000000000000000000000000000000000000000000000000000000000000"
        )
        self.assertIsNone(result["error"])


class TestTransactionHashConstants(unittest.TestCase):
    """Test cases for transaction hash constants."""
    
    def test_null_hash_constants(self):
        """Test null hash constants are properly defined."""
        self.assertEqual(
            TransactionHashValidator.NULL_TX_HASH_ETH,
            "0x0000000000000000000000000000000000000000000000000000000000000000"
        )
        self.assertEqual(
            TransactionHashValidator.NULL_TX_HASH_BTC,
            "0000000000000000000000000000000000000000000000000000000000000000"
        )
    
    def test_patterns_compiled(self):
        """Test regex patterns are properly compiled."""
        self.assertIsNotNone(TransactionHashValidator.ETH_TX_HASH_PATTERN)
        self.assertIsNotNone(TransactionHashValidator.BTC_TX_HASH_PATTERN)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
