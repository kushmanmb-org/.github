#!/usr/bin/env python3
"""
JSON-RPC server for blockchain transaction operations.
Implements the Electrum protocol's blockchain.transaction.get_merkle method.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List, Optional


class BlockchainRPC:
    """Business logic for blockchain JSON-RPC operations."""
    
    @staticmethod
    def handle_jsonrpc_request(request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a JSON-RPC request and return a response."""
        # Validate JSON-RPC version
        if request.get("jsonrpc") != "2.0":
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32600,
                    "message": "Invalid Request",
                    "data": "JSON-RPC version must be 2.0"
                },
                "id": request.get("id")
            }
        
        method = request.get("method")
        params = request.get("params", [])
        request_id = request.get("id")
        
        # Route to appropriate method handler
        if method == "blockchain.transaction.get_merkle":
            return BlockchainRPC.handle_get_merkle(params, request_id)
        else:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Method not found",
                    "data": f"Method '{method}' is not supported"
                },
                "id": request_id
            }
    
    @staticmethod
    def handle_get_merkle(params: List[Any], request_id: Any) -> Dict[str, Any]:
        """
        Handle blockchain.transaction.get_merkle request.
        
        Args:
            params: List containing [tx_hash, block_height]
            request_id: The JSON-RPC request ID
            
        Returns:
            JSON-RPC response with merkle proof data
        """
        # Validate parameters
        if not isinstance(params, list) or len(params) != 2:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params",
                    "data": "Expected 2 parameters: [tx_hash, block_height]"
                },
                "id": request_id
            }
        
        tx_hash = params[0]
        block_height = params[1]
        
        # Validate transaction hash format
        if not isinstance(tx_hash, str) or len(tx_hash) != 64:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params",
                    "data": "Transaction hash must be a 64-character hex string"
                },
                "id": request_id
            }
        
        # Validate transaction hash is hexadecimal
        try:
            int(tx_hash, 16)
        except ValueError:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params",
                    "data": "Transaction hash must contain only hexadecimal characters"
                },
                "id": request_id
            }
        
        # Validate block height
        if not isinstance(block_height, int) or block_height < 0:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params",
                    "data": "Block height must be a non-negative integer"
                },
                "id": request_id
            }
        
        # Get merkle proof
        try:
            merkle_data = BlockchainRPC.get_transaction_merkle_proof(tx_hash, block_height)
            return {
                "jsonrpc": "2.0",
                "result": merkle_data,
                "id": request_id
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Server error",
                    "data": str(e)
                },
                "id": request_id
            }
    
    @staticmethod
    def get_transaction_merkle_proof(tx_hash: str, block_height: int) -> Dict[str, Any]:
        """
        Retrieve the merkle proof for a transaction.
        
        Args:
            tx_hash: Transaction hash (hex string)
            block_height: Block height containing the transaction
            
        Returns:
            Dictionary containing merkle proof data with:
            - block_height: The block height
            - merkle: List of merkle branch hashes
            - pos: Position of transaction in the block
        """
        # This is a mock implementation. In a real scenario, this would:
        # 1. Connect to a blockchain node
        # 2. Query the transaction in the specified block
        # 3. Calculate or retrieve the merkle proof
        # 4. Return the merkle branch and position
        
        # For demonstration, return a properly formatted response
        # In production, this would make actual blockchain RPC calls
        return {
            "block_height": block_height,
            "merkle": [
                # Example merkle branch (would be real hashes in production)
                "d8c5d0f5e9f4e9a5d8c5d0f5e9f4e9a5d8c5d0f5e9f4e9a5d8c5d0f5e9f4e9a5",
                "a5e9f4d0c5d8e9a5f4d0c5d8e9a5f4d0c5d8e9a5f4d0c5d8e9a5f4d0c5d8e9a5"
            ],
            "pos": 0  # Position of the transaction in the merkle tree
        }


class BlockchainRPCHandler(BaseHTTPRequestHandler):
    """HTTP request handler for JSON-RPC blockchain operations."""
    
    def do_POST(self):
        """Handle POST requests containing JSON-RPC calls."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        request = None  # Initialize request variable
        try:
            request = json.loads(post_data.decode('utf-8'))
            response = BlockchainRPC.handle_jsonrpc_request(request)
            self.send_jsonrpc_response(response)
        except json.JSONDecodeError as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error",
                    "data": str(e)
                },
                "id": None
            }
            self.send_jsonrpc_response(error_response, status_code=400)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                },
                "id": request.get("id") if isinstance(request, dict) else None
            }
            self.send_jsonrpc_response(error_response, status_code=500)
    
    def send_jsonrpc_response(self, response: Dict[str, Any], status_code: int = 200):
        """Send a JSON-RPC response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        sys.stderr.write(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}\n")


def run_server(host: str = "127.0.0.1", port: int = 8332):
    """
    Start the JSON-RPC server.
    
    Args:
        host: Host to bind to (default: 127.0.0.1)
        port: Port to listen on (default: 8332)
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, BlockchainRPCHandler)
    print(f"Starting JSON-RPC server on {host}:{port}")
    print(f"Server supports: blockchain.transaction.get_merkle")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="JSON-RPC server for blockchain transaction operations"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8332,
        help="Port to listen on (default: 8332)"
    )
    
    args = parser.parse_args()
    run_server(args.host, args.port)
