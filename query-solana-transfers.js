#!/usr/bin/env node

/**
 * Query Solana account transfers using Solscan API v2.0
 * Usage: node query-solana-transfers.js --token YOUR_API_TOKEN [--account ACCOUNT] [--page PAGE]
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Load configuration from file
function loadConfig() {
  const configPath = path.join(__dirname, 'solscan-api-config.example.json');
  try {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return config;
  } catch (err) {
    // Return defaults if config file doesn't exist
    return {
      apiBaseUrl: 'https://pro-api.solscan.io/v2.0',
      defaultPage: '1',
      defaultPageSize: '10',
      defaultSortBy: 'block_time',
      defaultSortOrder: 'desc'
    };
  }
}

const config = loadConfig();

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    token: null,
    account: null,
    page: config.defaultPage,
    pageSize: config.defaultPageSize,
    sortBy: config.defaultSortBy,
    sortOrder: config.defaultSortOrder,
    pretty: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--token' && i + 1 < args.length) {
      options.token = args[++i];
    } else if (arg === '--account' && i + 1 < args.length) {
      options.account = args[++i];
    } else if (arg === '--page' && i + 1 < args.length) {
      options.page = args[++i];
    } else if (arg === '--page-size' && i + 1 < args.length) {
      options.pageSize = args[++i];
    } else if (arg === '--sort-by' && i + 1 < args.length) {
      options.sortBy = args[++i];
    } else if (arg === '--sort-order' && i + 1 < args.length) {
      options.sortOrder = args[++i];
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
Solscan API Query Tool (JavaScript)

Usage: node query-solana-transfers.js --token YOUR_API_TOKEN [options]

Description: Query Solana account transfer history using Solscan API v2.0

Options:
  --token <token>        Your Solscan API token (required)
  --account <address>    Solana account address to query (optional)
  --page <num>           Page number for pagination (default: ${config.defaultPage})
  --page-size <num>      Number of items per page (default: ${config.defaultPageSize})
  --sort-by <field>      Sort field (default: ${config.defaultSortBy})
  --sort-order <order>   Sort order: asc or desc (default: ${config.defaultSortOrder})
  --pretty               Pretty-print JSON output
  --help, -h             Show this help message

Environment Variables:
  SOLSCAN_API_TOKEN      Alternative way to provide API token

Examples:
  node query-solana-transfers.js --token YOUR_API_TOKEN
  node query-solana-transfers.js --token YOUR_API_TOKEN --page 2 --pretty
  node query-solana-transfers.js --token YOUR_API_TOKEN --page-size 20 --sort-order asc

Security Note:
  Never commit your API token to version control. Use environment variables
  or pass the token via command-line arguments.
`);
}

async function querySolanaTransfers(options) {
  const { token, account, page, pageSize, sortBy, sortOrder } = options;

  if (!token) {
    console.error('Error: API token is required. Use --token option or set SOLSCAN_API_TOKEN environment variable.');
    process.exit(1);
  }

  // Build request configuration
  const requestOptions = {
    method: 'get',
    url: `${config.apiBaseUrl}/account/transfer`,
    params: {
      page: page,
      page_size: pageSize,
      sort_by: sortBy,
      sort_order: sortOrder,
    },
    headers: {
      token: token
    }
  };

  // Add account to params if provided
  if (account) {
    requestOptions.params.account = account;
  }

  try {
    const response = await axios.request(requestOptions);
    
    // Format and display response
    if (options.pretty) {
      console.log(JSON.stringify(response.data, null, 2));
    } else {
      console.log(JSON.stringify(response.data));
    }
    
    return response.data;
  } catch (err) {
    if (err.response) {
      console.error('API Error:', err.response.status, err.response.statusText);
      if (err.response.data) {
        console.error('Response:', JSON.stringify(err.response.data, null, 2));
      }
    } else if (err.request) {
      console.error('Network Error: No response received from server');
    } else {
      console.error('Error:', err.message);
    }
    process.exit(1);
  }
}

// Main execution
if (require.main === module) {
  const options = parseArgs();
  
  // Allow API token from environment variable if not provided
  if (!options.token && process.env.SOLSCAN_API_TOKEN) {
    options.token = process.env.SOLSCAN_API_TOKEN;
  }
  
  querySolanaTransfers(options)
    .then(() => {
      process.exit(0);
    })
    .catch(err => {
      console.error('Unexpected error:', err);
      process.exit(1);
    });
}

module.exports = { querySolanaTransfers };
