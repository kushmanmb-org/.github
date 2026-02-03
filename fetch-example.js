// Simple fetch example for Etherscan API v2
// This demonstrates basic usage of the fetch API to query Etherscan
// Note: Replace 'YourApiKeyToken' with your actual Etherscan API key

const fs = require('fs');
const path = require('path');

// Load configuration from etherscan-config.json
const configPath = path.join(__dirname, 'etherscan-config.json');
let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (err) {
  console.error('Error: Failed to load etherscan-config.json');
  console.error('Please ensure the config file exists and contains valid JSON.');
  console.error('Config path:', configPath);
  process.exit(1);
}

const options = {method: 'GET'};

// Build the URL with all required parameters
const endpoint = config.etherscan_api.endpoints.addresstokenbalance;
const params = new URLSearchParams({
  chainid: config.etherscan_api.default_chain_id,
  module: endpoint.module,
  action: endpoint.action,
  address: config.etherscan_api.example_address,
  page: config.etherscan_api.default_pagination.page,
  offset: config.etherscan_api.default_pagination.offset,
  apikey: 'YourApiKeyToken'
});

const url = `${config.etherscan_api.base_url}?${params}`;

fetch(url, options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
