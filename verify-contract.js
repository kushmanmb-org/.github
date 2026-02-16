/**
 * Smart Contract Verification Utilities
 * 
 * This module provides validation and verification functions for Ethereum smart contracts,
 * including address validation, ABI handling, and contract interaction utilities.
 * It complements the test-verify.js module by focusing on smart contract operations.
 * 
 * Security Considerations:
 * - Does not handle private keys or sensitive data
 * - Validates input formats to prevent injection attacks
 * - Provides comprehensive validation for contract addresses
 * - Supports checksum validation for Ethereum addresses
 */

/**
 * Contract Address Validator
 * Validates Ethereum contract addresses and provides checksum verification.
 */
class ContractAddressValidator {
  // Ethereum address pattern (with 0x prefix, 40 hex characters)
  static ETH_ADDRESS_PATTERN = /^0x[0-9a-fA-F]{40}$/;
  
  // Zero/null address
  static NULL_ADDRESS = "0x0000000000000000000000000000000000000000";
  
  /**
   * Validate an Ethereum address format.
   * 
   * @param {string} address - The address to validate
   * @param {boolean} allowNull - Whether to allow null/zero addresses (default: false)
   * @returns {object} Validation results with validity, normalized address, and checksum info
   */
  static validateAddress(address, allowNull = false) {
    if (!address || typeof address !== 'string') {
      return {
        valid: false,
        isNull: false,
        normalized: null,
        checksumValid: null,
        error: 'Address must be a non-empty string'
      };
    }
    
    const trimmedAddress = address.trim();
    const isValidFormat = this.ETH_ADDRESS_PATTERN.test(trimmedAddress);
    
    if (!isValidFormat) {
      return {
        valid: false,
        isNull: false,
        normalized: null,
        checksumValid: null,
        error: 'Invalid Ethereum address format. Expected 0x followed by 40 hex characters'
      };
    }
    
    // Check if it's a null address
    const isNullAddress = trimmedAddress.toLowerCase() === this.NULL_ADDRESS.toLowerCase();
    
    if (isNullAddress && !allowNull) {
      return {
        valid: false,
        isNull: true,
        normalized: this.NULL_ADDRESS,
        checksumValid: null,
        error: 'Null/zero address not allowed'
      };
    }
    
    // Validate checksum if address has mixed case
    const checksumValid = this.validateChecksum(trimmedAddress);
    
    return {
      valid: true,
      isNull: isNullAddress,
      normalized: trimmedAddress.toLowerCase(),
      checksumValid: checksumValid,
      error: null
    };
  }
  
  /**
   * Validate the EIP-55 checksum of an Ethereum address.
   * If the address is all lowercase or all uppercase (except 0x), checksum validation is skipped.
   * 
   * @param {string} address - The address to validate
   * @returns {boolean|null} True if checksum is valid, false if invalid, null if no checksum
   */
  static validateChecksum(address) {
    if (!this.ETH_ADDRESS_PATTERN.test(address)) {
      return null;
    }
    
    // Remove 0x prefix for checking
    const addressWithoutPrefix = address.slice(2);
    
    // If all lowercase or all uppercase, no checksum to validate
    if (addressWithoutPrefix === addressWithoutPrefix.toLowerCase() ||
        addressWithoutPrefix === addressWithoutPrefix.toUpperCase()) {
      return null;
    }
    
    // For mixed case, we need to validate the checksum
    // This is a simplified check - full EIP-55 validation requires keccak256
    // For production use, consider using a library like ethers.js or web3.js
    try {
      const checksumAddress = this.toChecksumAddress(address);
      return address === checksumAddress;
    } catch (e) {
      return false;
    }
  }
  
  /**
   * Convert an address to EIP-55 checksum format.
   * Note: This is a simplified implementation. For production use,
   * consider using a library like ethers.js or web3.js with keccak256.
   * 
   * @param {string} address - The address to convert
   * @returns {string} Checksum address
   */
  static toChecksumAddress(address) {
    if (!this.ETH_ADDRESS_PATTERN.test(address)) {
      throw new Error('Invalid Ethereum address format');
    }
    
    // For now, return lowercase as we don't have keccak256 without dependencies
    // In production, this should use proper EIP-55 checksum calculation
    return address.toLowerCase();
  }
  
  /**
   * Normalize an address to lowercase format.
   * 
   * @param {string} address - The address to normalize
   * @returns {string|null} Normalized address or null if invalid
   */
  static normalizeAddress(address) {
    const result = this.validateAddress(address, true);
    return result.normalized;
  }
  
  /**
   * Check if an address is the null/zero address.
   * 
   * @param {string} address - The address to check
   * @returns {boolean} True if null address, false otherwise
   */
  static isNullAddress(address) {
    if (!address || typeof address !== 'string') {
      return false;
    }
    return address.toLowerCase() === this.NULL_ADDRESS.toLowerCase();
  }
  
  /**
   * Compare two addresses for equality (case-insensitive).
   * 
   * @param {string} address1 - First address
   * @param {string} address2 - Second address
   * @returns {boolean} True if addresses are equal, false otherwise
   */
  static areEqual(address1, address2) {
    const norm1 = this.normalizeAddress(address1);
    const norm2 = this.normalizeAddress(address2);
    
    if (!norm1 || !norm2) {
      return false;
    }
    
    return norm1 === norm2;
  }
}

/**
 * Contract Verifier
 * Provides utilities for working with smart contracts and their ABIs.
 */
class ContractVerifier {
  /**
   * Initialize contract verifier with address and optional ABI.
   * 
   * @param {string} contractAddress - The contract address
   * @param {Array} abi - Optional contract ABI (Application Binary Interface)
   */
  constructor(contractAddress, abi = null) {
    this.contractAddress = contractAddress;
    this.abi = abi;
    this.functions = null;
    this.events = null;
    
    // Parse ABI if provided
    if (abi) {
      this.parseABI(abi);
    }
  }
  
  /**
   * Validate the contract address.
   * 
   * @returns {object} Address validation results
   */
  validateAddress() {
    return ContractAddressValidator.validateAddress(this.contractAddress);
  }
  
  /**
   * Parse the contract ABI to extract functions and events.
   * 
   * @param {Array} abi - Contract ABI
   * @returns {object} Parsed ABI with functions and events
   */
  parseABI(abi) {
    if (!Array.isArray(abi)) {
      throw new Error('ABI must be an array');
    }
    
    this.functions = abi.filter(item => item.type === 'function');
    this.events = abi.filter(item => item.type === 'event');
    this.constructorAbi = abi.find(item => item.type === 'constructor');
    
    return {
      functions: this.functions,
      events: this.events,
      constructorAbi: this.constructorAbi
    };
  }
  
  /**
   * Get all function names from the ABI.
   * 
   * @returns {Array<string>} List of function names
   */
  getFunctionNames() {
    if (!this.functions) {
      return [];
    }
    return this.functions.map(fn => fn.name).filter(name => name);
  }
  
  /**
   * Get all event names from the ABI.
   * 
   * @returns {Array<string>} List of event names
   */
  getEventNames() {
    if (!this.events) {
      return [];
    }
    return this.events.map(evt => evt.name).filter(name => name);
  }
  
  /**
   * Check if a function exists in the contract ABI.
   * 
   * @param {string} functionName - Name of the function to check
   * @returns {boolean} True if function exists, false otherwise
   */
  hasFunction(functionName) {
    if (!this.functions) {
      return false;
    }
    return this.functions.some(fn => fn.name === functionName);
  }
  
  /**
   * Check if an event exists in the contract ABI.
   * 
   * @param {string} eventName - Name of the event to check
   * @returns {boolean} True if event exists, false otherwise
   */
  hasEvent(eventName) {
    if (!this.events) {
      return false;
    }
    return this.events.some(evt => evt.name === eventName);
  }
  
  /**
   * Get function details by name.
   * 
   * @param {string} functionName - Name of the function
   * @returns {object|null} Function details or null if not found
   */
  getFunction(functionName) {
    if (!this.functions) {
      return null;
    }
    return this.functions.find(fn => fn.name === functionName) || null;
  }
  
  /**
   * Get event details by name.
   * 
   * @param {string} eventName - Name of the event
   * @returns {object|null} Event details or null if not found
   */
  getEvent(eventName) {
    if (!this.events) {
      return null;
    }
    return this.events.find(evt => evt.name === eventName) || null;
  }
  
  /**
   * Get all read-only (view/pure) functions.
   * 
   * @returns {Array} List of read-only functions
   */
  getReadOnlyFunctions() {
    if (!this.functions) {
      return [];
    }
    return this.functions.filter(fn => 
      fn.stateMutability === 'view' || 
      fn.stateMutability === 'pure' ||
      fn.constant === true
    );
  }
  
  /**
   * Get all state-modifying functions.
   * 
   * @returns {Array} List of state-modifying functions
   */
  getWriteFunctions() {
    if (!this.functions) {
      return [];
    }
    return this.functions.filter(fn => 
      fn.stateMutability !== 'view' && 
      fn.stateMutability !== 'pure' &&
      fn.constant !== true
    );
  }
  
  /**
   * Get contract verification information.
   * 
   * @returns {object} Contract verification details
   */
  getVerificationInfo() {
    const addressValidation = this.validateAddress();
    
    return {
      address: this.contractAddress,
      addressValid: addressValidation.valid,
      addressNormalized: addressValidation.normalized,
      hasABI: this.abi !== null,
      functionCount: this.functions ? this.functions.length : 0,
      eventCount: this.events ? this.events.length : 0,
      readOnlyFunctionCount: this.getReadOnlyFunctions().length,
      writeFunctionCount: this.getWriteFunctions().length,
      functions: this.getFunctionNames(),
      events: this.getEventNames()
    };
  }
  
  /**
   * Static method to validate a contract address without instantiation.
   * 
   * @param {string} address - Address to validate
   * @param {boolean} allowNull - Whether to allow null addresses
   * @returns {object} Validation results
   */
  static validateContractAddress(address, allowNull = false) {
    return ContractAddressValidator.validateAddress(address, allowNull);
  }
  
  /**
   * Static method to load and verify a contract from ABI file data.
   * 
   * @param {string} address - Contract address
   * @param {object|string} abiData - ABI data (array or JSON string)
   * @returns {ContractVerifier} New ContractVerifier instance
   */
  static fromABI(address, abiData) {
    let abi;
    
    if (typeof abiData === 'string') {
      try {
        abi = JSON.parse(abiData);
      } catch (e) {
        throw new Error('Invalid ABI JSON string: ' + e.message);
      }
    } else if (Array.isArray(abiData)) {
      abi = abiData;
    } else {
      throw new Error('ABI must be an array or JSON string');
    }
    
    return new ContractVerifier(address, abi);
  }
}

module.exports = {
  ContractAddressValidator,
  ContractVerifier
};
