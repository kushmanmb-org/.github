/**
 * Shared validation and utility functions for Etherscan token balance queries.
 * This module provides common functionality used across multiple implementations.
 */

const fs = require('fs');
const path = require('path');

// Ethereum address validation pattern
const ETHEREUM_ADDRESS_PATTERN = /^0x[a-fA-F0-9]{40}$/;

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
 */
function loadConfig(configPath = null) {
  if (!configPath) {
    configPath = path.join(__dirname, 'etherscan-api-config.json');
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
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

module.exports = {
  validateEthereumAddress,
  loadConfig,
  buildApiParams,
  buildApiUrl,
  ETHEREUM_ADDRESS_PATTERN
};
