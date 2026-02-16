#!/usr/bin/env node

/**
 * Example usage of verify-contract.js utilities
 * 
 * This script demonstrates how to use the ContractAddressValidator and
 * ContractVerifier classes to validate Ethereum addresses and work with
 * smart contract ABIs.
 */

const { ContractAddressValidator, ContractVerifier } = require('./verify-contract');
const fs = require('fs');
const path = require('path');

console.log('='.repeat(60));
console.log('Smart Contract Verification Utilities - Example Usage');
console.log('='.repeat(60));
console.log();

// Example 1: Validate Ethereum addresses
console.log('Example 1: Address Validation');
console.log('-'.repeat(60));

const testAddresses = [
  '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7',  // Valid address
  '0x0000000000000000000000000000000000000000',  // Null address
  '0xInvalidAddress',                              // Invalid address
  'not-an-address'                                 // Not an address
];

testAddresses.forEach(addr => {
  const result = ContractAddressValidator.validateAddress(addr, true);
  console.log(`Address: ${addr}`);
  console.log(`  Valid: ${result.valid}`);
  console.log(`  Normalized: ${result.normalized || 'N/A'}`);
  console.log(`  Is Null: ${result.isNull}`);
  if (result.error) {
    console.log(`  Error: ${result.error}`);
  }
  console.log();
});

// Example 2: Compare addresses
console.log('Example 2: Address Comparison');
console.log('-'.repeat(60));

const addr1 = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
const addr2 = '0x6b834a2f2a24ae7e592aa0843aa2bdf58157bee7';
const addr3 = '0x0000000000000000000000000000000000000000';

console.log(`Comparing "${addr1}" and "${addr2}"`);
console.log(`  Are Equal: ${ContractAddressValidator.areEqual(addr1, addr2)}`);
console.log();

console.log(`Comparing "${addr1}" and "${addr3}"`);
console.log(`  Are Equal: ${ContractAddressValidator.areEqual(addr1, addr3)}`);
console.log();

// Example 3: Work with Contract ABI
console.log('Example 3: Contract Verification with ABI');
console.log('-'.repeat(60));

// Sample ERC-20 token ABI (simplified)
const erc20ABI = [
  {
    type: 'function',
    name: 'balanceOf',
    inputs: [{ name: 'account', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }],
    stateMutability: 'view'
  },
  {
    type: 'function',
    name: 'transfer',
    inputs: [
      { name: 'to', type: 'address' },
      { name: 'amount', type: 'uint256' }
    ],
    outputs: [{ name: '', type: 'bool' }],
    stateMutability: 'nonpayable'
  },
  {
    type: 'function',
    name: 'approve',
    inputs: [
      { name: 'spender', type: 'address' },
      { name: 'amount', type: 'uint256' }
    ],
    outputs: [{ name: '', type: 'bool' }],
    stateMutability: 'nonpayable'
  },
  {
    type: 'event',
    name: 'Transfer',
    inputs: [
      { name: 'from', type: 'address', indexed: true },
      { name: 'to', type: 'address', indexed: true },
      { name: 'value', type: 'uint256', indexed: false }
    ]
  },
  {
    type: 'event',
    name: 'Approval',
    inputs: [
      { name: 'owner', type: 'address', indexed: true },
      { name: 'spender', type: 'address', indexed: true },
      { name: 'value', type: 'uint256', indexed: false }
    ]
  }
];

const tokenAddress = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
const verifier = new ContractVerifier(tokenAddress, erc20ABI);

console.log('Contract Address:', tokenAddress);
console.log('Address Valid:', verifier.validateAddress().valid);
console.log();

const info = verifier.getVerificationInfo();
console.log('Contract Information:');
console.log(`  Total Functions: ${info.functionCount}`);
console.log(`  Read-Only Functions: ${info.readOnlyFunctionCount}`);
console.log(`  Write Functions: ${info.writeFunctionCount}`);
console.log(`  Total Events: ${info.eventCount}`);
console.log();

console.log('Available Functions:');
info.functions.forEach(fn => console.log(`  - ${fn}`));
console.log();

console.log('Available Events:');
info.events.forEach(evt => console.log(`  - ${evt}`));
console.log();

// Check specific functions
console.log('Function Checks:');
console.log(`  Has 'balanceOf': ${verifier.hasFunction('balanceOf')}`);
console.log(`  Has 'transfer': ${verifier.hasFunction('transfer')}`);
console.log(`  Has 'mint': ${verifier.hasFunction('mint')}`);
console.log();

// Get function details
const transferFn = verifier.getFunction('transfer');
if (transferFn) {
  console.log('Transfer Function Details:');
  console.log(`  Name: ${transferFn.name}`);
  console.log(`  State Mutability: ${transferFn.stateMutability}`);
  console.log(`  Inputs: ${transferFn.inputs.length}`);
  transferFn.inputs.forEach(input => {
    console.log(`    - ${input.name}: ${input.type}`);
  });
  console.log();
}

// Example 4: Load multisig wallet ABI (if available)
console.log('Example 4: Multisig Wallet Contract');
console.log('-'.repeat(60));

const multisigAbiPath = path.join(__dirname, 'multisig-wallet.abi.json');
if (fs.existsSync(multisigAbiPath)) {
  const multisigABI = JSON.parse(fs.readFileSync(multisigAbiPath, 'utf8'));
  const multisigVerifier = ContractVerifier.fromABI(
    '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7',
    multisigABI
  );
  
  const multisigInfo = verifier.getVerificationInfo();
  console.log('Multisig Wallet Information:');
  console.log(`  Total Functions: ${multisigInfo.functionCount}`);
  console.log(`  Total Events: ${multisigInfo.eventCount}`);
  console.log();
  
  // Check for specific multisig functions
  console.log('Multisig Functions Available:');
  const multisigFunctions = ['addOwner', 'removeOwner', 'execute', 'confirm'];
  multisigFunctions.forEach(fn => {
    console.log(`  ${fn}: ${multisigVerifier.hasFunction(fn) ? '✓' : '✗'}`);
  });
} else {
  console.log('multisig-wallet.abi.json not found - skipping this example');
}

console.log();
console.log('='.repeat(60));
console.log('Examples completed successfully!');
console.log('='.repeat(60));
