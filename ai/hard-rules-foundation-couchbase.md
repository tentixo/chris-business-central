# Couchbase Hard Rules (Foundation)

**Scope**: Couchbase-specific rules for TXO projects
**Version**: 1.1
**Updated**: 2026-03-07

---

## MUST (Required)

### CB-MUST-1: Document Key Format

- MUST use single colon (`:`) as primary delimiter
- MUST include type prefix in document keys
- Format: `{type}:{qualifiers}:{identifier}`

```
cert:v:1:partner@example.com
msg:in:raw:01957123-4567-7def-8901-234567890abc
chain:supplier-change:partner@example.com:2026-01
```

Source: ADR-CB001

### CB-MUST-2: Version in Key for Breaking Changes

- MUST include major version in document key: `{type}:v:{N}:{id}`
- MUST bump key version for breaking changes (remove field, change type, new required field)
- MUST keep minor version in `_schema` field inside document

```json
{
  "_doc_id": "cert:v:1:partner@example.com",
  "_schema": "1.2",
  "_doc_type": "certificate"
}
```

Source: ADR-CB002

### CB-MUST-3: Standard Document Fields

- MUST include `_doc_id` (document key in body for queries)
- MUST include `_doc_type` (document type for filtering)
- MUST include `_schema` (schema version `{major}.{minor}`)

```json
{
  "_doc_id": "cert:v:1:partner@example.com",
  "_doc_type": "certificate",
  "_schema": "1.0",
  "_created_at": "2026-01-02T10:00:00Z",
  "_updated_at": "2026-01-02T12:00:00Z"
}
```

Source: ADR-CB003

### CB-MUST-4: Expand-Contract for Migrations

- MUST support reading N-1 version during migration
- MUST write new version only (no old format writes)
- MUST NOT delete old version until confidence period passed

```
Phase 1: EXPAND  - New code reads v:1 AND v:2, writes v:2 only
Phase 2: MIGRATE - Background job copies v:1 → v:2
Phase 3: CONTRACT - Remove v:1 read support, delete v:1 docs
```

Source: ADR-CB002

---

## MUST NOT (Forbidden)

### CB-MUSTNOT-1: Forbidden Key Characters

| Character        | Why Forbidden               |
|------------------|-----------------------------|
| Space ` `        | Breaks services, URL issues |
| Backtick `` ` `` | N1QL escaping conflicts     |
| `$`              | N1QL parameter prefix       |
| `%`              | URL encoding conflicts      |
| `&`              | URL parameter delimiter     |
| `"` `'`          | Query string escaping       |
| `\`              | Escape character            |
| `;`              | Query delimiter             |
| Newline, tab     | Control characters          |

**Allowed**: `a-z`, `A-Z`, `0-9`, `:`, `@`, `.`, `-`, `_`
Source: ADR-CB001

### CB-MUSTNOT-2: Breaking Change Without Key Version Bump

- MUST NOT remove field without bumping key version
- MUST NOT change field type without bumping key version
- MUST NOT add required field without bumping key version
  Source: ADR-CB002

---

## SHOULD (Recommended)

### CB-SHOULD-1: Expand-Contract Migration Pattern

```java
// Reading with fallback (during EXPAND phase)
public Future<Certificate> getCertificate(String email) {
    String v2Key = docKeyFor(email, 2);
    String v1Key = docKeyFor(email, 1);

    return repository.get(v2Key)
        .recover(err -> repository.get(v1Key))  // Fallback to v:1
        .map(this:deserialize);
}

// Deserialize handles both versions
private Certificate deserialize(JsonObject doc) {
    String schema = doc.getString("_schema", "1.0");
    if (schema.startsWith("1.")) {
        return deserializeV1(doc);
    } else if (schema.startsWith("2.")) {
        return deserializeV2(doc);
    }
    throw new UnknownSchemaException(schema);
}
```

Source: ADR-CB002

### CB-SHOULD-2: Include Metadata

- SHOULD include `docMeta.createdAt` (ISO-8601 UTC)
- SHOULD include `docMeta.updatedAt` (ISO-8601 UTC)
  Source: ADR-CB003

### CB-SHOULD-3: Max Key Length

- SHOULD keep document keys under 246 bytes
- SHOULD use UTF-8 encoding
  Source: ADR-CB001

---

## Quick Reference

| Category        | Key Rules                                         |
|-----------------|---------------------------------------------------|
| Key Format      | `{type}:v:{version}:{id}`, single-colon delimiter |
| Versioning      | Major in key, minor in `_schema` field            |
| Standard Fields | _doc_id, _doc_type, _schema                       |
| Migration       | Expand-Contract pattern, support N-1              |
| Characters      | No spaces, backticks, $, %, &, quotes             |
