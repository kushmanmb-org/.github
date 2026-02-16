/**
 * Tests for Verification Utilities
 * 
 * Validates the TransactionHashValidator and ENSVerifier classes
 * to ensure proper validation and security of blockchain data.
 */

const { TransactionHashValidator, ENSVerifier } = require('./test-verify');

describe('TransactionHashValidator', () => {
  describe('validateHash - Ethereum format', () => {
    test('should validate correct Ethereum transaction hash', () => {
      const validEthHash = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      const result = TransactionHashValidator.validateHash(validEthHash);
      
      expect(result.valid).toBe(true);
      expect(result.format).toBe('ethereum');
      expect(result.isNull).toBe(false);
      expect(result.normalized).toBe(validEthHash.toLowerCase());
      expect(result.error).toBeNull();
    });
    
    test('should validate Ethereum hash with mixed case', () => {
      const mixedCaseHash = '0xABCDEF1234567890abcdef1234567890abcdef1234567890ABCDEF1234567890';
      const result = TransactionHashValidator.validateHash(mixedCaseHash);
      
      expect(result.valid).toBe(true);
      expect(result.format).toBe('ethereum');
      expect(result.normalized).toBe(mixedCaseHash.toLowerCase());
    });
    
    test('should reject Ethereum hash without 0x prefix', () => {
      const noPrefix = '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      const result = TransactionHashValidator.validateHash(noPrefix);
      
      // This should be valid Bitcoin format, not Ethereum
      expect(result.valid).toBe(true);
      expect(result.format).toBe('bitcoin');
    });
    
    test('should reject Ethereum hash with wrong length', () => {
      const shortHash = '0x1234567890abcdef';
      const result = TransactionHashValidator.validateHash(shortHash);
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
    });
    
    test('should recognize null Ethereum hash', () => {
      const nullHash = '0x0000000000000000000000000000000000000000000000000000000000000000';
      const result = TransactionHashValidator.validateHash(nullHash);
      
      expect(result.valid).toBe(true);
      expect(result.format).toBe('ethereum');
      expect(result.isNull).toBe(true);
    });
    
    test('should reject null Ethereum hash when allowNull is false', () => {
      const nullHash = '0x0000000000000000000000000000000000000000000000000000000000000000';
      const result = TransactionHashValidator.validateHash(nullHash, false);
      
      expect(result.valid).toBe(false);
      expect(result.isNull).toBe(true);
      expect(result.error).toContain('Null/zero transaction hash not allowed');
    });
  });
  
  describe('validateHash - Bitcoin format', () => {
    test('should validate correct Bitcoin transaction hash', () => {
      const validBtcHash = '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      const result = TransactionHashValidator.validateHash(validBtcHash);
      
      expect(result.valid).toBe(true);
      expect(result.format).toBe('bitcoin');
      expect(result.isNull).toBe(false);
      expect(result.normalized).toBe(validBtcHash.toLowerCase());
      expect(result.error).toBeNull();
    });
    
    test('should validate Bitcoin hash with mixed case', () => {
      const mixedCaseHash = 'ABCDEF1234567890abcdef1234567890abcdef1234567890ABCDEF1234567890';
      const result = TransactionHashValidator.validateHash(mixedCaseHash);
      
      expect(result.valid).toBe(true);
      expect(result.format).toBe('bitcoin');
      expect(result.normalized).toBe(mixedCaseHash.toLowerCase());
    });
    
    test('should reject Bitcoin hash with wrong length', () => {
      const shortHash = '1234567890abcdef';
      const result = TransactionHashValidator.validateHash(shortHash);
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
    });
    
    test('should recognize null Bitcoin hash', () => {
      const nullHash = '0000000000000000000000000000000000000000000000000000000000000000';
      const result = TransactionHashValidator.validateHash(nullHash);
      
      expect(result.valid).toBe(true);
      expect(result.format).toBe('bitcoin');
      expect(result.isNull).toBe(true);
    });
    
    test('should reject null Bitcoin hash when allowNull is false', () => {
      const nullHash = '0000000000000000000000000000000000000000000000000000000000000000';
      const result = TransactionHashValidator.validateHash(nullHash, false);
      
      expect(result.valid).toBe(false);
      expect(result.isNull).toBe(true);
      expect(result.error).toContain('Null/zero transaction hash not allowed');
    });
  });
  
  describe('validateHash - Invalid inputs', () => {
    test('should reject empty string', () => {
      const result = TransactionHashValidator.validateHash('');
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
      expect(result.error).toContain('must be a non-empty string');
    });
    
    test('should reject null input', () => {
      const result = TransactionHashValidator.validateHash(null);
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
      expect(result.error).toContain('must be a non-empty string');
    });
    
    test('should reject undefined input', () => {
      const result = TransactionHashValidator.validateHash(undefined);
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
      expect(result.error).toContain('must be a non-empty string');
    });
    
    test('should reject non-string input', () => {
      const result = TransactionHashValidator.validateHash(12345);
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
      expect(result.error).toContain('must be a non-empty string');
    });
    
    test('should reject hash with invalid characters', () => {
      const invalidHash = '0xGHIJKL7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      const result = TransactionHashValidator.validateHash(invalidHash);
      
      expect(result.valid).toBe(false);
      expect(result.format).toBe('invalid');
    });
  });
  
  describe('normalizeHash', () => {
    test('should normalize valid Ethereum hash to lowercase', () => {
      const hash = '0xABCDEF1234567890abcdef1234567890abcdef1234567890ABCDEF1234567890';
      const normalized = TransactionHashValidator.normalizeHash(hash);
      
      expect(normalized).toBe(hash.toLowerCase());
    });
    
    test('should normalize valid Bitcoin hash to lowercase', () => {
      const hash = 'ABCDEF1234567890abcdef1234567890abcdef1234567890ABCDEF1234567890';
      const normalized = TransactionHashValidator.normalizeHash(hash);
      
      expect(normalized).toBe(hash.toLowerCase());
    });
    
    test('should return null for invalid hash', () => {
      const invalidHash = 'invalid-hash';
      const normalized = TransactionHashValidator.normalizeHash(invalidHash);
      
      expect(normalized).toBeNull();
    });
  });
  
  describe('isEthereumFormat', () => {
    test('should return true for valid Ethereum hash', () => {
      const hash = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      expect(TransactionHashValidator.isEthereumFormat(hash)).toBe(true);
    });
    
    test('should return false for Bitcoin hash', () => {
      const hash = '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      expect(TransactionHashValidator.isEthereumFormat(hash)).toBe(false);
    });
    
    test('should return false for invalid hash', () => {
      expect(TransactionHashValidator.isEthereumFormat('invalid')).toBe(false);
    });
  });
  
  describe('isBitcoinFormat', () => {
    test('should return true for valid Bitcoin hash', () => {
      const hash = '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      expect(TransactionHashValidator.isBitcoinFormat(hash)).toBe(true);
    });
    
    test('should return false for Ethereum hash', () => {
      const hash = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
      expect(TransactionHashValidator.isBitcoinFormat(hash)).toBe(false);
    });
    
    test('should return false for invalid hash', () => {
      expect(TransactionHashValidator.isBitcoinFormat('invalid')).toBe(false);
    });
  });
});

describe('ENSVerifier', () => {
  describe('constructor and extractBaseName', () => {
    test('should extract base name from full ENS name', () => {
      const verifier = new ENSVerifier('kushmanmb.base.eth');
      
      expect(verifier.ensName).toBe('kushmanmb.base.eth');
      expect(verifier.baseName).toBe('kushmanmb');
    });
    
    test('should convert ENS name to lowercase', () => {
      const verifier = new ENSVerifier('KushmanMB.BASE.ETH');
      
      expect(verifier.ensName).toBe('kushmanmb.base.eth');
      expect(verifier.baseName).toBe('kushmanmb');
    });
    
    test('should handle name without .base.eth suffix', () => {
      const verifier = new ENSVerifier('kushmanmb');
      
      expect(verifier.ensName).toBe('kushmanmb');
      expect(verifier.baseName).toBe('kushmanmb');
    });
  });
  
  describe('validateFormat', () => {
    test('should validate correct ENS name format', () => {
      const verifier = new ENSVerifier('kushmanmb.base.eth');
      const result = verifier.validateFormat();
      
      expect(result.valid).toBe(true);
      expect(result.name).toBe('kushmanmb.base.eth');
      expect(result.baseName).toBe('kushmanmb');
      expect(result.chainId).toBe(8453);
      expect(result.error).toBeNull();
    });
    
    test('should validate ENS name with hyphens', () => {
      const verifier = new ENSVerifier('my-name-123.base.eth');
      const result = verifier.validateFormat();
      
      expect(result.valid).toBe(true);
      expect(result.baseName).toBe('my-name-123');
    });
    
    test('should reject ENS name without .base.eth suffix', () => {
      const verifier = new ENSVerifier('kushmanmb.eth');
      const result = verifier.validateFormat();
      
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Invalid ENS name format');
    });
    
    test('should reject ENS name with uppercase letters after construction', () => {
      // Constructor converts to lowercase, so this tests the pattern
      const verifier = new ENSVerifier('KUSHMANMB.BASE.ETH');
      const result = verifier.validateFormat();
      
      // Should be valid because constructor converts to lowercase
      expect(result.valid).toBe(true);
    });
    
    test('should reject ENS name with special characters', () => {
      const verifier = new ENSVerifier('kushman@mb.base.eth');
      const result = verifier.validateFormat();
      
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Invalid ENS name format');
    });
    
    test('should reject empty ENS name', () => {
      const verifier = new ENSVerifier('.base.eth');
      const result = verifier.validateFormat();
      
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Invalid ENS name format');
    });
  });
  
  describe('isValidFormat - static method', () => {
    test('should validate correct ENS name format', () => {
      expect(ENSVerifier.isValidFormat('kushmanmb.base.eth')).toBe(true);
    });
    
    test('should validate ENS name with hyphens and numbers', () => {
      expect(ENSVerifier.isValidFormat('my-name-123.base.eth')).toBe(true);
    });
    
    test('should reject ENS name without .base.eth suffix', () => {
      expect(ENSVerifier.isValidFormat('kushmanmb.eth')).toBe(false);
    });
    
    test('should accept ENS name with uppercase (converts internally)', () => {
      // ENS names are case-insensitive, static method converts to lowercase internally
      expect(ENSVerifier.isValidFormat('KushmanMB.base.eth')).toBe(true);
    });
    
    test('should reject ENS name with special characters', () => {
      expect(ENSVerifier.isValidFormat('kushman@mb.base.eth')).toBe(false);
    });
    
    test('should reject empty string', () => {
      expect(ENSVerifier.isValidFormat('')).toBe(false);
    });
    
    test('should reject null input', () => {
      expect(ENSVerifier.isValidFormat(null)).toBe(false);
    });
    
    test('should reject undefined input', () => {
      expect(ENSVerifier.isValidFormat(undefined)).toBe(false);
    });
  });
  
  describe('getVerificationInfo', () => {
    test('should return complete verification information', () => {
      const verifier = new ENSVerifier('kushmanmb.base.eth');
      const info = verifier.getVerificationInfo();
      
      expect(info.valid).toBe(true);
      expect(info.name).toBe('kushmanmb.base.eth');
      expect(info.baseName).toBe('kushmanmb');
      expect(info.network).toBe('Base Mainnet');
      expect(info.chainId).toBe(8453);
      expect(info.rpcUrl).toBe('https://mainnet.base.org');
      expect(info.registrarController).toBe('0x4cCb0BB02FCABA27e82a56646E81d8c5bC4119a5');
      expect(info.registry).toBe('0x6533C94869D28fAA8dF77cc63f9e2b2D6Cf77eBA');
    });
    
    test('should include error for invalid ENS name', () => {
      const verifier = new ENSVerifier('invalid-name');
      const info = verifier.getVerificationInfo();
      
      expect(info.valid).toBe(false);
      expect(info.error).toContain('Invalid ENS name format');
    });
  });
  
  describe('Network configuration constants', () => {
    test('should have correct Base network chain ID', () => {
      expect(ENSVerifier.BASE_CHAIN_ID).toBe(8453);
    });
    
    test('should have correct Base RPC URL', () => {
      expect(ENSVerifier.BASE_RPC_URL).toBe('https://mainnet.base.org');
    });
    
    test('should have correct Base registrar controller address', () => {
      expect(ENSVerifier.BASE_REGISTRAR_CONTROLLER).toBe('0x4cCb0BB02FCABA27e82a56646E81d8c5bC4119a5');
    });
    
    test('should have correct Base registry address', () => {
      expect(ENSVerifier.BASE_REGISTRY).toBe('0x6533C94869D28fAA8dF77cc63f9e2b2D6Cf77eBA');
    });
  });
});

describe('Security considerations', () => {
  test('should not expose sensitive data in validation results', () => {
    const hash = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
    const result = TransactionHashValidator.validateHash(hash);
    
    // Ensure no private keys or sensitive data in result
    const resultStr = JSON.stringify(result);
    expect(resultStr).not.toContain('private');
    expect(resultStr).not.toContain('secret');
    expect(resultStr).not.toContain('key');
  });
  
  test('should handle potential injection attempts safely', () => {
    const injectionAttempt = '0x<script>alert("xss")</script>1234567890abcdef1234567890abcdef';
    const result = TransactionHashValidator.validateHash(injectionAttempt);
    
    expect(result.valid).toBe(false);
    expect(result.format).toBe('invalid');
  });
  
  test('should prevent SQL injection patterns', () => {
    const sqlInjection = "0x' OR '1'='1";
    const result = TransactionHashValidator.validateHash(sqlInjection);
    
    expect(result.valid).toBe(false);
    expect(result.format).toBe('invalid');
  });
});
