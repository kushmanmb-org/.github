/**
 * Verification Test Utilities
 * 
 * This module provides validation and verification functions for blockchain-related data,
 * including transaction hashes and ENS names. It mirrors the functionality of the Python
 * verification utilities (verify_tx_hash.py and verify_ens_creator.py) in JavaScript.
 * 
 * Security Considerations:
 * - Does not handle private keys or sensitive data
 * - Validates input formats to prevent injection attacks
 * - Provides comprehensive validation for blockchain addresses and transaction hashes
 */

/**
 * Transaction Hash Validator
 * Validates blockchain transaction hashes for Ethereum and Bitcoin formats.
 */
class TransactionHashValidator {
  // Ethereum transaction hash pattern (with 0x prefix)
  static ETH_TX_HASH_PATTERN = /^0x[0-9a-fA-F]{64}$/;
  
  // Bitcoin transaction hash pattern (without prefix)
  static BTC_TX_HASH_PATTERN = /^[0-9a-fA-F]{64}$/;
  
  // Null/zero transaction hash (Ethereum format)
  static NULL_TX_HASH_ETH = "0x0000000000000000000000000000000000000000000000000000000000000000";
  
  // Null/zero transaction hash (Bitcoin format)
  static NULL_TX_HASH_BTC = "0000000000000000000000000000000000000000000000000000000000000000";
  
  /**
   * Validate a transaction hash.
   * 
   * @param {string} txHash - The transaction hash to validate
   * @param {boolean} allowNull - Whether to allow null/zero hashes (default: true)
   * @returns {object} Validation results with format, validity, and normalized hash
   */
  static validateHash(txHash, allowNull = true) {
    if (!txHash || typeof txHash !== 'string') {
      return {
        valid: false,
        format: 'invalid',
        isNull: false,
        normalized: null,
        error: 'Transaction hash must be a non-empty string'
      };
    }
    
    const trimmedHash = txHash.trim();
    const isEthFormat = this.ETH_TX_HASH_PATTERN.test(trimmedHash);
    const isBtcFormat = this.BTC_TX_HASH_PATTERN.test(trimmedHash);
    
    // Check if it's a null hash
    const isNullHash = trimmedHash === this.NULL_TX_HASH_ETH || 
                       trimmedHash === this.NULL_TX_HASH_BTC ||
                       trimmedHash === this.NULL_TX_HASH_ETH.toLowerCase() ||
                       trimmedHash === this.NULL_TX_HASH_BTC.toLowerCase();
    
    if (isNullHash && !allowNull) {
      return {
        valid: false,
        format: isEthFormat ? 'ethereum' : 'bitcoin',
        isNull: true,
        normalized: trimmedHash.toLowerCase(),
        error: 'Null/zero transaction hash not allowed'
      };
    }
    
    if (isEthFormat) {
      return {
        valid: true,
        format: 'ethereum',
        isNull: isNullHash,
        normalized: trimmedHash.toLowerCase(),
        error: null
      };
    }
    
    if (isBtcFormat) {
      return {
        valid: true,
        format: 'bitcoin',
        isNull: isNullHash,
        normalized: trimmedHash.toLowerCase(),
        error: null
      };
    }
    
    return {
      valid: false,
      format: 'invalid',
      isNull: false,
      normalized: null,
      error: 'Invalid transaction hash format'
    };
  }
  
  /**
   * Normalize a transaction hash to lowercase.
   * 
   * @param {string} txHash - The transaction hash to normalize
   * @returns {string|null} Normalized hash or null if invalid
   */
  static normalizeHash(txHash) {
    const result = this.validateHash(txHash);
    return result.normalized;
  }
  
  /**
   * Check if a transaction hash is in Ethereum format.
   * 
   * @param {string} txHash - The transaction hash to check
   * @returns {boolean} True if Ethereum format, false otherwise
   */
  static isEthereumFormat(txHash) {
    return this.ETH_TX_HASH_PATTERN.test(txHash);
  }
  
  /**
   * Check if a transaction hash is in Bitcoin format.
   * 
   * @param {string} txHash - The transaction hash to check
   * @returns {boolean} True if Bitcoin format, false otherwise
   */
  static isBitcoinFormat(txHash) {
    return this.BTC_TX_HASH_PATTERN.test(txHash);
  }
}

/**
 * ENS Verifier
 * Validates and verifies ENS names on Base network.
 */
class ENSVerifier {
  // Base network configuration
  static BASE_CHAIN_ID = 8453;
  static BASE_RPC_URL = "https://mainnet.base.org";
  
  // Base ENS registry contracts
  static BASE_REGISTRAR_CONTROLLER = "0x4cCb0BB02FCABA27e82a56646E81d8c5bC4119a5";
  static BASE_REGISTRY = "0x6533C94869D28fAA8dF77cc63f9e2b2D6Cf77eBA";
  
  // ENS name pattern (name.base.eth)
  static ENS_NAME_PATTERN = /^[a-z0-9-]+\.base\.eth$/;
  
  /**
   * Initialize ENS verifier with the name to verify.
   * 
   * @param {string} ensName - The ENS name to verify (e.g., kushmanmb.base.eth)
   */
  constructor(ensName) {
    this.ensName = ensName.toLowerCase(); // ENS names are case-insensitive
    this.baseName = this.extractBaseName(this.ensName);
  }
  
  /**
   * Extract the base name from the full ENS name.
   * 
   * @param {string} ensName - Full ENS name (e.g., kushmanmb.base.eth)
   * @returns {string} Base name without .base.eth suffix
   */
  extractBaseName(ensName) {
    if (ensName.endsWith('.base.eth')) {
      return ensName.replace('.base.eth', '');
    }
    return ensName;
  }
  
  /**
   * Validate ENS name format.
   * 
   * @returns {object} Validation results
   */
  validateFormat() {
    const isValid = ENSVerifier.ENS_NAME_PATTERN.test(this.ensName);
    
    return {
      valid: isValid,
      name: this.ensName,
      baseName: this.baseName,
      chainId: ENSVerifier.BASE_CHAIN_ID,
      error: isValid ? null : 'Invalid ENS name format. Expected format: name.base.eth'
    };
  }
  
  /**
   * Static method to validate ENS name format without instantiation.
   * 
   * @param {string} ensName - ENS name to validate
   * @returns {boolean} True if valid format, false otherwise
   */
  static isValidFormat(ensName) {
    if (!ensName || typeof ensName !== 'string') {
      return false;
    }
    return this.ENS_NAME_PATTERN.test(ensName.toLowerCase());
  }
  
  /**
   * Get verification information for the ENS name.
   * 
   * @returns {object} Verification information including contract addresses
   */
  getVerificationInfo() {
    const formatValidation = this.validateFormat();
    
    return {
      ...formatValidation,
      network: 'Base Mainnet',
      rpcUrl: ENSVerifier.BASE_RPC_URL,
      registrarController: ENSVerifier.BASE_REGISTRAR_CONTROLLER,
      registry: ENSVerifier.BASE_REGISTRY
    };
  }
}

module.exports = {
  TransactionHashValidator,
  ENSVerifier
};
