# TMM Templates - Document Templates with Extraction Prompts

**Version**: 0.9.2
**Purpose**: Templates for Four Boxes (4BM) documents (read when filling specific doc)
**Related**:

- [tmm-1-process_v0.7.md](tmm-1-process_v0.7.md)
- [tmm-0-foundation_v0.8.md](tmm-0-foundation_v0.8.md)
- [tmm-3-diagrams-examples_v0.3.md](tmm-3-diagrams-examples_v0.3.md) - Examples of excellent Mermaid diagrams

---

## How to Use This Document

Each template includes:

- **AI Extraction Prompts**: Comments with questions AI should ask
- **Section structure**: What to fill in each section
- **Filling rules**: null = not OK, n/a = OK

---

## 1. Foundation Template

### foundation-{domain}.md

**Location**: `ai/decided/`

```markdown
# Foundation: {Technology}

<!-- AI: Ask "What language, framework, runtime are you using?" -->

## Tech Stack

- Language: {required}
- Framework: {required}
- Runtime: {required}
- Build: {should}

<!-- AI: Ask "What architectural patterns does the system follow?" -->

## Patterns

- Architecture: {required}
- Messaging: {should}
- Data: {should}

<!-- AI: Ask "Where does this run? How is it deployed?" -->

## Topology

- Deployment: {required}
- Regions: {should}
- HA Strategy: {should}

<!-- AI: Ask "What logging, metrics, tracing standards?" -->

## Observability

- Logging: {required}
- Metrics: {should}
- Tracing: {should}

<!-- AI: Ask "What P0/P1/P2 objectives apply? Any conflict rules?" -->

## Objectives

### P0 - Non-Negotiable

1. Correctness - {how measured}
2. Security - {how measured}

### P1 - Primary

3. Reliability - {how measured}
4. Maintainability - {how measured}
5. Testability - {how measured}

### P2 - Secondary

6. Performance - {how measured}
7. Simplicity - {how measured}
8. Evolvability - {how measured}

### Conflict Resolution

- {rule for when objectives conflict}

## Hard Rules

- Link: {vertx-hard-rules.md, etc.}
```

---

## 2. System Graph Templates

### Naming Convention

> For the full 4BM naming system (prefixes, box-bases, sub-domains), see **tmm-0-foundation §5: Document Naming Convention**.

**Location**: `ai/project-docs/service-graph/`

**File naming uses node_id (no hyphens), not node_name:**

| Type  | Pattern                              | Example                         |
|-------|--------------------------------------|---------------------------------|
| Index | `service-graph-index.md`             | -                               |
| Node  | `node-{node_id}_v{X}.{Y}.md`         | `node-e1cert_v1.0.md`           |
| Edge  | `edge-{source}-{target}_v{X}.{Y}.md` | `edge-e1receive-e1cert_v1.0.md` |

**node_id derivation** (from node_name):

- `E1-Receive` → `e1receive`
- `E1-Cert` → `e1cert`

**Why no hyphens in node_id?**

- Java packages cannot have hyphens: `com.tentixo.numan.e1cert`
- Clear edge parsing: `edge-e1receive-e1cert` ← Clear: edge - source - target
- Avoids: `edge-e1-receive-e1-cert` ← Confusing: where does node_id end?

### service-graph-index.md

```markdown
# Service Graph Index

## Visual Overview

\`\`\`mermaid
graph TD
E1-Receive --> E1-Cert
E1-Receive --> V1
V1 --> P2
\`\`\`

## Nodes (Examples)

| node_name  | node_id   | Doc                    | Status         | TMM Stage |
|------------|-----------|------------------------|----------------|-----------|
| E1-Cert    | e1cert    | node-e1cert_v1.0.md    | ✅ Complete    | 7         |
| E1-Receive | e1receive | node-e1receive_v1.0.md | ✅ Complete    | 7         |
| V1         | v1        | node-v1_v1.0.md        | 🔄 In Progress | 3         |
| P2         | p2        | -                      | ⏳ Not started | -         |

## Edges (Examples)

| Contract             | Doc                           | Status |
|----------------------|-------------------------------|--------|
| E1-Receive → E1-Cert | edge-e1receive-e1cert_v1.0.md | ✅     |
| E1-Receive → V1      | edge-e1receive-v1_v1.0.md     | ⏳     |

## Completeness Check

- [ ] All nodes have docs
- [ ] All critical edges have docs
- [ ] Visual matches actual structure
```

### node-{node_id}_v1.0.md (Node Template)

```markdown
# {node_name} Design

<!-- ═══════════════════════════════════════════════════════════════════
     AI EXTRACTION GUIDE: Use these prompts to extract information.
     null = incomplete, n/a = valid (explicitly nothing)
     node_name: {node_name} (human-readable, e.g., E1-Receive)
     node_id: {node_id} (file/code identifier, e.g., e1receive)
     node_intent: {narrowed from Foundation Intent — the gauge for this node}
     ═══════════════════════════════════════════════════════════════════ -->

<!-- AI: Ask "What is the ONE thing this service does? One sentence." -->

## Responsibility

{Single sentence - what this service does, not how}

<!-- AI: Ask "What must ALWAYS be true, no matter what state the system is in?" -->

## Invariants

- [ ] {Something that must always be true}
- [ ] {Another thing that must always be true}
- [ ] n/a (if none - explicitly state)

<!-- AI: Ask "What should happen? What are the success criteria?" -->

## Functionality

| Feature | Description | Success Criteria |
|---------|-------------|-----------------------------|
| {name} | {what happens - not how} | {how AI verifies it works} |

<!-- AI: Ask "What could go wrong? What would be embarrassing to miss?" -->

## Failure Modes

| Failure             | Detection       | Recovery             |
|---------------------|-----------------|----------------------|
| {what goes wrong}   | {how to detect} | {what should happen} |

<!-- AI: Ask "What comes in? What goes out? From/to where?" -->

## Inputs / Outputs

| Direction | What | From/To | Format |
|-----------|------|---------|--------|
| IN | {data/event} | {source} | {schema ref} |
| OUT | {data/event} | {destination} | {schema ref} |

<!-- AI: Ask "What hard-rules apply? Link to them." -->

## Constraints

**Hard (MUST/MUST NOT):**

- {constraint} → [hard-rules.md#section](...)

**Soft (SHOULD/SHOULD NOT):**

- {constraint} → [hard-rules.md#section](...)

<!-- AI: SHOULD ask "Would any of these diagrams clarify this service?"
     - State diagram (service lifecycle, message states)
     - Sequence diagram (actor interactions, API calls)
     - ERD (data relationships, schema)
     - Flowchart (process flow, decisions)
     See tmm-3-diagrams-examples_v0.3.md for templates and colors -->

## Diagrams

{Optional: Include relevant mermaid diagrams, or mark n/a if none useful}

<!-- AI: Ask "What packages/modules make up this service? What order to build?" -->

## Packages

| Package | Purpose | Depends On |
|---------|---------|------------|
| {pkg-1} | ... | (none) |
| {pkg-2} | ... | pkg-1 |

## Development Order

1. First: {pkg} because {reason}
2. Then: {pkg} because {depends on above}
3. Finally: {integration}

<!-- AI: Ask "What tests prove this works? What tests prove it fails correctly?" -->
<!-- AI: Use NASA-style test categories to drag out all scenarios -->

## Test Cases

### Nominal (Expected Behavior)

| ID | Type | Given/When/Then | Success Criteria |
|----|------|-----------------|------------------|
| TC-N01 | unit | Given X, When Y, Then Z | {expected result} |
| n/a | - | - | - |

### Off-Nominal (Failure & Recovery)

| ID | Type | Given/When/Then | Recovery Action |
|----|------|-----------------|-----------------|
| TC-O01 | unit | Given failure X, When detected, Then Y | {how system recovers} |
| n/a | - | - | - |

### Boundary (Limits & Edge Cases)

| ID | Type | Given/When/Then | Edge Condition |
|----|------|-----------------|----------------|
| TC-B01 | unit | Given max/min/edge, When processed, Then Z | {boundary tested} |
| n/a | - | - | - |

### Stress (Load & Resource Constraints)

| ID | Type | Given/When/Then | Load Condition |
|----|------|-----------------|----------------|
| TC-S01 | perf | Given high volume, When processed, Then Z | {stress scenario} |
| n/a | - | - | - |

### Robustness (Graceful Degradation)

| ID | Type | Given/When/Then | Degradation Mode |
|----|------|-----------------|------------------|
| TC-R01 | integration | Given partial failure, When X, Then degrades to Y | {fallback behavior} |
| n/a | - | - | - |

### Safe State (Safety-Critical Only)

| ID | Type | Given/When/Then | Safe State Reached |
|----|------|-----------------|-------------------|
| TC-SS01 | integration | Given critical failure, When detected, Then safe state | {safety guarantee} |
| n/a | - | - | - |

### Chaos (Intentional Failure Injection)

<!-- SpaceX-inspired "cutting the strings" - what happens when we break things mid-flight? -->

| ID | Type | What We Break | Expected Behavior |
|----|------|---------------|-------------------|
| TC-C01 | chaos | Kill {component} mid-operation | {graceful degradation or recovery} |
| n/a | - | - | - |
```

### edge-{source}-{target}_v1.0.md (Edge Template)

```markdown
# Contract: {Provider node_name} → {Consumer node_name}

<!-- ═══════════════════════════════════════════════════════════════════
     AI EXTRACTION GUIDE: Use these prompts to extract information.
     null = incomplete, n/a = valid (explicitly nothing)
     Arrow direction: Source → Target (caller → callee)
     ═══════════════════════════════════════════════════════════════════ -->

<!-- AI: Ask "What does this contract achieve? One sentence, not implementation." -->

## Goal

{What this contract achieves - NOT how}

<!-- AI: Ask "Who starts the interaction? What triggers it?" -->

## Direction & Trigger

- Provider (callee): {node_name}
- Consumer (caller): {node_name}
- Type: API | Event | File
- Trigger: {what causes this interaction}

<!-- AI: Ask "What must be true BEFORE the call? What must caller ensure?" -->

## Preconditions (Caller Ensures)

- [ ] {what must be true before call}
- [ ] {another precondition}
- [ ] n/a (if none - explicitly state)

<!-- AI: Ask "What will be true AFTER success? What does callee guarantee?" -->

## Postconditions (Callee Guarantees)

- [ ] {what will be true after success}
- [ ] {another postcondition}

<!-- AI: Ask "What errors can happen? What should consumer do for each?" -->

## Error Semantics

| Error | Meaning | Consumer Action |
|-------|---------|-----------------|
| {error type} | {what went wrong} | {what consumer should do} |

<!-- AI: Ask "Delivery semantics? Ordering? Safe to retry?" -->

## Guarantees

- Delivery: {at-least-once | exactly-once | best-effort}
- Ordering: {ordered | unordered}
- Idempotent: {yes | no} - {explanation}
- Timeout: {expected response time}

<!-- AI: Ask "What's the data format? Schema?" -->

## Data Schema

{JSON Schema reference or inline schema}

<!-- AI: Ask "How do we verify this contract works?" -->

## Smoke Test

{How to verify this contract is working}
```

---

## 3. System Foundation Templates

**Location**: `ai/project-docs/`

### system-foundation_v1.0.md

Same structure as `foundation-{tech}.md` but project-specific:

```markdown
# System Foundation

<!-- Project-specific tech stack, patterns, objectives -->
<!-- See foundation-{tech}.md template for full structure -->

## Tech Stack

## Patterns

## Topology

## Observability

## Objectives

## Hard Rules
```

### system-foundation-datamodel_v1.0.md

```markdown
# System Foundation: Data Model

<!-- AI: Ask "What are the core entities in the system?" -->

## Entity Overview

\`\`\`mermaid
erDiagram
ENTITY_A ||--o{ ENTITY_B: "relationship"
...
\`\`\`

<!-- AI: Ask "What's the schema for each entity?" -->

## Entity Schemas

### {Entity Name}

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | yes | Primary key |
| ... | ... | ... | ... |

<!-- AI: Ask "What databases store what?" -->

## Storage Mapping

| Entity | Database | Table/Collection |
|--------|----------|------------------|
| {entity} | {db type} | {table name} |
```

### system-foundation-overview-diagram_v1.0.md (NEW)

```markdown
# System Foundation: Overview Diagram

<!-- AI: This is the top-level, low-granularity overview.
     Ask "Can you show me how all services communicate?"
     Ask "Which services read/write which databases?"
     Ask "What external systems connect to what?" -->

## Service Communication

\`\`\`mermaid
flowchart LR
%% Arrow direction: Source → Target (caller → callee)
%% Service → DB for writes, DB → Service for reads

    subgraph Services["Service Graph"]
        E1[E1-Receive]
        E1C[E1-Cert]
        V1[V1]
        P2[P2]
    end

    subgraph Storage["Databases"]
        CB[(Couchbase)]
        TS[(TimescaleDB)]
    end

    subgraph External["External"]
        LDAP[LDAP]
        IMAP[IMAP]
    end

    E1 --> E1C
    E1 --> V1
    V1 --> P2
    P2 -->|writes| CB
    CB -->|reads| V1
    E1C --> LDAP
    E1 --> IMAP

\`\`\`

## Data Flow Summary

| Service | Reads From | Writes To |
|---------|------------|-----------|
| E1-Receive | IMAP | - |
| E1-Cert | LDAP | - |
| V1 | Couchbase | - |
| P2 | - | Couchbase |

## External Integration Points

| External | Connected Service | Protocol | Notes |
|----------|-------------------|----------|-------|
| LDAP | E1-Cert | LDAPS | Certificate lookup |
| IMAP | E1-Receive | IMAPS | Email fetch |

<!-- See tmm-3-diagrams-examples for diagram types and colors -->
```

---

## 4. External Template

### external-{name}.md

**Location**: `ai/project-docs/`

```markdown
# External: {Service Name}

<!-- ═══════════════════════════════════════════════════════════════════
     AI EXTRACTION GUIDE: Use these prompts to extract information.
     ═══════════════════════════════════════════════════════════════════ -->

<!-- AI: Ask "How do we connect? Host, port, protocol?" -->

## Connection

- Host: {required}
- Port: {required}
- Protocol: {required}
- Auth: {method}

<!-- AI: Ask "How do we verify it's working?" -->

## Smoke Tests

| Test | Command/Code | Expected |
|------|--------------|----------|
| Reachable | {ping/connect} | success |
| Auth works | {test query} | response |

<!-- AI: Ask "Any rate limits? Does it block? Known downtime?" -->

## Constraints

- Rate limits: {if any, n/a if none}
- Blocking: {yes/no - critical for event loop!}
- Known downtime: {if any}

<!-- AI: Ask "What happens if this external is unavailable?" -->

## Fallback

{What happens if unavailable}
```

---

## 5. Process Templates

### dev-order.md

**Location**: `ai/project-docs/`

```markdown
# Development Order

## Service Dependencies

\`\`\`mermaid
graph TD
E1-Cert --> E1-Receive
E1-Receive --> V1
V1 --> P2
\`\`\`

## Build Sequence

1. {node_name} ({node_id}) - no dependencies
2. {node_name} ({node_id}) - depends on above
3. {node_name} ({node_id}) - depends on above

## Per-Service Package Order

See node-{node_id}_v{X}.{Y}.md for internal package order.
```

---

## 6. Hard-Rules Template

Hard-rules are terse, AI-scannable enforcement documents. Loaded via `/nudge`.

### {context}-hard-rules.md

```markdown
# {Context} Hard Rules

**Scope**: {What this applies to - e.g., "All Vert.x verticles", "Java code in this project"}
**Version**: {version}
**Updated**: {date}

---

## MUST (Required)

<!-- Format: One rule per line, imperative, testable -->

- MUST {do this specific thing}
- MUST {do this other specific thing}
- MUST {handle this case}

## MUST NOT (Forbidden)

<!-- Format: One rule per line, imperative, testable -->

- MUST NOT {do this forbidden thing}
- MUST NOT {do this dangerous thing}
- MUST NOT {violate this boundary}

## SHOULD (Recommended)

<!-- Format: One rule per line, with brief rationale -->

- SHOULD {do this} - {why}
- SHOULD {prefer this} - {trade-off}

## SHOULD NOT (Discouraged)

<!-- Format: One rule per line, with brief rationale -->

- SHOULD NOT {do this} - {why it's problematic}

---

## Quick Reference

<!-- One-liner summary for AI to scan quickly -->

| Category | Key Rules |
|----------|-----------|
| Threading | No blocking on event loop |
| Error handling | Always log, never swallow |
| ... | ... |
```

### Layering

Hard-rules layer from general to specific:

```
~/.claude/hard-rules.md           # Global (all projects)
  └─ ai/hard-rules.md             # Project-wide
      └─ ai/vertx-hard-rules.md   # Framework-specific
          └─ ai/e1-hard-rules.md  # Service-specific
```

**Lower layers can TIGHTEN but not LOOSEN upper layers.**

---

## 7. Validation Checklist

Use this during Stage 7 VALIDATE:

### Intent Alignment Check

Before checking completeness, check alignment:

- [ ] Re-read Intent + Anchors (FLIGHT-PLAN.md) and Foundation Intent (Stage 00)
- [ ] For each node doc: Does the Responsibility serve the Foundation Intent?
- [ ] Has the work drifted from the declared Intent? If yes — re-hammer Stage 00 before proceeding.

<!-- AI: Ask "Does the spec we built still serve the Intent we declared?" -->

### Four Boxes Checklist

| Box          | Check                 | Pass Criteria                                        |
|--------------|-----------------------|------------------------------------------------------|
| Foundation   | Has content?          | Tech stack, patterns, objectives filled              |
| Foundation   | Objectives defined?   | P0/P1/P2 with conflict rules                         |
| Process      | Dev-order exists?     | Service dependencies defined                         |
| System Graph | Index exists?         | service-graph-index.md with all nodes/edges listed   |
| System Graph | All nodes have docs?  | Each service has node-{node_id}.md with all sections |
| System Graph | Key edges have docs?  | Critical contracts with pre/post conditions          |
| System Graph | Overview diagram?     | system-foundation-overview-diagram.md exists         |
| External     | All externals listed? | Each has connection + smoke test                     |

### Per-Document Check

For each document, verify:

- [ ] No null sections (empty = incomplete)
- [ ] n/a explicitly stated where applicable
- [ ] All "How to Ask" prompts answered
- [ ] Links to hard-rules where constraints mentioned
- [ ] Node Intent present in node doc header

---

## Changelog v0.9

**v0.9.2** (2026-02-22):

- Back-reference to tmm-0-foundation §5 for full naming convention
- `foundation-{tech}` → `foundation-{domain}` in template header (domain is broader: python, database, delta-history...)
- Updated related links: tmm-0-foundation v0.7 → v0.8, tmm-1-process v0.6 → v0.7

**v0.9.1** (2026-02-22):

- `epic_intent` → `node_intent` in node template header (each node has its own intent, narrowed from Foundation Intent)
- "Epic Intent" → "Foundation Intent" throughout (lives in system-foundation doc, not Beads)
- Validation checklist: "Node Intent present" instead of "Epic Intent present"

**v0.9** (2026-01-23):

- **4BM Standard**: Aligned with Four Box Model naming convention v1.0
- **Box rename**: "Design Graph" → "System Graph"
- **Folder rename**: `design-graph/` → `service-graph/`
- **Terminology**: node_id vs node_name in templates
- **New template**: `system-foundation-overview-diagram`
- **Index renamed**: `design-graph-index.md` → `service-graph-index.md`