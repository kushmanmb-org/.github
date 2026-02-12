#!/usr/bin/env node

/**
 * Query ERC-20 token balances for an Ethereum address using Etherscan API v2
 * Usage: node query-token-balance.js --apikey YOUR_API_KEY [--address ADDRESS] [--chainid CHAIN_ID]
 */

const { loadConfig, buildApiParams, buildApiUrl, loadMessages, isResponseSuccessful, formatResponse } = require('./etherscan-common.js');

// Load shared configuration and messages
const sharedConfig = loadConfig();
const messages = loadMessages();

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    apikey: null,
    address: sharedConfig.defaultAddress,
    chainid: sharedConfig.defaultChainId,
    page: sharedConfig.defaultPage,
    offset: sharedConfig.defaultOffset,
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
  const helpConfig = sharedConfig.helpText;
  console.log(`
Etherscan Token Balance Query Tool (JavaScript)

Usage: node query-token-balance.js --apikey YOUR_API_KEY [options]

Description: ${helpConfig.description}

Options:
  --apikey <key>      ${helpConfig.options.apikey}
  --address <addr>    ${helpConfig.options.address} (default: ${sharedConfig.defaultAddress})
  --chainid <id>      ${helpConfig.options.chainid} (default: ${sharedConfig.defaultChainId})
  --page <num>        ${helpConfig.options.page} (default: ${sharedConfig.defaultPage})
  --offset <num>      ${helpConfig.options.offset} (default: ${sharedConfig.defaultOffset})
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
    console.error(messages.errors.apiKeyRequired + '. Use --apikey option or set ETHERSCAN_API_KEY environment variable.');
    process.exit(1);
  }

  // Build API parameters and URL using shared module
  const params = buildApiParams(sharedConfig, address, apikey, chainid, page, offset);
  const url = buildApiUrl(sharedConfig, params);

  const fetchOptions = { method: 'GET' };

  try {
    const response = await fetch(url, fetchOptions);
    
    if (!response.ok) {
      throw new Error(`${messages.errors.apiError}: ${response.status}`);
    }
    
    const data = await response.json();
    
    console.log(formatResponse(data, options));
    
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
