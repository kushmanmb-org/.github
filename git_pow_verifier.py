#!/usr/bin/env python3
"""
Git POW (Proof of Work) Verification Utility

This utility verifies Git commit signatures using GPG, ensuring commits are properly
signed and authenticated. It follows security best practices for handling cryptographic
verification data.

Private verification data should be stored in files that are excluded by .gitignore
patterns (e.g., verification-data/, *verification-config*, gpg-verification.*, etc.)

Security Best Practices:
- Never commit GPG private keys or passphrases
- Store verification policies in .gitignore-protected files
- Use environment variables for sensitive configuration
- Verify commit signatures against trusted public keys
"""

import re
import sys
import json
import argparse
import subprocess
import os
from typing import Optional, Dict, Any, List
from pathlib import Path


class GitCommitVerifier:
    """Verifies Git commit signatures using GPG."""
    
    # Git commit SHA pattern (40 hex characters)
    COMMIT_SHA_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')
    
    # Short commit SHA pattern (7+ hex characters)
    SHORT_COMMIT_SHA_PATTERN = re.compile(r'^[0-9a-fA-F]{7,40}$')
    
    @staticmethod
    def is_git_repository(path: str = ".") -> bool:
        """
        Check if the current directory is a Git repository.
        
        Args:
            path: Path to check (default: current directory)
            
        Returns:
            True if path is a Git repository, False otherwise
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    def validate_commit_sha(commit_sha: str, resolve_refs: bool = False) -> Dict[str, Any]:
        """
        Validate a Git commit SHA.
        
        Args:
            commit_sha: The commit SHA to validate
            resolve_refs: If True, allow Git references like HEAD (default: False)
            
        Returns:
            Dictionary with validation results:
            {
                "valid": bool,
                "normalized": str,
                "error": Optional[str]
            }
        """
        if not commit_sha or not isinstance(commit_sha, str):
            return {
                "valid": False,
                "normalized": "",
                "error": "Commit SHA must be a non-empty string"
            }
        
        # Strip whitespace
        commit_sha = commit_sha.strip()
        
        # If resolve_refs is True, allow any non-empty string (Git will resolve it)
        if resolve_refs:
            return {
                "valid": True,
                "normalized": commit_sha,
                "error": None
            }
        
        # Check for valid commit SHA format (full or short)
        if GitCommitVerifier.COMMIT_SHA_PATTERN.match(commit_sha):
            return {
                "valid": True,
                "normalized": commit_sha.lower(),
                "error": None
            }
        
        if GitCommitVerifier.SHORT_COMMIT_SHA_PATTERN.match(commit_sha):
            return {
                "valid": True,
                "normalized": commit_sha.lower(),
                "error": None
            }
        
        return {
            "valid": False,
            "normalized": "",
            "error": f"Invalid commit SHA format: {commit_sha}"
        }
    
    @staticmethod
    def verify_commit_signature(commit_sha: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Verify the GPG signature of a Git commit.
        
        Args:
            commit_sha: The commit SHA to verify
            repo_path: Path to the Git repository (default: current directory)
            
        Returns:
            Dictionary with verification results:
            {
                "commit": str,
                "signed": bool,
                "valid": bool,
                "key_id": Optional[str],
                "signer": Optional[str],
                "fingerprint": Optional[str],
                "trust_level": Optional[str],
                "error": Optional[str],
                "raw_output": str
            }
        """
        # Validate commit SHA format (allow Git refs like HEAD)
        validation = GitCommitVerifier.validate_commit_sha(commit_sha, resolve_refs=True)
        if not validation["valid"]:
            return {
                "commit": commit_sha,
                "signed": False,
                "valid": False,
                "key_id": None,
                "signer": None,
                "fingerprint": None,
                "trust_level": None,
                "error": validation["error"],
                "raw_output": ""
            }
        
        # Check if path is a Git repository
        if not GitCommitVerifier.is_git_repository(repo_path):
            return {
                "commit": commit_sha,
                "signed": False,
                "valid": False,
                "key_id": None,
                "signer": None,
                "fingerprint": None,
                "trust_level": None,
                "error": f"Not a Git repository: {repo_path}",
                "raw_output": ""
            }
        
        try:
            # Run git verify-commit command
            result = subprocess.run(
                ["git", "verify-commit", "-v", commit_sha],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            
            raw_output = result.stderr + result.stdout
            
            # Parse verification output
            signed = "gpg: Signature made" in raw_output or "Good signature" in raw_output
            valid = result.returncode == 0 and "Good signature" in raw_output
            
            # Extract key information from GPG output
            key_id = None
            signer = None
            fingerprint = None
            trust_level = None
            
            for line in raw_output.split('\n'):
                # Extract key ID
                if "using" in line.lower() and ("RSA" in line or "DSA" in line or "ECDSA" in line or "EdDSA" in line):
                    # Pattern: "gpg: using RSA key ABCD1234..."
                    parts = line.split()
                    if len(parts) >= 4:
                        key_id = parts[-1]
                
                # Extract signer information
                if "Good signature from" in line or "signature from" in line:
                    # Pattern: 'gpg: Good signature from "Name <email@example.com>"'
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        signer = match.group(1)
                
                # Extract fingerprint
                if "fingerprint:" in line.lower():
                    parts = line.split()
                    if len(parts) >= 2:
                        fingerprint = parts[-1]
                
                # Extract trust level
                if "trust:" in line.lower():
                    if "ultimate" in line.lower():
                        trust_level = "ultimate"
                    elif "full" in line.lower():
                        trust_level = "full"
                    elif "marginal" in line.lower():
                        trust_level = "marginal"
                    elif "unknown" in line.lower():
                        trust_level = "unknown"
            
            error = None
            if not signed:
                error = "Commit is not signed"
            elif not valid:
                if "Can't check signature" in raw_output:
                    error = "Cannot check signature: GPG key not found in keyring"
                elif "BAD signature" in raw_output:
                    error = "Bad signature: Signature verification failed"
                else:
                    error = "Signature verification failed"
            
            return {
                "commit": commit_sha,
                "signed": signed,
                "valid": valid,
                "key_id": key_id,
                "signer": signer,
                "fingerprint": fingerprint,
                "trust_level": trust_level,
                "error": error,
                "raw_output": raw_output
            }
            
        except FileNotFoundError:
            return {
                "commit": commit_sha,
                "signed": False,
                "valid": False,
                "key_id": None,
                "signer": None,
                "fingerprint": None,
                "trust_level": None,
                "error": "Git command not found. Please install Git.",
                "raw_output": ""
            }
        except Exception as e:
            return {
                "commit": commit_sha,
                "signed": False,
                "valid": False,
                "key_id": None,
                "signer": None,
                "fingerprint": None,
                "trust_level": None,
                "error": f"Verification error: {str(e)}",
                "raw_output": ""
            }
    
    @staticmethod
    def get_commit_info(commit_sha: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Get detailed information about a Git commit.
        
        Args:
            commit_sha: The commit SHA to get information for
            repo_path: Path to the Git repository (default: current directory)
            
        Returns:
            Dictionary with commit information
        """
        try:
            # Get commit information
            result = subprocess.run(
                ["git", "show", "-s", "--format=%H%n%h%n%an%n%ae%n%at%n%s", commit_sha],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 6:
                return {
                    "full_sha": lines[0],
                    "short_sha": lines[1],
                    "author_name": lines[2],
                    "author_email": lines[3],
                    "timestamp": int(lines[4]),
                    "subject": lines[5]
                }
            
            return {
                "full_sha": commit_sha,
                "short_sha": commit_sha[:7],
                "author_name": "Unknown",
                "author_email": "Unknown",
                "timestamp": 0,
                "subject": "Unknown"
            }
            
        except Exception:
            return {
                "full_sha": commit_sha,
                "short_sha": commit_sha[:7],
                "author_name": "Unknown",
                "author_email": "Unknown",
                "timestamp": 0,
                "subject": "Unknown"
            }
    
    @staticmethod
    def verify_commits_from_file(filepath: str, repo_path: str = ".") -> List[Dict[str, Any]]:
        """
        Verify multiple commits from a JSON file.
        
        Args:
            filepath: Path to JSON file containing commit SHAs
            repo_path: Path to the Git repository (default: current directory)
            
        Returns:
            List of verification results
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            commits = []
            if isinstance(data, list):
                commits = data
            elif isinstance(data, dict) and 'commits' in data:
                commits = data['commits']
            else:
                return [{
                    "commit": filepath,
                    "signed": False,
                    "valid": False,
                    "error": "Invalid file format. Expected list of commits or object with 'commits' key."
                }]
            
            results = []
            for commit in commits:
                if isinstance(commit, str):
                    commit_sha = commit
                elif isinstance(commit, dict) and 'sha' in commit:
                    commit_sha = commit['sha']
                elif isinstance(commit, dict) and 'commit' in commit:
                    commit_sha = commit['commit']
                else:
                    results.append({
                        "commit": str(commit),
                        "signed": False,
                        "valid": False,
                        "error": "Invalid commit format"
                    })
                    continue
                
                result = GitCommitVerifier.verify_commit_signature(commit_sha, repo_path)
                results.append(result)
            
            return results
            
        except FileNotFoundError:
            return [{
                "commit": filepath,
                "signed": False,
                "valid": False,
                "error": f"File not found: {filepath}"
            }]
        except json.JSONDecodeError as e:
            return [{
                "commit": filepath,
                "signed": False,
                "valid": False,
                "error": f"Invalid JSON: {str(e)}"
            }]
        except Exception as e:
            return [{
                "commit": filepath,
                "signed": False,
                "valid": False,
                "error": f"Error reading file: {str(e)}"
            }]


def format_verification_result(result: Dict[str, Any], verbose: bool = False, 
                               include_commit_info: bool = False,
                               repo_path: str = ".") -> str:
    """Format a verification result for display."""
    lines = []
    
    commit = result.get("commit", "Unknown")
    lines.append(f"Commit: {commit}")
    
    if include_commit_info:
        info = GitCommitVerifier.get_commit_info(commit, repo_path)
        lines.append(f"  Author: {info['author_name']} <{info['author_email']}>")
        lines.append(f"  Subject: {info['subject']}")
    
    if result.get("error"):
        lines.append(f"  Status: ❌ ERROR")
        lines.append(f"  Error: {result['error']}")
    elif result.get("valid"):
        lines.append(f"  Status: ✅ VALID")
        lines.append(f"  Signed: Yes")
        if result.get("signer"):
            lines.append(f"  Signer: {result['signer']}")
        if result.get("key_id"):
            lines.append(f"  Key ID: {result['key_id']}")
        if result.get("trust_level"):
            lines.append(f"  Trust: {result['trust_level']}")
    elif result.get("signed"):
        lines.append(f"  Status: ⚠️  SIGNED BUT UNVERIFIED")
        lines.append(f"  Signed: Yes")
        lines.append(f"  Valid: No")
        if result.get("error"):
            lines.append(f"  Reason: {result['error']}")
    else:
        lines.append(f"  Status: ❌ UNSIGNED")
        lines.append(f"  Signed: No")
    
    if verbose and result.get("raw_output"):
        lines.append(f"\n  Raw GPG Output:")
        for line in result['raw_output'].split('\n'):
            if line.strip():
                lines.append(f"    {line}")
    
    return '\n'.join(lines)


def main():
    """Main entry point for the Git POW verifier."""
    parser = argparse.ArgumentParser(
        description="Git POW (Proof of Work) Verification - Verify Git commit signatures using GPG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify a single commit
  %(prog)s --commit abc123def456

  # Verify current HEAD commit
  %(prog)s --commit HEAD

  # Verify multiple commits from a file
  %(prog)s --file commits.json

  # Output as JSON
  %(prog)s --commit abc123def456 --json --pretty

  # Verbose output with GPG details
  %(prog)s --commit abc123def456 --verbose

Security Notes:
  - Private verification data is automatically excluded by .gitignore
  - Store verification policies in .gitignore-protected files
  - Never commit GPG private keys or passphrases
  - See SECURITY_BEST_PRACTICES.md for detailed guidance
        """
    )
    
    parser.add_argument(
        "--commit",
        help="Single commit SHA to verify (can be full or short SHA, or HEAD)"
    )
    parser.add_argument(
        "--file",
        help="JSON file containing commit SHAs to verify"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to Git repository (default: current directory)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output (requires --json)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output including raw GPG output"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Include commit information (author, subject)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.commit and not args.file:
        parser.error("Either --commit or --file must be specified")
    
    if args.commit and args.file:
        parser.error("Cannot specify both --commit and --file")
    
    # Verify commits
    results = []
    
    if args.commit:
        result = GitCommitVerifier.verify_commit_signature(args.commit, args.repo)
        results.append(result)
    
    if args.file:
        results = GitCommitVerifier.verify_commits_from_file(args.file, args.repo)
    
    # Output results
    if args.json:
        if args.pretty:
            print(json.dumps(results if len(results) > 1 else results[0], indent=2))
        else:
            print(json.dumps(results if len(results) > 1 else results[0]))
    else:
        for i, result in enumerate(results):
            if i > 0:
                print()  # Blank line between results
            print(format_verification_result(result, args.verbose, args.info, args.repo))
        
        # Summary
        if len(results) > 1:
            valid_count = sum(1 for r in results if r.get("valid"))
            signed_count = sum(1 for r in results if r.get("signed"))
            unsigned_count = sum(1 for r in results if not r.get("signed"))
            
            print(f"\n{'='*60}")
            print(f"Summary: {len(results)} commit(s) checked")
            print(f"  ✅ Valid: {valid_count}")
            print(f"  ⚠️  Signed but unverified: {signed_count - valid_count}")
            print(f"  ❌ Unsigned: {unsigned_count}")
    
    # Exit with appropriate code
    if all(r.get("valid") for r in results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
