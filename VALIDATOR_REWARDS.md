# Beaconcha.in Validator Rewards API

This document provides information about querying Ethereum validator rewards using the Beaconcha.in API v2.

## API Endpoint

The Beaconcha.in API v2 allows you to retrieve detailed information about validator rewards on the Ethereum Beacon Chain.

### Endpoint URL

```text
https://beaconcha.in/api/v2/ethereum/validators/rewards-list
```

### HTTP Method

`POST`

### Headers

| Header | Required | Description |
| ------ | -------- | ----------- |
| `Authorization` | Yes | Bearer token format: `Bearer YOUR_API_KEY` |
| `Content-Type` | Yes | Must be `application/json` |

### Request Body Parameters

The API accepts a JSON body with the following structure:

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `validators` | array | No | Array of validator indices (e.g., `[1, 2, 3]`) |
| `epoch` | integer | No | Specific epoch to query rewards for |
| `limit` | integer | No | Number of results to return (default: 100) |
| `offset` | integer | No | Pagination offset (default: 0) |

## Authentication

The API requires authentication via Bearer token. Your API key should be passed in the `Authorization` header:

```text
Authorization: Bearer YOUR_API_KEY
```

**Security Note:** Never commit API keys to version control. Use environment variables or gitignored configuration files to store sensitive credentials.

## Example Usage

### Testing API Endpoint

Before making full API requests, you can test the endpoint availability:

```bash
./validator-rewards-test.sh
```

### cURL Command

#### Basic Request

```bash
curl -X POST 'https://beaconcha.in/api/v2/ethereum/validators/rewards-list' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "validators": [1, 2, 3],
    "limit": 10
  }'
```

#### Query Specific Epoch

```bash
curl -X POST 'https://beaconcha.in/api/v2/ethereum/validators/rewards-list' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "epoch": 123456,
    "limit": 100
  }'
```

### Bash Script

```bash
# Query validator rewards with default settings
./query-validator-rewards.sh --apikey YOUR_API_KEY

# Query specific validators
./query-validator-rewards.sh --apikey YOUR_API_KEY --validators "1,2,3"

# Query specific epoch with custom limit
./query-validator-rewards.sh --apikey YOUR_API_KEY --epoch 123456 --limit 50
```

### Python Script

```bash
# Basic query
./query-validator-rewards.py --apikey YOUR_API_KEY

# Query with specific validators
./query-validator-rewards.py --apikey YOUR_API_KEY --validators 1 2 3 --pretty

# Query specific epoch with pagination
./query-validator-rewards.py --apikey YOUR_API_KEY --epoch 123456 --limit 100 --offset 0 --pretty
```

### JavaScript/Node.js Script

```bash
# Basic query
node query-validator-rewards.js --apikey YOUR_API_KEY

# Query specific validators with pretty output
node query-validator-rewards.js --apikey YOUR_API_KEY --validators "1,2,3" --pretty

# Query with pagination
node query-validator-rewards.js --apikey YOUR_API_KEY --limit 50 --offset 0 --pretty
```

## Response Format

### Success Response

```json
{
  "status": "success",
  "data": [
    {
      "validatorindex": 1,
      "epoch": 123456,
      "attesterslot": 3951393,
      "attestation_source": 234,
      "attestation_target": 567,
      "attestation_head": 890,
      "attestation_inclusiondelay": 1,
      "attestation_scheduledinclusionslot": 3951394,
      "proposerslot": null,
      "deposits": 0,
      "withdrawals": 0
    }
  ]
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Invalid API key",
  "code": 401
}
```

## Environment Variables

You can set your API key as an environment variable to avoid passing it on the command line:

```bash
export BEACONCHAIN_API_KEY="YOUR_API_KEY"
```

Then use the scripts without the `--apikey` parameter:

```bash
./query-validator-rewards.sh --validators "1,2,3"
```

## Security Best Practices

- **Never commit API keys to Git repositories**
- Store API keys in environment variables or local configuration files
- Add configuration files to `.gitignore` (e.g., `validator-rewards-config.json`)
- Use read-only API keys when possible
- Rotate API keys regularly
- Monitor API usage for unexpected patterns

For more security guidelines, see [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md).

## Rate Limits

The Beaconcha.in API has rate limits that depend on your subscription tier. Ensure you:

- Respect the API rate limits
- Implement appropriate retry logic
- Cache responses when appropriate
- Use pagination for large datasets

## Additional Resources

- [Beaconcha.in API Documentation](https://beaconcha.in/api/v2/docs)
- [Ethereum Beacon Chain Specifications](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/)
- [Validator Rewards Explanation](https://ethereum.org/en/staking/rewards/)

## Related Tools

- [ENS Verification](ENS_VERIFICATION.md) - Verify ENS creator status
- [Transaction Hash Verification](TX_HASH_VERIFICATION.md) - Verify blockchain transactions
- [Etherscan Token Balance API](ETHERSCAN_TOKEN_BALANCE.md) - Query ERC-20 token balances
