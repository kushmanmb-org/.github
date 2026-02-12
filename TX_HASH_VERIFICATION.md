# Transaction Hash Verification

This guide explains how to verify blockchain transaction hashes while protecting private transaction data using `.gitignore` patterns.

## Overview

The `verify_tx_hash.py` utility validates blockchain transaction hashes for both Ethereum (0x-prefixed) and Bitcoin (non-prefixed) formats. It ensures hashes are properly formatted and can detect null/zero transaction hashes.

## Features

- ✅ Validates Ethereum transaction hashes (0x-prefixed, 64 hex characters)
- ✅ Validates Bitcoin transaction hashes (non-prefixed, 64 hex characters)
- ✅ Detects null/zero transaction hashes
- ✅ Batch validation from files (JSON or plain text)
- ✅ JSON output format support
- ✅ Case-insensitive validation with normalization

## Private Data Protection

Transaction data files are automatically excluded from version control using `.gitignore` patterns:

### Protected File Patterns

The following patterns are automatically gitignored to protect private transaction data:

```gitignore
# Transaction data and hashes (private data)
tx-data/
tx-hashes/
*tx-data*
*tx-hashes*
transaction-data.*
transactions.*
*.txdata
*.txhash
private-transactions.*
*private-tx*
```

### Example Files (Safe to Commit)

Example files with placeholder data are safe to commit:
- `tx-hashes-example.json` - Contains example transaction hashes for testing

### Private Files (Never Commit)

The following file patterns should NEVER be committed:
- `tx-hashes.json` - Real transaction hashes (gitignored)
- `private-transactions.json` - Sensitive transaction data (gitignored)
- `tx-data/` directory - Transaction data storage (gitignored)

## Usage

### Basic Examples

#### Verify a Single Transaction Hash

```bash
# Ethereum format (with 0x prefix)
./verify_tx_hash.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000

# Bitcoin format (without prefix)
./verify_tx_hash.py --hash 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898
```

#### Verify Multiple Hashes

```bash
./verify_tx_hash.py \
  --hash 0x0000000000000000000000000000000000000000000000000000000000000000 \
  --hash 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  --hash 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898
```

#### Verify Hashes from a File

```bash
# Plain text file (one hash per line)
./verify_tx_hash.py --file tx-hashes.txt

# JSON array file
./verify_tx_hash.py --file tx-hashes-example.json
```

### Output Formats

#### Human-Readable Output (Default)

```bash
./verify_tx_hash.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000
```

Output:
```
Transaction Hash: 0x0000000000000000000000000000000000000000000000000000000000000000
Valid: True
Format: ethereum
Is Null: True
Normalized: 0x0000000000000000000000000000000000000000000000000000000000000000
```

#### JSON Output

```bash
./verify_tx_hash.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000 --json --pretty
```

Output:
```json
{
  "valid": true,
  "format": "ethereum",
  "is_null": true,
  "normalized": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "error": null
}
```

### Advanced Options

#### Disallow Null Hashes

Use `--no-null` to reject null/zero transaction hashes:

```bash
./verify_tx_hash.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000 --no-null
```

This will fail validation with an error message.

#### Batch Validation with Statistics

```bash
./verify_tx_hash.py --file tx-hashes-example.json
```

Output:
```
Total: 3
Valid: 3
Invalid: 0
Null: 1

✓ [0] 0x0000000000000000000000000000000000000000000000000000000000000000
✓ [1] 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
✓ [2] 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898
```

## File Format Support

### Plain Text Format

Create a file with one transaction hash per line:

```text
0x0000000000000000000000000000000000000000000000000000000000000000
0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898
```

### JSON Array Format

```json
[
  "0x0000000000000000000000000000000000000000000000000000000000000000",
  "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
]
```

### JSON Object Format

```json
[
  {
    "hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "description": "Null transaction"
  },
  {
    "tx_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "description": "Example transaction"
  }
]
```

Supported field names: `hash`, `tx_hash`, `txHash`, `transaction_hash`

## Transaction Hash Formats

### Ethereum Format

- **Prefix**: `0x`
- **Length**: 64 hexadecimal characters (after prefix)
- **Total**: 66 characters
- **Example**: `0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef`
- **Null Hash**: `0x0000000000000000000000000000000000000000000000000000000000000000`

### Bitcoin Format

- **Prefix**: None
- **Length**: 64 hexadecimal characters
- **Example**: `08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898`
- **Null Hash**: `0000000000000000000000000000000000000000000000000000000000000000`

## Null/Zero Transaction Hashes

A null or zero transaction hash is:
- All zeros: `0x0000000000000000000000000000000000000000000000000000000000000000`
- Often used for testing or placeholder purposes
- Can be allowed or disallowed based on your use case

## Integration with Existing Tools

### Use with Blockchain RPC Server

The transaction hash validator can be used in conjunction with the blockchain RPC server:

```bash
# Verify hash before querying
./verify_tx_hash.py --hash 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898

# Query merkle proof if hash is valid
python3 blockchain_rpc_client.py \
  --tx 08901b81e39bc61d632c93241c44ec3763366bd57444b01494481ed46079c898 \
  --height 172165
```

## Testing

Run the test suite to verify functionality:

```bash
python3 test_verify_tx_hash.py
```

This will run comprehensive tests including:
- Valid hash validation (Ethereum and Bitcoin formats)
- Null hash detection
- Invalid hash rejection
- Batch validation
- Case insensitivity
- Whitespace handling

## Security Best Practices

1. **Never commit real transaction hashes** to version control unless they are public examples
2. **Store sensitive transaction data** in gitignored directories like `tx-data/` or `private-tx/`
3. **Use example files** with placeholder hashes for documentation and testing
4. **Verify .gitignore is working** before committing:
   ```bash
   git status
   git check-ignore -v tx-hashes.json
   ```

## Command-Line Reference

```
usage: verify_tx_hash.py [-h] [--hash HASHES] [--file FILE] [--no-null] [--json] [--pretty]

Verify blockchain transaction hashes

optional arguments:
  -h, --help     show this help message and exit
  --hash HASHES  Transaction hash to verify (can be specified multiple times)
  --file FILE    File containing transaction hashes (one per line or JSON)
  --no-null      Disallow null/zero transaction hashes
  --json         Output results as JSON
  --pretty       Pretty-print JSON output (requires --json)
```

## Exit Codes

- `0` - All transaction hashes are valid
- `1` - One or more transaction hashes are invalid or arguments are missing

## Related Documentation

- [Blockchain RPC Server](BLOCKCHAIN_RPC.md) - JSON-RPC server for blockchain operations
- [Security Best Practices](SECURITY_BEST_PRACTICES.md) - Guidelines for protecting sensitive data
- [.gitignore](.gitignore) - Comprehensive list of excluded file patterns

---

*Last Updated: 2026-02-12*
