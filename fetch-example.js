// Simple fetch example for Etherscan API v2
// This demonstrates basic usage by utilizing the query-token-balance module
// Note: Replace 'YourApiKeyToken' with your actual Etherscan API key

const { queryTokenBalance } = require('./query-token-balance.js');

// Example usage with custom options
const options = {
  apikey: 'YourApiKeyToken',
  pretty: true
  // Optionally override defaults:
  // address: '0x...',
  // chainid: 1,
  // page: 1,
  // offset: 100
};

queryTokenBalance(options)
  .then(data => {
    console.log('Success! Token balance retrieved.');
    // Data is already printed by queryTokenBalance when pretty=true
  })
  .catch(err => {
    console.error('Failed to fetch token balance:', err.message);
  });
