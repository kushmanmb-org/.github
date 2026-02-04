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
    const configPath = path.join(__dirname, 'etherscan-api-config.json');
    const configData = fs.readFileSync(configPath, 'utf8');
    _config = JSON.parse(configData);
  }
  return _config;
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

// Export pattern for backward compatibility
const ETHEREUM_ADDRESS_PATTERN = new RegExp(getConfig().validationPatterns.ethereumAddress);

/**
 * Load shared configuration from JSON file.
 * @param {string} [configPath] - Path to config file. If null, uses default location.
 * @returns {object} Configuration data
 * @throws {Error} If config file doesn't exist or contains invalid JSON
 */
function loadConfig(configPath = null) {
  if (!configPath) {
    configPath = path.join(__dirname, 'etherscan-api-config.json');
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
        'Please ensure etherscan-api-config.json exists in the script directory.'
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

module.exports = {
  validateEthereumAddress,
  loadConfig,
  buildApiParams,
  buildApiUrl,
  formatTokenBalance,
  ETHEREUM_ADDRESS_PATTERN
};
