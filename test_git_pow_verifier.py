#!/usr/bin/env python3
"""
Tests for Git POW (Proof of Work) verification utility.
Tests commit SHA validation, signature verification, and batch processing.
"""

import unittest
import sys
import os
import json
import tempfile
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_pow_verifier import GitCommitVerifier


class TestGitCommitVerifier(unittest.TestCase):
    """Test cases for Git commit verifier."""
    
    def test_valid_full_commit_sha(self):
        """Test validation of valid full commit SHA."""
        commit_sha = "1234567890abcdef1234567890abcdef12345678"
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["normalized"], commit_sha.lower())
        self.assertIsNone(result["error"])
    
    def test_valid_short_commit_sha(self):
        """Test validation of valid short commit SHA (7 characters)."""
        commit_sha = "1234567"
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["normalized"], commit_sha.lower())
        self.assertIsNone(result["error"])
    
    def test_valid_medium_commit_sha(self):
        """Test validation of valid medium commit SHA (10 characters)."""
        commit_sha = "1234567890"
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["normalized"], commit_sha.lower())
        self.assertIsNone(result["error"])
    
    def test_uppercase_commit_sha(self):
        """Test validation normalizes uppercase to lowercase."""
        commit_sha = "ABCDEF1234567890ABCDEF1234567890ABCDEF12"
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["normalized"], commit_sha.lower())
        self.assertIsNone(result["error"])
    
    def test_mixed_case_commit_sha(self):
        """Test validation normalizes mixed case to lowercase."""
        commit_sha = "AbCdEf1234567890AbCdEf1234567890AbCdEf12"
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["normalized"], commit_sha.lower())
        self.assertIsNone(result["error"])
    
    def test_invalid_commit_sha_too_short(self):
        """Test validation fails for commit SHA that is too short."""
        commit_sha = "123456"  # Only 6 characters
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])
        self.assertIn("Invalid", result["error"])
    
    def test_invalid_commit_sha_too_long(self):
        """Test validation fails for commit SHA that is too long."""
        commit_sha = "1234567890abcdef1234567890abcdef123456789"  # 41 characters
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])
        self.assertIn("Invalid", result["error"])
    
    def test_invalid_commit_sha_non_hex(self):
        """Test validation fails for commit SHA with non-hex characters."""
        commit_sha = "1234567890abcdefghij1234567890abcdef1234"
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])
    
    def test_invalid_commit_sha_empty(self):
        """Test validation fails for empty commit SHA."""
        commit_sha = ""
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])
        self.assertIn("non-empty string", result["error"])
    
    def test_invalid_commit_sha_none(self):
        """Test validation fails for None commit SHA."""
        commit_sha = None
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])
    
    def test_invalid_commit_sha_whitespace(self):
        """Test validation fails for whitespace-only commit SHA."""
        commit_sha = "   "
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])
    
    def test_commit_sha_with_leading_trailing_whitespace(self):
        """Test validation strips leading/trailing whitespace."""
        commit_sha = "  1234567890abcdef1234567890abcdef12345678  "
        result = GitCommitVerifier.validate_commit_sha(commit_sha)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["normalized"], "1234567890abcdef1234567890abcdef12345678")
        self.assertIsNone(result["error"])
    
    def test_is_git_repository_current_dir(self):
        """Test checking if current directory is a Git repository."""
        # We're running in a Git repository
        result = GitCommitVerifier.is_git_repository(".")
        self.assertTrue(result)
    
    def test_is_git_repository_absolute_path(self):
        """Test checking if absolute path is a Git repository."""
        # Use the current directory's absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        result = GitCommitVerifier.is_git_repository(current_dir)
        self.assertTrue(result)
    
    def test_is_not_git_repository(self):
        """Test checking a directory that is not a Git repository."""
        # /tmp is typically not a Git repository
        result = GitCommitVerifier.is_git_repository("/tmp")
        self.assertFalse(result)
    
    def test_verify_commit_invalid_sha_format(self):
        """Test verification fails gracefully for invalid SHA format."""
        # Use an empty string which should fail
        result = GitCommitVerifier.verify_commit_signature("")
        
        self.assertFalse(result["valid"])
        self.assertFalse(result["signed"])
        self.assertIsNotNone(result["error"])
        self.assertIn("non-empty string", result["error"])
    
    def test_verify_commit_in_current_repo(self):
        """Test verification of a commit in the current repository."""
        # Get the current HEAD commit
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            commit_sha = result.stdout.strip()
            
            # Verify the commit
            verification = GitCommitVerifier.verify_commit_signature(commit_sha)
            
            # Should have a valid result structure
            self.assertIn("commit", verification)
            self.assertIn("signed", verification)
            self.assertIn("valid", verification)
            self.assertEqual(verification["commit"], commit_sha)
            
        except subprocess.CalledProcessError:
            # Skip test if we can't get HEAD
            self.skipTest("Could not get HEAD commit")
    
    def test_verify_commit_with_head_ref(self):
        """Test verification using HEAD reference."""
        verification = GitCommitVerifier.verify_commit_signature("HEAD")
        
        # Should have a valid result structure
        self.assertIn("commit", verification)
        self.assertIn("signed", verification)
        self.assertIn("valid", verification)
    
    def test_get_commit_info(self):
        """Test getting commit information."""
        # Get info for HEAD
        info = GitCommitVerifier.get_commit_info("HEAD")
        
        self.assertIn("full_sha", info)
        self.assertIn("short_sha", info)
        self.assertIn("author_name", info)
        self.assertIn("author_email", info)
        self.assertIn("timestamp", info)
        self.assertIn("subject", info)
        
        # Validate some fields
        self.assertTrue(len(info["full_sha"]) == 40)
        self.assertTrue(len(info["short_sha"]) >= 7)
        self.assertTrue(info["timestamp"] > 0)
    
    def test_verify_commits_from_file_list_format(self):
        """Test verifying commits from a JSON file with list format."""
        # Create a temporary JSON file with commit list
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                "HEAD",
                "HEAD~1"
            ], f)
            temp_file = f.name
        
        try:
            results = GitCommitVerifier.verify_commits_from_file(temp_file)
            
            self.assertEqual(len(results), 2)
            for result in results:
                self.assertIn("commit", result)
                self.assertIn("signed", result)
                self.assertIn("valid", result)
        finally:
            os.unlink(temp_file)
    
    def test_verify_commits_from_file_object_format(self):
        """Test verifying commits from a JSON file with object format."""
        # Create a temporary JSON file with commits object
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "commits": [
                    {"sha": "HEAD"},
                    {"commit": "HEAD~1"}
                ]
            }, f)
            temp_file = f.name
        
        try:
            results = GitCommitVerifier.verify_commits_from_file(temp_file)
            
            self.assertEqual(len(results), 2)
            for result in results:
                self.assertIn("commit", result)
                self.assertIn("signed", result)
                self.assertIn("valid", result)
        finally:
            os.unlink(temp_file)
    
    def test_verify_commits_from_nonexistent_file(self):
        """Test verifying commits from a non-existent file."""
        results = GitCommitVerifier.verify_commits_from_file("/nonexistent/file.json")
        
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0]["valid"])
        self.assertIn("not found", results[0]["error"].lower())
    
    def test_verify_commits_from_invalid_json_file(self):
        """Test verifying commits from a file with invalid JSON."""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_file = f.name
        
        try:
            results = GitCommitVerifier.verify_commits_from_file(temp_file)
            
            self.assertEqual(len(results), 1)
            self.assertFalse(results[0]["valid"])
            self.assertIn("JSON", results[0]["error"])
        finally:
            os.unlink(temp_file)
    
    def test_verify_commits_from_file_invalid_format(self):
        """Test verifying commits from a file with invalid format."""
        # Create a temporary JSON file with invalid format
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"invalid": "format"}, f)
            temp_file = f.name
        
        try:
            results = GitCommitVerifier.verify_commits_from_file(temp_file)
            
            self.assertEqual(len(results), 1)
            self.assertFalse(results[0]["valid"])
            self.assertIn("format", results[0]["error"].lower())
        finally:
            os.unlink(temp_file)
    
    def test_verify_commits_from_file_mixed_valid_invalid(self):
        """Test verifying commits with mix of valid and invalid SHAs."""
        # Create a temporary JSON file with mixed commits
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                "HEAD",
                "invalid_sha",
                {"sha": "HEAD~1"}
            ], f)
            temp_file = f.name
        
        try:
            results = GitCommitVerifier.verify_commits_from_file(temp_file)
            
            self.assertEqual(len(results), 3)
            # First should be valid structure
            self.assertIn("commit", results[0])
            # Second should fail validation
            self.assertFalse(results[1]["valid"])
            # Third should be valid structure
            self.assertIn("commit", results[2])
        finally:
            os.unlink(temp_file)


class TestVerificationOutput(unittest.TestCase):
    """Test cases for verification output formatting."""
    
    def test_format_valid_signature(self):
        """Test formatting of valid signature result."""
        from git_pow_verifier import format_verification_result
        
        result = {
            "commit": "abc123",
            "signed": True,
            "valid": True,
            "signer": "John Doe <john@example.com>",
            "key_id": "ABCD1234",
            "trust_level": "ultimate"
        }
        
        output = format_verification_result(result)
        
        self.assertIn("abc123", output)
        self.assertIn("VALID", output)
        self.assertIn("John Doe", output)
        self.assertIn("ABCD1234", output)
    
    def test_format_unsigned_commit(self):
        """Test formatting of unsigned commit result."""
        from git_pow_verifier import format_verification_result
        
        result = {
            "commit": "xyz789",
            "signed": False,
            "valid": False,
            "error": "Commit is not signed"
        }
        
        output = format_verification_result(result)
        
        self.assertIn("xyz789", output)
        self.assertIn("ERROR", output)
        self.assertIn("Commit is not signed", output)
    
    def test_format_signed_but_unverified(self):
        """Test formatting of signed but unverified commit result."""
        from git_pow_verifier import format_verification_result
        
        result = {
            "commit": "def456",
            "signed": True,
            "valid": False,
            "error": "Cannot check signature: GPG key not found in keyring"
        }
        
        output = format_verification_result(result)
        
        self.assertIn("def456", output)
        self.assertIn("ERROR", output)
        self.assertIn("Cannot check signature", output)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
