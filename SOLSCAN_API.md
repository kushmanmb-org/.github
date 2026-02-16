# Solscan API - Solana Account Transfers

This document provides information about querying Solana account transfer history using the Solscan API v2.0.

## Overview

Solscan provides a comprehensive API for querying Solana blockchain data. This repository includes utilities for querying account transfer history with pagination and sorting capabilities.

## API Endpoint

The Solscan Pro API v2.0 allows you to retrieve transfer history for Solana accounts.

### Endpoint URL

```text
https://pro-api.solscan.io/v2.0/account/transfer
```

### Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `account` | No | The Solana account address to query |
| `page` | No | Page number for pagination (default: 1) |
| `page_size` | No | Number of results per page (default: 10) |
| `sort_by` | No | Field to sort by (default: `block_time`) |
| `sort_order` | No | Sort order: `asc` or `desc` (default: `desc`) |

### Authentication

The API requires an API token passed in the request headers:

```
token: YOUR_API_TOKEN
```

**Security Warning**: Never commit your API token to version control. Use environment variables or pass the token via command-line arguments.

## Example Usage

### Using the JavaScript/Node.js Script

#### Basic Usage

```bash
node query-solana-transfers.js --token YOUR_API_TOKEN
```

#### With Pretty Printing

```bash
node query-solana-transfers.js --token YOUR_API_TOKEN --pretty
```

#### With Custom Pagination

```bash
node query-solana-transfers.js --token YOUR_API_TOKEN --page 2 --page-size 20
```

#### Query Specific Account

```bash
node query-solana-transfers.js --token YOUR_API_TOKEN --account ACCOUNT_ADDRESS --pretty
```

#### Using Environment Variable for Token

```bash
export SOLSCAN_API_TOKEN="YOUR_API_TOKEN"
node query-solana-transfers.js --pretty
```

### Using the Example Module

The repository includes a simple example file that demonstrates usage:

```bash
node solscan-example.js
```

You can also import and use the module in your own scripts:

```javascript
const { querySolanaTransfers } = require('./query-solana-transfers.js');

const options = {
  token: process.env.SOLSCAN_API_TOKEN,
  page: '1',
  pageSize: '10',
  pretty: true
};

querySolanaTransfers(options)
  .then(data => console.log('Success!'))
  .catch(err => console.error('Error:', err));
```

### Using axios Directly

You can also use axios directly in your code:

```javascript
import axios from 'axios'

const requestOptions = {
  method: "get",
  url: "https://pro-api.solscan.io/v2.0/account/transfer",
  params: {
    page: "1",
    page_size: "10",
    sort_by: "block_time",
    sort_order: "desc",
  },
  headers: {
    token: process.env.SOLSCAN_API_TOKEN
  },
}

axios
  .request(requestOptions)
  .then(response => console.log(response.data))
  .catch(err => console.error(err));
```

### Using cURL

```bash
curl --request GET \
  --url 'https://pro-api.solscan.io/v2.0/account/transfer?page=1&page_size=10&sort_by=block_time&sort_order=desc' \
  --header 'token: YOUR_API_TOKEN'
```

## Configuration

The default configuration is stored in `solscan-api-config.example.json`:

```json
{
  "apiBaseUrl": "https://pro-api.solscan.io/v2.0",
  "defaultPage": "1",
  "defaultPageSize": "10",
  "defaultSortBy": "block_time",
  "defaultSortOrder": "desc"
}
```

## Command-Line Options

The `query-solana-transfers.js` script supports the following options:

```
--token <token>        Your Solscan API token (required)
--account <address>    Solana account address to query (optional)
--page <num>           Page number for pagination (default: 1)
--page-size <num>      Number of items per page (default: 10)
--sort-by <field>      Sort field (default: block_time)
--sort-order <order>   Sort order: asc or desc (default: desc)
--pretty               Pretty-print JSON output
--help, -h             Show help message
```

## Environment Variables

- `SOLSCAN_API_TOKEN`: Your Solscan API token (alternative to `--token`)

## Security Best Practices

1. **Never commit API tokens** to version control
2. Use environment variables for sensitive credentials
3. Use `.gitignore` to exclude configuration files with secrets
4. Rotate API tokens periodically
5. Use minimal permissions on API tokens
6. Monitor API usage for unusual activity

## Dependencies

The script requires Node.js (>=18.0.0) and the following npm packages:

- `axios`: HTTP client for making API requests

Install dependencies with:

```bash
npm install axios
```

## Response Format

The API returns JSON data with transfer history. Example response structure:

```json
{
  "success": true,
  "data": [
    {
      "block_time": 1234567890,
      "transaction_id": "...",
      "amount": 1000000,
      // ... additional fields
    }
  ]
}
```

## Rate Limiting

Be aware of Solscan API rate limits. The Pro API typically has higher rate limits than the free tier. Check the [Solscan documentation](https://docs.solscan.io/) for current limits.

## Troubleshooting

### Authentication Errors

If you receive authentication errors:
- Verify your API token is correct
- Ensure the token is properly passed in the `token` header
- Check if your API token has the necessary permissions

### Network Errors

If you receive network errors:
- Verify your internet connection
- Check if the API endpoint is accessible
- Ensure no firewall is blocking the connection

### Invalid Parameters

If you receive parameter validation errors:
- Check parameter formats (page numbers should be numeric strings)
- Verify account addresses are valid Solana addresses
- Ensure sort_by field is a valid sortable field

## Additional Resources

- [Solscan Official Website](https://solscan.io/)
- [Solscan API Documentation](https://docs.solscan.io/)
- [Solana Documentation](https://docs.solana.com/)

## Support

For issues or questions:
1. Check this documentation
2. Review the example files
3. Consult the [Solscan API documentation](https://docs.solscan.io/)
4. Contact Solscan support for API-specific issues

## Related Files

- `query-solana-transfers.js`: Main query script
- `solscan-example.js`: Example usage
- `solscan-api-config.example.json`: Configuration template
- `README.md`: Repository overview with quick start guide
