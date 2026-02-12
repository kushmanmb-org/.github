#!/usr/bin/env node

/**
 * Query ETH balance for an Ethereum address using Etherscan API v2
 * Usage: node query-balance.js --apikey YOUR_API_KEY [--address ADDRESS] [--chainid CHAIN_ID]
 */

const { loadConfig, loadMessages, buildApiUrl, isResponseSuccessful, formatResponse, validateEthereumAddress } = require('./etherscan-common.js');

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
    tag: 'latest',
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
    } else if (arg === '--tag' && i + 1 < args.length) {
      options.tag = args[++i];
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
Etherscan Balance Query Tool (JavaScript)

Usage: node query-balance.js --apikey YOUR_API_KEY [options]

Options:
  --apikey <key>      Etherscan API key (required)
  --address <addr>    Ethereum address to query (default: ${sharedConfig.defaultAddress})
  --chainid <id>      Chain ID (default: ${sharedConfig.defaultChainId} for Ethereum mainnet)
  --tag <tag>         Block parameter: latest, earliest, or block number in hex (default: latest)
  --pretty            Pretty-print JSON output
  --help, -h          Show this help message

Examples:
  node query-balance.js --apikey YourApiKeyToken
  node query-balance.js --apikey YourApiKeyToken --address 0x123... --pretty
  node query-balance.js --apikey YourApiKeyToken --chainid 1 --tag latest
`);
}

/**
 * Build API parameters for balance query
 */
function buildBalanceParams(config, address, apiKey, chainId, tag) {
  return {
    chainid: chainId,
    module: 'account',
    action: 'balance',
    address: address,
    tag: tag,
    apikey: apiKey
  };
}

/**
 * Format balance from wei to ETH
 * Note: Uses parseFloat which may lose precision for very large balances.
 * For production use with precise financial calculations, consider using
 * a library like BigNumber.js or ethers.js
 */
function formatBalance(balanceWei) {
  const balanceEth = parseFloat(balanceWei) / 1e18;
  return balanceEth.toFixed(18);
}

async function queryBalance(options) {
  const { apikey, address, chainid, tag } = options;

  if (!apikey) {
    console.error(messages.errors.apiKeyRequired + '. Use --apikey option or set ETHERSCAN_API_KEY environment variable.');
    process.exit(1);
  }

  // Validate address format
  if (!validateEthereumAddress(address)) {
    console.error(messages.errors.invalidAddress);
    console.error(messages.errors.expectedAddressFormat);
    process.exit(1);
  }

  // Build API parameters and URL
  const params = buildBalanceParams(sharedConfig, address, apikey, chainid, tag);
  const url = buildApiUrl(sharedConfig, params);

  const fetchOptions = { method: 'GET' };

  try {
    const response = await fetch(url, fetchOptions);
    
    if (!response.ok) {
      throw new Error(`${messages.errors.apiError}: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Display formatted output
    if (options.pretty && isResponseSuccessful(data)) {
      console.log(formatResponse(data, options));
      console.log('\nBalance Information:');
      console.log(`  Address: ${address}`);
      console.log(`  Balance (wei): ${data.result}`);
      console.log(`  Balance (ETH): ${formatBalance(data.result)} ETH`);
    } else {
      console.log(formatResponse(data, options));
    }
    
    return data;
  } catch (err) {
    console.error('Error fetching balance:', err.message);
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
  
  queryBalance(options)
    .then(() => {
      process.exit(0);
    })
    .catch(err => {
      console.error('Unexpected error:', err);
      process.exit(1);
    });
}

module.exports = { queryBalance };
