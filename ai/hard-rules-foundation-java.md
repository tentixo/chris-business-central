# Java Hard Rules (Foundation)

**Scope**: Java-specific rules for TXO projects
**Version**: 1.0
**Extracted from**: txo-java-adr_v1.0.md
**Updated**: 2026-01-04

---

## MUST (Required)

### JAVA-MUST-1: Hard-Fail Config Philosophy
```java
// ✅ CORRECT - Hard fail
public String getRequired(JsonObject config, String key) {
    if (!config.containsKey(key)) {
        throw new IllegalStateException("Missing required config: " + key);
    }
    return config.getString(key);
}

// ❌ WRONG - Silent default
int timeout = config.getInteger("timeout", 30);  // Masks configuration errors
```
Source: ADR-J001

### JAVA-MUST-2: Never Print - Always Log
- MUST use SLF4J structured logging
- MUST NOT use System.out/System.err
- MUST NOT use e.printStackTrace()
```java
// ✅ CORRECT
private static final Logger logger = LoggerFactory.getLogger(MyClass.class);
logger.error("Failed to process record {}", recordId, exception);

// ❌ WRONG
System.out.println("Processing " + recordCount + " records");
e.printStackTrace();
```
Source: ADR-J002

### JAVA-MUST-3: Never Swallow Exceptions
- MUST log exceptions before handling
- MUST NOT have empty catch blocks
- MUST preserve stack traces when wrapping
```java
// ✅ CORRECT - Log and rethrow
try {
    processMessage(message);
} catch (Exception e) {
    logger.error("Failed to process message {}", message.getId(), e);
    throw e;
}

// ❌ WRONG - Swallowing
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure - NEVER
}

// ❌ WRONG - Lost stack trace
throw new RuntimeException(e.getMessage());  // Missing cause!
```
Source: ADR-J005

### JAVA-MUST-4: Config File Collision Detection
- MUST detect and fail on key collisions between config and secrets
- MUST check during config loading, before use
```java
Set<String> collisions = new HashSet<>(configKeys);
collisions.retainAll(secretKeys);
if (!collisions.isEmpty()) {
    throw new ConfigurationException("Key collision: " + collisions);
}
```
Source: ADR-J006

---

## MUST NOT (Forbidden)

### JAVA-MUSTNOT-1: Print Statements
- MUST NOT use System.out.println()
- MUST NOT use System.err.println()
- MUST NOT use e.printStackTrace()
Source: ADR-J002

### JAVA-MUSTNOT-2: Empty Catch Blocks
```java
// ❌ NEVER DO THIS
try {
    riskyOperation();
} catch (Exception e) {
    // Empty - swallows error
}
```
Source: ADR-J005

---

## SHOULD (Recommended)

### JAVA-SHOULD-1: Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `EmailProcessor` |
| Interfaces | PascalCase (no I prefix) | `MessageHandler` |
| Methods | camelCase, verb-first | `processEmail()` |
| Variables | camelCase | `emailCount` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Packages | lowercase | `com.tentixo.numan.e1` |
| Config keys | kebab-case | `api-base-url` |
| Status values | UPPERCASE | `READY`, `FAILED` |
Source: ADR-J003

### JAVA-SHOULD-2: Custom Exception Pattern
```java
public class ConfigurationException extends RuntimeException {
    public ConfigurationException(String message) {
        super(message);
    }
    public ConfigurationException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
Source: ADR-J005

---

## Quick Reference

| Category | Key Rules |
|----------|-----------|
| Config | Hard-fail on missing, collision detection |
| Logging | SLF4J only, never print |
| Exceptions | Never swallow, preserve stack traces |
| Naming | PascalCase classes, camelCase methods, kebab-case config |
