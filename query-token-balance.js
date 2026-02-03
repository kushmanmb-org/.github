#!/usr/bin/env node

/**
 * Query ERC-20 token balances for an Ethereum address using Etherscan API v2
 * Usage: node query-token-balance.js --apikey YOUR_API_KEY [--address ADDRESS] [--chainid CHAIN_ID]
 */

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

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    apikey: null,
    address: config.etherscan_api.example_address,
    chainid: config.etherscan_api.default_chain_id,
    page: config.etherscan_api.default_pagination.page,
    offset: config.etherscan_api.default_pagination.offset,
    pretty: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--apikey' && i + 1 < args.length) {
      options.apikey = args[++i];
    } else if (arg === '--address' && i + 1 < args.length) {
      options.address = args[++i];
    } else if (arg === '--chainid' && i + 1 < args.length) {
      options.chainid = parseInt(args[++i]);
    } else if (arg === '--page' && i + 1 < args.length) {
      options.page = parseInt(args[++i]);
    } else if (arg === '--offset' && i + 1 < args.length) {
      options.offset = parseInt(args[++i]);
    } else if (arg === '--pretty') {
      options.pretty = true;
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    }
  }

  return options;
}

function printHelp() {
  console.log(`
Etherscan Token Balance Query Tool (JavaScript)

Usage: node query-token-balance.js --apikey YOUR_API_KEY [options]

Options:
  --apikey <key>      Etherscan API key (required)
  --address <addr>    Ethereum address to query (default: ${config.etherscan_api.example_address})
  --chainid <id>      Chain ID (default: ${config.etherscan_api.default_chain_id} for Ethereum mainnet)
  --page <num>        Page number for pagination (default: ${config.etherscan_api.default_pagination.page})
  --offset <num>      Number of results per page (default: ${config.etherscan_api.default_pagination.offset})
  --pretty            Pretty-print JSON output
  --help, -h          Show this help message

Examples:
  node query-token-balance.js --apikey YourApiKeyToken
  node query-token-balance.js --apikey YourApiKeyToken --address 0x123... --pretty
  node query-token-balance.js --apikey YourApiKeyToken --chainid 1 --offset 50
`);
}

async function queryTokenBalance(options) {
  const { apikey, address, chainid, page, offset } = options;

  if (!apikey) {
    console.error('Error: API key is required. Use --apikey option or set ETHERSCAN_API_KEY environment variable.');
    process.exit(1);
  }

  // Build the URL with query parameters
  const endpoint = config.etherscan_api.endpoints.addresstokenbalance;
  const url = new URL(config.etherscan_api.base_url);
  url.searchParams.append('chainid', chainid);
  url.searchParams.append('module', endpoint.module);
  url.searchParams.append('action', endpoint.action);
  url.searchParams.append('address', address);
  url.searchParams.append('page', page);
  url.searchParams.append('offset', offset);
  url.searchParams.append('apikey', apikey);

  const fetchOptions = { method: 'GET' };

  try {
    const response = await fetch(url.toString(), fetchOptions);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (options.pretty) {
      console.log(JSON.stringify(data, null, 2));
    } else {
      console.log(JSON.stringify(data));
    }
    
    return data;
  } catch (err) {
    console.error('Error fetching token balance:', err.message);
    process.exit(1);
  }
}

// Main execution
if (require.main === module) {
  const options = parseArgs();
  
  // Allow API key from environment variable if not provided
  if (!options.apikey && process.env.ETHERSCAN_API_KEY) {
    options.apikey = process.env.ETHERSCAN_API_KEY;
  }
  
  queryTokenBalance(options)
    .then(() => {
      process.exit(0);
    })
    .catch(err => {
      console.error('Unexpected error:', err);
      process.exit(1);
    });
}

module.exports = { queryTokenBalance };
