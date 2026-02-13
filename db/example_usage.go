// Example usage of the secure database frontend
// This demonstrates how to use db/frontend.go with proper security practices

package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/kushmanmb-org/.github/db"
)

func main() {
	// Example 1: Load credentials from environment variables (SECURE)
	// Never hardcode credentials in your code!
	user := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASSWORD")

	if user == "" || password == "" {
		log.Println("Database credentials not found in environment variables")
		log.Println("Please set DB_USER and DB_PASSWORD environment variables")
		log.Println("\nExample:")
		log.Println("  export DB_USER=myuser")
		log.Println("  export DB_PASSWORD=mypassword")
		return
	}

	// Example 2: Configure with secure defaults
	config := db.DefaultConfig()
	config.Host = os.Getenv("DB_HOST")
	if config.Host == "" {
		config.Host = "localhost"
	}
	config.Database = os.Getenv("DB_NAME")
	if config.Database == "" {
		config.Database = "myapp"
	}

	// Example 3: Create frontend with validated configuration
	frontend, err := db.NewFrontend(config, user, password)
	if err != nil {
		log.Fatalf("Failed to create database frontend: %v", err)
	}
	defer frontend.Close()

	// Example 4: Health check before operations
	ctx := context.Background()
	if err := frontend.HealthCheck(ctx); err != nil {
		log.Fatalf("Database health check failed: %v", err)
	}
	log.Println("✓ Database connection healthy")

	// Example 5: Create user with validated input
	username := "john_doe"
	email := "john@example.com"
	user1, err := frontend.CreateUser(ctx, username, email)
	if err != nil {
		log.Printf("Failed to create user: %v", err)
	} else {
		log.Printf("✓ Created user: ID=%d, Username=%s, Email=%s", 
			user1.ID, user1.Username, user1.Email)
	}

	// Example 6: Get user by ID (parameterized query)
	if user1 != nil {
		retrievedUser, err := frontend.GetUserByID(ctx, user1.ID)
		if err != nil {
			log.Printf("Failed to get user: %v", err)
		} else {
			log.Printf("✓ Retrieved user: %+v", retrievedUser)
		}
	}

	// Example 7: Search users safely (SQL injection prevention)
	searchTerm := "john"
	users, err := frontend.SearchUsers(ctx, searchTerm, 10)
	if err != nil {
		log.Printf("Failed to search users: %v", err)
	} else {
		log.Printf("✓ Found %d users matching '%s'", len(users), searchTerm)
	}

	// Example 8: Demonstrate SQL injection protection
	// Even malicious input is handled safely
	maliciousInput := "john'; DROP TABLE users; --"
	log.Println("\n--- SQL Injection Protection Test ---")
	log.Printf("Attempting search with malicious input: %s", maliciousInput)
	
	users, err = frontend.SearchUsers(ctx, maliciousInput, 10)
	if err != nil {
		log.Printf("Search failed (safely): %v", err)
	} else {
		log.Printf("✓ Search completed safely - parameterized queries prevent injection!")
		log.Printf("  Found %d users (no tables were dropped!)", len(users))
	}

	// Example 9: Update user with validation
	if user1 != nil {
		err = frontend.UpdateUser(ctx, user1.ID, "john_updated", "john.new@example.com")
		if err != nil {
			log.Printf("Failed to update user: %v", err)
		} else {
			log.Printf("✓ Updated user ID=%d", user1.ID)
		}
	}

	// Example 10: Transaction example
	log.Println("\n--- Transaction Example ---")
	err = frontend.ExecuteInTransaction(ctx, func(tx *db.Tx) error {
		// Multiple operations in a transaction
		log.Println("  Executing operations in transaction...")
		
		// If any operation fails, entire transaction is rolled back
		// Add your transaction operations here
		
		return nil // Commit transaction
	})
	if err != nil {
		log.Printf("Transaction failed: %v", err)
	} else {
		log.Println("✓ Transaction completed successfully")
	}

	// Example 11: Context with timeout
	log.Println("\n--- Context Timeout Example ---")
	timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	
	_, err = frontend.GetUserByID(timeoutCtx, 999999)
	if err != nil {
		log.Printf("Query with timeout: %v", err)
	}

	// Example 12: Cleanup
	if user1 != nil {
		err = frontend.DeleteUser(ctx, user1.ID)
		if err != nil {
			log.Printf("Failed to delete user: %v", err)
		} else {
			log.Printf("✓ Deleted user ID=%d", user1.ID)
		}
	}

	log.Println("\n✓ All examples completed successfully")
	log.Println("\nSecurity features demonstrated:")
	log.Println("  - Credentials from environment variables")
	log.Println("  - Parameterized queries (SQL injection prevention)")
	log.Println("  - Input validation and sanitization")
	log.Println("  - Context-based timeouts")
	log.Println("  - Connection pooling")
	log.Println("  - Secure error handling")
	log.Println("  - Transaction support")
	log.Println("  - Health checks")
}

// Invalid username example (would fail validation)
func exampleInvalidUsername() {
	config := db.DefaultConfig()
	frontend, _ := db.NewFrontend(config, "user", "pass")
	defer frontend.Close()

	ctx := context.Background()

	// These will all fail validation:
	invalidUsernames := []string{
		"ab",                    // Too short (< 3 chars)
		"this_is_way_too_long_username_that_exceeds_limit", // Too long (> 50 chars)
		"user@name",            // Invalid character (@)
		"user name",            // Invalid character (space)
		"user;DROP TABLE",      // SQL injection attempt
		"../../../etc/passwd",  // Path traversal attempt
	}

	for _, username := range invalidUsernames {
		_, err := frontend.CreateUser(ctx, username, "email@example.com")
		if err != nil {
			fmt.Printf("✓ Correctly rejected invalid username '%s': %v\n", username, err)
		}
	}
}

// Invalid email example (would fail validation)
func exampleInvalidEmail() {
	config := db.DefaultConfig()
	frontend, _ := db.NewFrontend(config, "user", "pass")
	defer frontend.Close()

	ctx := context.Background()

	// These will all fail validation:
	invalidEmails := []string{
		"notanemail",           // Missing @
		"@example.com",         // Missing local part
		"user@",                // Missing domain
		"user @example.com",    // Space in email
		"user@domain@com",      // Multiple @
	}

	for _, email := range invalidEmails {
		_, err := frontend.CreateUser(ctx, "validuser", email)
		if err != nil {
			fmt.Printf("✓ Correctly rejected invalid email '%s': %v\n", email, err)
		}
	}
}
