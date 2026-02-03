// Simple fetch example for Etherscan API v2
// This demonstrates basic usage of the fetch API to query Etherscan
// Note: Replace 'YourApiKeyToken' with your actual Etherscan API key

const fs = require('fs');
const path = require('path');

// Load shared configuration
const configPath = path.join(__dirname, 'etherscan-api-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const options = {method: 'GET'};

// Build the URL with all required parameters
const params = new URLSearchParams({
  chainid: config.defaultChainId,
  module: config.module,
  action: config.action,
  address: config.defaultAddress,
  page: config.defaultPage,
  offset: config.defaultOffset,
  apikey: 'YourApiKeyToken'
});

const url = `${config.apiBaseUrl}?${params}`;

fetch(url, options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
