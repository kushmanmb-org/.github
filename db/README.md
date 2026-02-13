# Database Frontend Security Documentation

This document describes the security practices implemented in `db/frontend.go`.

## Security Features

### 1. SQL Injection Prevention

**All queries use parameterized statements** to prevent SQL injection attacks:

```go
// ✅ SECURE - Parameterized query
query := `SELECT id, username, email FROM users WHERE id = $1`
err := db.QueryRowContext(ctx, query, userID).Scan(&user.ID, &user.Username, &user.Email)

// ❌ INSECURE - String concatenation (NEVER DO THIS)
query := fmt.Sprintf("SELECT * FROM users WHERE id = %d", userID)
```

### 2. Input Validation

**All user inputs are validated** before use:

- **Username validation**: 3-50 alphanumeric characters, underscore, or hyphen
- **Email validation**: Proper email format with regex
- **Length limits**: Prevent DoS attacks by limiting input sizes
- **Type validation**: Ensure correct data types (e.g., userID > 0)

```go
func validateUsername(username string) error {
    if len(username) < 3 || len(username) > 50 {
        return ErrInvalidInput
    }
    validUsername := regexp.MustCompile(`^[a-zA-Z0-9_-]+$`)
    if !validUsername.MatchString(username) {
        return ErrInvalidInput
    }
    return nil
}
```

### 3. Secure Error Handling

**Errors are sanitized** to prevent information disclosure:

- Database connection details are not exposed
- Sensitive data (passwords, tokens, API keys) is redacted from error messages
- Generic error messages prevent enumeration attacks

```go
// Error sanitization removes sensitive patterns
func sanitizeError(err error) error {
    sensitivePatterns := []string{
        `password[:\s]*[^\s]+`,
        `token[:\s]*[^\s]+`,
        `api[_-]?key[:\s]*[^\s]+`,
    }
    // Replace with [REDACTED]
}
```

### 4. No Hardcoded Credentials

**Credentials are never hardcoded**:

```go
// ✅ SECURE - Load from environment variables
user := os.Getenv("DB_USER")
password := os.Getenv("DB_PASSWORD")
frontend, err := NewFrontend(config, user, password)

// ❌ INSECURE - Hardcoded credentials (NEVER DO THIS)
frontend, err := NewFrontend(config, "admin", "password123")
```

### 5. Connection Pooling and Resource Management

**Proper resource management** prevents resource exhaustion:

```go
// Configure connection pool with secure defaults
db.SetMaxOpenConns(10)              // Limit concurrent connections
db.SetMaxIdleConns(5)                // Limit idle connections
db.SetConnMaxLifetime(time.Hour)     // Rotate connections
```

### 6. Context-Based Timeouts

**All operations have timeouts** to prevent hanging:

```go
// Create context with timeout
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()

// Use context in query
err := db.QueryRowContext(ctx, query, userID).Scan(...)
```

### 7. Defense in Depth

**Multiple layers of security**:

- Input validation (first layer)
- Parameterized queries (second layer)
- Search term sanitization (third layer)
- Error sanitization (fourth layer)

```go
func sanitizeSearchTerm(term string) string {
    // Remove SQL special characters even though we use parameterized queries
    term = strings.ReplaceAll(term, ";", "")
    term = strings.ReplaceAll(term, "--", "")
    term = strings.ReplaceAll(term, "/*", "")
    term = strings.ReplaceAll(term, "*/", "")
    return strings.TrimSpace(term)
}
```

### 8. SSL/TLS Connections

**Database connections require SSL**:

```go
dsn := fmt.Sprintf("host=%s port=%d dbname=%s user=%s password=%s sslmode=require",
    config.Host, config.Port, config.Database, user, password)
```

### 9. Transaction Support

**Atomic operations with automatic rollback**:

```go
err := frontend.ExecuteInTransaction(ctx, func(tx *sql.Tx) error {
    // Multiple operations here
    // Automatically rolled back on error
    return nil
})
```

### 10. Health Checks

**Built-in health monitoring**:

```go
err := frontend.HealthCheck(ctx)
if err != nil {
    log.Fatal("Database unhealthy:", err)
}
```

## Usage Examples

### Basic Usage

```go
package main

import (
    "context"
    "log"
    "os"
    "your-repo/db"
)

func main() {
    // Load credentials from environment
    user := os.Getenv("DB_USER")
    password := os.Getenv("DB_PASSWORD")
    
    // Create configuration
    config := db.DefaultConfig()
    config.Host = "localhost"
    config.Port = 5432
    config.Database = "mydb"
    
    // Create frontend
    frontend, err := db.NewFrontend(config, user, password)
    if err != nil {
        log.Fatal(err)
    }
    defer frontend.Close()
    
    // Health check
    if err := frontend.HealthCheck(context.Background()); err != nil {
        log.Fatal("Database unhealthy:", err)
    }
    
    // Create user
    user, err := frontend.CreateUser(context.Background(), "johndoe", "john@example.com")
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Created user: %+v", user)
}
```

### Search with Security

```go
// Search users safely
users, err := frontend.SearchUsers(ctx, "john", 10)
if err != nil {
    log.Fatal(err)
}

// Safe even with malicious input - parameterized queries prevent injection
maliciousInput := "john'; DROP TABLE users; --"
users, err = frontend.SearchUsers(ctx, maliciousInput, 10)
// Input is sanitized and parameterized - no SQL injection possible
```

### Transaction Example

```go
// Execute multiple operations atomically
err := frontend.ExecuteInTransaction(ctx, func(tx *sql.Tx) error {
    // Create multiple users
    _, err := tx.Exec(`INSERT INTO users (username, email) VALUES ($1, $2)`, "user1", "user1@example.com")
    if err != nil {
        return err // Automatically rolled back
    }
    
    _, err = tx.Exec(`INSERT INTO users (username, email) VALUES ($1, $2)`, "user2", "user2@example.com")
    if err != nil {
        return err // Automatically rolled back
    }
    
    return nil // Committed
})
```

## Security Checklist

Before deploying:

- [ ] Database credentials stored in environment variables
- [ ] SSL/TLS enabled for database connections
- [ ] Connection pool limits configured appropriately
- [ ] Query timeouts set based on application needs
- [ ] Input validation rules match business requirements
- [ ] Error logging does not expose sensitive information
- [ ] Health check endpoint implemented
- [ ] Transaction support used for multi-step operations
- [ ] Database user has minimal required privileges (principle of least privilege)
- [ ] Regular security audits scheduled

## Common Pitfalls to Avoid

### 1. String Concatenation in Queries

```go
// ❌ NEVER DO THIS - SQL Injection vulnerability
query := "SELECT * FROM users WHERE username = '" + username + "'"

// ✅ ALWAYS DO THIS - Parameterized query
query := "SELECT * FROM users WHERE username = $1"
db.QueryRowContext(ctx, query, username)
```

### 2. Exposing Errors to Users

```go
// ❌ NEVER DO THIS - Information disclosure
return fmt.Errorf("Database connection failed: %v", err)

// ✅ ALWAYS DO THIS - Sanitized error
return fmt.Errorf("%w: %v", ErrDatabaseError, sanitizeError(err))
```

### 3. Hardcoding Credentials

```go
// ❌ NEVER DO THIS - Credentials in code
db, err := sql.Open("postgres", "user=admin password=secret123")

// ✅ ALWAYS DO THIS - Environment variables
user := os.Getenv("DB_USER")
password := os.Getenv("DB_PASSWORD")
dsn := fmt.Sprintf("user=%s password=%s", user, password)
```

### 4. No Timeouts

```go
// ❌ NEVER DO THIS - No timeout (can hang indefinitely)
err := db.QueryRow(query, userID).Scan(&user)

// ✅ ALWAYS DO THIS - Context with timeout
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
err := db.QueryRowContext(ctx, query, userID).Scan(&user)
```

### 5. Ignoring Resource Cleanup

```go
// ❌ NEVER DO THIS - Resource leak
rows, _ := db.Query(query)
for rows.Next() {
    // ...
}

// ✅ ALWAYS DO THIS - Proper cleanup
rows, err := db.Query(query)
if err != nil {
    return err
}
defer rows.Close()  // Always close rows

for rows.Next() {
    // ...
}
if err := rows.Err(); err != nil {  // Check for iteration errors
    return err
}
```

## Compliance Standards

This implementation follows:

- **OWASP Top 10**: Addresses injection, sensitive data exposure, and security misconfiguration
- **CWE-89**: SQL Injection prevention
- **CWE-200**: Information exposure prevention
- **CWE-259**: Hard-coded password prevention
- **PCI DSS**: Secure coding practices for payment applications
- **GDPR**: Data protection by design

## Additional Resources

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Go database/sql Documentation](https://pkg.go.dev/database/sql)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

## Maintenance

### Regular Security Tasks

1. **Weekly**: Review database connection pool metrics
2. **Monthly**: Update dependencies and security patches
3. **Quarterly**: Conduct security audit and penetration testing
4. **Annually**: Review and update validation rules

### Monitoring

Monitor these metrics:

- Failed login attempts (potential brute force)
- Query timeout rates (potential DoS)
- Error rates (potential attacks or bugs)
- Connection pool exhaustion (resource issues)
- Unusual query patterns (potential SQL injection attempts)

---

**Last Updated**: 2026-02-13  
**Version**: 1.0
