# Blockchain JSON-RPC Server

This implementation provides a JSON-RPC 2.0 server for blockchain transaction operations, specifically supporting the Electrum protocol's `blockchain.transaction.get_merkle` method.

## Overview

The server implements the JSON-RPC 2.0 specification and provides merkle proof retrieval for blockchain transactions.

## Supported Methods

### blockchain.transaction.get_merkle

Retrieves the merkle branch and position for a transaction in a specific block.

**Parameters:**
- `tx_hash` (string): Transaction hash (64-character hexadecimal string)
- `block_height` (integer): Block height containing the transaction (non-negative integer)

**Returns:**
```json
{
  "block_height": 172165,
  "merkle": [
    "hash1",
    "hash2",
    ...
  ],
  "pos": 0
}
```

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "blockchain.transaction.get_merkle",
  "params": [
    "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
    172165
  ]
}
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "block_height": 172165,
    "merkle": [
      "d8c5d0f5e9f4e9a5d8c5d0f5e9f4e9a5d8c5d0f5e9f4e9a5d8c5d0f5e9f4e9a5",
      "a5e9f4d0c5d8e9a5f4d0c5d8e9a5f4d0c5d8e9a5f4d0c5d8e9a5f4d0c5d8e9a5"
    ],
    "pos": 0
  }
}
```

## Files

### Core Implementation

- **blockchain_rpc_server.py**: Main server implementation
  - `BlockchainRPC` class: Core JSON-RPC business logic
  - `BlockchainRPCHandler` class: HTTP request handler
  - Server entry point with command-line arguments

### Client and Testing

- **blockchain_rpc_client.py**: Client script for testing the server
- **test_blockchain_rpc.py**: Comprehensive test suite

## Usage

### Starting the Server

```bash
# Start with default settings (127.0.0.1:8332)
python3 blockchain_rpc_server.py

# Start on custom host/port
python3 blockchain_rpc_server.py --host 0.0.0.0 --port 8080
```

### Using the Client

```bash
# Query merkle proof
python3 blockchain_rpc_client.py \
  --tx 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898 \
  --height 172165 \
  --pretty

# Connect to custom server URL
python3 blockchain_rpc_client.py \
  --url http://localhost:8080 \
  --tx <transaction_hash> \
  --height <block_height>
```

### Using cURL

```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "blockchain.transaction.get_merkle",
    "params": [
      "08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898",
      172165
    ]
  }'
```

### Running Tests

```bash
# Run all tests
python3 test_blockchain_rpc.py

# Run with verbose output
python3 test_blockchain_rpc.py -v
```

## Error Codes

The server follows JSON-RPC 2.0 error code conventions:

- `-32700`: Parse error (invalid JSON)
- `-32600`: Invalid Request (invalid JSON-RPC)
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error
- `-32000`: Server error (blockchain operation failed)

## Implementation Notes

### Current Implementation

This is a reference implementation that returns mock merkle proof data. In a production environment, the server should:

1. Connect to a real blockchain node (e.g., Bitcoin Core, Electrum server)
2. Query the actual transaction and block data
3. Calculate or retrieve the real merkle branch
4. Return authentic merkle proof data

### Extending the Server

To add new methods:

1. Add a new handler method in the `BlockchainRPC` class
2. Register the method in `handle_jsonrpc_request`
3. Add corresponding tests in `test_blockchain_rpc.py`

## JSON-RPC 2.0 Compliance

This implementation fully complies with the JSON-RPC 2.0 specification:

- ✅ Proper request/response structure
- ✅ Error handling with standard error codes
- ✅ Request ID preservation
- ✅ Parameter validation
- ✅ Content-Type: application/json
- ✅ POST method support

## Security Considerations

- The server binds to `127.0.0.1` by default (localhost only)
- No authentication is implemented in this reference version
- Input validation is performed on all parameters
- Consider adding:
  - API key authentication
  - Rate limiting
  - TLS/SSL support
  - Request logging

## Dependencies

- Python 3.7+
- Standard library only (no external dependencies)

## License

See individual files for licensing information.
