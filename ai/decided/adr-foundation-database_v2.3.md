# TXO Database Architecture Decision Records

Reusable patterns for Couchbase and TimescaleDB databases.

**Status**: Living document
**Version:** v2.3
**Created**: 2026-01-02
**Updated**: 2026-03-07
**Scope**: Any TXO project using Couchbase and/or TimescaleDB

---

## Database Selection

| Database        | Purpose        | Data Characteristics                               |
|-----------------|----------------|----------------------------------------------------|
| **Couchbase**   | Document store | Entities, metadata, current state, relationships   |
| **TimescaleDB** | Time series    | High-volume temporal data, aggregations, retention |

---

# Part 1: Couchbase (CB)

## ADR-CB001: Document Key Conventions

**Status:** DECIDED
**Date:** 2026-01-02

### Context

Couchbase document keys (primary keys) are developer-assigned. We need consistent conventions for:

- Readability and debugging
- Query patterns (prefix scans)
- Version management
- Safe character usage

### Decision

**Key Format**: `{type}:{qualifiers}:{identifier}`

**Delimiter**: Single colon (`:`) - unambiguous, avoids collision with timestamps/URIs

**Examples**:

```
cert:v:1:partner@example.com
msg:in:raw:01957123-4567-7def-8901-234567890abc
user:123
chain:supplier-change:partner@example.com:2026-01
```

**Character Rules**:

| Status       | Characters          | Notes                            |
|--------------|---------------------|----------------------------------|
| **ALLOWED**  | `a-z`, `A-Z`, `0-9` | Alphanumeric                     |
| **ALLOWED**  | `:`                 | Primary delimiter (single colon) |
| **ALLOWED**  | `@`                 | Required for emails              |
| **ALLOWED**  | `.`                 | Domain names, version numbers    |
| **ALLOWED**  | `-`                 | UUIDs, dates                     |
| **ALLOWED**  | `_`                 | Alternative delimiter            |
| **MUST NOT** | Space ` `           | Breaks services, URL issues      |
| **MUST NOT** | Backtick `` ` ``    | N1QL escaping conflicts          |
| **MUST NOT** | `$`                 | N1QL parameter prefix            |
| **MUST NOT** | `%`                 | URL encoding conflicts           |
| **MUST NOT** | `&`                 | URL parameter delimiter          |
| **MUST NOT** | `"` `'`             | Query string escaping            |
| **MUST NOT** | `\`                 | Escape character                 |
| **MUST NOT** | `;`                 | Query delimiter                  |
| **MUST NOT** | Newline, tab        | Control characters               |

**Encoding**: SHOULD use UTF-8. Max length 246 bytes.

### Consequences

- Positive: Consistent, debuggable keys
- Positive: Safe for N1QL queries
- Positive: Prefix scans work (`cert:v:1:*`)

---

## ADR-CB002: Data Structure Versioning (Expand-Contract)

**Status:** DECIDED
**Date:** 2026-01-02

### Context

Couchbase is schema-less, but application code expects specific document structures. When structures change, we need:

1. Zero-downtime deployments (old/new code coexist)
2. Rollback capability without database restore
3. Gradual migration path

### Decision

**SHOULD use Expand-Contract pattern** for data structure migrations.

**MUST use version in document key** for breaking changes.

#### Two-Level Versioning

| Level     | Location        | Format            | When to Change                                    |
|-----------|-----------------|-------------------|---------------------------------------------------|
| **Major** | `_doc_id`       | `v:{n}`           | Breaking changes (old code can't read new format) |
| **Minor** | `_schema` field | `{major}.{minor}` | Additive changes (old code ignores new fields)    |

**Example**:

```json
{
  "_doc_id": "cert:v:1:partner@example.com",
  "_schema": "1.2",
  "_doc_type": "certificate"
}
```

**Version Matching**: Major version in key matches major in `_schema`:

- `cert:v:1:...` → `_schema: 1.0`, `1.1`, `1.2`
- `cert:v:2:...` → `_schema: 2.0`, `2.1`

#### Breaking vs Additive Changes

| Change Type  | Example                                       | Key Version | _schema   |
|--------------|-----------------------------------------------|-------------|-----------|
| **Breaking** | Remove field, change type, new required field | v:1 → v:2   | 2.0       |
| **Additive** | New optional field with default               | v:1 (same)  | 1.0 → 1.1 |

#### Expand-Contract Pattern

**Phase 1: EXPAND (deploy new code)**

```
┌─────────────────────────────────────────────────────────┐
│ New code deployed (rolling)                             │
│ - Reads: v:1 AND v:2 formats                            │
│ - Writes: v:2 format only                               │
│ - Old code still running: reads v:1, writes v:1         │
└─────────────────────────────────────────────────────────┘
```

**Phase 2: MIGRATE (background job)**

```
┌─────────────────────────────────────────────────────────┐
│ Migration job runs                                      │
│ - Copies cert:v:1:email → cert:v:2:email                │
│ - Both versions coexist                                 │
│ - Old code: still works with v:1 docs                   │
│ - New code: prefers v:2, falls back to v:1              │
└─────────────────────────────────────────────────────────┘
```

**Phase 3: CONTRACT (cleanup)**

```
┌─────────────────────────────────────────────────────────┐
│ After confidence period                                 │
│ - Remove v:1 read support from code                     │
│ - Delete v:1 documents                                  │
│ - Rollback no longer possible without restore           │
└─────────────────────────────────────────────────────────┘
```

#### Rollback Scenario

If v:2 code has bugs after EXPAND phase:

1. Roll back to v:1 code (standard deploy rollback)
2. v:1 code reads v:1 docs (still exist)
3. v:2 docs are orphaned but harmless
4. Fix bug, redeploy v:2

#### Code Example (Java)

```java
// Document key helper
public static String docKeyFor(String email, int version) {
    return "cert:v:" + version + ":" + email.toLowerCase(Locale.ROOT);
}

// Reading with fallback (during EXPAND phase)
public Future<Certificate> getCertificate(String email) {
    String v2Key = docKeyFor(email, 2);
    String v1Key = docKeyFor(email, 1);

    return repository.get(v2Key)
            .recover(err -> repository.get(v1Key))  // Fallback to v:1
            .map(this:deserialize);
}

// Deserialize handles both _schema versions
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

### Consequences

- Positive: Zero-downtime deployments
- Positive: Safe rollback during EXPAND/MIGRATE phases
- Positive: Gradual migration, no big-bang
- Negative: Temporary storage increase (both versions)
- Negative: Code complexity during migration
- Mitigation: Contract phase cleans up; migration code is temporary

---

## ADR-CB003: Standard Document Fields

**Status:** DECIDED
**Date:** 2026-01-02

### Context

Documents need consistent metadata for debugging, auditing, and versioning.

### Decision

**Standard fields for all documents**:

```json
{
  "_doc_id": "cert:v:1:partner@example.com",
  "_doc_type": "certificate",
  "_schema": "1.0",
  "_created_at": "2026-01-02T10:00:00Z",
  "_updated_at": "2026-01-02T12:00:00Z"
}
```

| Field         | Required | Description                                    |
|---------------|----------|------------------------------------------------|
| `_doc_id`     | MUST     | Document key (also stored in body for queries) |
| `_doc_type`   | MUST     | Document type for filtering                    |
| `_schema`     | MUST     | Schema version (`{major}.{minor}`)             |
| `_created_at` | SHOULD   | ISO-8601 creation timestamp UTC                |
| `_updated_at` | SHOULD   | ISO-8601 last update timestamp UTC             |

### Consequences

- Positive: Consistent structure across all documents
- Positive: Easy debugging and auditing
- Positive: Version tracking for migrations

---

## ADR-CB004: Document Identifier Strategy

**Status:** DECIDED
**Date:** 2026-01-11

### Context

Document keys follow the format `{type}:v:{version}:{qualifiers}:{identifier}` (ADR-CB001).
This ADR defines what type of `{identifier}` to use for different entity types.

**Identifier types available**:

| Type            | Example                                | Uniqueness             | Stability          | Size     |
|-----------------|----------------------------------------|------------------------|--------------------|----------|
| **UUIDv7**      | `019471a3-5678-7abc-9def-012345678901` | Global, collision-free | Immutable          | 36 chars |
| **UUIDv4**      | `550e8400-e29b-41d4-a716-446655440000` | Global, collision-free | Immutable          | 36 chars |
| **External ID** | `735999000000000001` (GSRN)            | External system        | External-dependent | Varies   |
| **Legal ID**    | `198501011234` (personnummer)          | Country-guaranteed     | Mostly stable*     | Fixed    |
| **Semantic**    | `anders`, `acme`                       | Manual assignment      | **Mutable**        | Variable |
| **Composite**   | `se:2024-001`, `spot_flex:2025`        | Scoped                 | Depends            | Variable |

*Legal IDs can change: personnummer corrections, org restructuring

**Problems with semantic keys**:

- `el_end_cust:v:1:se:anders` - Name "anders" can change
- `numan_el_sup:v:1:se:acme` - Trade name "acme" can change
- Renaming requires key migration (expensive)

### Decision

#### MUST: Use UUIDv7 for Generated Entities

**MUST use UUIDv7** for entities created by the system:

| Entity Type   | Key Pattern                                        | Example                                                  |
|---------------|----------------------------------------------------|----------------------------------------------------------|
| Agreements    | `el_sup_agr:v:1:{market}:{uuidv7}`                 | `el_sup_agr:v:1:se:019471a3-5678-7abc-9def-012345678901` |
| Contracts     | `el_sup_contract:{ind\|org}:v:1:{market}:{uuidv7}` | `el_sup_contract:ind:v:1:se:019471a3...`                 |
| Customers     | `el_end_cust:v:1:{market}:{uuidv7}`                | `el_end_cust:v:1:se:019471a3...`                         |
| Messages      | `msg:in:raw:{uuidv7}`                              | `msg:in:raw:019471a3...`                                 |
| Conversations | `conv:v:1:{uuidv7}`                                | `conv:v:1:019471a3...`                                   |

**Why UUIDv7** (not UUIDv4 or Snowflake):

- **Time-ordered**: First 48 bits = millisecond timestamp → B-tree friendly
- **No coordination**: Unlike Snowflake, no worker-id assignment needed
- **Cross-region safe**: Essential for XDCR (3-region Couchbase)
- **Standard**: RFC 9562 (2024), well-supported in libraries
- **Collision-free**: Random component ensures uniqueness

**UUIDv7 structure**:

```
019471a3-5678-7abc-9def-012345678901
├──────────────┤ ├──────────────────┤
   timestamp      random (version 7)
   (48 bits)         (74 bits)
```

#### SHOULD: Use External IDs When Externally Assigned

**SHOULD use external identifiers** when they are:

1. Assigned by an authoritative external system
2. Immutable or rarely change
3. Required for interoperability

| Entity Type         | External ID     | Key Pattern                          | Example                                |
|---------------------|-----------------|--------------------------------------|----------------------------------------|
| Metering Point      | GSRN (18-digit) | `el_mp:v:1:{market}:{gsrn}`          | `el_mp:v:1:se:735999000000000001`      |
| Network Operator    | GLN (13-digit)  | `el_net_op:v:1:{market}:gln:{gln}`   | `el_net_op:v:1:se:gln:7350000000100`   |
| Balance Responsible | GLN             | `el_bal_resp:v:1:{market}:gln:{gln}` | `el_bal_resp:v:1:se:gln:7350000000200` |
| Metering Operator   | GLN             | `el_met_op:v:1:{market}:gln:{gln}`   | `el_met_op:v:1:se:gln:7350000000300`   |

**Note**: `gln:` prefix makes it explicit that a GLN is used, not a UUIDv7.

#### SHOULD: Use Semantic Keys for Reference/Config Data

**SHOULD use semantic keys** for low-volume, human-managed configuration:

| Entity Type    | Key Pattern                              | Example                          | Rationale                 |
|----------------|------------------------------------------|----------------------------------|---------------------------|
| General Terms  | `terms:general:v:{version}`              | `terms:general:v:3`              | Version IS the identity   |
| Product Terms  | `product:{code}:v:{version}`             | `product:spot_flex:v:2`          | Product code is stable    |
| Price Schedule | `price:{code}:{year}`                    | `price:spot_flex:2025`           | Product + year is natural |
| Country Market | `el_ref_market:v:1:{country}`            | `el_ref_market:v:1:se`           | ISO country code          |
| Price Area     | `el_ref_price_area:v:1:{country}:{code}` | `el_ref_price_area:v:1:se:se4`   | Standard codes            |
| Grid Area      | `el_ref_grid_area:v:1:{country}:{code}`  | `el_ref_grid_area:v:1:se:ga-001` | Assigned codes            |

#### MUST NOT: Use Mutable Data in Keys

**MUST NOT use** in document keys:

- Names (personal or company names)
- Addresses
- Email addresses (for person entities - OK for certificate lookup)
- Phone numbers
- Any data that can be corrected/updated

**Exception**: Email is allowed in `cert:v:1:{email}` because:

1. Certificate lookup is BY email (email is the query parameter)
2. If email changes, a new certificate is needed anyway

#### MAY: Use Legal IDs with Caution

**MAY use legal identifiers** (personnummer, org-id) only when:

1. The entity IS the legal identity (not referencing it)
2. You accept the migration cost if ID changes
3. There's a strong business reason

| Scenario                                 | Recommendation                           |
|------------------------------------------|------------------------------------------|
| IND_ORG_PERSON service (shared identity) | MAY use personnummer/org-id              |
| EL_END_CUSTOMER (tenant customer record) | MUST use UUIDv7, store legal_id as field |
| Certificate lookup                       | SHOULD use email (the lookup key)        |

**Rationale**: Legal IDs do change (personnummer corrections, org mergers). Using UUIDv7 and storing legal_id as a
queryable field avoids key migrations.

### UUIDv7 Generation (Java)

```java
// Using java-uuid-generator library (com.fasterxml.uuid:java-uuid-generator)

import com.fasterxml.uuid.Generators;
import com.fasterxml.uuid.impl.TimeBasedEpochGenerator;

public class IdGenerator {
    private static final TimeBasedEpochGenerator generator =
            Generators.timeBasedEpochGenerator();

    public static String newId() {
        return generator.generate().toString();
    }

    public static String docKey(String type, int version, String market) {
        return String.format("%s:v:%d:%s:%s", type, version, market, newId());
    }
}

// Usage
String key = IdGenerator.docKey("el_end_cust", 1, "se");
// → "el_end_cust:v:1:se:019471a3-5678-7abc-9def-012345678901"
```

### Performance Characteristics

| Aspect                  | UUIDv7                    | Semantic            | External ID        |
|-------------------------|---------------------------|---------------------|--------------------|
| Insert order            | Sequential (time-based) ✅ | Random              | Depends            |
| B-tree fragmentation    | Minimal ✅                 | High                | Varies             |
| Key size                | 36 chars                  | Variable            | Fixed              |
| Human debugging         | Needs lookup              | Easy                | Semi-readable      |
| Cross-region uniqueness | Guaranteed ✅              | Manual coordination | External guarantee |
| Range queries by time   | Natural ✅                 | Not possible        | Not possible       |

### Consequences

**Positive**:

- Consistent key generation across codebase
- No coordination needed for distributed ID generation
- Time-ordering benefits for queries and debugging
- No key migrations when mutable data changes

**Negative**:

- UUIDv7 keys are not human-readable
- Slightly larger than sequential integers

**Mitigations**:

- Store human-readable identifiers (name, email, customer_id) as document fields
- Use these fields in UI and logs
- Key is primarily for database operations

---

## ADR-CB005: App-Scoped Keys (Multi-App Couchbase)

**Status:** DECIDED
**Date:** 2026-01-20

### Context

Multiple applications may share a Couchbase cluster. Keys must:

1. Avoid collisions between applications
2. Support queries scoped to a single application
3. Allow prefix-based filtering

### Decision

**SHOULD use app-scoped keys** when multiple applications share a Couchbase bucket.

**Key Format**: `{doc-type}:{app-name}:v:{version}:{identifier}`

| Component      | Purpose               | Example                               |
|----------------|-----------------------|---------------------------------------|
| `{doc-type}`   | Structural type       | `node`, `edge`, `cert`, `msg`         |
| `{app-name}`   | Application namespace | `iso-graph`, `el-billing`, `cert-mgr` |
| `v:{version}`  | Breaking version      | `v:1`, `v:2`                          |
| `{identifier}` | Unique identifier     | UUIDv7, external ID, or semantic      |

**Examples**:

```
node:iso-graph:v:1:019471a3-5678-7abc-9def-012345678901
edge:iso-graph:v:1:019471a3...--019471b4...
cert:cert-mgr:v:1:partner@example.com
msg:el-billing:v:1:019471a3-5678-7abc-9def-012345678901
```

**App-scoped query**:

```sql
SELECT *
FROM bucket
WHERE _doc_id LIKE 'node:iso-graph:v:1:%';
```

#### When to Use App Scoping

| Scenario                    | App Scoping | Rationale                |
|-----------------------------|-------------|--------------------------|
| Shared multi-tenant bucket  | MUST        | Prevent collisions       |
| Dedicated single-app bucket | MAY         | Future-proofing          |
| Development/testing         | SHOULD      | Match production pattern |

### Consequences

- Positive: Clear namespace separation
- Positive: Prefix scans work per-app
- Positive: Easy to identify document ownership
- Negative: Longer keys (8-15 chars added)
- Mitigation: Key length is negligible vs document size

---

## ADR-CB006: Graph Document Patterns (Nodes and Edges)

**Status:** DECIDED
**Date:** 2026-01-20

### Context

Graph databases store two fundamental document types:

1. **Nodes**: Entities with properties
2. **Edges**: Relationships between nodes

Couchbase can model graphs using documents with SQL++ `WITH RECURSIVE` for traversal.

### Decision

#### Node Key Format

**Key Format**: `node:{app}:v:{version}:{identifier}`

**Identifier strategy by node type**:

| Node Category                 | Identifier Type      | Example                                |
|-------------------------------|----------------------|----------------------------------------|
| **External reference data**   | Semantic/external ID | `iso-5-15`, `gln:7350000000100`        |
| **System-generated entities** | UUIDv7               | `019471a3-5678-7abc-9def-012345678901` |
| **Configuration/reference**   | Semantic             | `tame-tier0`, `price-area-se4`         |

**Rule**: If the entity is created by users/system and may change over time → UUIDv7.
If the entity represents external standard data or stable reference → semantic ID.

**Examples**:

```
node:iso-graph:v:1:iso-5-15              (ISO control - external standard)
node:iso-graph:v:1:tame-tier0            (framework - stable reference)
node:iso-graph:v:1:019471a3-5678-7abc... (task - system-generated)
node:iso-graph:v:1:019471b4-6789-8bcd... (deliverable - system-generated)
```

#### Edge Key Format

**Key Format**: `edge:{app}:v:{version}:{source-id}--{target-id}`

**Delimiter**: Double hyphen (`--`) separates source and target IDs.

**Examples**:

```
edge:iso-graph:v:1:iso-5-15--tame-tier0
edge:iso-graph:v:1:019471a3...--019471b4...
```

**Why composite key for edges**:

- Natural uniqueness (one edge per source-target pair per type)
- Efficient lookup by source or target with prefix scan
- Human-readable for debugging

**Edge with same endpoints but different types**: Store edge type in document body (`_edge_type`), not key. This allows
multiple relationship types between same nodes.

#### Node Document Structure

```json
{
  "_doc_id": "node:iso-graph:v:1:019471a3-5678-7abc-9def-012345678901",
  "_doc_type": "node",
  "_schema": "1.0",
  "_node_type": "task",
  "_node_schema": "1.0",
  "id": "019471a3-5678-7abc-9def-012345678901",
  "structure": {
    ...
  },
  "type_data": {
    ...
  }
}
```

#### Edge Document Structure

```json
{
  "_doc_id": "edge:iso-graph:v:1:019471a3...--019471b4...",
  "_doc_type": "edge",
  "_schema": "1.0",
  "_edge_type": "produces",
  "_edge_schema": "1.0",
  "sourceId": "node:iso-graph:v:1:019471a3...",
  "targetId": "node:iso-graph:v:1:019471b4...",
  "type_data": {
    ...
  }
}
```

#### Graph Traversal Index Strategy

```sql
-- Node lookup by type
CREATE INDEX idx_node_type ON bucket (_node_type)
    WHERE _doc_type = 'node' AND _doc_id LIKE 'node:iso-graph:%';

-- Edge source lookup (forward traversal)
CREATE INDEX idx_edge_source ON bucket (sourceId)
    WHERE _doc_type = 'edge' AND _doc_id LIKE 'edge:iso-graph:%';

-- Edge target lookup (reverse traversal)
CREATE INDEX idx_edge_target ON bucket (targetId)
    WHERE _doc_type = 'edge' AND _doc_id LIKE 'edge:iso-graph:%';
```

### Consequences

- Positive: Clear node/edge distinction
- Positive: Efficient graph traversal with indexes
- Positive: UUIDv7 for mutable entities, semantic for stable references
- Positive: Composite edge keys prevent duplicates
- Negative: Edge keys can be long with two UUIDs
- Mitigation: Still within 246-byte limit, compression handles it

---

# Part 2: TimescaleDB (TsDB)

## ADR-TS001: TimescaleDB Purpose and Scope

**Status:** DECIDED
**Date:** 2026-01-09

### Context

Time series data (consumption readings, spot prices) has different access patterns than entity data:

- High write volume (millions of readings)
- Time-range queries (last 30 days, year-over-year)
- Aggregations (hourly → daily → monthly rollups)
- Retention policies (delete old granular data, keep aggregates)

Couchbase is not optimized for these patterns.

### Decision

**Use TimescaleDB for time series data**:

| Data Type       | Storage     | Rationale                                  |
|-----------------|-------------|--------------------------------------------|
| `usage_report`  | TimescaleDB | High volume, time-range queries, retention |
| `spot_price`    | TimescaleDB | Time series, aggregations                  |
| Entity metadata | Couchbase   | Relationships, current state               |

**TimescaleDB capabilities used**:

- Hypertables (automatic partitioning by time)
- Continuous aggregates (pre-computed rollups)
- Retention policies (automatic data lifecycle)
- Compression (reduce storage for old data)

### Consequences

- Positive: Optimized time-range queries
- Positive: Built-in retention and aggregation
- Positive: Reduced Couchbase storage
- Negative: Two databases to manage
- Negative: Cross-database joins require application logic

---

## ADR-TS002: Cross-Database Linking (CB ↔ TsDB)

**Status:** DECIDED
**Date:** 2026-01-09

### Context

Entity data lives in Couchbase, time series in TimescaleDB. We need to:

1. Link time series records to entities
2. Join data for reports
3. Maintain referential integrity

### Decision

**Use UUID v7 as shared identifier**:

```
┌───────────────────────────────────────────────────────────────────────┐
│ Couchbase                        │ TimescaleDB                        │
├───────────────────────────────────────────────────────────────────────┤
│ metering_point                   │ usage_report                       │
│ ├─ _idoc_d: "mp:735999..."       │ ├─ metering_point_id: "735999..."  │
│ ├─ gsrn: "735999..."             │ ├─ timestamp: 2026-01-09T10:00:00Z │
│ └─ (metadata)                    │ ├─ value_kwh: 1.234                │
│                                  │ └─ (time series data)              │
└───────────────────────────────────────────────────────────────────────┘
```

**Linking strategies**:

| Strategy       | Link Field        | Use Case                     |
|----------------|-------------------|------------------------------|
| **GSRN**       | `gsrn` (18-digit) | Metering point → usage data  |
| **Price Area** | `price_area_id`   | Price area → spot prices     |
| **UUID v7**    | `entity_id`       | Generic entity → time series |

**Why UUID v7**:

- Time-ordered (first 48 bits = timestamp)
- Globally unique
- Works in both PostgreSQL and Couchbase
- Sortable by creation time

#### Query Pattern (Application Layer Join)

```java
// 1. Fetch entity from Couchbase
MeteringPoint mp = couchbase.get("mp:735999...");

// 2. Fetch time series from TimescaleDB
List<UsageReport> readings = timescale.query("""
        SELECT timestamp, value_kwh
        FROM usage_report
        WHERE metering_point_id = ?
          AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp
        """, mp.gsrn(), startDate, endDate);

// 3. Combine in application
return new

MeteringPointWithUsage(mp, readings);
```

#### Report Generation Pattern

```java
// For reports needing both metadata and time series:
// 1. Query TimescaleDB for aggregated data
Map<String, BigDecimal> monthlyUsage = timescale.query("""
                SELECT metering_point_id, SUM(value_kwh) as total
                FROM usage_report
                WHERE timestamp >= DATE_TRUNC('month', NOW() - INTERVAL '1 year')
                GROUP BY metering_point_id
                """);

// 2. Enrich with Couchbase metadata (batch fetch)
List<String> mpIds = monthlyUsage.keySet().stream()
        .map(gsrn -> "mp:" + gsrn)
        .toList();
Map<String, MeteringPoint> metadata = couchbase.getBatch(mpIds);

// 3. Join in application
return monthlyUsage.

entrySet().

stream()
    .

map(e ->new

Report(metadata.get(e.getKey()),e.

getValue()))
        .

toList();
```

### Consequences

- Positive: Clear separation of concerns
- Positive: Each database used for its strengths
- Positive: UUID v7 provides time-ordering bonus
- Negative: No database-level referential integrity
- Negative: Application must handle joins
- Mitigation: Service layer abstracts the complexity

---

## ADR-TS003: Retention Policies

**Status:** DECIDED
**Date:** 2026-01-09

### Context

Time series data grows continuously. Users need:

- Recent data at full resolution (15-min or hourly)
- Historical data at lower resolution (daily, monthly)
- Eventually, old data can be deleted

### Decision

**Tiered retention with continuous aggregates**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Age          │ Resolution    │ Storage                          │
├─────────────────────────────────────────────────────────────────┤
│ 0-6 months   │ 15-min/hourly │ usage_report (raw)               │
│ 6-12 months  │ hourly        │ usage_report_hourly (aggregate)  │
│ 1-7 years    │ daily         │ usage_report_daily (aggregate)   │
│ 7+ years     │ monthly       │ usage_report_monthly (aggregate) │
└─────────────────────────────────────────────────────────────────┘
```

**TimescaleDB implementation**:

```sql
-- Create continuous aggregates
CREATE
MATERIALIZED VIEW usage_report_hourly
WITH (timescaledb.continuous) AS
SELECT metering_point_id,
       time_bucket('1 hour', timestamp) AS hour,
       SUM(value_kwh)                   AS total_kwh,
       AVG(value_kwh)                   AS avg_kwh,
       COUNT(*)                         AS reading_count
FROM usage_report
GROUP BY metering_point_id, time_bucket('1 hour', timestamp);

-- Retention policy: drop raw data after 6 months
SELECT add_retention_policy('usage_report', INTERVAL '6 months');

-- Compression policy: compress data older than 7 days
SELECT add_compression_policy('usage_report', INTERVAL '7 days');
```

**Spot price retention**:

| Data              | Retention | Rationale                |
|-------------------|-----------|--------------------------|
| Raw hourly prices | 2 years   | Billing disputes, audits |
| Daily aggregates  | 10 years  | Historical analysis      |

### Consequences

- Positive: Storage costs controlled
- Positive: Query performance maintained (smaller datasets)
- Positive: Users get appropriate resolution
- Negative: Raw data eventually lost
- Mitigation: Aggregates preserve statistical value

---

## ADR-TS004: TimescaleDB Schema

**Status:** DECIDED
**Date:** 2026-01-09

### Context

Define the schema for time series tables in TimescaleDB.

### Decision

**usage_report table**:

```sql
CREATE TABLE usage_report ( id UUID DEFAULT gen_random_uuid
(
),
    metering_point_id VARCHAR
(
    18
) NOT NULL, -- GSRN
    timestamp TIMESTAMPTZ NOT NULL,
    value_kwh DECIMAL
(
    12,
    6
) NOT NULL,
    quality VARCHAR
(
    10
) DEFAULT 'measured', -- measured | estimated | corrected
    source VARCHAR
(
    50
), -- DSO identifier
    received_at TIMESTAMPTZ DEFAULT NOW
(
),
    PRIMARY KEY
(
    metering_point_id,
    timestamp
)
    );

-- Convert to hypertable
SELECT create_hypertable('usage_report', 'timestamp');

-- Index for entity lookups
CREATE INDEX idx_usage_mp ON usage_report (metering_point_id, timestamp DESC);
```

**spot_price table**:

```sql
CREATE TABLE spot_price ( id UUID DEFAULT gen_random_uuid
(
),
    price_area_id VARCHAR
(
    10
) NOT NULL, -- SE1, SE2, SE3, SE4, etc.
    timestamp TIMESTAMPTZ NOT NULL,
    price_eur_mwh DECIMAL
(
    10,
    2
) NOT NULL,
    currency VARCHAR
(
    3
) DEFAULT 'EUR',
    source VARCHAR
(
    20
) DEFAULT 'nord_pool',
    fetched_at TIMESTAMPTZ DEFAULT NOW
(
),
    PRIMARY KEY
(
    price_area_id,
    timestamp
)
    );

-- Convert to hypertable
SELECT create_hypertable('spot_price', 'timestamp');

-- Index for price area lookups
CREATE INDEX idx_price_area ON spot_price (price_area_id, timestamp DESC);
```

### Consequences

- Positive: Optimized for time-range queries
- Positive: Automatic partitioning
- Positive: Composite primary key prevents duplicates

---

# Summary

## Couchbase Patterns

1. **Key conventions**: Single-colon delimiter, safe characters, type prefix (CB001)
2. **Versioning**: Major in key (`v:1`), minor in body (`_schema: 1.0`) (CB002)
3. **Migration**: Expand-Contract pattern for zero-downtime (CB002)
4. **Standard fields**: _doc_id, _doc_type, _schema, docMeta (CB003)
5. **Identifier strategy**: UUIDv7 for entities, external IDs for interop, semantic for config (CB004)
6. **App-scoped keys**: `{type}:{app}:v:{version}:{id}` for multi-app buckets (CB005)
7. **Graph patterns**: Node/Edge documents with composite edge keys (CB006)

## TimescaleDB Patterns

1. **Purpose**: Time series data (usage_report, spot_price)
2. **Linking**: GSRN/price_area_id as shared key with Couchbase
3. **Retention**: Tiered (raw → hourly → daily → monthly)
4. **Schema**: Hypertables with timestamp-based partitioning

## Cross-Database Patterns

1. **Join strategy**: Application layer (fetch from both, combine)
2. **Key format**: Use natural keys (GSRN, price_area_id) not synthetic UUIDs
3. **Report pattern**: TimescaleDB aggregates + Couchbase metadata enrichment

---

**Version:** v2.2
**Last Updated:** 2026-01-20
**Changes:**

- v2.2: Added ADR-CB005 (App-Scoped Keys), ADR-CB006 (Graph Document Patterns)
- v2.1: Added ADR-CB004 (Document Identifier Strategy - UUIDv7, external IDs, semantic keys)
