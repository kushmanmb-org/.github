# Address Labels Configuration

This document describes the address labeling configuration format used for identifying and categorizing blockchain addresses.

## Overview

The address labels configuration follows the Etherscan API response format and provides a standardized way to store and manage labeled blockchain addresses. This is useful for:

- Identifying known exchanges, projects, and entities
- Categorizing addresses by type (Exchange, DEX, DeFi Protocol, etc.)
- Tracking reputation scores
- Maintaining metadata about blockchain addresses

## Configuration Format

The configuration uses JSON format with the following structure:

```json
{
  "status": "1",
  "message": "OK",
  "result": [
    {
      "address": "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43",
      "nametag": "kushmanmb10",
      "url": "https://coinbase.com",
      "labels": [
        "Coinbase",
        "Exchange"
      ],
      "reputation": 0,
      "lastUpdatedTimestamp": 1721899658
    }
  ]
}
```

## Field Descriptions

### Root Level

- **status** (string, required): API response status code
  - `"1"` for success
  - `"0"` for error
  
- **message** (string, required): API response message
  - `"OK"` for successful response
  - Error description for failed response
  
- **result** (array, required): Array of labeled address entries

### Address Entry Fields

- **address** (string, required): Ethereum address in hexadecimal format
  - Must start with `0x`
  - Followed by exactly 40 hexadecimal characters (0-9, a-f, A-F)
  - Example: `0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43`

- **nametag** (string, required): Human-readable identifier
  - Unique name or identifier for the address
  - Should be descriptive and recognizable
  - Example: `kushmanmb10`

- **url** (string, optional): Associated website URL
  - Must be a valid URL format
  - Typically points to the project or entity's official website
  - Example: `https://coinbase.com`

- **labels** (array, optional): Category labels
  - Array of strings describing the address category or type
  - Common labels: `Exchange`, `DEX`, `DeFi`, `NFT`, `Bridge`, `Wallet`
  - Can include multiple labels for comprehensive categorization
  - Example: `["Coinbase", "Exchange"]`

- **reputation** (integer, optional): Reputation score
  - Default: `0` (neutral)
  - Positive values indicate trusted addresses
  - Negative values indicate suspicious or malicious addresses
  - Range typically from -100 to +100

- **lastUpdatedTimestamp** (integer, optional): Last update time
  - Unix timestamp (seconds since epoch)
  - Indicates when the label information was last updated
  - Example: `1721899658` (July 25, 2024)

## Best Practices

### 1. Naming Conventions

- Use **camelCase** for field names (e.g., `lastUpdatedTimestamp`, not `last_updated_timestamp`)
- Keep field names descriptive but concise
- Maintain consistency with existing Etherscan API conventions

### 2. Data Quality

- Always validate Ethereum addresses using the pattern: `^0x[a-fA-F0-9]{40}$`
- Use checksummed addresses when possible for additional validation
- Ensure URLs are valid and use HTTPS when available
- Keep nametags unique and descriptive

### 3. Label Organization

- Use standardized label categories for consistency
- Avoid redundant labels (e.g., don't use both "Coinbase" and "coinbase")
- Order labels from most specific to most general
- Common categories:
  - Exchanges: `Exchange`, `CEX`, `DEX`
  - Finance: `DeFi`, `Lending`, `Staking`
  - NFT: `NFT`, `Marketplace`, `Collection`
  - Infrastructure: `Bridge`, `Oracle`, `Layer2`

### 4. Optional Fields

- Omit optional fields with empty values rather than including empty strings or arrays
- Include `url` when the address represents a known project or organization
- Use `reputation` to flag addresses requiring special attention
- Update `lastUpdatedTimestamp` whenever label information changes

### 5. Array Structure

- Keep the `result` array for consistency with API response format
- Each entry should represent a unique address
- Sort entries alphabetically by address or by nametag for easier maintenance

## Example Use Cases

### Exchange Address

```json
{
  "address": "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43",
  "nametag": "Coinbase 10",
  "url": "https://coinbase.com",
  "labels": ["Coinbase", "Exchange", "CEX"],
  "reputation": 100,
  "lastUpdatedTimestamp": 1721899658
}
```

### DeFi Protocol

```json
{
  "address": "0x1234567890abcdef1234567890abcdef12345678",
  "nametag": "Uniswap V3 Router",
  "url": "https://uniswap.org",
  "labels": ["Uniswap", "DEX", "DeFi"],
  "reputation": 95,
  "lastUpdatedTimestamp": 1721899658
}
```

### Suspicious Address

```json
{
  "address": "0xabcdef1234567890abcdef1234567890abcdef12",
  "nametag": "Reported Scam",
  "labels": ["Scam", "Phishing"],
  "reputation": -100,
  "lastUpdatedTimestamp": 1721899658
}
```

## Schema Validation

A JSON schema is provided in `address-labels.schema.json` for validation purposes. You can use it with JSON schema validators to ensure your configuration adheres to the expected format.

### Using with VS Code

Add the following to your VS Code settings or in the JSON file itself:

```json
{
  "$schema": "./address-labels.schema.json"
}
```

### Using with Command-Line Tools

```bash
# Using ajv-cli
npm install -g ajv-cli
ajv validate -s address-labels.schema.json -d address-labels.json

# Using jsonschema (Python)
pip install jsonschema
python -c "import jsonschema, json; jsonschema.validate(json.load(open('address-labels.json')), json.load(open('address-labels.schema.json')))"
```

## Integration with Etherscan API

This format is compatible with Etherscan's address labeling API response. When querying labeled addresses from Etherscan, the response will follow this structure, making it easy to:

- Cache API responses locally
- Extend with custom labels
- Merge multiple sources of address labels
- Build address lookup tools

## Maintenance

- Review and update labels periodically
- Remove obsolete or incorrect labels
- Update `lastUpdatedTimestamp` when making changes
- Maintain a changelog for significant updates
- Consider versioning the configuration for major changes

## Related Files

- **address-labels.json** - Main configuration file
- **address-labels.schema.json** - JSON schema for validation
- **etherscan-api-config.example.json** - Etherscan API configuration
- **ETHERSCAN_TOKEN_BALANCE.md** - Documentation for Etherscan API usage

## References

- [Etherscan API Documentation](https://docs.etherscan.io/)
- [Ethereum Address Format](https://ethereum.org/en/developers/docs/accounts/)
- [JSON Schema Specification](https://json-schema.org/)
