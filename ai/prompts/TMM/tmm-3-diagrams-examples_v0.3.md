# TMM Diagrams Examples

**Version**: 0.3
**Purpose**: Mermaid diagram examples for TMM documentation
**Related**:

- [tmm-0-foundation_v0.8.md](tmm-0-foundation_v0.8.md)
- [tmm-2-templates_v0.9.md](tmm-2-templates_v0.9.md)
- [mermaid-colors.md](../mermaid-colors.md)

---

## Changelog v0.3

**v0.3** (2026-01-23):

- **Arrow direction standard**: Source → Target (caller → callee) documented
- **DB read/write convention**: Service → DB for writes, DB → Service for reads
- **4BM alignment**: Updated terminology

---

## Arrow Direction Standard

**CRITICAL**: All flowcharts MUST follow Source → Target convention.

```mermaid
flowchart LR
    Caller[Source<br/>caller] -->|calls| Target[Target<br/>callee]
```

| Interaction | Arrow Direction    | Example           |
|-------------|--------------------|-------------------|
| API call    | Caller → Callee    | `E1 --> V1`       |
| Event send  | Sender → Receiver  | `E1 --> EventBus` |
| DB write    | Service → Database | `P2 --> CB`       |
| DB read     | Database → Service | `CB --> V1`       |

**Rationale**: Arrow shows flow of control (calls) or flow of data (reads/writes).

---

## Color Palette

| Color    | Hex     | Use For                         |
|----------|---------|---------------------------------|
| Blue     | #0D5ED7 | Service nodes, primary entities |
| Green    | #237046 | Data, success states            |
| Dark Red | #870000 | Foundation, schemas, critical   |
| Indigo   | #4B0082 | Edges, contracts, decisions     |
| Orange   | #A34700 | Data Model, warnings            |
| Slate    | #2F4F4F | Containers, grouping            |
| Teal     | #006C6C | Process, workflow               |
| Olive    | #556B2F | System Graph container          |
| Magenta  | #8B008B | External services               |
| Gray     | #696969 | Background, neutral             |

---

## 1. ERD (Entity Relationship Diagram)

Use for: Data model, database schema, document relationships

```mermaid
erDiagram
    METERING_POINT ||--o{ CONTRACT: "has"
    CONTRACT ||--|| RETAILER: "belongs_to"
    CONTRACT ||--o{ UTILTS_MESSAGE: "receives"
    RETAILER ||--o{ PRODAT_MESSAGE: "sends"
    DSO ||--o{ UTILTS_MESSAGE: "sends"
    DSO ||--o{ METERING_POINT: "owns"

    METERING_POINT {
        string id PK
        string elomrade
        string address
        datetime created
    }

    CONTRACT {
        string id PK
        string metering_point_id FK
        string retailer_id FK
        date start_date
        date end_date
    }

    RETAILER {
        string id PK
        string ediel_id
        string name
        string email
    }

    DSO {
        string id PK
        string ediel_id
        string name
        string region
    }

    UTILTS_MESSAGE {
        string id PK
        string contract_id FK
        string subtype
        datetime timestamp
        json payload
    }

    PRODAT_MESSAGE {
        string id PK
        string retailer_id FK
        string subtype
        datetime timestamp
        json payload
    }
```

---

## 2. Flowchart

Use for: Process flows, decision trees, workflows

**Note**: Arrow direction = Source → Target (caller → callee)

```mermaid
flowchart TB
    Start([Email Arrives]) --> Fetch[Fetch from IMAP]
    Fetch --> Classify{Classify}
    Classify -->|EDI| Decrypt[Decrypt S/MIME]
    Classify -->|Bounce| Bounce[Handle Bounce]
    Classify -->|Spam| Spam[Move to Spam]
    Classify -->|Unknown| Unknown[Alert Ops]
    Decrypt --> Parse[Parse EDIFACT]
    Parse --> Validate{Valid?}
    Validate -->|Yes| Route[Route to Handler]
    Validate -->|No| Reject[Send APERAK Error]
    Route --> Process[Process Message]
    Process --> Ack[Send CONTRL]
    Ack --> Done([Complete])
    Bounce --> Done
    Spam --> Done
    Unknown --> Done
    Reject --> Done
    style Start fill: #0D5ED7, stroke: #444, stroke-width: 4px, color: #fff
    style Done fill: #237046, stroke: #444, stroke-width: 4px, color: #fff
    style Classify fill: #4B0082, stroke: #444, stroke-width: 4px, color: #fff
    style Validate fill: #4B0082, stroke: #444, stroke-width: 4px, color: #fff
    style Decrypt fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style Parse fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style Route fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style Process fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style Reject fill: #870000, stroke: #444, stroke-width: 4px, color: #fff
    style Bounce fill: #A34700, stroke: #444, stroke-width: 4px, color: #fff
    style Spam fill: #A34700, stroke: #444, stroke-width: 4px, color: #fff
    style Unknown fill: #A34700, stroke: #444, stroke-width: 4px, color: #fff
```

---

## 3. State Diagram

Use for: Entity lifecycle, message states, workflow states

```mermaid
stateDiagram-v2
    [*] --> RECEIVED: Email arrives
    RECEIVED --> CLASSIFYING: Start classification
    CLASSIFYING --> ENCRYPTED: Is S/MIME
    CLASSIFYING --> PLAINTEXT: Not encrypted
    CLASSIFYING --> REJECTED: Not EDI
    ENCRYPTED --> PENDING_CERT: Need certificate
    ENCRYPTED --> DECRYPTING: Have certificate
    PENDING_CERT --> DECRYPTING: Cert delivered
    PENDING_CERT --> CERT_FAILED: Cert not found
    DECRYPTING --> DECRYPTED: Success
    DECRYPTING --> DECRYPT_FAILED: Error
    PLAINTEXT --> PARSING: Parse EDIFACT
    DECRYPTED --> PARSING: Parse EDIFACT
    PARSING --> VALIDATED: Valid message
    PARSING --> PARSE_FAILED: Invalid syntax
    VALIDATED --> PROCESSING: Route to handler
    PROCESSING --> COMPLETE: Processed
    PROCESSING --> PROCESS_FAILED: Handler error
    COMPLETE --> [*]
    REJECTED --> [*]
    CERT_FAILED --> [*]
    DECRYPT_FAILED --> [*]
    PARSE_FAILED --> [*]
    PROCESS_FAILED --> [*]
```

---

## 4. Sequence Diagram

Use for: Service interactions, message flows, API calls

```mermaid
sequenceDiagram
    participant R as Retailer (numan_us)
    participant D as DSO (dso-oracle)
    participant R2 as Retailer (numan_them)
    Note over R, R2: Supplier Change Flow (PRODAT Z03-Z05)
    R ->>+ D: Z03 Request supplier change
    D -->> R: CONTRL (syntax OK)
    D ->> D: Validate request

    alt Approved
        D ->>+ R: Z04 Confirm change
        R -->> D: CONTRL
        D ->>+ R2: Z05 Notify losing retailer
        R2 -->> D: CONTRL
        Note over R, R2: UTILTS starts flowing to R
    else Rejected
        D ->>+ R: Z04 Reject with reason
        R -->> D: CONTRL
        R ->> R: Handle rejection
    end
```

---

## 5. Graph (Nodes and Edges)

Use for: System architecture, service dependencies, Service Graph

**Note**: Arrow direction = Source → Target (caller → callee)
**Note**: DB writes = Service → DB, DB reads = DB → Service

```mermaid
flowchart LR
    subgraph Intake["Intake Layer"]
        E1[E1-Receive<br/>e1receive]
        E1C[E1-Cert<br/>e1cert]
    end

    subgraph Validation["Validation Layer"]
        V1[V1-Inner<br/>v1inner]
        V2P[V2-PRODAT<br/>v2prodat]
        V2U[V2-UTILTS<br/>v2utilts]
        V2C[V2-CONTRL<br/>v2contrl]
    end

    subgraph Business["Business Layer"]
        P2[P2-SupplierChange<br/>p2supplierchange]
        P3[P3-MasterData<br/>p3masterdata]
        U1[U1-TimeSeries<br/>u1timeseries]
    end

    subgraph Storage["Storage Layer"]
        CB[(Couchbase)]
        TS[(TimescaleDB)]
    end

    E1 -->|raw email| V1
    E1 <-->|cert request| E1C
    V1 -->|PRODAT| V2P
    V1 -->|UTILTS| V2U
    V1 -->|CONTRL| V2C
    V2P --> P2
    V2P --> P3
    V2U --> U1
    P2 -->|writes| CB
    P3 -->|writes| CB
    CB -->|reads| V1
    U1 -->|writes| TS
    style E1 fill: #0D5ED7, stroke: #444, stroke-width: 4px, color: #fff
    style E1C fill: #0D5ED7, stroke: #444, stroke-width: 4px, color: #fff
    style V1 fill: #4B0082, stroke: #444, stroke-width: 4px, color: #fff
    style V2P fill: #4B0082, stroke: #444, stroke-width: 4px, color: #fff
    style V2U fill: #4B0082, stroke: #444, stroke-width: 4px, color: #fff
    style V2C fill: #4B0082, stroke: #444, stroke-width: 4px, color: #fff
    style P2 fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style P3 fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style U1 fill: #006C6C, stroke: #444, stroke-width: 4px, color: #fff
    style CB fill: #237046, stroke: #444, stroke-width: 4px, color: #fff
    style TS fill: #237046, stroke: #444, stroke-width: 4px, color: #fff
    style Intake fill: #2F4F4F, stroke: #444, stroke-width: 2px, color: #fff
    style Validation fill: #2F4F4F, stroke: #444, stroke-width: 2px, color: #fff
    style Business fill: #2F4F4F, stroke: #444, stroke-width: 2px, color: #fff
    style Storage fill: #2F4F4F, stroke: #444, stroke-width: 2px, color: #fff
```

---

## 6. Class Diagram (Bonus)

Use for: Domain model, object relationships, interfaces

```mermaid
classDiagram
    class Message {
        +String id
        +String edielId
        +DateTime received
        +MessageState state
        +process()
        +validate()
    }

    class ProdatMessage {
        +String subtype
        +String meteringPointId
        +handleZ03()
        +handleZ04()
    }

    class UtiltsMessage {
        +String subtype
        +TimeSeriesData data
        +handleE01()
        +handleE05()
    }

    class Certificate {
        +String email
        +byte[] publicKey
        +DateTime expiry
        +CertVersion version
        +isValid()
        +isExpired()
    }

    Message <|-- ProdatMessage
    Message <|-- UtiltsMessage
    Message --> Certificate: encrypted_with
```

---

## 7. Gantt Chart

Use for: Project timelines, implementation phases, migration schedules

```mermaid
gantt
    title EDI Migration Project
    dateFormat YYYY-MM-DD
    excludes weekends

    section Foundation
        Schema design: done, f1, 2026-01-06, 5d
        Database setup: done, f2, after f1, 3d
        Certificate management: active, f3, after f2, 4d

    section Intake Layer
        E1-Receive service: e1, after f3, 5d
        E1-Cert service: e2, after e1, 3d
        Integration tests: e3, after e2, 2d

    section Validation Layer
        V1-Inner parser: v1, after e3, 4d
        V2-PRODAT validator: v2, after v1, 3d
        V2-UTILTS validator: v3, after v1, 3d
        V2-CONTRL validator: v4, after v1, 2d

    section Business Layer
        P2-SupplierChange: p2, after v2, 5d
        U1-TimeSeries: u1, after v3, 4d

    section Milestones
        MVP Ready: milestone, m1, after p2, 0d
        Production Go-Live: milestone, m2, after u1, 0d
```

---

## Quick Reference

| Diagram Type | Mermaid Keyword            | Best For                 |
|--------------|----------------------------|--------------------------|
| ERD          | `erDiagram`                | Data model, schemas      |
| Flowchart    | `flowchart TB/LR`          | Process, decisions       |
| State        | `stateDiagram-v2`          | Lifecycle, states        |
| Sequence     | `sequenceDiagram`          | Interactions, APIs       |
| Graph        | `flowchart` with subgraphs | Architecture             |
| Class        | `classDiagram`             | Domain model             |
| Gantt        | `gantt`                    | Timelines, project plans |

---

## Omitted Diagram Types

Other Mermaid diagram types not included in this guide:

| Diagram      | Keyword         | Use Case                   | TMM Relevance                 |
|--------------|-----------------|----------------------------|-------------------------------|
| Pie          | `pie`           | Proportions, distributions | Low - rarely needed           |
| Timeline     | `timeline`      | Events over time           | Low - Gantt covers most cases |
| Quadrant     | `quadrantChart` | 2x2 matrices               | Low - better in tables        |
| Mindmap      | `mindmap`       | Brainstorming, concepts    | Low - exploration, not docs   |
| Git Graph    | `gitGraph`      | Branch visualization       | Low - niche use case          |
| C4           | `C4Context`     | Formal C4 architecture     | Low - flowchart suffices      |
| User Journey | `journey`       | UX flows                   | Low - backend focus           |
| Sankey       | `sankey-beta`   | Flow quantities            | Low - very specialized        |
| XY Chart     | `xychart-beta`  | Data visualization         | Low - use real charting tools |

---

## Version History

| Version | Date       | Changes                                                       |
|---------|------------|---------------------------------------------------------------|
| 0.3     | 2026-01-23 | Arrow direction standard, DB read/write convention, 4BM terms |
| 0.2     | 2026-01-15 | Add Gantt chart, Omitted diagram types table                  |
| 0.1     | 2026-01-05 | Initial examples for ERD, Flow, State, Sequence, Graph, Class |
