#!/usr/bin/env python3
"""
Unit tests for ENS Creator Verification script.

Usage:
    python3 test_verify_ens_creator.py
    python3 -m pytest test_verify_ens_creator.py -v
"""

import unittest
import json
import sys
import os

# Add the parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verify_ens_creator import ENSVerifier


class TestENSVerifier(unittest.TestCase):
    """Test cases for ENS Creator Verification."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_name = "kushmanmb.base.eth"
        self.invalid_name = "kushmanmb.eth"
        
    def test_initialization(self):
        """Test ENSVerifier initialization."""
        verifier = ENSVerifier(self.valid_name)
        self.assertEqual(verifier.ens_name, self.valid_name)
        self.assertEqual(verifier.base_name, "kushmanmb")
        
    def test_extract_base_name_valid(self):
        """Test extracting base name from valid ENS name."""
        verifier = ENSVerifier(self.valid_name)
        self.assertEqual(verifier.base_name, "kushmanmb")
        
    def test_extract_base_name_invalid(self):
        """Test extracting base name from invalid ENS name."""
        verifier = ENSVerifier(self.invalid_name)
        self.assertEqual(verifier.base_name, self.invalid_name)
        
    def test_verify_name_format_valid(self):
        """Test name format verification with valid name."""
        verifier = ENSVerifier(self.valid_name)
        result = verifier.verify_name_format()
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["check"], "name_format")
        self.assertEqual(result["name"], self.valid_name)
        self.assertEqual(result["base_name"], "kushmanmb")
        
    def test_verify_name_format_invalid(self):
        """Test name format verification with invalid name."""
        verifier = ENSVerifier(self.invalid_name)
        result = verifier.verify_name_format()
        
        self.assertFalse(result["valid"])
        self.assertEqual(result["check"], "name_format")
        self.assertIn("must end with .base.eth", result["message"])
        
    def test_verify_creator_status_valid(self):
        """Test creator status verification with valid name."""
        verifier = ENSVerifier(self.valid_name)
        result = verifier.verify_creator_status()
        
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"], "VERIFIED")
        self.assertEqual(result["ens_name"], self.valid_name)
        self.assertEqual(result["base_name"], "kushmanmb")
        self.assertEqual(result["chain_id"], 8453)
        self.assertEqual(result["network"], "Base Mainnet")
        
        # Check that all checks passed
        for check in result["checks"]:
            self.assertTrue(check["valid"])
            
    def test_verify_creator_status_invalid(self):
        """Test creator status verification with invalid name."""
        verifier = ENSVerifier(self.invalid_name)
        result = verifier.verify_creator_status()
        
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "INVALID_FORMAT")
        
    def test_verify_creator_checks_structure(self):
        """Test that verification returns proper check structure."""
        verifier = ENSVerifier(self.valid_name)
        result = verifier.verify_creator_status()
        
        # Verify checks array exists and has expected checks
        self.assertIn("checks", result)
        self.assertIsInstance(result["checks"], list)
        self.assertGreater(len(result["checks"]), 0)
        
        # Verify each check has required fields
        for check in result["checks"]:
            self.assertIn("check", check)
            self.assertIn("valid", check)
            self.assertIn("message", check)
            
    def test_get_announcement_valid(self):
        """Test announcement generation for valid name."""
        verifier = ENSVerifier(self.valid_name)
        announcement = verifier.get_announcement()
        
        self.assertIsInstance(announcement, str)
        self.assertIn("ENS CREATOR STATUS VERIFIED", announcement)
        self.assertIn(self.valid_name, announcement)
        self.assertIn("VERIFIED CREATOR", announcement)
        self.assertIn("Base Mainnet", announcement)
        
    def test_get_announcement_invalid(self):
        """Test announcement generation for invalid name."""
        verifier = ENSVerifier(self.invalid_name)
        announcement = verifier.get_announcement()
        
        self.assertIsInstance(announcement, str)
        self.assertIn("Verification failed", announcement)
        self.assertIn(self.invalid_name, announcement)
        
    def test_chain_configuration(self):
        """Test that Base network configuration is correct."""
        self.assertEqual(ENSVerifier.BASE_CHAIN_ID, 8453)
        self.assertEqual(ENSVerifier.BASE_RPC_URL, "https://mainnet.base.org")
        self.assertIsInstance(ENSVerifier.BASE_REGISTRAR_CONTROLLER, str)
        self.assertIsInstance(ENSVerifier.BASE_REGISTRY, str)
        
    def test_different_base_names(self):
        """Test verification with different base names."""
        test_cases = [
            ("test.base.eth", "test", True),
            ("another.base.eth", "another", True),
            ("test.eth", "test.eth", False),
            ("invalid", "invalid", False),
        ]
        
        for ens_name, expected_base, should_be_valid in test_cases:
            verifier = ENSVerifier(ens_name)
            self.assertEqual(verifier.base_name, expected_base)
            
            result = verifier.verify_name_format()
            self.assertEqual(result["valid"], should_be_valid)


class TestENSVerifierEdgeCases(unittest.TestCase):
    """Test edge cases for ENS Creator Verification."""
    
    def test_empty_name(self):
        """Test with empty name."""
        verifier = ENSVerifier("")
        result = verifier.verify_creator_status()
        self.assertFalse(result["verified"])
        
    def test_only_suffix(self):
        """Test with only .base.eth suffix."""
        verifier = ENSVerifier(".base.eth")
        self.assertEqual(verifier.base_name, "")
        
    def test_multiple_dots(self):
        """Test with subdomain."""
        verifier = ENSVerifier("sub.kushmanmb.base.eth")
        result = verifier.verify_name_format()
        self.assertTrue(result["valid"])
        
    def test_case_sensitivity(self):
        """Test case handling."""
        verifier_upper = ENSVerifier("KUSHMANMB.BASE.ETH")
        verifier_lower = ENSVerifier("kushmanmb.base.eth")
        
        # Both should be treated as valid format
        self.assertTrue(verifier_upper.verify_name_format()["valid"])
        self.assertTrue(verifier_lower.verify_name_format()["valid"])


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestENSVerifier))
    suite.addTests(loader.loadTestsFromTestCase(TestENSVerifierEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
