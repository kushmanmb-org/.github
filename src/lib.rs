use std::path::PathBuf;
use std::fs;
use std::error::Error;
use serde::{Deserialize, Serialize};

// Type definitions compatible with SP1 SDK
// These are simplified versions that match the SP1 SDK interface

/// SP1 Proof with public values
/// This is a simplified version compatible with SP1 SDK's SP1ProofWithPublicValues
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SP1ProofWithPublicValues {
    /// The proof bytes
    pub proof: Vec<u8>,
    /// The public values/inputs
    pub public_values: Vec<u8>,
}

/// SP1 Verifying Key
/// This is a simplified version compatible with SP1 SDK's SP1VerifyingKey
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SP1VerifyingKey {
    /// The verifying key bytes
    pub vk: Vec<u8>,
}

/// Proof system types supported by SP1
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum ProofSystem {
    /// Plonk proof system
    Plonk,
    /// Groth16 proof system
    Groth16,
    /// STARK proof system
    STARK,
}

/// Proof fixture structure for serialization
#[derive(Debug, Serialize, Deserialize)]
pub struct ProofFixture {
    /// The proof data with public values
    pub proof: Vec<u8>,
    /// The public values
    pub public_values: Vec<u8>,
    /// The verifying key
    pub vk: Vec<u8>,
    /// The proof system used
    pub system: ProofSystem,
}

/// Creates a proof fixture file from SP1 proof data
///
/// # Arguments
///
/// * `proof` - The SP1 proof with public values
/// * `vk` - The SP1 verifying key
/// * `system` - The proof system used (Plonk, Groth16, or Stark)
///
/// # Returns
///
/// Returns `Ok(())` on success, or an error if the fixture cannot be created
///
/// # Errors
///
/// This function will return an error if:
/// * The fixture directory cannot be created
/// * The proof data cannot be serialized
/// * The file cannot be written
///
/// # Example
///
/// ```
/// use proof_fixture_utils::{create_proof_fixture, ProofSystem, SP1ProofWithPublicValues, SP1VerifyingKey};
/// use std::error::Error;
///
/// fn example() -> Result<(), Box<dyn Error>> {
///     let proof = SP1ProofWithPublicValues {
///         proof: vec![1, 2, 3, 4],
///         public_values: vec![5, 6, 7, 8],
///     };
///     let vk = SP1VerifyingKey {
///         vk: vec![9, 10, 11, 12],
///     };
///     create_proof_fixture(&proof, &vk, ProofSystem::Plonk)?;
///     Ok(())
/// }
/// ```
pub fn create_proof_fixture(
    proof: &SP1ProofWithPublicValues,
    vk: &SP1VerifyingKey,
    system: ProofSystem,
) -> Result<(), Box<dyn Error>> {
    // Create fixtures directory if it doesn't exist
    let fixtures_dir = PathBuf::from("fixtures");
    fs::create_dir_all(&fixtures_dir)?;

    // Create the fixture structure
    // Note: We use the raw Vec<u8> values directly since they're already in binary format
    let fixture = ProofFixture {
        proof: proof.proof.clone(),
        public_values: proof.public_values.clone(),
        vk: vk.vk.clone(),
        system,
    };

    // Generate filename based on proof system
    let filename = match system {
        ProofSystem::Plonk => "proof_fixture_plonk.json",
        ProofSystem::Groth16 => "proof_fixture_groth16.json",
        ProofSystem::STARK => "proof_fixture_STARK.json",
    };

    let fixture_path = fixtures_dir.join(filename);

    // Serialize to JSON and write to file
    let json = serde_json::to_string_pretty(&fixture)?;
    fs::write(&fixture_path, json)?;

    println!("Proof fixture created at: {}", fixture_path.display());

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_proof_system_serialization() {
        let systems = vec![
            ProofSystem::Plonk,
            ProofSystem::Groth16,
            ProofSystem::STARK,
        ];

        for system in systems {
            let json = serde_json::to_string(&system).unwrap();
            let deserialized: ProofSystem = serde_json::from_str(&json).unwrap();
            assert_eq!(system, deserialized);
        }
    }

    #[test]
    fn test_proof_fixture_structure() {
        let fixture = ProofFixture {
            proof: vec![1, 2, 3],
            public_values: vec![4, 5, 6],
            vk: vec![7, 8, 9],
            system: ProofSystem::Plonk,
        };

        let json = serde_json::to_string(&fixture).unwrap();
        let deserialized: ProofFixture = serde_json::from_str(&json).unwrap();

        assert_eq!(fixture.proof, deserialized.proof);
        assert_eq!(fixture.public_values, deserialized.public_values);
        assert_eq!(fixture.vk, deserialized.vk);
        assert_eq!(fixture.system, deserialized.system);
    }
}
