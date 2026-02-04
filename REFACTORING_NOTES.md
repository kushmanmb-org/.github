# Code Refactoring Documentation

## Overview

This document describes the refactoring work done to reduce code duplication across the Etherscan API query scripts and modules.

## Objectives

The primary goal was to identify and eliminate code duplication while maintaining:
- Feature parity across JavaScript, Python, and Shell implementations
- Consistent user experience across all three scripts
- Single source of truth for configuration and error messages
- Maintainability and ease of future updates

## Changes Made

### 1. Centralized Configuration

**File**: `etherscan-api-config.json`

All common configuration, help text, error messages, and validation patterns are now stored in a single JSON file:

```json
{
  "apiBaseUrl": "...",
  "defaultAddress": "...",
  "defaultChainId": 1,
  "helpText": { ... },
  "errorMessages": { ... },
  "validationPatterns": { ... }
}
```

**Benefits**:
- Single source of truth for all configuration
- Easy to update error messages and help text in one place
- Consistent messaging across all implementations
- No hardcoded strings scattered across multiple files

### 2. Environment Variable Support

**Before**: Only JavaScript script supported `ETHERSCAN_API_KEY` environment variable

**After**: All three scripts (JS, Python, Shell) now support the environment variable

**Usage**:
```bash
export ETHERSCAN_API_KEY="your-api-key"
./query-token-balance.sh --address 0x...
python3 query-token-balance.py --address 0x...
node query-token-balance.js --address 0x...
```

### 3. Standardized Error Messages

**Before**: Each script had its own hardcoded error messages with slight variations

**After**: All scripts use error messages from `etherscan-api-config.json`

**Standardized Messages**:
- `apiKeyRequired`: "Error: API key is required. Use --apikey option or set ETHERSCAN_API_KEY environment variable."
- `invalidAddress`: "Error: Invalid Ethereum address format"
- `invalidAddressFormat`: "Expected format: 0x followed by 40 hexadecimal characters"
- `apiRequestFailed`: "Error: Failed to connect to Etherscan API"

### 4. Module Feature Parity

#### JavaScript Module (`etherscan-common.js`)

**Added**:
- `formatTokenBalance(tokenData)` - Format token data for display

#### Python Module (`etherscan_common.py`)

**Added**:
- `build_api_url(config, params)` - Build complete API URL with query parameters

**Result**: Both modules now have identical functionality, just in different languages.

### 5. Shared Validation Pattern

**Before**: Ethereum address validation regex was duplicated in three places:
- `etherscan-common.js`: `/^0x[a-fA-F0-9]{40}$/`
- `etherscan_common.py`: `r'^0x[a-fA-F0-9]{40}$'`
- Both used the same pattern but maintained separately

**After**: Single validation pattern in config:
```json
{
  "validationPatterns": {
    "ethereumAddress": "^0x[a-fA-F0-9]{40}$"
  }
}
```

Both modules load and compile this pattern at runtime.

## Code Reduction Summary

### Eliminated Duplications

1. **Error Messages**: ~8 duplicated error messages → 1 shared config
2. **Help Text**: ~3 implementations → 1 shared config (partially used)
3. **Validation Pattern**: 2 hardcoded patterns → 1 config pattern
4. **Environment Variable Support**: Added to 2 scripts that were missing it

### Lines of Code Impact

- **Removed**: ~40 lines of duplicated code
- **Added**: ~35 lines of shared configuration and loader logic
- **Net Result**: More maintainable code with single source of truth

## Migration Guide

### For Developers

#### Using the Shared Config in New Scripts

**JavaScript**:
```javascript
const { loadConfig } = require('./etherscan-common.js');
const config = loadConfig();
console.log(config.errorMessages.apiKeyRequired);
```

**Python**:
```python
from etherscan_common import get_config
config = get_config()
print(config['errorMessages']['apiKeyRequired'])
```

**Shell**:
```bash
get_error_message() {
    python3 -c "from etherscan_common import get_config; print(get_config()['errorMessages']['$1'])"
}
get_error_message "apiKeyRequired"
```

#### Adding New Error Messages

1. Edit `etherscan-api-config.json`
2. Add new message under `errorMessages`:
```json
{
  "errorMessages": {
    "newError": "Your new error message here"
  }
}
```
3. Use in scripts:
   - JS: `config.errorMessages.newError`
   - Python: `config['errorMessages']['newError']`
   - Shell: `get_error_message "newError"`

## Testing

All scripts were tested to ensure:
- ✅ Help messages display correctly
- ✅ Error messages are consistent across all implementations
- ✅ Environment variable support works
- ✅ Address validation works with shared pattern
- ✅ Backward compatibility maintained

## Future Improvements

### Potential Next Steps

1. **Documentation Consolidation**: 
   - Move duplicate examples from `README.md` to `ETHERSCAN_TOKEN_BALANCE.md`
   - Reference detailed docs from README

2. **Workflow Templates**:
   - Create reusable GitHub Actions composite actions
   - Reduce boilerplate in workflow YAML files

3. **CLI Argument Handling**:
   - While we've standardized error messages and help text, the actual argument parsing logic is still duplicated
   - Could potentially create a shared CLI spec in JSON

4. **Additional Shared Functions**:
   - Response validation
   - Token data formatting standards
   - Logging utilities

## Conclusion

This refactoring significantly reduced code duplication while maintaining full backward compatibility. The codebase is now:
- **Easier to maintain**: Changes to error messages or config only need to be made once
- **More consistent**: All scripts behave identically from a user perspective
- **Better organized**: Clear separation between configuration and implementation
- **More testable**: Shared logic can be tested in one place

All three implementations (JavaScript, Python, Shell) now share a common foundation while preserving their language-specific strengths.
