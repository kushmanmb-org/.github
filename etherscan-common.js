/**
 * Shared validation and utility functions for Etherscan token balance queries.
 * This module provides common functionality used across multiple implementations.
 */

const fs = require('fs');
const path = require('path');

// Ethereum address validation pattern
const ETHEREUM_ADDRESS_PATTERN = /^0x[a-fA-F0-9]{40}$/;

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
  return ETHEREUM_ADDRESS_PATTERN.test(address);
}

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
    return JSON.parse(configData);
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
  // Use URLSearchParams constructor for efficiency
  const searchParams = new URLSearchParams(params);
  url.search = searchParams.toString();
  return url.toString();
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
  isResponseSuccessful,
  formatResponse,
  ETHEREUM_ADDRESS_PATTERN
};
