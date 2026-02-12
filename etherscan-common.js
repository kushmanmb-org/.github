/**
 * Shared validation and utility functions for Etherscan token balance queries.
 * This module provides common functionality used across multiple implementations.
 */

const fs = require('fs');
const path = require('path');

// Cache for config
let _config = null;

/**
 * Get cached configuration.
 * @returns {object} Configuration data
 */
function getConfig() {
  if (!_config) {
    _config = loadConfig();
  }
  return _config;
}

// Load shared messages
let MESSAGES = null;
function loadMessages() {
  if (!MESSAGES) {
    const messagesPath = path.join(__dirname, 'etherscan-messages.json');
    try {
      const messagesData = fs.readFileSync(messagesPath, 'utf8');
      MESSAGES = JSON.parse(messagesData);
    } catch (err) {
      // Fallback to empty object if messages file not found
      MESSAGES = { errors: {}, status: {}, labels: {} };
    }
  }
  return MESSAGES;
}

/**
 * Validate Ethereum address format.
 * @param {string} address - Ethereum address to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateEthereumAddress(address) {
  const config = getConfig();
  const pattern = new RegExp(config.validationPatterns.ethereumAddress);
  return pattern.test(address);
}

/**
 * Get Ethereum address validation pattern (for backward compatibility).
 * @returns {RegExp} Ethereum address validation pattern
 */
function getEthereumAddressPattern() {
  const config = getConfig();
  return new RegExp(config.validationPatterns.ethereumAddress);
}

// Lazy-loaded pattern for backward compatibility
let _ethereumAddressPattern = null;
Object.defineProperty(exports, 'ETHEREUM_ADDRESS_PATTERN', {
  get: function() {
    if (!_ethereumAddressPattern) {
      _ethereumAddressPattern = getEthereumAddressPattern();
    }
    return _ethereumAddressPattern;
  }
});

/**
 * Load shared configuration from JSON file.
 * @param {string} [configPath] - Path to config file. If null, uses default location.
 * @returns {object} Configuration data
 * @throws {Error} If config file doesn't exist or contains invalid JSON
 */
function loadConfig(configPath = null) {
  if (!configPath) {
    // Try to load etherscan-api-config.json first, fall back to example
    const configFile = path.join(__dirname, 'etherscan-api-config.json');
    const exampleFile = path.join(__dirname, 'etherscan-api-config.example.json');
    
    if (fs.existsSync(configFile)) {
      configPath = configFile;
    } else {
      configPath = exampleFile;
    }
  }
  
  try {
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    // Update cached config
    _config = config;
    return config;
  } catch (err) {
    if (err.code === 'ENOENT') {
      throw new Error(
        `Configuration file not found: ${configPath}\n` +
        'Please ensure etherscan-api-config.json or etherscan-api-config.example.json exists in the script directory.'
      );
    } else if (err instanceof SyntaxError) {
      throw new Error(`Invalid JSON in configuration file: ${configPath}\n${err.message}`);
    }
    throw err;
  }
}

/**
 * Build API request parameters from config and user inputs.
 * @param {object} config - Shared configuration
 * @param {string} address - Ethereum address to query
 * @param {string} apiKey - Etherscan API key
 * @param {number} [chainId] - Chain ID
 * @param {number} [page] - Page number
 * @param {number} [offset] - Results per page
 * @returns {object} API request parameters
 */
function buildApiParams(config, address, apiKey, chainId = null, page = null, offset = null) {
  return {
    chainid: chainId || config.defaultChainId,
    module: config.module,
    action: config.action,
    address: address,
    page: page || config.defaultPage,
    offset: offset || config.defaultOffset,
    apikey: apiKey
  };
}

/**
 * Build full API URL with parameters.
 * @param {object} config - Shared configuration
 * @param {object} params - API request parameters
 * @returns {string} Full API URL
 */
function buildApiUrl(config, params) {
  const url = new URL(config.apiBaseUrl);
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.append(key, value);
  });
  return url.toString();
}

/**
 * Format token balance data for display.
 * @param {object} tokenData - Token data from API response
 * @returns {string} Formatted token information
 */
function formatTokenBalance(tokenData) {
  const lines = [];
  lines.push(`  Token: ${tokenData.TokenName || 'Unknown'}`);
  lines.push(`  Symbol: ${tokenData.TokenSymbol || 'N/A'}`);
  lines.push(`  Address: ${tokenData.TokenAddress || 'N/A'}`);
  lines.push(`  Quantity: ${tokenData.TokenQuantity || '0'}`);
  lines.push(`  Divisor: ${tokenData.TokenDivisor || '18'}`);
  return lines.join('\n');
}

/**
 * Check if API response indicates success.
 * @param {object} response - API response data
 * @returns {boolean} True if successful, false otherwise
 */
function isResponseSuccessful(response) {
  return response && response.status === "1";
}

/**
 * Format API response output based on options.
 * @param {object} response - API response data
 * @param {object} options - Formatting options (e.g., {pretty: true})
 * @returns {string} Formatted output string
 */
function formatResponse(response, options = {}) {
  const indent = options.pretty ? 2 : undefined;
  return JSON.stringify(response, null, indent);
}

module.exports = {
  validateEthereumAddress,
  loadConfig,
  loadMessages,
  buildApiParams,
  buildApiUrl,
  formatTokenBalance,
  isResponseSuccessful,
  formatResponse,
  ETHEREUM_ADDRESS_PATTERN
};
