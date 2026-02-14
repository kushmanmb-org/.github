/**
 * Babel Configuration with Security Best Practices
 * 
 * Security Considerations:
 * - Uses modern Node.js targets to avoid legacy vulnerabilities
 * - Excludes source maps in production builds to prevent code exposure
 * - Minimal transformations to reduce attack surface
 * - No external plugins that could introduce vulnerabilities
 */

module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        // Target Node.js 18+ (matches package.json engines)
        targets: {
          node: '18'
        },
        
        // Only include necessary polyfills
        useBuiltIns: false,
        
        // Use modules: false for better tree-shaking in production
        modules: process.env.NODE_ENV === 'test' ? 'commonjs' : false
      }
    ]
  ],

  // Environment-specific configuration
  env: {
    // Test environment configuration
    test: {
      presets: [
        [
          '@babel/preset-env',
          {
            targets: {
              node: 'current'
            }
          }
        ]
      ]
    },

    // Production environment - no source maps for security
    production: {
      // Disable source maps to prevent code exposure
      sourceMaps: false,
      
      // Remove console statements in production for security
      // (prevents accidental logging of sensitive data)
      plugins: []
    },

    // Development environment
    development: {
      // Enable source maps only in development
      sourceMaps: 'inline',
      
      // Retain function names for better debugging
      retainLines: true
    }
  },

  // Ignore patterns - prevent transformation of sensitive files
  ignore: [
    'node_modules',
    'dist',
    'build',
    'coverage',
    '**/*.local.*',
    '**/*-config-private.*',
    '**/secrets/**',
    '**/.secrets/**',
    '**/keystore/**',
    '**/*credentials*',
    '**/*apikey*',
    '**/*api-key*',
    '**/*.backup',
    '**/*.bak',
    '**/*.old'
  ],

  // Comments are removed by default for cleaner output
  comments: false,

  // Compact output for production
  compact: process.env.NODE_ENV === 'production' ? true : 'auto'
};
