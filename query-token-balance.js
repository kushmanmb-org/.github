#!/usr/bin/env node

/**
 * Query ERC-20 token balances for an Ethereum address using Etherscan API v2
 * Usage: node query-token-balance.js --apikey YOUR_API_KEY [--address ADDRESS] [--chainid CHAIN_ID]
 */

const fs = require('fs');
const path = require('path');

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    apikey: null,
    address: '0x983e3660c0bE01991785F80f266A84B911ab59b0',
    chainid: 1,
    page: 1,
    offset: 100,
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
  --address <addr>    Ethereum address to query (default: 0x983e3660c0bE01991785F80f266A84B911ab59b0)
  --chainid <id>      Chain ID (default: 1 for Ethereum mainnet)
  --page <num>        Page number for pagination (default: 1)
  --offset <num>      Number of results per page (default: 100)
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
  const url = new URL('https://api.etherscan.io/v2/api');
  url.searchParams.append('chainid', chainid);
  url.searchParams.append('module', 'account');
  url.searchParams.append('action', 'addresstokenbalance');
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
