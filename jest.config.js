/**
 * Jest Configuration with Security Best Practices
 * 
 * Security Considerations:
 * - Excludes sensitive directories (node_modules, secrets, keys, etc.)
 * - Prevents coverage collection on sensitive files
 * - Clears mocks between tests to prevent data leakage
 * - Configures safe test environment
 */

module.exports = {
  // Use Node.js test environment
  testEnvironment: 'node',

  // Automatically clear mock calls and instances between every test
  clearMocks: true,

  // Automatically restore mock state and implementation between every test
  restoreMocks: true,

  // Automatically reset mock state between every test
  resetMocks: true,

  // Test match patterns - look for test files
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js'
  ],

  // Files to exclude from testing
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/build/',
    '/coverage/',
    '/tmp/',
    '/temp/',
    '/.secrets/',
    '/secrets/',
    '/keystore/',
    '/deployments/',
    '/chaindata/',
    '/.git/',
    '\\.backup$',
    '\\.bak$',
    '\\.old$',
    '\\.local\\.',
    'example\\.json$'
  ],

  // Coverage collection settings
  collectCoverageFrom: [
    '**/*.js',
    '!**/node_modules/**',
    '!**/dist/**',
    '!**/build/**',
    '!**/coverage/**',
    '!**/tmp/**',
    '!**/temp/**',
    '!**/.secrets/**',
    '!**/secrets/**',
    '!**/keystore/**',
    '!**/deployments/**',
    '!**/*.config.js',
    '!**/*.local.*',
    '!**/*-config-private.*',
    '!**/*credentials*',
    '!**/*apikey*',
    '!**/*api-key*',
    '!**/*.example.*',
    '!**/examples/**',
    '!jest.config.js',
    '!babel.config.js'
  ],

  // Coverage directory - add to .gitignore
  coverageDirectory: 'coverage',

  // Coverage reporters
  coverageReporters: [
    'text',
    'lcov',
    'html'
  ],

  // Transform files using babel-jest
  transform: {
    '^.+\\.js$': 'babel-jest'
  },

  // Module file extensions
  moduleFileExtensions: [
    'js',
    'json'
  ],

  // Setup files to run before tests
  // setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // Global test timeout (30 seconds) - prevents long-running tests
  testTimeout: 30000,

  // Verbose output for better debugging
  verbose: true,

  // Prevent tests from being run in parallel if they might interfere
  // maxWorkers: 1,

  // Force exit after tests complete
  forceExit: true,

  // Detect open handles and warn about them
  detectOpenHandles: true
};
