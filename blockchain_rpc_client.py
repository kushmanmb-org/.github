#!/usr/bin/env python3
"""
Client script for testing blockchain JSON-RPC server.
Demonstrates usage of blockchain.transaction.get_merkle method.
"""

import json
import sys
import argparse
import urllib.request
import urllib.error


def make_jsonrpc_request(url: str, method: str, params: list, request_id: int = 1) -> dict:
    """
    Make a JSON-RPC request to the server.
    
    Args:
        url: The server URL
        method: The RPC method name
        params: The method parameters
        request_id: The request ID (default: 1)
        
    Returns:
        The JSON-RPC response as a dictionary
    """
    request_data = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params
    }
    
    # Convert to JSON and encode
    json_data = json.dumps(request_data)
    data = json_data.encode('utf-8')
    
    # Create request
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        # Send request and get response
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            return json.loads(response_data.decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            return json.loads(error_body)
        except json.JSONDecodeError:
            return {
                "error": {
                    "code": -1,
                    "message": f"HTTP Error {e.code}",
                    "data": error_body
                }
            }
    except urllib.error.URLError as e:
        return {
            "error": {
                "code": -1,
                "message": "Connection error",
                "data": str(e.reason)
            }
        }


def get_merkle_proof(url: str, tx_hash: str, block_height: int, pretty: bool = False):
    """
    Get the merkle proof for a transaction.
    
    Args:
        url: The server URL
        tx_hash: Transaction hash
        block_height: Block height
        pretty: Whether to pretty-print the output
    """
    response = make_jsonrpc_request(
        url,
        "blockchain.transaction.get_merkle",
        [tx_hash, block_height]
    )
    
    if pretty:
        print(json.dumps(response, indent=2))
    else:
        print(json.dumps(response))
    
    # Return exit code based on success/error
    if "error" in response:
        return 1
    return 0


def main():
    """Main entry point for the client script."""
    parser = argparse.ArgumentParser(
        description="Client for blockchain JSON-RPC server"
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8332",
        help="Server URL (default: http://127.0.0.1:8332)"
    )
    parser.add_argument(
        "--tx",
        required=True,
        help="Transaction hash (64-character hex string)"
    )
    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="Block height"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output"
    )
    
    args = parser.parse_args()
    
    exit_code = get_merkle_proof(
        args.url,
        args.tx,
        args.height,
        args.pretty
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
