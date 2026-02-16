/**
 * Tests for Smart Contract Verification Utilities
 * 
 * Validates the ContractAddressValidator and ContractVerifier classes
 * to ensure proper validation and security of smart contract operations.
 */

const { ContractAddressValidator, ContractVerifier } = require('./verify-contract');
const fs = require('fs');
const path = require('path');

describe('ContractAddressValidator', () => {
  describe('validateAddress', () => {
    test('should validate correct Ethereum address', () => {
      const validAddress = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const result = ContractAddressValidator.validateAddress(validAddress);
      
      expect(result.valid).toBe(true);
      expect(result.isNull).toBe(false);
      expect(result.normalized).toBe(validAddress.toLowerCase());
      expect(result.error).toBeNull();
    });
    
    test('should validate address with all lowercase', () => {
      const lowercaseAddress = '0x6b834a2f2a24ae7e592aa0843aa2bdf58157bee7';
      const result = ContractAddressValidator.validateAddress(lowercaseAddress);
      
      expect(result.valid).toBe(true);
      expect(result.normalized).toBe(lowercaseAddress);
      expect(result.checksumValid).toBeNull(); // All lowercase = no checksum
    });
    
    test('should validate address with all uppercase', () => {
      const uppercaseAddress = '0x6B834A2F2A24AE7E592AA0843AA2BDF58157BEE7';
      const result = ContractAddressValidator.validateAddress(uppercaseAddress);
      
      expect(result.valid).toBe(true);
      expect(result.checksumValid).toBeNull(); // All uppercase = no checksum
    });
    
    test('should reject address without 0x prefix', () => {
      const noPrefix = '6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const result = ContractAddressValidator.validateAddress(noPrefix);
      
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Invalid Ethereum address format');
    });
    
    test('should reject address with wrong length', () => {
      const shortAddress = '0x6B834a2f2a24';
      const result = ContractAddressValidator.validateAddress(shortAddress);
      
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Invalid Ethereum address format');
    });
    
    test('should reject empty string', () => {
      const result = ContractAddressValidator.validateAddress('');
      
      expect(result.valid).toBe(false);
      expect(result.error).toBe('Address must be a non-empty string');
    });
    
    test('should reject null input', () => {
      const result = ContractAddressValidator.validateAddress(null);
      
      expect(result.valid).toBe(false);
      expect(result.error).toBe('Address must be a non-empty string');
    });
    
    test('should reject undefined input', () => {
      const result = ContractAddressValidator.validateAddress(undefined);
      
      expect(result.valid).toBe(false);
      expect(result.error).toBe('Address must be a non-empty string');
    });
    
    test('should handle address with whitespace', () => {
      const addressWithSpace = '  0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7  ';
      const result = ContractAddressValidator.validateAddress(addressWithSpace);
      
      expect(result.valid).toBe(true);
      expect(result.normalized).toBe('0x6b834a2f2a24ae7e592aa0843aa2bdf58157bee7');
    });
    
    test('should recognize null address', () => {
      const nullAddress = '0x0000000000000000000000000000000000000000';
      const result = ContractAddressValidator.validateAddress(nullAddress);
      
      expect(result.valid).toBe(false); // Not allowed by default
      expect(result.isNull).toBe(true);
      expect(result.error).toBe('Null/zero address not allowed');
    });
    
    test('should allow null address when specified', () => {
      const nullAddress = '0x0000000000000000000000000000000000000000';
      const result = ContractAddressValidator.validateAddress(nullAddress, true);
      
      expect(result.valid).toBe(true);
      expect(result.isNull).toBe(true);
    });
    
    test('should recognize null address in different case', () => {
      const nullAddressUpper = '0x' + '0000000000000000000000000000000000000000'.toUpperCase();
      const result = ContractAddressValidator.validateAddress(nullAddressUpper, true);
      
      expect(result.valid).toBe(true);
      expect(result.isNull).toBe(true);
    });
    
    test('should reject invalid hex characters', () => {
      const invalidHex = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157beeG';
      const result = ContractAddressValidator.validateAddress(invalidHex);
      
      expect(result.valid).toBe(false);
    });
  });
  
  describe('normalizeAddress', () => {
    test('should normalize valid address to lowercase', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const normalized = ContractAddressValidator.normalizeAddress(address);
      
      expect(normalized).toBe('0x6b834a2f2a24ae7e592aa0843aa2bdf58157bee7');
    });
    
    test('should return null for invalid address', () => {
      const invalidAddress = 'not-an-address';
      const normalized = ContractAddressValidator.normalizeAddress(invalidAddress);
      
      expect(normalized).toBeNull();
    });
  });
  
  describe('isNullAddress', () => {
    test('should identify null address', () => {
      const nullAddress = '0x0000000000000000000000000000000000000000';
      expect(ContractAddressValidator.isNullAddress(nullAddress)).toBe(true);
    });
    
    test('should identify null address in uppercase', () => {
      const nullAddress = '0x0000000000000000000000000000000000000000'.toUpperCase();
      expect(ContractAddressValidator.isNullAddress(nullAddress)).toBe(true);
    });
    
    test('should return false for non-null address', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      expect(ContractAddressValidator.isNullAddress(address)).toBe(false);
    });
    
    test('should return false for invalid input', () => {
      expect(ContractAddressValidator.isNullAddress(null)).toBe(false);
      expect(ContractAddressValidator.isNullAddress(undefined)).toBe(false);
      expect(ContractAddressValidator.isNullAddress('')).toBe(false);
    });
  });
  
  describe('areEqual', () => {
    test('should compare addresses case-insensitively', () => {
      const addr1 = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const addr2 = '0x6b834a2f2a24ae7e592aa0843aa2bdf58157bee7';
      
      expect(ContractAddressValidator.areEqual(addr1, addr2)).toBe(true);
    });
    
    test('should return false for different addresses', () => {
      const addr1 = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const addr2 = '0x0000000000000000000000000000000000000000';
      
      expect(ContractAddressValidator.areEqual(addr1, addr2)).toBe(false);
    });
    
    test('should return false for invalid addresses', () => {
      const validAddr = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const invalidAddr = 'not-an-address';
      
      expect(ContractAddressValidator.areEqual(validAddr, invalidAddr)).toBe(false);
    });
  });
});

describe('ContractVerifier', () => {
  const sampleABI = [
    {
      type: 'function',
      name: 'balanceOf',
      inputs: [{ name: 'account', type: 'address' }],
      outputs: [{ name: '', type: 'uint256' }],
      stateMutability: 'view',
      constant: true
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
      type: 'event',
      name: 'Transfer',
      inputs: [
        { name: 'from', type: 'address', indexed: true },
        { name: 'to', type: 'address', indexed: true },
        { name: 'value', type: 'uint256', indexed: false }
      ]
    },
    {
      type: 'constructor',
      inputs: [
        { name: 'initialSupply', type: 'uint256' }
      ]
    }
  ];
  
  describe('constructor', () => {
    test('should create verifier with address only', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      
      expect(verifier.contractAddress).toBe(address);
      expect(verifier.abi).toBeNull();
      expect(verifier.functions).toBeNull();
      expect(verifier.events).toBeNull();
    });
    
    test('should create verifier with address and ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      
      expect(verifier.contractAddress).toBe(address);
      expect(verifier.abi).toBe(sampleABI);
      expect(verifier.functions).toHaveLength(2);
      expect(verifier.events).toHaveLength(1);
    });
  });
  
  describe('validateAddress', () => {
    test('should validate contract address', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const result = verifier.validateAddress();
      
      expect(result.valid).toBe(true);
      expect(result.normalized).toBe(address.toLowerCase());
    });
    
    test('should detect invalid contract address', () => {
      const invalidAddress = 'invalid';
      const verifier = new ContractVerifier(invalidAddress);
      const result = verifier.validateAddress();
      
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Invalid Ethereum address format');
    });
  });
  
  describe('parseABI', () => {
    test('should parse ABI correctly', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const parsed = verifier.parseABI(sampleABI);
      
      expect(parsed.functions).toHaveLength(2);
      expect(parsed.events).toHaveLength(1);
      expect(parsed.constructor).toBeDefined();
      expect(parsed.constructor.type).toBe('constructor');
    });
    
    test('should throw error for non-array ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      
      expect(() => verifier.parseABI('not-an-array')).toThrow('ABI must be an array');
    });
  });
  
  describe('getFunctionNames', () => {
    test('should return all function names', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const names = verifier.getFunctionNames();
      
      expect(names).toContain('balanceOf');
      expect(names).toContain('transfer');
      expect(names).toHaveLength(2);
    });
    
    test('should return empty array when no ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const names = verifier.getFunctionNames();
      
      expect(names).toEqual([]);
    });
  });
  
  describe('getEventNames', () => {
    test('should return all event names', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const names = verifier.getEventNames();
      
      expect(names).toContain('Transfer');
      expect(names).toHaveLength(1);
    });
    
    test('should return empty array when no ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const names = verifier.getEventNames();
      
      expect(names).toEqual([]);
    });
  });
  
  describe('hasFunction', () => {
    test('should return true for existing function', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      
      expect(verifier.hasFunction('balanceOf')).toBe(true);
      expect(verifier.hasFunction('transfer')).toBe(true);
    });
    
    test('should return false for non-existing function', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      
      expect(verifier.hasFunction('nonExistent')).toBe(false);
    });
    
    test('should return false when no ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      
      expect(verifier.hasFunction('balanceOf')).toBe(false);
    });
  });
  
  describe('hasEvent', () => {
    test('should return true for existing event', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      
      expect(verifier.hasEvent('Transfer')).toBe(true);
    });
    
    test('should return false for non-existing event', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      
      expect(verifier.hasEvent('NonExistent')).toBe(false);
    });
  });
  
  describe('getFunction', () => {
    test('should return function details', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const fn = verifier.getFunction('balanceOf');
      
      expect(fn).toBeDefined();
      expect(fn.name).toBe('balanceOf');
      expect(fn.inputs).toHaveLength(1);
      expect(fn.stateMutability).toBe('view');
    });
    
    test('should return null for non-existing function', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const fn = verifier.getFunction('nonExistent');
      
      expect(fn).toBeNull();
    });
  });
  
  describe('getEvent', () => {
    test('should return event details', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const evt = verifier.getEvent('Transfer');
      
      expect(evt).toBeDefined();
      expect(evt.name).toBe('Transfer');
      expect(evt.inputs).toHaveLength(3);
    });
    
    test('should return null for non-existing event', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const evt = verifier.getEvent('NonExistent');
      
      expect(evt).toBeNull();
    });
  });
  
  describe('getReadOnlyFunctions', () => {
    test('should return only read-only functions', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const readOnly = verifier.getReadOnlyFunctions();
      
      expect(readOnly).toHaveLength(1);
      expect(readOnly[0].name).toBe('balanceOf');
    });
    
    test('should return empty array when no ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const readOnly = verifier.getReadOnlyFunctions();
      
      expect(readOnly).toEqual([]);
    });
  });
  
  describe('getWriteFunctions', () => {
    test('should return only write functions', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const write = verifier.getWriteFunctions();
      
      expect(write).toHaveLength(1);
      expect(write[0].name).toBe('transfer');
    });
    
    test('should return empty array when no ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const write = verifier.getWriteFunctions();
      
      expect(write).toEqual([]);
    });
  });
  
  describe('getVerificationInfo', () => {
    test('should return complete verification info', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address, sampleABI);
      const info = verifier.getVerificationInfo();
      
      expect(info.address).toBe(address);
      expect(info.addressValid).toBe(true);
      expect(info.addressNormalized).toBe(address.toLowerCase());
      expect(info.hasABI).toBe(true);
      expect(info.functionCount).toBe(2);
      expect(info.eventCount).toBe(1);
      expect(info.readOnlyFunctionCount).toBe(1);
      expect(info.writeFunctionCount).toBe(1);
      expect(info.functions).toContain('balanceOf');
      expect(info.functions).toContain('transfer');
      expect(info.events).toContain('Transfer');
    });
    
    test('should handle verifier without ABI', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = new ContractVerifier(address);
      const info = verifier.getVerificationInfo();
      
      expect(info.hasABI).toBe(false);
      expect(info.functionCount).toBe(0);
      expect(info.eventCount).toBe(0);
      expect(info.functions).toEqual([]);
      expect(info.events).toEqual([]);
    });
  });
  
  describe('static validateContractAddress', () => {
    test('should validate address without creating instance', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const result = ContractVerifier.validateContractAddress(address);
      
      expect(result.valid).toBe(true);
    });
  });
  
  describe('static fromABI', () => {
    test('should create verifier from ABI array', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const verifier = ContractVerifier.fromABI(address, sampleABI);
      
      expect(verifier).toBeInstanceOf(ContractVerifier);
      expect(verifier.contractAddress).toBe(address);
      expect(verifier.functions).toHaveLength(2);
    });
    
    test('should create verifier from ABI JSON string', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const abiString = JSON.stringify(sampleABI);
      const verifier = ContractVerifier.fromABI(address, abiString);
      
      expect(verifier).toBeInstanceOf(ContractVerifier);
      expect(verifier.functions).toHaveLength(2);
    });
    
    test('should throw error for invalid JSON string', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      const invalidJSON = '{invalid json}';
      
      expect(() => ContractVerifier.fromABI(address, invalidJSON)).toThrow('Invalid ABI JSON string');
    });
    
    test('should throw error for invalid ABI type', () => {
      const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
      
      expect(() => ContractVerifier.fromABI(address, 123)).toThrow('ABI must be an array or JSON string');
    });
  });
  
  describe('integration with multisig-wallet.abi.json', () => {
    test('should load and verify multisig wallet ABI', () => {
      const abiPath = path.join(__dirname, 'multisig-wallet.abi.json');
      
      // Only run this test if the file exists
      if (fs.existsSync(abiPath)) {
        const abiData = JSON.parse(fs.readFileSync(abiPath, 'utf8'));
        const address = '0x6B834a2f2a24ae7e592AA0843aa2bDF58157bee7';
        const verifier = new ContractVerifier(address, abiData);
        
        expect(verifier.hasFunction('addOwner')).toBe(true);
        expect(verifier.hasFunction('removeOwner')).toBe(true);
        expect(verifier.hasFunction('isOwner')).toBe(true);
        expect(verifier.hasEvent('OwnerAdded')).toBe(true);
        expect(verifier.hasEvent('OwnerRemoved')).toBe(true);
        
        const info = verifier.getVerificationInfo();
        expect(info.functionCount).toBeGreaterThan(0);
        expect(info.eventCount).toBeGreaterThan(0);
      }
    });
  });
});
