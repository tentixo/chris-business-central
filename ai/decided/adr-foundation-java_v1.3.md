# TXO Java Architecture Decision Records v1.1

These ADRs define **TXO-specific patterns for Java projects**, reflecting how TentXO operates regardless of framework.
For Vert.x-specific patterns, see `adr-foundation-vertx_v1.1.md`.

**Status**: Living document - grows iteratively  
**Created**: 2026-01-02  
**Updated**: 2026-01-04 (v1.1 - Java 21 patterns, logging context, validation timing, frontend strategy)

---

## ADR-J001: Hard-Fail Configuration Philosophy

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

TXO values predictable, consistent behavior. Configuration errors should fail immediately and clearly, not silently use
defaults.

### Decision

- **Hard fail** for configuration values - throw exceptions on missing keys
- **No defaults** in code for configuration values
- **Soft fail** (`Optional`, `getOrDefault`) ONLY for external API responses

### Implementation

```java
// ✅ CORRECT - Configuration (hard fail)
public class ConfigLoader {

    public String getRequired(JsonObject config, String key) {
        if (!config.containsKey(key)) {
            throw new IllegalStateException("Missing required config: " + key);
        }
        return config.getString(key);
    }

    // Usage
    String apiUrl = getRequired(config, "api-base-url");  // Throws if missing
    int timeout = config.getInteger("timeout-seconds");   // NPE if missing - acceptable
}

// ✅ CORRECT - External API response (soft fail OK)
String email = jsonResponse.getString("email", null);  // null OK for optional field
String name = Optional.ofNullable(jsonResponse.getString("name"))
    .orElse("Unknown");

// ❌ WRONG - Configuration with defaults
int timeout = config.getInteger("timeout", 30);  // Masks configuration errors
String url = config.getString("api-url", "http://localhost");  // Silent fallback
```

### Consequences

- Positive: Fail fast on misconfiguration, no silent errors
- Negative: Must have complete configuration
- Mitigation: Provide complete templates, clear error messages

---

## ADR-J002: Never Print - Always Log

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

TXO needs consistent, structured, searchable output for debugging and audit trails.

### Decision

**Absolute prohibition on System.out/System.err.** All output must use SLF4J structured logging.

### Implementation

```java
// ✅ CORRECT - Structured logging
private static final Logger logger = LoggerFactory.getLogger(MyClass.class);

logger.info("Processing started for {} records", recordCount);
logger.debug("API request payload: {}", sanitizedPayload);
logger.error("Failed to process record {}", recordId, exception);

// ❌ WRONG - Print statements
System.out.println("Processing " + recordCount + " records");
System.err.println("Error: " + exception.getMessage());
e.printStackTrace();  // Never use this
```

### Logging Levels

| Level | Console | File | Use Case                     |
|-------|---------|------|------------------------------|
| DEBUG | No      | Yes  | Detailed troubleshooting     |
| INFO  | Yes     | Yes  | Normal operation status      |
| WARN  | Yes     | Yes  | Recoverable issues           |
| ERROR | Yes     | Yes  | Failures requiring attention |

### Consequences

- Positive: All output captured, structured for analysis, AI-friendly debugging
- Negative: Requires logger setup in every class
- Mitigation: Use Lombok `@Slf4j` annotation or IDE templates

---

## ADR-J003: Naming Conventions

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Consistent naming reduces cognitive load and supports tooling. Java has established conventions that differ from Python.

### Decision

Follow standard Java conventions with TXO-specific additions:

### Naming Rules

| Element        | Convention               | Example                                |
|----------------|--------------------------|----------------------------------------|
| **Classes**    | PascalCase               | `EmailProcessor`, `ConfigLoader`       |
| **Interfaces** | PascalCase (no I prefix) | `MessageHandler`, `CertificateService` |
| **Methods**    | camelCase, verb-first    | `processEmail()`, `loadConfig()`       |
| **Variables**  | camelCase                | `emailCount`, `configPath`             |
| **Constants**  | UPPER_SNAKE_CASE         | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`   |
| **Packages**   | lowercase, dot-separated | `com.tentixo.numan.e1`                 |

### TXO-Specific Conventions

| Element                | Convention | Example                               |
|------------------------|------------|---------------------------------------|
| **Config keys** (JSON) | kebab-case | `"api-base-url"`, `"timeout-seconds"` |
| **Status values**      | UPPERCASE  | `READY`, `PROCESSING`, `FAILED`       |
| **Metadata prefix**    | Underscore | `_metadata`, `_createdAt`             |
| **Module directories** | kebab-case | `e1-receive/`, `e1-cert/`             |

### Implementation

```java
// ✅ CORRECT - Java naming
public class E1ReceiveVerticle {
    private static final int MAX_RETRY_COUNT = 3;

    private final String apiBaseUrl;  // camelCase variable

    public void processIncomingEmail(Email email) {
        String status = CoreConstants.STATUS_READY;  // UPPERCASE constant
    }
}

// ✅ CORRECT - Config key access (kebab-case in JSON)
String apiUrl = config.getString("api-base-url");  // kebab-case key
int timeout = config.getInteger("timeout-seconds");

// ❌ WRONG - Mixed conventions
String api_base_url;  // snake_case in Java
private static final int maxRetryCount = 3;  // camelCase for constant
```

### Consequences

- Positive: Familiar to Java developers, IDE support, clear distinction between code and config
- Negative: Must remember JSON uses kebab-case
- Mitigation: Consistent patterns, clear documentation

---

## ADR-J004: Project Directory Structure

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Multi-module Gradle projects need consistent structure for maintainability and automation.

### Decision

Standard Gradle multi-module structure with TXO conventions:

```
project-root/
├── gradle/
│   └── libs.versions.toml     # Version catalog (mandatory)
├── core/                       # Shared utilities module
│   ├── build.gradle.kts
│   └── src/main/java/{package}/core/
├── {module}/                   # Feature modules (kebab-case)
│   ├── build.gradle.kts
│   └── src/main/java/{package}/{module}/
├── app/                        # Assembly module (fat JAR)
│   ├── build.gradle.kts
│   └── src/main/resources/
│       └── logback.xml
├── build.gradle.kts            # Root build file
├── settings.gradle.kts         # Module definitions
├── gradle.properties           # Gradle settings
│
├── ai/                         # AI and documentation
│   ├── decided/                # ADRs and patterns
│   ├── project-docs/           # Architecture docs
│   ├── skills/                 # Reusable procedures
│   └── working/                # Session notes
├── config/                     # Runtime configuration (gitignored secrets)
├── logs/                       # Log files (gitignored)
└── CLAUDE.md                   # AI context summary
```

### Package Structure

```
com.tentixo.{project}.{module}

Examples:
- com.tentixo.numan.core       # Shared utilities
- com.tentixo.numan.e1         # E1 Email verticle
- com.tentixo.numan.e1cert     # E1-Cert service
- com.tentixo.numan.app        # Main application
```

### Consequences

- Positive: Consistent structure, clear module boundaries, IDE-friendly
- Negative: Deeper package paths
- Mitigation: IDE navigation, package-info.java for documentation

---

## ADR-J005: Error Handling Patterns

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Java uses checked and unchecked exceptions. TXO needs consistent error handling that integrates with logging and doesn't
swallow errors.

### Decision

- **Checked exceptions**: Wrap in unchecked or handle explicitly
- **Never swallow**: Always log, never empty catch blocks
- **Fail fast**: Let configuration errors propagate
- **Structured errors**: Use custom exception types for business errors

### Implementation

```java
// ✅ CORRECT - Wrap checked exception
public JsonObject loadConfig(Path path) {
    try {
        String content = Files.readString(path);
        return new JsonObject(content);
    } catch (IOException e) {
        throw new ConfigurationException("Failed to load config: " + path, e);
    }
}

// ✅ CORRECT - Log and rethrow
try {
    processMessage(message);
} catch (Exception e) {
    logger.error("Failed to process message {}", message.getId(), e);
    throw e;  // Let caller handle
}

// ✅ CORRECT - Handle with recovery
try {
    return primaryService.fetch(id);
} catch (ServiceException e) {
    logger.warn("Primary service failed, trying fallback: {}", e.getMessage());
    return fallbackService.fetch(id);
}

// ❌ WRONG - Swallowing exception
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure - NEVER do this
}

// ❌ WRONG - Losing stack trace
try {
    riskyOperation();
} catch (Exception e) {
    throw new RuntimeException(e.getMessage());  // Lost stack trace!
}
```

### Custom Exception Pattern

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

### Consequences

- Positive: Consistent error handling, full stack traces, clear logging
- Negative: More verbose than try-with-resources alone
- Mitigation: IDE templates, base exception classes

---

## ADR-J006: Configuration Files and Secrets

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

TXO projects need runtime configuration that varies by environment (dev/test/prod). Secrets (passwords, certificates)
must be gitignored while non-secret config can be tracked.

### Decision

- **Directory per module**: `config/{module}/`
- **Two-file pattern**: `{env}-config.json` (trackable) + `{env}-config-secrets.json` (gitignored)
- **Nested config**: Structured JSON for config files (supports JSON Schema validation)
- **Flat secrets**: Unique key names, no nesting (simpler, less to validate)
- **Separate access**: Shared and module config accessed explicitly, not merged

### Directory Structure

```
project-root/
├── schemas/                         # JSON Schema definitions
│   ├── shared-config.schema.json
│   ├── app-config.schema.json
│   ├── e1-receive-config.schema.json
│   └── e1-cert-config.schema.json
├── config/
│   ├── shared/                      # Common infrastructure config
│   │   ├── dev-config.json          # ✅ Tracked - Couchbase, TimescaleDB
│   │   ├── dev-config-secrets.json  # ❌ Gitignored - DB credentials
│   │   ├── test-config.json
│   │   ├── test-config-secrets.json
│   │   └── prod-config.json
│   ├── app/                         # Deployment orchestration
│   │   ├── dev-config.json          # ✅ Tracked - which verticles, instances
│   │   └── dev-config-secrets.json  # ❌ Gitignored (usually empty)
│   ├── e1-receive/                    # E1 Email Intake module
│   │   ├── dev-config.json
│   │   └── dev-config-secrets.json  # IMAP credentials
│   ├── e1-cert/                     # E1-Cert module
│   │   ├── dev-config.json
│   │   └── dev-config-secrets.json  # Cert passwords
│   ├── certs/                       # ❌ Gitignored entirely
│   │   ├── dev-signing.p12
│   │   ├── dev-encryption.p12
│   │   └── *.pem
│   └── README.md                    # ✅ Tracked - documents required secrets
```

### Naming Conventions

| File Type    | Pattern                     | Tracked |
|--------------|-----------------------------|---------|
| Config       | `{env}-config.json`         | Yes     |
| Secrets      | `{env}-config-secrets.json` | **No**  |
| Certificates | `{env}-{purpose}.p12`       | **No**  |
| PEM files    | `*.pem`                     | **No**  |

**Environment values**: `dev`, `test`, `prod`

### File Contents

**shared/dev-config.json** (trackable):

```json
{
  "couchbase-connection-string": "couchbase://localhost",
  "couchbase-bucket": "numan-edi",
  "timescale-host": "localhost",
  "timescale-port": 5432
}
```

**shared/dev-config-secrets.json** (gitignored, flat structure):

```json
{
  "couchbase-username": "admin",
  "couchbase-password": "cbpassword",
  "timescale-username": "numan",
  "timescale-password": "tspassword"
}
```

**e1-cert/dev-config.json** (trackable):

```json
{
  "ldap-url": "ldap://sodir01.expisoft.se:389",
  "cache-ttl-hours": 24,
  "v2-grace-period": "2028-09-14",
  "signing-cert-path": "config/certs/dev-signing.p12",
  "encryption-cert-path": "config/certs/dev-encryption.p12"
}
```

**e1-cert/dev-config-secrets.json** (gitignored, flat structure):

```json
{
  "signing-cert-password": "certpass123",
  "encryption-cert-password": "certpass456"
}
```

**app/dev-config.json** (trackable):

```json
{
  "verticles": [
    "e1-cert",
    "e1-receive"
  ],
  "instances": {
    "e1-cert": 1,
    "e1-receive": 2
  },
  "deploy-order": [
    "e1-cert",
    "e1-receive"
  ]
}
```

### Loading Pattern

```java
public record ModuleConfig(
    JsonObject shared,
    JsonObject sharedSecrets,
    JsonObject module,
    JsonObject moduleSecrets
) {
    public static ModuleConfig load(String envType, String moduleName) {
        Path configDir = Path.of("config");
        return new ModuleConfig(
            loadJson(configDir.resolve("shared/" + envType + "-config.json")),
            loadJson(configDir.resolve("shared/" + envType + "-config-secrets.json")),
            loadJson(configDir.resolve(moduleName + "/" + envType + "-config.json")),
            loadJson(configDir.resolve(moduleName + "/" + envType + "-config-secrets.json"))
        );
    }

    /** Get from module config (hard fail) */
    public String get(String key) {
        if (module.containsKey(key)) return module.getString(key);
        throw new IllegalStateException("Missing module config: " + key);
    }

    /** Get from shared config (hard fail) */
    public String getShared(String key) {
        if (shared.containsKey(key)) return shared.getString(key);
        throw new IllegalStateException("Missing shared config: " + key);
    }

    /** Get from secrets - checks module first, then shared (hard fail) */
    public String getSecret(String key) {
        if (moduleSecrets.containsKey(key)) return moduleSecrets.getString(key);
        if (sharedSecrets.containsKey(key)) return sharedSecrets.getString(key);
        throw new IllegalStateException("Missing secret: " + key);
    }
}
```

### JSON Schema Validation

**SHOULD** validate config files against JSON Schema during loading:

| File Type                      | Schema Required                     | Rationale              |
|--------------------------------|-------------------------------------|------------------------|
| `{module}-config.json`         | **SHOULD** (complex files **MUST**) | Structured, many keys  |
| `{module}-config-secrets.json` | No                                  | Flat, simple key-value |

**Schema location**: `schemas/{module}-config.schema.json`

**Schema example** (`schemas/e1-cert-config.schema.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "e1-cert-config.schema.json",
  "title": "E1-Cert Configuration",
  "type": "object",
  "required": [
    "ldap-url",
    "cache-ttl-hours",
    "v2-grace-period"
  ],
  "properties": {
    "ldap-url": {
      "type": "string",
      "format": "uri",
      "description": "LDAP server URL for certificate lookup"
    },
    "cache-ttl-hours": {
      "type": "integer",
      "minimum": 1,
      "maximum": 168
    },
    "v2-grace-period": {
      "type": "string",
      "format": "date",
      "description": "End date for V2 certificate support"
    }
  },
  "additionalProperties": false
}
```

### Key Collision Detection

**MUST** detect and fail on key collisions between config and secrets during loading.

```java
public static ModuleConfig load(String envType, String moduleName) {
    // ... load files ...

    // MUST: Detect key collisions
    Set<String> configKeys = module.fieldNames();
    Set<String> secretKeys = moduleSecrets.fieldNames();
    Set<String> collisions = new HashSet<>(configKeys);
    collisions.retainAll(secretKeys);

    if (!collisions.isEmpty()) {
        throw new ConfigurationException(
            "Key collision between config and secrets in " + moduleName +
            ": " + collisions);
    }

    // Same check for shared
    Set<String> sharedConfigKeys = shared.fieldNames();
    Set<String> sharedSecretKeys = sharedSecrets.fieldNames();
    Set<String> sharedCollisions = new HashSet<>(sharedConfigKeys);
    sharedCollisions.retainAll(sharedSecretKeys);

    if (!sharedCollisions.isEmpty()) {
        throw new ConfigurationException(
            "Key collision between shared config and secrets: " + sharedCollisions);
    }

    return new ModuleConfig(shared, sharedSecrets, module, moduleSecrets);
}
```

**Why collision detection matters:**

- Prevents accidental secret exposure in trackable config
- Catches copy-paste errors early
- Ensures `getSecret()` lookup is unambiguous

### .gitignore Entries

```gitignore
# Already in .gitignore:
*-secrets.json
*.pem
*.p12
```

### config/README.md Template

Track a README documenting required secrets:

```markdown
# Configuration

## Structure

Each module has its own directory with env-prefixed config files.

## Required Secret Files

| Module     | File                      | Keys                                            |
|------------|---------------------------|-------------------------------------------------|
| shared     | {env}-config-secrets.json | couchbase-password, timescale-password          |
| e1-receive | {env}-config-secrets.json | imap-password                                   |
| e1-cert    | {env}-config-secrets.json | signing-cert-password, encryption-cert-password |

## Required Certificates

| File                       | Purpose                |
|----------------------------|------------------------|
| certs/{env}-signing.p12    | S/MIME message signing |
| certs/{env}-encryption.p12 | S/MIME decryption      |
```

### Consequences

- Positive: Clear separation, secrets never tracked, environment-specific
- Positive: Schema validation catches config errors early
- Positive: Collision detection prevents secret leakage
- Negative: More files to manage (config + secrets + schema per module)
- Mitigation: Loading pattern handles complexity, IDE schema validation

---

## ADR-J007: Java Version Management

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

TXO uses Java 21 (LTS). Gradle 8.x and Kotlin DSL require Java 21 or lower to run - newer Java versions (22+) cause
build failures. Developers may have multiple Java versions installed.

### Decision

- Use **SDKMAN** for Java version management
- Install via Homebrew: `brew install sdkman-cli`
- Configure shell to use correct Java for Gradle

### Implementation

**Install SDKMAN (macOS):**

```bash
brew install sdkman-cli

# Add to ~/.zshrc (or ~/.bashrc):
export SDKMAN_DIR=$(brew --prefix sdkman-cli)/libexec
[[ -s "${SDKMAN_DIR}/bin/sdkman-init.sh" ]] && source "${SDKMAN_DIR}/bin/sdkman-init.sh"
```

**Install and use Java 21:**

```bash
# Reload shell
source ~/.zshrc

# Install Java 21 (Temurin)
sdk install java 21-tem

# Set as default
sdk default java 21-tem

# Verify
java -version  # Should show 21.x
```

**Per-project version (optional):**

```bash
# In project root, create .sdkmanrc
echo "java=21-tem" > .sdkmanrc

# SDKMAN auto-switches when entering directory
sdk env
```

### IDE vs Terminal

| Context              | Java Source          | How to Configure                          |
|----------------------|----------------------|-------------------------------------------|
| IntelliJ build       | Project SDK          | File → Project Structure → Project SDK    |
| IntelliJ Gradle      | Gradle JDK           | Preferences → Build → Gradle → Gradle JDK |
| Terminal `./gradlew` | Shell PATH/JAVA_HOME | SDKMAN `sdk use java 21-tem`              |

**IMPORTANT:** IDE settings do NOT affect terminal builds. Both must be configured.

### Consequences

- Positive: Consistent Java version across all contexts
- Positive: Easy switching between versions
- Negative: Requires shell configuration
- Mitigation: One-time setup, documented here

---

## ADR-J008: Resource Placement for Container Builds

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Multi-module Gradle projects with JIB containerization need clear rules for where different resource types belong.
Resources have different security profiles and deployment needs:

- **Public certificates**: Verification certs, can be baked into JARs
- **Config files**: Environment-specific, should be injected at runtime
- **Dev-only data**: Test fixtures, backfill files - never in production
- **Secrets**: Private keys, passwords - never in repo

### Decision

Resources are categorized by where they live and how they reach containers:

| Category         | Repo Location                        | In JAR? | Container Mount |
|------------------|--------------------------------------|---------|-----------------|
| **Public certs** | `{module}/src/main/resources/certs/` | YES     | Baked in        |
| **Config files** | `config/{module}/{env}-config.json`  | NO      | K8s ConfigMap   |
| **Secrets**      | Never in repo                        | NO      | K8s Secret      |

### Directory Structure

```
project-root/
├── config/                           # EXTERNAL - not in JARs
│   ├── {module}/
│   │   ├── dev-config.json
│   │   ├── devsrv-config.json
│   │   ├── test-config.json
│   │   └── prod-config.json
├── {module}/
│   └── src/main/resources/
│       └── certs/                    # PUBLIC certs - baked in
│           └── *.pem
└── secrets/                          # .gitignored - local dev only
    └── .gitkeep
```

### .gitignore Pattern

```gitignore
# Already ignoring:
*.pem
*.p12

# BUT allow public CA certs in module resources
!{module}/src/main/resources/certs/*.pem

# Secrets directory for local dev
secrets/
```

### Accessing Resources

**Public certs (from classpath):**

```java
InputStream is = getClass().getResourceAsStream("/certs/ca-cert.pem");
if (is == null) {
    throw new IllegalStateException("Missing required CA cert");
}
```

**Config files (from filesystem):**

```java
// Path resolved from ENV_TYPE and CONFIG_PATH env vars
String configPath = System.getenv().getOrDefault("CONFIG_PATH", "config");
String envType = System.getenv().getOrDefault("ENV_TYPE", "dev");
Path configFile = Path.of(configPath, moduleName, envType + "-config.json");
```

**Secrets (from mounted volume):**

```java
// Path comes from config file, not hardcoded
String keystorePath = config.getString("keystore-path");  // "secrets/signing.p12" or "/app/secrets/signing.p12"
String password = System.getenv("KEYSTORE_PASSWORD");     // From K8s Secret as env var
```

### Kubernetes Deployment

**ConfigMap mount:**

```yaml
volumes:
  - name: config
    configMap:
      name: numan-edi-config
volumeMounts:
  - name: config
    mountPath: /app/config
```

**Secret mount:**

```yaml
volumes:
  - name: secrets
    secret:
      secretName: numan-edi-secrets
volumeMounts:
  - name: secrets
    mountPath: /app/secrets
```

### Environment Paths

| Environment        | CONFIG_PATH   | Secrets Path   | Notes                    |
|--------------------|---------------|----------------|--------------------------|
| dev (IDE)          | `config`      | `secrets/`     | Relative to project root |
| devsrv (JIB local) | `/app/config` | `/app/secrets` | Container paths          |
| test/prod (K8s)    | `/app/config` | `/app/secrets` | Mounted volumes          |

### Why Public Certs in JAR?

1. **EDIEL CA certs are truly public** - available from LDAP, not secrets
2. **Avoids startup dependency** - container doesn't need external fetch
3. **Can still override** - mount volume shadows classpath resource if needed
4. **Simpler deployment** - fewer ConfigMap entries to manage

### Consequences

- Positive: Clear separation by security profile
- Positive: Containers stay minimal (no dev data, no secrets baked in)
- Positive: Public certs available immediately without external lookup
- Negative: Must remember `.gitignore` exception pattern for public certs
- Mitigation: Document pattern here, IDE highlights ignored files

---

## ADR-J009: Java 21 Modern Patterns

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Java 21 (LTS) introduces features that reduce boilerplate and improve code clarity. TXO should use modern patterns
instead of falling back to "old-school Java" patterns.

### Decision

**SHOULD** prefer Java 21 features for new code:

| Feature                         | Use Case                             | Pattern                                          |
|---------------------------------|--------------------------------------|--------------------------------------------------|
| **Records**                     | DTOs, config objects, immutable data | Replace POJOs                                    |
| **Pattern Matching for switch** | Type-safe multi-type handling        | Replace instanceof chains                        |
| **Record Patterns**             | Deconstructing data objects          | Simplify extraction                              |
| **Sequenced Collections**       | Order-guaranteed iteration           | `SequencedCollection`, `getFirst()`, `getLast()` |
| **Text Blocks**                 | Multi-line strings, JSON, SQL        | Replace string concatenation                     |

### Implementation

```java
// ✅ CORRECT - Record for immutable data
public record CertificateInfo(
    String email,
    X509Certificate cert,
    Instant fetchedAt,
    CertificateVersion version
) {}

// ✅ CORRECT - Pattern matching for switch
public String describe(Object obj) {
    return switch (obj) {
        case String s -> "String: " + s;
        case Integer i -> "Integer: " + i;
        case CertificateInfo(var email, var cert, _, _) -> "Cert for: " + email;
        case null -> "null";
        default -> "Unknown: " + obj.getClass();
    };
}

// ✅ CORRECT - Text blocks for multi-line
String query = """
    SELECT * FROM certificates
    WHERE email = ?
    AND status = 'VALID'
    """;

// ✅ CORRECT - Sequenced collections
SequencedSet<String> orderedEmails = new LinkedHashSet<>();
String first = orderedEmails.getFirst();
String last = orderedEmails.getLast();

// ❌ WRONG - Old-school POJO when record fits
public class CertificateInfoOld {
    private final String email;
    private final X509Certificate cert;
    // ... getters, equals, hashCode, toString boilerplate
}

// ❌ WRONG - instanceof chains
if (obj instanceof String) {
    String s = (String) obj;
    // ...
} else if (obj instanceof Integer) {
    Integer i = (Integer) obj;
    // ...
}
```

### Virtual Threads

**Note:** Virtual threads are covered in `adr-foundation-vertx_v1.1.md` as they interact with Vert.x's event loop model.

### Consequences

- Positive: Less boilerplate, clearer intent, better IDE support
- Positive: Records enforce immutability, reduce bugs
- Negative: Learning curve for developers unfamiliar with Java 21
- Mitigation: Use IDE inspections to suggest modern patterns

---

## ADR-J010: Smart Logging Context Strategy

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Logging context should be **proportional to complexity** - simple for local operations, detailed for external service
calls and multi-entity operations.

### Decision

Use context strategy based on operation type:

#### Local Operations (File processing, data transformation)

**Context**: **Optional** - simple, result-focused logging

```java
// Local file operations - simple logging
logger.info("Processing certificate data from cache");
logger.info("Saved {} records to {}", results.size(), outputPath);
logger.info("Local processing completed successfully");
```

#### External Service Operations

**Context**: **Mandatory** - full context for traceability

```java
// ✅ BEST - Use SLF4J placeholders directly (no String.format)
logger.info("[{}/{}/{}] Starting certificate lookup", envType, serviceName, operation);
logger.debug("[{}/{}/{}] Request: {}", envType, serviceName, operation, sanitizedRequest);
logger.error("[{}/{}/{}] LDAP lookup failed: {}", envType, serviceName, operation, errorMessage);

// Real examples:
logger.info("[prod/E1-Cert/LDAP] Retrieved certificate for partner@example.com");
logger.error("[dev/E1-Receive/IMAP] Authentication failed: token expired");
logger.debug("[test/E1-Cert/CRL] Checking revocation status for 5 certificates");
```

### Context Decision Rules

| Operation Type      | Context Required | Format                    |
|---------------------|------------------|---------------------------|
| Local file I/O      | Optional         | Simple message            |
| Cache operations    | Optional         | Simple message            |
| External API calls  | **Mandatory**    | `[env/service/operation]` |
| Database operations | **Mandatory**    | `[env/service/operation]` |
| Cross-service calls | **Mandatory**    | `[env/service/operation]` |

### Implementation Options

#### Option 1: Direct SLF4J Placeholders (Preferred)

```java
// ✅ BEST - SLF4J handles formatting, no intermediate string
logger.info("[{}/{}/{}] Looking up certificate for {}",
    envType, "E1-Cert", "LDAP", email);
```

#### Option 2: MDC for Structured Logging

```java
import org.slf4j.MDC;

// Set context once at operation start
MDC.put("env", envType);
MDC.put("service", "E1-Cert");
MDC.put("operation", "LDAP");

try {
    logger.info("Starting certificate lookup");  // Context in log format
    logger.debug("Request: {}", sanitizedRequest);
    // ... operation ...
    logger.info("Certificate retrieved for {}", email);
} finally {
    MDC.clear();  // Always clear!
}

// Configure logback to include MDC:
// %d{HH:mm:ss} [%X{env}/%X{service}/%X{operation}] %-5level %msg%n
```

#### Option 3: Context Helper (When Needed)

```java
// For complex reuse, still avoid String.format in hot paths
public record LogContext(String envType, String service, String operation) {
    @Override
    public String toString() {
        return "[" + envType + "/" + service + "/" + operation + "]";
    }
}

// Usage
LogContext ctx = new LogContext(envType, "E1-Cert", "LDAP");
logger.info("{} Looking up certificate for {}", ctx, email);
```

### Why NOT String.format()?

| Pattern         | Performance             | Readability |
|-----------------|-------------------------|-------------|
| SLF4J `{}`      | Fast (lazy eval)        | Good        |
| String.format() | Slow (always evaluates) | Verbose     |
| Concatenation   | Fast but messy          | Poor        |

SLF4J only builds the string if the log level is enabled.

### Consequences

- Positive: Proportional complexity, clear traceability
- Positive: Easy to grep logs by service/operation
- Positive: SLF4J placeholders are performant
- Negative: Requires discipline to add context
- Mitigation: MDC for automatic context in all logs

---

## ADR-J011: JSON Schema Validation Timing

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

When should JSON Schema validation happen? Early validation catches errors fast but may be expensive for large files.

### Decision

**Validation timing based on file type and size:**

#### Early Validation (Preferred - Fail Fast)

| File Type              | When         | Rationale             |
|------------------------|--------------|-----------------------|
| **Config files**       | At load time | MANDATORY - fail fast |
| **Small input** (<1MB) | At load time | Fast validation       |
| **Critical data**      | At load time | Affects program flow  |

```java
// ✅ Config - validate immediately
public JsonObject loadConfig(String moduleName) {
    JsonObject config = loadJson(configPath);
    validateSchema(config, moduleName + "-config.schema.json");  // Fail fast
    return config;
}
```

#### Late Validation (Performance)

| File Type              | When      | Rationale        |
|------------------------|-----------|------------------|
| **Large input** (>1MB) | On demand | Performance      |
| **Streaming data**     | Per chunk | Memory efficient |
| **Optional features**  | When used | Skip if unused   |

```java
// ✅ Large data - validate selectively
public void processLargeDataset(Path dataFile) {
    for (JsonObject chunk : readChunks(dataFile, 1000)) {
        if (isCriticalOperation(chunk)) {
            validateSchema(chunk, "data-schema.json");
        }
        processChunk(chunk);
    }
}
```

#### Hybrid Validation

```java
// ✅ Structure early, content late
public void importData(Path inputFile) {
    JsonObject data = loadJson(inputFile);
    validateStructure(data, "structure-schema.json");  // Fast check

    for (JsonObject record : data.getJsonArray("records")) {
        if (needsDetailedValidation(record)) {
            validateSchema(record, "record-schema.json");  // Detailed check
        }
        process(record);
    }
}
```

### Decision Matrix

| File Type    | Size | Validation          | Rationale          |
|--------------|------|---------------------|--------------------|
| Config       | Any  | Early (load)        | MANDATORY          |
| Input data   | <1MB | Early (load)        | Fast, clear errors |
| Input data   | >1MB | Late (on use)       | Performance        |
| API payloads | Any  | Early (before send) | Prevent bad calls  |
| Cached data  | Any  | Skip                | Already validated  |

### Consequences

- Positive: Catch errors early where it matters
- Positive: Performance-conscious for large files
- Negative: Must choose timing strategy
- Mitigation: Decision matrix above

---

## ADR-J012: Frontend Strategy

**Status:** RECOMMENDED
**Date:** 2026-01-04

### Context

numan-edi is primarily an API-driven backend system. However, admin interfaces may be needed for configuration,
monitoring, and manual operations.

### Decision

**Primary**: REST API (possibly GraphQL for complex queries)
**Admin UI**: HTMX for simple admin pages (if needed)

### API First

```
┌─────────────────────────────────────────────────────┐
│                  External Systems                    │
│         (Business Central, Partner Systems)          │
└───────────────────────┬─────────────────────────────┘
                        │ REST/JSON
                        ▼
┌─────────────────────────────────────────────────────┐
│                    numan-edi API                     │
│              (Vert.x HTTP Verticle)                  │
└───────────────────────┬─────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   REST/JSON       GraphQL?        HTMX Admin
   (primary)     (if complex)     (if needed)
```

### HTMX for Admin (MAY use)

HTMX returns HTML fragments from server, not JSON. Suitable for:

- Simple admin dashboards
- Configuration interfaces
- Manual operation triggers
- Monitoring views

```java
// Vert.x route returning HTML fragment
router.get("/admin/status").handler(ctx -> {
    String html = templateEngine.render("status-fragment.html", statusData);
    ctx.response()
       .putHeader("Content-Type", "text/html")
       .end(html);
});
```

**Note**: HTMX is NOT server-side rendering of full pages. It returns fragments that update parts of the page.

### Consequences

- Positive: API-first keeps system clean and testable
- Positive: HTMX avoids JavaScript framework complexity for admin
- Negative: HTMX requires template engine setup
- Mitigation: Only use HTMX if admin UI actually needed

---

## ADR-J013: Variable Naming for Debuggability

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Generic short variable names like `env`, `id`, `val` are hard to search for, cause collisions in debuggers, and don't
stand out in stack traces.

### Decision

**SHOULD** use descriptive compound names that are:

- Searchable (unique enough to grep)
- Clear in stack traces
- Less likely to collide in debugger watch lists

### Implementation

```java
// ✅ CORRECT - Descriptive, searchable
public static ModuleConfig load(String envType, String moduleName) {
    String configPath = buildPath(envType);
    String messageId = generateMessageId();
    String certEmail = extractEmailFromCert(certificate);
    int retryCount = config.getInteger("retry-count");
}

// ❌ WRONG - Too generic, hard to search
public static ModuleConfig load(String env, String name) {
    String path = buildPath(env);
    String id = generateId();
    String email = extractEmail(cert);
    int count = config.getInteger("count");
}
```

### Naming Patterns

| Avoid          | Prefer                         | Rationale                     |
|----------------|--------------------------------|-------------------------------|
| `env`          | `envType`, `environment`       | "env" matches too many things |
| `id`           | `messageId`, `docId`, `certId` | Context-specific ID           |
| `name`         | `moduleName`, `configName`     | What kind of name?            |
| `path`         | `configPath`, `certPath`       | What kind of path?            |
| `count`        | `retryCount`, `messageCount`   | Count of what?                |
| `val`, `value` | `configValue`, `secretValue`   | Value of what?                |
| `e`, `ex`      | `exception`, `error`           | Full word in catch            |
| `i`, `j`       | `index`, or descriptive        | OK in tight loops only        |

### Exception: Loop Variables

Short names acceptable in tight loops with small scope:

```java
// ✅ OK - Small scope, obvious meaning
for (int i = 0; i < items.size(); i++) {
    process(items.get(i));
}

// ✅ BETTER - Even in loops, prefer descriptive
for (String email : certificateEmails) {
    lookupCertificate(email);
}
```

### Consequences

- Positive: Easier debugging, clearer stack traces
- Positive: Grep/search finds exact matches
- Negative: Slightly more verbose
- Mitigation: IDE autocomplete handles length

---

## ADR-J014: Avoiding Singletons

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Singletons create hidden dependencies, make testing difficult, and cause issues with Vert.x's multi-verticle
architecture.

### Decision

**MUST NOT** use singleton pattern for service classes.
**MUST** use dependency injection (constructor injection preferred).

### Implementation

```java
// ✅ CORRECT - Constructor injection
public class E1CertVerticle extends AbstractVerticle {
    private final CertificateCache cache;
    private final LdapClient ldapClient;

    public E1CertVerticle(CertificateCache cache, LdapClient ldapClient) {
        this.cache = cache;
        this.ldapClient = ldapClient;
    }
}

// ✅ CORRECT - Factory method for complex construction
public class CertificateCacheFactory {
    public static CertificateCache create(JsonObject config) {
        int ttlHours = config.getInteger("cache-ttl-hours");
        return new CertificateCache(ttlHours);
    }
}

// ❌ WRONG - Singleton pattern
public class CertificateCache {
    private static CertificateCache INSTANCE;

    public static CertificateCache getInstance() {
        if (INSTANCE == null) {
            INSTANCE = new CertificateCache();
        }
        return INSTANCE;
    }
}

// ❌ WRONG - Static access to shared state
public class ConfigHolder {
    public static JsonObject CONFIG;  // Global mutable state!
}
```

### Why Singletons Fail with Vert.x

| Problem                      | Explanation                               |
|------------------------------|-------------------------------------------|
| **Multi-instance verticles** | Each instance needs own state             |
| **Testing**                  | Can't inject mocks                        |
| **Thread safety**            | Vert.x runs multiple event loops          |
| **Lifecycle**                | Singleton doesn't respect verticle stop() |

### Alternatives

| Instead of        | Use                                 |
|-------------------|-------------------------------------|
| Singleton service | Pass via constructor                |
| Global config     | Pass config to verticle deployment  |
| Shared cache      | Vert.x SharedData or external cache |
| Static utilities  | Instance methods with injected deps |

### Consequences

- Positive: Testable, clear dependencies, Vert.x-safe
- Negative: More constructor parameters
- Mitigation: Records for config bundles, factory methods

---

## ADR-J015: ID Generation Strategy

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Distributed systems need IDs that are:

- Globally unique (no collisions across nodes)
- Locally generatable (no central authority)
- Time-ordered (for efficient database indexing)

### Decision

**MUST** use **UUID v7** for document IDs and message IDs.

### Why UUID v7?

| Feature             | UUID v4 | UUID v7            | Snowflake            |
|---------------------|---------|--------------------|----------------------|
| Globally unique     | Yes     | Yes                | Yes (with node ID)   |
| Locally generatable | Yes     | Yes                | Needs node ID config |
| Time-ordered        | No      | **Yes**            | Yes                  |
| Standard            | Yes     | **Yes (RFC 9562)** | Proprietary          |
| No coordination     | Yes     | Yes                | Needs node ID        |

**UUID v7** is the best choice because:

- Time-ordered prefix = efficient B-tree indexing in Couchbase
- Standard format = wide library support
- No node coordination = simpler deployment

### Implementation

```java
// ✅ CORRECT - UUID v7 (Java 21+ or library)
import java.util.UUID;

// Using library (com.fasterxml.uuid:java-uuid-generator)
import com.fasterxml.uuid.Generators;
import com.fasterxml.uuid.impl.TimeBasedEpochGenerator;

public class IdGenerator {
    private static final TimeBasedEpochGenerator generator =
        Generators.timeBasedEpochGenerator();

    public static String newDocId() {
        return generator.generate().toString();
    }

    public static String newMessageId() {
        return "msg:" + generator.generate().toString();
    }
}

// Usage
String docId = IdGenerator.newDocId();
// Result: "01957123-4567-7def-8901-234567890abc"
// Note: First segment is time-based, sorts chronologically
```

### Document Key Pattern

Combine UUID v7 with document key format (ADR-CB001):

```
{type}::v::{version}::{uuid-v7}

Examples:
- msg::v::1::01957123-4567-7def-8901-234567890abc
- cert::v::1::01957124-1234-7abc-def0-123456789012
```

### When NOT to Use UUID v7

| Case                | Use Instead                     |
|---------------------|---------------------------------|
| Human-readable IDs  | Short codes + UUID v7 suffix    |
| Sequential display  | Add sequence field, sort by it  |
| External system IDs | Use their format, store mapping |

### Consequences

- Positive: Time-ordered, efficient indexing, no coordination
- Positive: Standard format, wide support
- Negative: Longer than Snowflake IDs
- Mitigation: Storage is cheap, clarity is valuable

---

## ADR-J016: Code Comments and Documentation

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Code comments improve maintainability but can become stale or noisy. Java 21+ has enhanced Javadoc features. TXO needs
clear guidelines on when and how to comment.

### Decision

**MUST** document public APIs with Javadoc.
**SHOULD** use inline comments sparingly - code should be self-documenting.
**MUST NOT** add redundant comments that repeat what the code says.

### Javadoc Requirements

#### Public APIs (MUST document)

```java
/**
 * Looks up a certificate for the given email from LDAP.
 *
 * <p>Uses circuit breaker pattern - returns cached certificate if LDAP unavailable.
 * Certificate is validated against CA chain before return.
 *
 * @param email the email address to look up (must be valid format)
 * @return Future containing the certificate, or failed future if not found
 * @throws IllegalArgumentException if email is null or invalid format
 *
 * {@snippet :
 *   Future<Certificate> cert = certService.lookup("partner@example.com");
 *   cert.onSuccess(c -> logger.info("Found cert: {}", c.getSubject()));
 * }
 */
public Future<Certificate> lookup(String email) {
    // ...
}
```

#### Private Methods (SHOULD document if complex)

```java
/**
 * Validates certificate chain against trusted CA roots.
 * Returns true if all certs in chain are valid and not revoked.
 */
private boolean validateChain(List<X509Certificate> chain) {
    // ...
}
```

### Inline Comments

#### When to Use (SHOULD)

```java
// ✅ GOOD - Explains WHY, not WHAT
// Use odd minutes to avoid thundering herd with other polling systems
int pollMinute = 17;

// ✅ GOOD - Explains business rule
// V2 certificates deprecated after 2028-09-14 per Ediel standard
if (cert.getVersion() == 2 && isAfter(V2_GRACE_PERIOD)) {
    logger.warn("V2 certificate deprecated");
}

// ✅ GOOD - Explains non-obvious behavior
// LDAP returns null (not exception) for missing entries
Certificate cert = ldapClient.lookup(email);
if (cert == null) {
    throw new NotFoundException("Certificate not found: " + email);
}
```

#### When NOT to Use (MUST NOT)

```java
// ❌ BAD - Restates the code
// Increment counter by 1
counter++;

// ❌ BAD - Obvious from method name
// Get the email from the certificate
String email = getEmailFromCertificate(cert);

// ❌ BAD - Stale comment (code changed, comment didn't)
// Check if certificate is valid
if (cert.isExpired()) {  // Comment says "valid", code checks "expired"
    // ...
}
```

### TODO Comments

```java
// ✅ GOOD - Linked to tracking system
// TODO(beads-xyz): Add CRL caching when LDAP stabilizes

// ❌ BAD - No tracking, will be forgotten
// TODO: fix this later
```

### Java 21+ Javadoc Features

#### @snippet (Java 18+)

```java
/**
 * Processes incoming email messages.
 *
 * {@snippet :
 *   EmailProcessor processor = new EmailProcessor(config);
 *   processor.process(rawMessage)
 *       .onSuccess(msg -> logger.info("Processed: {}", msg.getId()))
 *       .onFailure(err -> logger.error("Failed", err));
 * }
 */
```

#### Markdown in Javadoc (Preview in Java 23+)

When available, prefer markdown over HTML in Javadoc.

### Consequences

- Positive: Clear public API documentation
- Positive: Self-documenting code with minimal noise
- Positive: Modern Javadoc features improve examples
- Negative: Requires discipline to keep comments current
- Mitigation: Code review checks for stale comments

---

## Summary

These patterns apply to **all TXO Java projects**, regardless of framework:

1. **Hard-fail config**: No silent defaults, throw on missing
2. **Structured logging**: SLF4J only, never print, context for external calls
3. **Naming conventions**: Java standards + TXO config patterns
4. **Project structure**: Gradle multi-module with version catalog
5. **Error handling**: Never swallow, always log, preserve stack traces
6. **Config & secrets**: `config/{module}/{envType}-config.json` + `{envType}-config-secrets.json`, schema validated,
   collision detected
7. **Java version**: SDKMAN for version management, Java 21 for Gradle
8. **Resource placement**: Public certs in JAR, config via mount, secrets via K8s Secrets
9. **Java 21 patterns**: Records, pattern matching, text blocks, sequenced collections
10. **Validation timing**: Config early (MUST), large files late, hybrid for complex
11. **Frontend**: API-first, HTMX for admin pages if needed
12. **Variable naming**: Descriptive compound names (`envType` not `env`)
13. **No singletons**: Constructor injection, factory methods
14. **ID generation**: UUID v7 for document IDs (time-ordered, globally unique)
15. **Code comments**: Javadoc for public APIs, inline for WHY not WHAT

For Vert.x-specific patterns (async, event bus, verticle lifecycle, virtual threads, async DB, circuit breaker), see
`adr-foundation-vertx_v1.2.md`.

---

**Version:** v1.3
**Last Updated:** 2026-01-04
**Domain:** TXO Java Architecture
**Purpose:** Base patterns for all Java projects
