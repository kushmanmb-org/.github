# Proof Fixture Utils

A Rust utility library for creating and managing SP1 (Succinct Proof 1) proof fixtures.

## Overview

This library provides functionality to create proof fixture files from SP1 proof data. These fixtures can be used for testing, verification, and integration with SP1 zero-knowledge proof systems.

## Features

- Support for multiple proof systems (Plonk, Groth16, STARK)
- Serialization of proof data, public values, and verifying keys
- JSON-based fixture format for easy inspection and portability
- Comprehensive error handling

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
proof-fixture-utils = "0.1.0"
```

## Usage

```rust
use proof_fixture_utils::{create_proof_fixture, ProofSystem, SP1ProofWithPublicValues, SP1VerifyingKey};
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    // Create proof data structures
    // In a real implementation, these would come from the SP1 SDK's ProverClient
    let proof = SP1ProofWithPublicValues {
        proof: vec![1, 2, 3, 4, 5, 6, 7, 8],
        public_values: vec![42, 100, 200],
    };
    
    let vk = SP1VerifyingKey {
        vk: vec![9, 10, 11, 12, 13, 14, 15, 16],
    };
    
    // Create a Plonk proof fixture
    create_proof_fixture(&proof, &vk, ProofSystem::Plonk)?;
    
    // Create a Groth16 proof fixture
    create_proof_fixture(&proof, &vk, ProofSystem::Groth16)?;
    
    // Create a STARK proof fixture
    create_proof_fixture(&proof, &vk, ProofSystem::STARK)?;
    
    Ok(())
}
```

## Function Reference

### `create_proof_fixture`

Creates a proof fixture file from SP1 proof data.

**Signature:**
```rust
pub fn create_proof_fixture(
    proof: &SP1ProofWithPublicValues,
    vk: &SP1VerifyingKey,
    system: ProofSystem,
) -> Result<(), Box<dyn Error>>
```

**Parameters:**
- `proof`: The SP1 proof with public values
- `vk`: The SP1 verifying key
- `system`: The proof system used (Plonk, Groth16, or Stark)

**Returns:**
- `Ok(())` on success
- `Err(Box<dyn Error>)` if the fixture cannot be created

**Errors:**
This function will return an error if:
- The fixture directory cannot be created
- The proof data cannot be serialized
- The file cannot be written

### `ProofSystem` Enum

Represents the supported proof systems:
- `ProofSystem::Plonk` - Plonk proof system
- `ProofSystem::Groth16` - Groth16 proof system
- `ProofSystem::STARK` - STARK proof system

### `ProofFixture` Structure

The fixture data structure that gets serialized to JSON:
```rust
pub struct ProofFixture {
    pub proof: Vec<u8>,
    pub public_values: Vec<u8>,
    pub vk: Vec<u8>,
    pub system: ProofSystem,
}
```

## Output

Fixture files are created in the `fixtures/` directory with the following naming convention:
- `proof_fixture_plonk.json` - For Plonk proofs
- `proof_fixture_groth16.json` - For Groth16 proofs
- `proof_fixture_STARK.json` - For STARK proofs

Each file contains JSON-formatted proof data that can be easily inspected or loaded for testing.

## Example

See `examples/create_fixtures.rs` for a complete example of how to use this library.

To run the example:
```bash
cargo run --example create_fixtures
```

## Testing

Run the test suite:
```bash
cargo test
```

## Dependencies

- `serde` - Serialization framework
- `serde_json` - JSON serialization
- `bincode` - Binary serialization

Note: This library defines its own simplified types (`SP1ProofWithPublicValues`, `SP1VerifyingKey`) that are compatible with the SP1 SDK interface but don't require the full SP1 SDK as a dependency. This makes the library lightweight and easy to build.

## Security Considerations

- Proof fixtures may contain sensitive data depending on your use case
- Consider adding `fixtures/` directory to `.gitignore` if fixtures contain private information
- Verify proof data integrity before using fixtures in production

## License

See the repository root for license information.

## Contributing

Contributions are welcome! Please see the repository's CONTRIBUTING.md for guidelines.
