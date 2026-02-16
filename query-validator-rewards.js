#!/usr/bin/env node

/**
 * Query Ethereum validator rewards using Beaconcha.in API v2
 * Usage: node query-validator-rewards.js --apikey YOUR_API_KEY [options]
 */

// Default configuration
const API_ENDPOINT = 'https://beaconcha.in/api/v2/ethereum/validators/rewards-list';
const DEFAULT_LIMIT = 100;
const DEFAULT_OFFSET = 0;

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    apikey: process.env.BEACONCHAIN_API_KEY || null,
    validators: null,
    epoch: null,
    limit: DEFAULT_LIMIT,
    offset: DEFAULT_OFFSET,
    pretty: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--apikey' || arg === '-k') {
      if (i + 1 < args.length) {
        options.apikey = args[++i];
      }
    } else if (arg === '--validators' || arg === '-v') {
      if (i + 1 < args.length) {
        // Parse comma-separated or space-separated validator IDs
        const validatorString = args[++i];
        options.validators = validatorString.split(',').map(v => parseInt(v.trim())).filter(v => !isNaN(v));
      }
    } else if (arg === '--epoch' || arg === '-e') {
      if (i + 1 < args.length) {
        options.epoch = parseInt(args[++i]);
      }
    } else if (arg === '--limit' || arg === '-l') {
      if (i + 1 < args.length) {
        options.limit = parseInt(args[++i]);
      }
    } else if (arg === '--offset' || arg === '-o') {
      if (i + 1 < args.length) {
        options.offset = parseInt(args[++i]);
      }
    } else if (arg === '--pretty' || arg === '-p') {
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
Beaconcha.in Validator Rewards Query Tool (JavaScript)

Usage: node query-validator-rewards.js --apikey YOUR_API_KEY [options]

Description: Query Ethereum validator rewards using Beaconcha.in API v2

Options:
  -k, --apikey <key>      Beaconcha.in API key (required)
  -v, --validators <ids>  Comma-separated list of validator indices (e.g., "1,2,3")
  -e, --epoch <epoch>     Specific epoch to query rewards for
  -l, --limit <limit>     Number of results to return (default: ${DEFAULT_LIMIT})
  -o, --offset <offset>   Pagination offset (default: ${DEFAULT_OFFSET})
  -p, --pretty            Pretty-print JSON output
  -h, --help              Show this help message

Examples:
  node query-validator-rewards.js --apikey YOUR_API_KEY
  node query-validator-rewards.js --apikey YOUR_API_KEY --validators "1,2,3" --pretty
  node query-validator-rewards.js --apikey YOUR_API_KEY --epoch 123456 --limit 50

Environment Variables:
  BEACONCHAIN_API_KEY     API key for Beaconcha.in (alternative to --apikey)

Security Note:
  Never commit API keys to version control. Use environment variables or
  gitignored configuration files. See SECURITY_BEST_PRACTICES.md for details.
`);
}

function formatResponse(data, pretty = false) {
  if (pretty) {
    return JSON.stringify(data, null, 2);
  }
  return JSON.stringify(data);
}

function formatRewardRecord(record) {
  const lines = [];
  lines.push(`  Validator Index: ${record.validatorindex ?? 'N/A'}`);
  lines.push(`  Epoch: ${record.epoch ?? 'N/A'}`);
  
  if (record.attesterslot !== null && record.attesterslot !== undefined) {
    lines.push(`  Attester Slot: ${record.attesterslot}`);
  }
  
  if (record.attestation_source !== null && record.attestation_source !== undefined) {
    lines.push(`  Attestation Source: ${record.attestation_source}`);
  }
  
  if (record.attestation_target !== null && record.attestation_target !== undefined) {
    lines.push(`  Attestation Target: ${record.attestation_target}`);
  }
  
  if (record.attestation_head !== null && record.attestation_head !== undefined) {
    lines.push(`  Attestation Head: ${record.attestation_head}`);
  }
  
  if (record.proposerslot !== null && record.proposerslot !== undefined) {
    lines.push(`  Proposer Slot: ${record.proposerslot}`);
  }
  
  if (record.deposits !== null && record.deposits !== undefined) {
    lines.push(`  Deposits: ${record.deposits}`);
  }
  
  if (record.withdrawals !== null && record.withdrawals !== undefined) {
    lines.push(`  Withdrawals: ${record.withdrawals}`);
  }
  
  return lines.join('\n');
}

async function queryValidatorRewards(options) {
  const { apikey, validators, epoch, limit, offset } = options;

  if (!apikey) {
    console.error('Error: API key is required.');
    console.error('Provide it via --apikey option or set BEACONCHAIN_API_KEY environment variable.');
    process.exit(1);
  }

  // Build request body
  const body = {
    limit: limit,
    offset: offset
  };

  if (validators && validators.length > 0) {
    body.validators = validators;
  }

  if (epoch !== null && epoch !== undefined) {
    body.epoch = epoch;
  }

  // Display query information
  console.log('Querying Beaconcha.in Validator Rewards API...');
  console.log(`Endpoint: ${API_ENDPOINT}`);
  if (validators && validators.length > 0) {
    console.log(`Validators: ${validators.join(', ')}`);
  }
  if (epoch !== null && epoch !== undefined) {
    console.log(`Epoch: ${epoch}`);
  }
  console.log(`Limit: ${limit}`);
  console.log(`Offset: ${offset}`);
  console.log();

  const fetchOptions = {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apikey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  };

  try {
    const response = await fetch(API_ENDPOINT, fetchOptions);
    
    if (!response.ok) {
      const errorText = await response.text();
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch (e) {
        errorData = { error: errorText };
      }
      console.error('HTTP Error:', response.status);
      console.error('Error details:', formatResponse(errorData, true));
      process.exit(1);
    }
    
    const data = await response.json();
    
    console.log('Response:');
    console.log(formatResponse(data, options.pretty));
    
    // Check status
    const status = data.status || 'unknown';
    if (status === 'success') {
      console.log();
      console.log('✓ Query successful');
      
      // Display summary if pretty output requested
      if (options.pretty && data.data) {
        const results = data.data;
        if (Array.isArray(results)) {
          console.log(`Results: ${results.length} record(s)`);
          
          if (results.length > 0 && results.length <= 10) {
            console.log();
            console.log('Details:');
            results.forEach((record, i) => {
              console.log(`\nRecord #${i + 1}:`);
              console.log(formatRewardRecord(record));
            });
          } else if (results.length > 10) {
            console.log(`(showing first 10 of ${results.length} records)`);
            console.log();
            console.log('Details:');
            results.slice(0, 10).forEach((record, i) => {
              console.log(`\nRecord #${i + 1}:`);
              console.log(formatRewardRecord(record));
            });
          }
        }
      }
    } else if (status === 'error') {
      console.log();
      console.log('✗ Query failed');
      const errorMsg = data.error || 'Unknown error';
      console.log(`Error: ${errorMsg}`);
      process.exit(1);
    } else {
      console.log();
      console.log('⚠ Unknown response status');
    }
    
    return data;
  } catch (err) {
    console.error('Error fetching validator rewards:', err.message);
    process.exit(1);
  }
}

// Main execution
if (require.main === module) {
  const options = parseArgs();
  
  queryValidatorRewards(options)
    .then(() => {
      process.exit(0);
    })
    .catch(err => {
      console.error('Unexpected error:', err);
      process.exit(1);
    });
}

module.exports = { queryValidatorRewards };
