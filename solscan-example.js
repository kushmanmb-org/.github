// Solscan API example using axios
// This demonstrates how to query Solana account transfers using Solscan API v2.0
// Note: Replace 'YOUR_API_TOKEN' with your actual Solscan API token

const { querySolanaTransfers } = require('./query-solana-transfers.js');

// Example usage with custom options
const options = {
  token: process.env.SOLSCAN_API_TOKEN || 'YOUR_API_TOKEN',
  page: '1',
  pageSize: '10',
  sortBy: 'block_time',
  sortOrder: 'desc',
  pretty: true
  // Optionally specify an account:
  // account: 'YourSolanaAccountAddressHere'
};

querySolanaTransfers(options)
  .then(data => {
    console.log('Success! Solana transfers retrieved.');
    // Data is already printed by querySolanaTransfers when pretty=true
  })
  .catch(err => {
    console.error('Failed to fetch transfers:', err.message);
  });
