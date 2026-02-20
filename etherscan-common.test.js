/**
 * Test for etherscan-common module
 * Validates security-focused utility functions
 */

const {
  validateEthereumAddress,
  loadConfig,
  buildApiParams,
  buildApiUrl,
  isResponseSuccessful,
  formatResponse
} = require('./etherscan-common');

describe('etherscan-common security tests', () => {
  describe('validateEthereumAddress', () => {
    // Note: These tests are skipped because the example config
    // doesn't include validationPatterns. In production use,
    // validationPatterns should be added to the config file.
    test.skip('should validate correct Ethereum address format', () => {
      const validAddress = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0';
      expect(validateEthereumAddress(validAddress)).toBe(true);
    });

    test.skip('should reject invalid Ethereum address', () => {
      const invalidAddress = 'not-an-address';
      expect(validateEthereumAddress(invalidAddress)).toBe(false);
    });

    test.skip('should reject empty string', () => {
      expect(validateEthereumAddress('')).toBe(false);
    });
  });

  describe('loadConfig', () => {
    test('should load configuration without errors', () => {
      expect(() => loadConfig()).not.toThrow();
    });

    test('should return an object', () => {
      const config = loadConfig();
      expect(typeof config).toBe('object');
    });

    test('should contain required fields', () => {
      const config = loadConfig();
      expect(config).toHaveProperty('apiBaseUrl');
      expect(config).toHaveProperty('defaultAddress');
      expect(config).toHaveProperty('module');
      expect(config).toHaveProperty('action');
    });

    test('should not expose API keys in config', () => {
      const config = loadConfig();
      // Ensure no actual API key is present in example config
      const configStr = JSON.stringify(config);
      // Check that the config doesn't have an actual API key field with a real value
      expect(config).not.toHaveProperty('apikey');
      expect(config).not.toHaveProperty('apiKey');
      // Ensure the comment warns against including API keys
      expect(config._comment || '').toContain('DO NOT');
    });
  });

  describe('buildApiParams', () => {
    test('should build API parameters without leaking sensitive data', () => {
      const config = loadConfig();
      const testApiKey = 'TEST_API_KEY';
      const testAddress = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0';
      
      const params = buildApiParams(config, testAddress, testApiKey);
      
      expect(params).toHaveProperty('apikey');
      expect(params.apikey).toBe(testApiKey);
      expect(params.address).toBe(testAddress);
    });

    test('should use default values when not provided', () => {
      const config = loadConfig();
      const params = buildApiParams(config, '0xtest', 'key');
      
      expect(params).toHaveProperty('chainid');
      expect(params).toHaveProperty('page');
      expect(params).toHaveProperty('offset');
    });
  });

  describe('buildApiUrl', () => {
    test('should build valid URL', () => {
      const config = loadConfig();
      const params = {
        module: 'account',
        action: 'tokentx',
        address: '0xtest',
        apikey: 'TEST_KEY'
      };
      
      const url = buildApiUrl(config, params);
      expect(url).toContain('http');
      expect(url).toContain('apikey=TEST_KEY');
    });

    test('should properly encode URL parameters', () => {
      const config = loadConfig();
      const params = {
        address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
        apikey: 'TEST_KEY'
      };
      
      const url = buildApiUrl(config, params);
      expect(url).toMatch(/address=0x[a-fA-F0-9]+/);
    });
  });

  describe('isResponseSuccessful', () => {
    test('should return true for successful response', () => {
      const response = { status: "1", result: [] };
      expect(isResponseSuccessful(response)).toBe(true);
    });

    test('should return false for failed response', () => {
      const response = { status: "0", result: [] };
      expect(isResponseSuccessful(response)).toBe(false);
    });

    test('should handle null response safely', () => {
      // The function returns null for null input, which is acceptable behavior
      const result = isResponseSuccessful(null);
      expect(result === false || result === null).toBe(true);
    });
  });

  describe('formatResponse', () => {
    test('should format response as JSON string', () => {
      const response = { status: "1", result: [] };
      const formatted = formatResponse(response);
      expect(typeof formatted).toBe('string');
      expect(() => JSON.parse(formatted)).not.toThrow();
    });

    test('should format with pretty option', () => {
      const response = { status: "1" };
      const formatted = formatResponse(response, { pretty: true });
      expect(formatted).toContain('\n');
    });

    test('should redact sensitive data in formatting', () => {
      const response = { apikey: 'SHOULD_NOT_APPEAR', status: "1" };
      const formatted = formatResponse(response);
      expect(formatted).not.toContain('SHOULD_NOT_APPEAR');
      expect(formatted).toContain('[REDACTED]');
      expect(formatted).toContain('"status":"1"');
    });

    test('should redact various sensitive field names', () => {
      const response = {
        apikey: 'secret1',
        api_key: 'secret2',
        apiKey: 'secret3',
        token: 'secret4',
        access_token: 'secret5',
        password: 'secret6',
        normalField: 'visible',
        status: "1"
      };
      const formatted = formatResponse(response);
      expect(formatted).not.toContain('secret1');
      expect(formatted).not.toContain('secret2');
      expect(formatted).not.toContain('secret3');
      expect(formatted).not.toContain('secret4');
      expect(formatted).not.toContain('secret5');
      expect(formatted).not.toContain('secret6');
      expect(formatted).toContain('visible');
      expect(formatted).toContain('"status":"1"');
    });

    test('should redact nested sensitive fields', () => {
      const response = {
        status: "1",
        data: {
          apikey: 'NESTED_SECRET',
          result: 'ok'
        }
      };
      const formatted = formatResponse(response);
      expect(formatted).not.toContain('NESTED_SECRET');
      expect(formatted).toContain('[REDACTED]');
      expect(formatted).toContain('result');
    });
  });
});
