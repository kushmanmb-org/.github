# Code Structure and Implementation Notes

## Query Token Balance Scripts

This repository provides three implementations of the Etherscan token balance query functionality:

### Primary Implementation: Python (`query-token-balance.py`)
- **Status**: ✅ Canonical implementation
- **Features**: Full-featured with token formatting, validation, and comprehensive error handling
- **Recommended**: Use this version for production and as the reference implementation

### JavaScript Implementation (`query-token-balance.js`)
- **Status**: ⚠️ Compatibility layer
- **Purpose**: Provided for Node.js environments
- **Note**: Mirrors Python functionality but Python version has additional features

### Shell Script Implementation (`query-token-balance.sh`)
- **Status**: ⚠️ Compatibility layer  
- **Purpose**: Provided for shell scripting environments
- **Note**: Uses Python for validation and config loading; consider using Python directly

## Common Modules

### `etherscan_common.py` (Primary)
Full-featured utility module with:
- Configuration loading from JSON
- Message loading from JSON
- Ethereum address validation
- API parameter building
- API URL construction
- Response formatting
- Token balance formatting

### `etherscan-common.js` (Compatibility)
JavaScript version with core functionality:
- Configuration loading
- Message loading
- Address validation
- API parameter/URL building
- Response formatting

## Workflow Files

### Validation Workflows
The repository uses a reusable workflow pattern to reduce duplication:

- `reusable-validation.yml`: Base workflow template
- `json-validation.yml`: Uses reusable workflow
- `python-validation.yml`: Standalone (with language-specific setup)
- `shell-validation.yml`: Standalone (with ShellCheck)
- `markdown-validation.yml`: Standalone (with markdownlint)

## Reducing Duplication

The following steps have been taken to reduce code duplication:

1. ✅ **Removed redundant constants** in `query-token-balance.py` - all config values now come from shared config
2. ✅ **Added `build_api_url()`** to Python common module to match JavaScript version
3. ✅ **Created reusable workflow** template for validation workflows
4. ✅ **Refactored JSON validation** to use reusable workflow

## Recommendations for Future Refactoring

1. **Single Implementation**: Consider maintaining only the Python version as the primary implementation
2. **JavaScript Wrapper**: If Node.js support is needed, create a thin wrapper that calls the Python script
3. **Shell Wrapper**: The shell script could be simplified to just call the Python script
4. **Workflow Consolidation**: Python and Shell validation could potentially use the reusable workflow pattern with setup steps
