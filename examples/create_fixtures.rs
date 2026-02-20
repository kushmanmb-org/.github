// Example usage of the create_proof_fixture function
// This demonstrates how to create proof fixtures for different proof systems

use proof_fixture_utils::{create_proof_fixture, ProofSystem, SP1ProofWithPublicValues, SP1VerifyingKey};
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    println!("SP1 Proof Fixture Generator Example");
    println!("====================================\n");

    // Create example proof data
    // In a real scenario, these would come from the SP1 prover
    let proof = SP1ProofWithPublicValues {
        proof: vec![1, 2, 3, 4, 5, 6, 7, 8], // Example proof bytes
        public_values: vec![42, 100, 200], // Example public values
    };

    let vk = SP1VerifyingKey {
        vk: vec![9, 10, 11, 12, 13, 14, 15, 16], // Example verifying key
    };

    // Generate fixtures for different proof systems
    println!("Generating Plonk proof fixture...");
    create_proof_fixture(&proof, &vk, ProofSystem::Plonk)?;
    println!("✓ Plonk fixture created\n");

    println!("Generating Groth16 proof fixture...");
    create_proof_fixture(&proof, &vk, ProofSystem::Groth16)?;
    println!("✓ Groth16 fixture created\n");

    println!("Generating STARK proof fixture...");
    create_proof_fixture(&proof, &vk, ProofSystem::STARK)?;
    println!("✓ STARK fixture created\n");

    println!("All fixture files created in the './fixtures' directory");
    println!("Each proof system has its own fixture file:");
    println!("  - fixtures/proof_fixture_plonk.json");
    println!("  - fixtures/proof_fixture_groth16.json");
    println!("  - fixtures/proof_fixture_STARK.json");

    println!("\nNote: In a real implementation, proof and vk would come from");
    println!("the SP1 SDK's ProverClient after generating actual zero-knowledge proofs.");

    Ok(())
}
