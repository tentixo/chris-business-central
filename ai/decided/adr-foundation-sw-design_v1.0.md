# TXO Software Design ADR

**Version**: 1.0  
**Status**: Active  
**Created**: 2026-01-02  
**Updated**: 2026-01-02  
**Scope**: General software design principles applicable across TXO projects  

---

## ADR-SD001: Polling Time Selection (Anti-Thundering-Herd)

**Status**: Accepted
**Date**: 2026-01-02

### Context

When multiple systems poll shared resources (APIs, databases, CRL endpoints), choosing common polling times causes
thundering herd problems. Humans naturally gravitate toward round numbers when configuring schedules.

### Decision

Choose **odd minutes** for polling schedules, avoiding quarter-hour boundaries.

| Quality   | Minutes                                                                                    | Rationale                     |
|-----------|--------------------------------------------------------------------------------------------|-------------------------------|
| **Best**  | 03, 07, 09, 11, 13, 17, 19, 21, 23, 27, 29, 31, 33, 37, 39, 41, 43, 47, 49, 51, 53, 57, 59 | Odd numbers humans don't pick |
| **Avoid** | 15, 45                                                                                     | Quarter hours - common choice |
| **Worst** | 00, 30                                                                                     | Everyone's default            |

### Examples

| Use Case               | Bad                | Good               |
|------------------------|--------------------|--------------------|
| CRL refresh (hourly)   | `:00`              | `:07` or `:37`     |
| Health check (5 min)   | `:00, :05, :10...` | `:03, :08, :13...` |
| Cache refresh (30 min) | `:00, :30`         | `:07, :37`         |
| Daily batch job        | `00:00`            | `03:17`            |

### Applies To

- CRL/certificate polling
- Health checks against shared endpoints
- Cache refresh schedules
- Batch job scheduling
- Any periodic task hitting shared infrastructure

### Consequences

**Positive**:

- Distributes load across time windows
- Reduces contention on shared resources
- Avoids correlation with other systems' schedules

**Negative**:

- Slightly harder to remember schedules
- May need documentation for ops team

### Implementation Notes

When configuring polling intervals:

```java
// Bad: Poll at top of hour
scheduler.scheduleAtFixedRate(task, 0, 1, TimeUnit.HOURS);

// Good: Poll at :07 past each hour
long initialDelay = calculateDelayToMinute(7);
scheduler.scheduleAtFixedRate(task, initialDelay, 1, TimeUnit.HOURS);
```

---

## ADR-SD002: Event Bus Contract Versioning

**Status**: Accepted
**Date**: 2026-01-02

### Context

During rolling deployments or multi-version operation, producers may send different message formats. Consumers must
handle both simultaneously without breaking.

### Decision

**Hybrid approach** combining version field with additive-only changes:

1. **Always include `_version`** in messages (format: `"major.minor"`)
2. **Additive changes** don't bump version - consumer ignores unknown fields
3. **Breaking changes** bump major version + support N-1 for transition period
4. **Central registry** documents all contracts

### Message Structure

```json 
{
  "_version": "2.0",
  "_type": "CertResponse",
  "code": "OK"
}
```

### Consumer Handling

```java
void handleMessage(JsonObject json) {
    String version = json.getString("_version", "1.0");
    int major = parseMajor(version);

    switch (major) {
        case 1 -> handleV1(json);
        case 2 -> handleV2(json);
        default -> {
            if (major > CURRENT_MAJOR) {
                handleLatest(json);  // Forward compatible attempt
            } else {
                reject("Unsupported version: " + version);
            }
        }
    }
}
```

### Version Bump Rules

| Change Type                     | Version Bump | Example                        |
|---------------------------------|--------------|--------------------------------|
| Add optional field              | None         | Add `message` field            |
| Add required field with default | Minor        | Add `retryAfter` (default: 1h) |
| Rename field                    | Major        | `cert` → `v2`, `v3`            |
| Remove field                    | Major        | Remove `cert`                  |
| Change field type               | Major        | `String` → `Object`            |

### Transition Period

- Support N-1 major version for **2 release cycles** minimum
- Log warnings when receiving old versions
- Remove old handler after transition period

### Consequences

**Positive**:

- Explicit version makes debugging easier
- Graceful rolling deployments
- Clear migration path

**Negative**:

- Slight message overhead (`_version` field)
- Consumer complexity for multi-version support

---

## ADR-SD003: JSON Schema Validation

**Status**: Accepted
**Date**: 2026-01-02

### Context

Config files and event bus contracts are JSON. Validation catches errors early. Question: when to validate?

### Decision

| Artifact                 | Validation Time    | Rationale                                |
|--------------------------|--------------------|------------------------------------------|
| **Config files**         | Compile/build time | Always clean at runtime, faster startup  |
| **Contracts (outgoing)** | Unit tests         | Verify our messages are schema-compliant |
| **Contracts (incoming)** | Dev/test mode only | Runtime validation too slow for prod     |

### Implementation

#### Config Files (Build Time)

```xml
<!-- Maven plugin validates JSON against schema during build -->
<plugin>
    <groupId>com.groupon.maven</groupId>
    <artifactId>json-schema-validator-maven-plugin</artifactId>
    <executions>
        <execution>
            <phase>validate</phase>
            <goals>
                <goal>validate</goal>
            </goals>
            <configuration>
                <schemas>
                    <schema>config/schema/shared-config.schema.json</schema>
                </schemas>
            </configuration>
        </execution>
    </executions>
</plugin>
```

#### Contracts (Testing)

```java
@Test
void certResponseMatchesSchema() {
    CertResponse response = createTestResponse();
    JsonObject json = response.toJson();

    Schema schema = loadSchema("e1cert-response.schema.json");
    schema.validate(json);  // Throws on mismatch
}
```

#### Runtime (Dev Mode Only)

```java
if (config.isDevMode()) {
    contractValidator.validate(message, "CertResponse");
}
```

### Schema Location

Central registry in `contracts/` directory:

```
contracts/
├── e1-cert/
│   ├── cert-request.schema.json
│   ├── cert-response.schema.json
│   └── README.md  (contract documentation)
├── e1-receive/
│   └── ...
└── shared/
    └── common-types.schema.json
```

### Consequences

**Positive**:

- Config errors caught at build time (CI fails, not runtime)
- Contract compliance verified in tests
- Central documentation of all message formats
- No runtime overhead in production

**Negative**:

- Schema files to maintain
- Build dependency on validator plugin

---

## ADR-SD004: (Reserved for future)

<!-- Template for future ADRs:

## ADR-SDXXX: Title

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD

### Context
[Why is this decision needed?]

### Decision
[What is the decision?]

### Consequences
[What are the results of this decision?]

-->

---

## Document History

| Version | Date       | Author   | Changes                                                                                |
|---------|------------|----------|----------------------------------------------------------------------------------------|
| 1.0     | 2026-01-02 | AI/Human | Initial: ADR-SD001 polling times, ADR-SD002 contract versioning, ADR-SD003 JSON Schema |
