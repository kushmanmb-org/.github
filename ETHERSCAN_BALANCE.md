# Etherscan Address Balance API

This document provides information about querying ETH balance for Ethereum addresses using the Etherscan API v2.

## API Endpoint

The Etherscan API v2 allows you to retrieve the native ETH balance for a specific Ethereum address.

### Endpoint URL

```text
https://api.etherscan.io/v2/api
```

### Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `chainid` | Yes | The chain ID (1 for Ethereum mainnet) |
| `module` | Yes | The module name (`account`) |
| `action` | Yes | The action to perform (`balance`) |
| `address` | Yes | The Ethereum address to query (e.g., `0x983e3660c0bE01991785F80f266A84B911ab59b0`) |
| `tag` | No | The block parameter (`latest`, `earliest`, or block number in hex) (default: `latest`) |
| `apikey` | Yes | Your Etherscan API key |

## Example Usage

### Testing API Endpoint Connectivity

Before making API calls with parameters, you can test basic connectivity to the Etherscan API v2 endpoint:

#### Basic GET Request

```bash
curl --request GET \
  --url https://api.etherscan.io/v2/api
```

Or use the provided test script:

```bash
./api-test.sh
```

**Note:** The API requires specific parameters for actual queries. The basic GET request above is useful for testing endpoint availability.

### cURL Command (Full Query)

```bash
curl "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=0x983e3660c0bE01991785F80f266A84B911ab59b0&tag=latest&apikey=YourApiKeyToken"
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
  action: 'balance',
  address: '0x983e3660c0bE01991785F80f266A84B911ab59b0',
  tag: 'latest',
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
async function getAddressBalance(address, apiKey, tag = 'latest') {
  const url = `https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=${address}&tag=${tag}&apikey=${apiKey}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching balance:', error);
    throw error;
  }
}

// Usage
const address = '0x983e3660c0bE01991785F80f266A84B911ab59b0';
const apiKey = 'YourApiKeyToken';
getAddressBalance(address, apiKey)
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

#### Using the Command-Line Script

For a full-featured command-line tool, use the included script:

```bash
node query-balance.js --apikey YOUR_API_KEY
```

### Python Example

```python
import requests

def get_address_balance(address, api_key, tag='latest'):
    """
    Fetch ETH balance for a given Ethereum address.
    
    Args:
        address (str): Ethereum address to query
        api_key (str): Etherscan API key
        tag (str): Block parameter (default: 'latest')
        
    Returns:
        dict: API response with balance data
    """
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": 1,
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": tag,
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance: {e}")
        raise

# Usage
if __name__ == "__main__":
    address = "0x983e3660c0bE01991785F80f266A84B911ab59b0"
    api_key = "YourApiKeyToken"
    data = get_address_balance(address, api_key)
    print(data)
```

## Expected Response Format

```json
{
  "status": "1",
  "message": "OK",
  "result": "1234567890123456789"
}
```

The `result` field contains the ETH balance in wei (1 ETH = 10^18 wei).

To convert wei to ETH, divide by 10^18:

```javascript
const balanceInWei = "1234567890123456789";
const balanceInEth = parseFloat(balanceInWei) / 1e18;
console.log(`Balance: ${balanceInEth} ETH`);
```

## Related Documentation

This documentation is related to querying native ETH balances for Ethereum addresses. For ERC-20 token balances, see [ETHERSCAN_TOKEN_BALANCE.md](ETHERSCAN_TOKEN_BALANCE.md).

**Primary Address for Balance Queries:** `0x983e3660c0bE01991785F80f266A84B911ab59b0`

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
- [Understanding Wei and ETH Units](https://ethereum.org/en/developers/docs/intro-to-ether/)
