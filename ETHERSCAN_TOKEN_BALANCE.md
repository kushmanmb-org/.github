# Etherscan Address Token Balance API

This document provides information about querying ERC-20 token balances for Ethereum addresses using the Etherscan API v2.

## API Endpoint

The Etherscan API v2 allows you to retrieve all ERC-20 token balances for a specific Ethereum address.

### Endpoint URL

```text
https://api.etherscan.io/v2/api
```

### Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `chainid` | Yes | The chain ID (1 for Ethereum mainnet) |
| `module` | Yes | The module name (`account`) |
| `action` | Yes | The action to perform (`addresstokenbalance`) |
| `address` | Yes | The Ethereum address to query (e.g., `0x983e3660c0bE01991785F80f266A84B911ab59b0`) |
| `page` | No | Page number for pagination (default: 1) |
| `offset` | No | Number of results per page (default: 100, max: 10000) |
| `apikey` | Yes | Your Etherscan API key |

## Example Usage

### cURL Command

```bash
curl "https://api.etherscan.io/v2/api?chainid=1&module=account&action=addresstokenbalance&address=0x983e3660c0bE01991785F80f266A84B911ab59b0&page=1&offset=100&apikey=YourApiKeyToken"
```

### JavaScript Example

#### Simple Fetch Example

> **Note:** Replace `YourApiKeyToken` with your actual Etherscan API key. For production use, consider using environment variables to store sensitive credentials.

```javascript
const options = {method: 'GET'};

const baseUrl = 'https://api.etherscan.io/v2/api';
const params = new URLSearchParams({
  chainid: 1,
  module: 'account',
  action: 'addresstokenbalance',
  address: '0x983e3660c0bE01991785F80f266A84B911ab59b0',
  page: 1,
  offset: 100,
  apikey: 'YourApiKeyToken'
});

const url = `${baseUrl}?${params}`;

fetch(url, options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

#### Full Example with Function

```javascript
async function getAddressTokenBalance(address, apiKey) {
  const url = `https://api.etherscan.io/v2/api?chainid=1&module=account&action=addresstokenbalance&address=${address}&page=1&offset=100&apikey=${apiKey}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching token balance:', error);
    throw error;
  }
}

// Usage
const address = '0x983e3660c0bE01991785F80f266A84B911ab59b0';
const apiKey = 'YourApiKeyToken';
getAddressTokenBalance(address, apiKey)
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

#### Using the Command-Line Script

For a full-featured command-line tool, use the included script:

```bash
node query-token-balance.js --apikey YOUR_API_KEY --pretty
```

### Python Example

```python
import requests

def get_address_token_balance(address, api_key):
    """
    Fetch ERC-20 token balances for a given Ethereum address.
    
    Args:
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        
    Returns:
        dict: API response with token balance data
    """
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": 1,
        "module": "account",
        "action": "addresstokenbalance",
        "address": address,
        "page": 1,
        "offset": 100,
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token balance: {e}")
        raise

# Usage
if __name__ == "__main__":
    address = "0x983e3660c0bE01991785F80f266A84B911ab59b0"
    api_key = "YourApiKeyToken"
    data = get_address_token_balance(address, api_key)
    print(data)
```

## Expected Response Format

```json
{
  "status": "1",
  "message": "OK",
  "result": [
    {
      "TokenAddress": "0x...",
      "TokenName": "Token Name",
      "TokenSymbol": "TKN",
      "TokenQuantity": "1000000000000000000",
      "TokenDivisor": "18"
    }
  ]
}
```

## Related Address

This documentation is related to querying token balances for Ethereum addresses. For more information about the multisig wallet contract, see [MULTISIG_WALLET_README.md](MULTISIG_WALLET_README.md).

**Primary Address for Token Balance Queries:** `0x983e3660c0bE01991785F80f266A84B911ab59b0`

## Getting an API Key

To use the Etherscan API, you need to:

1. Create an account at [etherscan.io](https://etherscan.io)
2. Navigate to your account settings
3. Generate a new API key
4. Replace `YourApiKeyToken` in the examples above with your actual API key

## Rate Limits

- Free tier: 5 calls/second
- For higher rate limits, consider upgrading to a paid plan

## Additional Resources

- [Etherscan API Documentation](https://docs.etherscan.io/)
- [Ethereum Address Format](https://ethereum.org/en/developers/docs/accounts/)
- [ERC-20 Token Standard](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/)
