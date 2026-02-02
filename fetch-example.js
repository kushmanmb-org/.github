// Simple fetch example for Etherscan API v2
// This demonstrates basic usage of the fetch API to query Etherscan
// Note: Replace 'YourApiKeyToken' with your actual Etherscan API key

const options = {method: 'GET'};

// Build the URL with all required parameters
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
