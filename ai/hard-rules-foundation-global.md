# Global Hard Rules (Foundation)

**Scope**: Cross-language, cross-framework rules for all TXO projects
**Version**: 1.1
**Extracted from**: txo-sw-design-adr, txo-java-adr, user requirements
**Updated**: 2026-01-04 (v1.1 - added safe logging, input validation)

---

## MUST (Required)

### GLOBAL-MUST-1: Secrets Never in Git
- MUST NOT commit secrets, API keys, tokens, or credentials to git
- MUST use environment variables or gitignored files for secrets
- Source: ADR-J006

### GLOBAL-MUST-2: Config Hard-Fail on Missing
- MUST fail early and loudly when required config is missing
- MUST NOT use silent defaults for config values
- MUST throw exception on missing required config key
- Source: ADR-J001

### GLOBAL-MUST-3: Large Config JSON Schema Validation
- MUST validate large/complex config files against JSON Schema
- SHOULD validate small config files against JSON Schema
- MUST validate at build-time or read-time (prefer build-time)
- Source: ADR-SD003, user clarification

### GLOBAL-MUST-4: Secrets JSON Flat Structure
- MUST use flat JSON (no nesting) for secrets files
- Rationale: Simpler to validate, less to go wrong
- Source: ADR-J006, user clarification

### GLOBAL-MUST-5: JSON for Config Files
- MUST use JSON format for all config files
- MUST NOT use YAML, TOML, or other formats for config
- Source: user requirement

### GLOBAL-MUST-6: Versioning in Document Keys
- MUST include version in document keys for breaking changes
- Format: `{type}:v:{version}:{identifier}`
- Source: ADR-CB002

### GLOBAL-MUST-7: API Contract Versioning
- MUST include `_version` field in all event bus messages
- MUST support N-1 version during transitions
- Source: ADR-SD002

### GLOBAL-MUST-8: Safe Logging - Redaction Required
- MUST redact sensitive data from logs (tokens, passwords, API keys, certificate private keys)
- MUST have redaction patterns file (`log-redaction-patterns.json`) before logging starts
- MUST fail startup if redaction patterns file is missing
- Source: Python ADR-B009, user requirement

### GLOBAL-MUST-9: Input Validation - Server-Side Required
- MUST validate all input on server-side (client validation is bypassable)
- MUST use allowlisting over denylisting for input validation
- MUST validate input before any processing
- Source: OWASP Input Validation Cheat Sheet

### GLOBAL-MUST-10: Logging Rotation Required
- MUST use rotating file handler for log files
- MUST configure max file size (default: 10MB)
- MUST configure backup count (default: 5 files)
- Rationale: Prevent disk exhaustion from logs
- Source: Python logging patterns

---

## MUST NOT (Forbidden)

### GLOBAL-MUSTNOT-1: Default Config Values in Code
- MUST NOT hardcode default values for config in code
- MUST NOT use `getOrDefault()` for config values
- Exception: External API responses MAY use defaults
- Source: ADR-J001

### GLOBAL-MUSTNOT-2: Silent Config Failures
- MUST NOT silently use fallback values when config missing
- MUST NOT log warning and continue with default
- MUST throw/fail when config missing
- Source: ADR-J001

---

## SHOULD (Recommended)

### GLOBAL-SHOULD-1: kebab-case in Config Files
- SHOULD use kebab-case for config keys (`api-base-url`, not `apiBaseUrl`)
- Rationale: Consistency across environments
- Exception: When consuming external service dumps that use different casing
- Source: ADR-J003

### GLOBAL-SHOULD-2: Odd Minutes for Polling
- SHOULD use odd minutes for polling schedules (03, 07, 13, 17...)
- SHOULD avoid :00, :15, :30, :45 boundaries
- Rationale: Avoid thundering herd with other systems
- Source: ADR-SD001

### GLOBAL-SHOULD-3: Injected Values Underscore Prefix
- SHOULD prefix injected secrets with underscore in merged config
- Example: `db-password` from secrets becomes `_db-password`
- Rationale: Distinguish injected from static config
- Source: ADR-J006

---

## Quick Reference

| Category | Key Rules |
|----------|-----------|
| Secrets | Never in git, flat JSON, underscore prefix |
| Config | Hard-fail on missing, JSON Schema validation, JSON format |
| Versioning | In doc keys for breaking changes, `_version` in messages |
| Naming | kebab-case in config files |
| Polling | Odd minutes to avoid thundering herd |
| Logging | Redact sensitive data, rotation required, fail if patterns missing |
| Input | Server-side validation required, allowlisting over denylisting |