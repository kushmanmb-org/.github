/**
 * Basic tests for query-solana-transfers.js
 */

const { querySolanaTransfers } = require('./query-solana-transfers.js');

describe('query-solana-transfers', () => {
  test('module exports querySolanaTransfers function', () => {
    expect(typeof querySolanaTransfers).toBe('function');
  });

  test('querySolanaTransfers is defined', () => {
    expect(querySolanaTransfers).toBeDefined();
  });
  
  // Note: We cannot test actual API calls without a valid token
  // Integration tests would require a test token or mock
});
