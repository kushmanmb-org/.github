#!/usr/bin/env python3
"""
Tests for blockchain JSON-RPC server.
Tests the blockchain.transaction.get_merkle method and JSON-RPC protocol compliance.
"""

import json
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blockchain_rpc_server import BlockchainRPC


class TestBlockchainRPCServer(unittest.TestCase):
    """Test cases for blockchain RPC server."""
    
    def test_valid_get_merkle_request(self):
        """Test valid blockchain.transaction.get_merkle request."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": [
                "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
                172165
            ]
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        # Verify response structure
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], 1)
        self.assertIn("result", response)
        self.assertNotIn("error", response)
        
        # Verify result structure
        result = response["result"]
        self.assertIn("block_height", result)
        self.assertIn("merkle", result)
        self.assertIn("pos", result)
        self.assertEqual(result["block_height"], 172165)
        self.assertIsInstance(result["merkle"], list)
        self.assertIsInstance(result["pos"], int)
    
    def test_invalid_jsonrpc_version(self):
        """Test request with invalid JSON-RPC version."""
        request = {
            "jsonrpc": "1.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": ["abc123", 100]
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32600)
        self.assertIn("Invalid Request", response["error"]["message"])
    
    def test_method_not_found(self):
        """Test request with unsupported method."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.unknown.method",
            "params": []
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)
        self.assertIn("Method not found", response["error"]["message"])
    
    def test_invalid_params_count(self):
        """Test request with wrong number of parameters."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": ["abc123"]  # Missing block_height
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("Invalid params", response["error"]["message"])
    
    def test_invalid_tx_hash_format(self):
        """Test request with invalid transaction hash format."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": ["invalid_hash", 100]
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("64-character hex string", response["error"]["data"])
    
    def test_invalid_block_height_type(self):
        """Test request with invalid block height type."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": [
                "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
                "not_an_integer"
            ]
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("non-negative integer", response["error"]["data"])
    
    def test_negative_block_height(self):
        """Test request with negative block height."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": [
                "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
                -1
            ]
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("non-negative integer", response["error"]["data"])
    
    def test_request_id_preserved(self):
        """Test that request ID is preserved in response."""
        test_ids = [1, "test-id", None, {"nested": "id"}]
        
        for test_id in test_ids:
            request = {
                "jsonrpc": "2.0",
                "id": test_id,
                "method": "blockchain.transaction.get_merkle",
                "params": [
                    "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
                    172165
                ]
            }
            
            response = BlockchainRPC.handle_jsonrpc_request(request)
            self.assertEqual(response["id"], test_id)
    
    def test_example_from_problem_statement(self):
        """Test the exact example from the problem statement."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "blockchain.transaction.get_merkle",
            "params": [
                "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
                172165
            ]
        }
        
        response = BlockchainRPC.handle_jsonrpc_request(request)
        
        # Verify it's a successful response
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], 1)
        self.assertIn("result", response)
        
        # Verify result has required fields
        result = response["result"]
        self.assertEqual(result["block_height"], 172165)
        self.assertIsInstance(result["merkle"], list)
        self.assertIsInstance(result["pos"], int)
        self.assertGreaterEqual(result["pos"], 0)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
