// Package db provides secure database operations with industry-standard security practices.
//
// This implementation follows OWASP secure coding guidelines and includes:
// - SQL injection prevention through parameterized queries
// - Input validation and sanitization
// - Secure error handling
// - Connection pooling and resource management
// - Context-based timeouts
// - No hardcoded credentials
package db

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"
	"regexp"
	"strings"
	"time"
)

// Common errors
var (
	ErrInvalidInput     = errors.New("invalid input provided")
	ErrDatabaseError    = errors.New("database operation failed")
	ErrNotFound         = errors.New("record not found")
	ErrConnectionFailed = errors.New("database connection failed")
	ErrTimeout          = errors.New("operation timeout")
)

// Config holds database configuration with secure defaults
type Config struct {
	Host            string
	Port            int
	Database        string
	MaxConnections  int
	MaxIdleConns    int
	ConnMaxLifetime time.Duration
	QueryTimeout    time.Duration
}

// DefaultConfig returns secure default configuration
func DefaultConfig() *Config {
	return &Config{
		Host:            "localhost",
		Port:            5432,
		MaxConnections:  10,
		MaxIdleConns:    5,
		ConnMaxLifetime: time.Hour,
		QueryTimeout:    30 * time.Second,
	}
}

// Frontend provides secure database operations
type Frontend struct {
	db     *sql.DB
	config *Config
}

// NewFrontend creates a new database frontend with secure configuration.
// Credentials should be provided via environment variables, not hardcoded.
//
// Example usage:
//   user := os.Getenv("DB_USER")
//   password := os.Getenv("DB_PASSWORD")
//   frontend, err := NewFrontend(config, user, password)
func NewFrontend(config *Config, user, password string) (*Frontend, error) {
	if config == nil {
		config = DefaultConfig()
	}

	// Validate configuration
	if err := validateConfig(config); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	// Validate credentials (don't log them)
	if user == "" || password == "" {
		return nil, ErrInvalidInput
	}

	// Build connection string without exposing credentials in logs
	// Using PostgreSQL as example; adjust DSN format for your database
	dsn := fmt.Sprintf("host=%s port=%d dbname=%s user=%s password=%s sslmode=require",
		config.Host, config.Port, config.Database, user, password)

	// Open database connection
	db, err := sql.Open("postgres", dsn)
	if err != nil {
		// Don't expose connection details in error
		return nil, fmt.Errorf("%w: %v", ErrConnectionFailed, sanitizeError(err))
	}

	// Configure connection pool with secure defaults
	db.SetMaxOpenConns(config.MaxConnections)
	db.SetMaxIdleConns(config.MaxIdleConns)
	db.SetConnMaxLifetime(config.ConnMaxLifetime)

	// Verify connection
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := db.PingContext(ctx); err != nil {
		db.Close()
		return nil, fmt.Errorf("%w: %v", ErrConnectionFailed, sanitizeError(err))
	}

	return &Frontend{
		db:     db,
		config: config,
	}, nil
}

// Close closes the database connection
func (f *Frontend) Close() error {
	if f.db != nil {
		return f.db.Close()
	}
	return nil
}

// User represents a user record
type User struct {
	ID        int64
	Username  string
	Email     string
	CreatedAt time.Time
}

// GetUserByID retrieves a user by ID using parameterized query to prevent SQL injection
func (f *Frontend) GetUserByID(ctx context.Context, userID int64) (*User, error) {
	// Validate input
	if userID <= 0 {
		return nil, ErrInvalidInput
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(ctx, f.config.QueryTimeout)
	defer cancel()

	// Use parameterized query to prevent SQL injection
	query := `SELECT id, username, email, created_at FROM users WHERE id = $1`
	
	var user User
	err := f.db.QueryRowContext(ctx, query, userID).Scan(
		&user.ID,
		&user.Username,
		&user.Email,
		&user.CreatedAt,
	)

	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNotFound
		}
		// Sanitize error before returning
		return nil, fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	return &user, nil
}

// CreateUser creates a new user with validated input
func (f *Frontend) CreateUser(ctx context.Context, username, email string) (*User, error) {
	// Validate inputs
	if err := validateUsername(username); err != nil {
		return nil, err
	}
	if err := validateEmail(email); err != nil {
		return nil, err
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(ctx, f.config.QueryTimeout)
	defer cancel()

	// Use parameterized query to prevent SQL injection
	query := `INSERT INTO users (username, email, created_at) VALUES ($1, $2, $3) RETURNING id, created_at`
	
	var user User
	user.Username = username
	user.Email = email

	err := f.db.QueryRowContext(ctx, query, username, email, time.Now()).Scan(
		&user.ID,
		&user.CreatedAt,
	)

	if err != nil {
		// Check for duplicate entry without exposing internal details
		if strings.Contains(err.Error(), "duplicate") || strings.Contains(err.Error(), "unique") {
			return nil, fmt.Errorf("%w: username or email already exists", ErrInvalidInput)
		}
		return nil, fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	return &user, nil
}

// SearchUsers searches for users with validated input to prevent SQL injection
func (f *Frontend) SearchUsers(ctx context.Context, searchTerm string, limit int) ([]*User, error) {
	// Validate and sanitize input
	if searchTerm == "" {
		return nil, ErrInvalidInput
	}
	
	// Limit search term length to prevent DoS
	if len(searchTerm) > 100 {
		return nil, fmt.Errorf("%w: search term too long", ErrInvalidInput)
	}

	// Validate limit
	if limit <= 0 || limit > 100 {
		limit = 10 // Safe default
	}

	// Sanitize search term - remove potentially dangerous characters
	searchTerm = sanitizeSearchTerm(searchTerm)

	// Create context with timeout
	ctx, cancel := context.WithTimeout(ctx, f.config.QueryTimeout)
	defer cancel()

	// Use parameterized query with LIKE - still safe from SQL injection
	query := `SELECT id, username, email, created_at FROM users 
	          WHERE username LIKE $1 OR email LIKE $2 
	          ORDER BY created_at DESC LIMIT $3`
	
	searchPattern := "%" + searchTerm + "%"
	rows, err := f.db.QueryContext(ctx, query, searchPattern, searchPattern, limit)
	if err != nil {
		return nil, fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}
	defer rows.Close()

	var users []*User
	for rows.Next() {
		var user User
		if err := rows.Scan(&user.ID, &user.Username, &user.Email, &user.CreatedAt); err != nil {
			return nil, fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
		}
		users = append(users, &user)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	return users, nil
}

// UpdateUser updates user information with validated input
func (f *Frontend) UpdateUser(ctx context.Context, userID int64, username, email string) error {
	// Validate inputs
	if userID <= 0 {
		return ErrInvalidInput
	}
	if err := validateUsername(username); err != nil {
		return err
	}
	if err := validateEmail(email); err != nil {
		return err
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(ctx, f.config.QueryTimeout)
	defer cancel()

	// Use parameterized query
	query := `UPDATE users SET username = $1, email = $2 WHERE id = $3`
	
	result, err := f.db.ExecContext(ctx, query, username, email, userID)
	if err != nil {
		return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	if rowsAffected == 0 {
		return ErrNotFound
	}

	return nil
}

// DeleteUser deletes a user by ID
func (f *Frontend) DeleteUser(ctx context.Context, userID int64) error {
	// Validate input
	if userID <= 0 {
		return ErrInvalidInput
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(ctx, f.config.QueryTimeout)
	defer cancel()

	// Use parameterized query
	query := `DELETE FROM users WHERE id = $1`
	
	result, err := f.db.ExecContext(ctx, query, userID)
	if err != nil {
		return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	if rowsAffected == 0 {
		return ErrNotFound
	}

	return nil
}

// ExecuteInTransaction executes a function within a database transaction
func (f *Frontend) ExecuteInTransaction(ctx context.Context, fn func(*sql.Tx) error) error {
	// Create context with timeout
	ctx, cancel := context.WithTimeout(ctx, f.config.QueryTimeout)
	defer cancel()

	tx, err := f.db.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	// Execute function
	if err := fn(tx); err != nil {
		if rbErr := tx.Rollback(); rbErr != nil {
			log.Printf("rollback error: %v", sanitizeError(rbErr))
		}
		return err
	}

	// Commit transaction
	if err := tx.Commit(); err != nil {
		return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
	}

	return nil
}

// Validation functions

// validateConfig validates database configuration
func validateConfig(config *Config) error {
	if config.Host == "" {
		return fmt.Errorf("%w: host is required", ErrInvalidInput)
	}
	if config.Port <= 0 || config.Port > 65535 {
		return fmt.Errorf("%w: invalid port number", ErrInvalidInput)
	}
	if config.Database == "" {
		return fmt.Errorf("%w: database name is required", ErrInvalidInput)
	}
	if config.MaxConnections <= 0 {
		return fmt.Errorf("%w: max connections must be positive", ErrInvalidInput)
	}
	return nil
}

// validateUsername validates username format
func validateUsername(username string) error {
	if username == "" {
		return fmt.Errorf("%w: username is required", ErrInvalidInput)
	}
	if len(username) < 3 || len(username) > 50 {
		return fmt.Errorf("%w: username must be 3-50 characters", ErrInvalidInput)
	}
	// Allow alphanumeric, underscore, and hyphen
	validUsername := regexp.MustCompile(`^[a-zA-Z0-9_-]+$`)
	if !validUsername.MatchString(username) {
		return fmt.Errorf("%w: username contains invalid characters", ErrInvalidInput)
	}
	return nil
}

// validateEmail validates email format
func validateEmail(email string) error {
	if email == "" {
		return fmt.Errorf("%w: email is required", ErrInvalidInput)
	}
	if len(email) > 255 {
		return fmt.Errorf("%w: email too long", ErrInvalidInput)
	}
	// Basic email validation
	validEmail := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
	if !validEmail.MatchString(email) {
		return fmt.Errorf("%w: invalid email format", ErrInvalidInput)
	}
	return nil
}

// sanitizeSearchTerm removes potentially dangerous characters from search terms
func sanitizeSearchTerm(term string) string {
	// Remove SQL special characters that could be used in injection attempts
	// even though we use parameterized queries (defense in depth)
	term = strings.ReplaceAll(term, ";", "")
	term = strings.ReplaceAll(term, "--", "")
	term = strings.ReplaceAll(term, "/*", "")
	term = strings.ReplaceAll(term, "*/", "")
	term = strings.ReplaceAll(term, "xp_", "")
	term = strings.ReplaceAll(term, "sp_", "")
	return strings.TrimSpace(term)
}

// sanitizeError removes sensitive information from error messages
func sanitizeError(err error) error {
	if err == nil {
		return nil
	}
	
	errMsg := err.Error()
	
	// Remove potential sensitive information from error messages
	sensitivePatterns := []string{
		`password[:\s]*[^\s]+`,
		`pwd[:\s]*[^\s]+`,
		`token[:\s]*[^\s]+`,
		`secret[:\s]*[^\s]+`,
		`api[_-]?key[:\s]*[^\s]+`,
	}
	
	for _, pattern := range sensitivePatterns {
		re := regexp.MustCompile(`(?i)` + pattern)
		errMsg = re.ReplaceAllString(errMsg, "[REDACTED]")
	}
	
	return errors.New(errMsg)
}

// HealthCheck performs a database health check
func (f *Frontend) HealthCheck(ctx context.Context) error {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	if err := f.db.PingContext(ctx); err != nil {
		return fmt.Errorf("database health check failed: %w", err)
	}

	// Test a simple query
	var result int
	err := f.db.QueryRowContext(ctx, "SELECT 1").Scan(&result)
	if err != nil {
		return fmt.Errorf("database query check failed: %w", err)
	}

	return nil
}
