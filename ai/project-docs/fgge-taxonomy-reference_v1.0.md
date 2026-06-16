# FGGE Taxonomy Reference — Definitions and Data Model

**Version**: 1.0
**Status**: Draft
**Purpose**: Single reference for all FGGE-specific terms, Eidos, edges, data model, and how the AV-R model applies to
financial governance
**Scope**: Domain-specific to FGGE (Financial Governance & Guidance Engine). For the general AV-R model, see
`credo-avr-model_v1.1.md`.
**Provenance**: W-H-S sessions: whs-srs-governance-2026-03-31.md (F1-F19) + whs-thing-eidos-2026-03-31.md (T1-T22) +
whs-econsales-2026-03-12.md (E1-E27)

---

## 1. The FGGE Domain

FGGE wraps around Microsoft Business Central (BC) with financial governance (Rim compliance) and guidance (Shaw Lenses
for steering). BC does the bookkeeping. FGGE ensures the Rim is not crossed and helps the ORG see Reality clearly.

**Root Intent** (from FLIGHT-PLAN.md): Make BC work correctly from day one for any ORG — sole proprietor to listed
global group — by dragging complexity into the architect's now so the user gets correct numbers without consulting
hours.

---

## 2. S-R-S — Shield-Reserve-Sword

Agency decomposes into three zones with different Intents:

| Zone        | Intent                    | Cost control                                                                    | What it reads                                                       |
|-------------|---------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------|
| **Shield**  | "Is the Rim intact?"      | Automate + standardize (Musk 5-step, Danaher DBS)                               | EVERYTHING broadly — compliance requires checking all parameters    |
| **Reserve** | "Can we survive a shock?" | Policy, not optimization. Set floor, don't breach (Buffett $30B, Taleb barbell) | Focused SUBSET — risk, volatility, capacity, concentration          |
| **Sword**   | "Where should we aim?"    | Context-dependent ($1 test, first-principles, relative performance, flywheel)   | OPPORTUNITY SIGNAL — where value concentrates, where to aim Vectors |

**Shield is mandatory** (Rim demands it). **Reserve is prudent** (survival). **Sword is what's left** after Shield and
Reserve.

Same data, three Shaw-resolutions. Three independent lenses → synthesis meeting → decide Vectors. Replaces the budget
process.

---

## 3. Nodes (Eidos)

### node:org — Legal Entity

Full Eidos. Identity authority: Bolagsverket (org_nr).

**What it is**: An organization in the group. The structural backbone.

**Key governance properties**:

- `jurisdiction`, `functional_currency`, `reporting_date` (IAS 21, IFRS 10)
- `entity_type`: operating / holding / spe / investment_entity (mutable property, not _doc_type)
- `registered_share_capital`, `equity_latest` → KBR monitoring (ABL 25:13)
- `accounting_policy_set` → uniform policy enforcement (IFRS 10.19)
- `held_for_sale` section (IFRS 5) — classification, FVLCD, discontinued operation flag
- `acquisition_history` (IFRS 3) — was_acquired, acquisition_date, business_or_asset
- `cgu` (IAS 36) — CGU allocation, goodwill_allocated, headroom
- `tax` section — jurisdiction, local_gaap, TP required, CbCR scope, Pillar Two scope

**Full definition**: `node-org-governance_v1.0.md`

### node:xitem — The Sellable Thing

Eidos. Identity authority: Item Number (BC) or catalog ID.

**What it is**: What an ORG sells that creates xtValue for the buyer. NOT manufacturing (that's Agency). NOT transport (
that's Incoterms/Repose).

**Three top-level types** (g/v/h) — immutable at instance level, valid as _doc_type. Stress-tested against 20+ real
cases (session 6) and survived sharp attack:

| Type                          | What                                              | Inventory?  | IFRS                                                             | VAT                                                                         | Effector                                  |
|-------------------------------|---------------------------------------------------|-------------|------------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------|
| **gItem** (goods)             | Physical matter transferred to buyer              | Yes (IAS 2) | IFRS 15                                                          | Goods (varor) — rate varies: 25%/12%/6% by sub-type                         | Machine + material                        |
| **vItem** (virtual)           | Delivered without human at point of delivery      | No          | IFRS 15 (e-svc/svc) or IFRS 9 (financial) or IFRS 17 (insurance) | Services (tjänster) or exempt (financial) — EU e-svc has specific VAT rules | Infrastructure (electronic or mechanical) |
| **hItem** (human performance) | Seller's employees/subcontractors ARE the xtValue | No          | IFRS 15                                                          | Services (tjänster) 25% or exempt (healthcare/education)                    | Person                                    |

**Full taxonomy** (refined session 6):

```
xItem (sellable thing — what creates xtValue for buyer)
├── gItem (goods — physical matter transferred to buyer)
│   ├── gItem.energy (continuous flow: gas, electricity, water)
│   └── gItem.physical (discrete objects at any production stage)
│       └── gItem.physical.raw (raw materials / halvfabrikat sold — automation-driven)
├── vItem (virtual — delivered without human at point of delivery)
│   ├── vItem.e-svc (electronically supplied — EU VAT specific rules, MOSS/OSS)
│   │   ├── vItem.e-svc.access (right-to-access: SaaS, streaming, data → over-time)
│   │   ├── vItem.e-svc.use (right-to-use: perpetual license, ePUB → point-in-time)
│   │   └── vItem.e-svc.platform (marketplace, ad space → agent/principal critical)
│   ├── vItem.svc (non-electronic service — infrastructure/machine delivered)
│   │   ├── vItem.svc.auto (automated physical: laundromat, car wash, parking)
│   │   └── vItem.svc.transport (selling transport: freight, shipping, logistics)
│   ├── vItem.financial (financial instrument → IFRS 9 Rim. VAT: exempt)
│   │   ├── vItem.financial.insurance (insurance contract → IFRS 17 Rim)
│   │   └── vItem.financial.lease (leasing product → IFRS 16 lessor. Underlying may be physical.)
│   └── vItem.physical-media (virtual content on physical carrier — legacy)
├── hItem (human performance — seller's people ARE xtValue)
│   ├── hItem.consulting (expert judgment, advice, design)
│   ├── hItem.labor (physical work: installation, construction, cleaning)
│   └── hItem.regulated (healthcare, education → VAT: EXEMPT)
└── NOT xItem:
    ├── Machine/asset rental where buyer controls use → IFRS 16 lease (not xItem)
    ├── Inventory stages (raw/WIP/finished) → gItem.physical (accounting property, not identity)
    └── Transport for another's goods → Incoterms (Repose), not the THING sold

xPackage (bundle of xItems, freely mixed)
├── xPackage.continuous (ongoing: dev team + QA, managed service, support)
└── xPackage.project (defined goal: implementation, migration, build)
```

**BC mapping (locked)**:

- xItem type → **Gen. Prod. Posting Group** (on BC Item Card)
- xItem VAT → **VAT Prod. Posting Group** (on BC Item Card)
- Five-group matrix: Gen. Bus. (WHO) × Gen. Prod. (WHAT) × VAT Bus. × VAT Prod. × Purchase/Sales
- FGGE Shield validates: correct posting groups for this g/v/h type?

**Key EU VAT boundary**: vItem.e-svc vs vItem.svc confirmed by EU VAT Rim — different place-of-supply rules for
electronically supplied services (MOSS/OSS regime). This is not an artificial split — the EU regulation demands it.

**Key properties**: type, sub_type, SSP, cost_standard, effector_mix, vat_class, ifrs_standard, xtvalue_pattern,
useful_life

**Full definition**: `node-xitem_v1.0.md`

### node:ind — Person

Full Eidos. Identity authority: personnummer (Skatteverket).

**In FGGE**: Board members (personal liability under ABL), CEO, CFO, KMP (IAS 24), auditors. Connected to ORG via
board-member, kmp, auditor edges.

### node:mach — System

Full Eidos. Identity authority: system ID.

**In FGGE**: BC (the ERP), Power BI (Shaw Lenses), consolidation tools. Cast as Effector on ergons (automated steps).

---

## 4. Edges and Relationships

### edge:org-org — Bilateral Relationship

One conceptual document per ORG pair. Direction lives inside.

**Structure**:

```
common:          Non-directional (relationship_active, ic_elimination_required, T_overall, bffb_any_direction)
org1_to_org2:    Directed A→B (owns, sells_to, lends_to, guarantees, disposal, ppa, tamagos_summary)
org2_to_org1:    Directed B→A (same structure)
```

**Key sections**:

- `owns` — Ownership with control assessment (IFRS 10), NCI, acquisition data
- `owns.control_assessment` — Power + Returns + Link = Control (IFRS 10.5-18)
- `owns.de_facto` — De facto control evidence (when voting < 50%)
- `sells_to` — Commercial trading with xItem refs, pricing, Incoterms, payment terms
- `lends_to` — IC lending (IAS 24, ABL 21)
- `guarantees` — IC guarantees (IAS 24, ABL 17)
- `disposal` — IFRS 5 disposal plan (status, expected proceeds)
- `ppa` — Purchase Price Allocation (IFRS 3): goodwill, identified intangibles, contingent consideration
- `tamagos_summary` — Pipeline summary: active count, weighted value, BFFB, T, dT/dt

**Full definition**: `edge-org-org-relationship_v1.0.md`

### edge:ind-org — Person-to-Organization

| Edge type      | What it carries                                          |
|----------------|----------------------------------------------------------|
| `board-member` | Board seat. Personal liability under ABL.                |
| `kmp`          | Key Management Personnel. IAS 24 disclosure.             |
| `auditor`      | Statutory auditor. Revisorslagen obligations.            |
| `effector`     | (existing) IND cast on Pragma for IFRS ergon HitL steps. |

---

## 5. The Tamagos (Pre-Contract Deal)

**NOT Eidos** — Metamorphon (transient, confined, vulnerable). Tracked because Sword (pipeline) and Reserve (revenue
forecast) need it.

**What it is**: The forming deal between seller and buyer. Contains the Morphon (embryo) that becomes a Contract at
hatching (IFRS event).

**Key properties**: xItem refs, estimated value, Ladder Gate (1-6), T, dT/dt, Vector Events, probability, status (
alive/hatched/annihilated/dormant).

**Lifecycle**: Born at first contact → fed by Vector Events → hatches at IFRS event (Contract born, BFFB granted if
first) → OR annihilated (deal died, nothing remains).

**Full definition**: `doc-tamagos_v1.0.md`

---

## 6. xtValue — When Value Comes into Existence

xtValue = the moment the xItem creates value for the buyer. Everything LEFT of xtValue is cost chain (Shield). xtValue
itself is the exchange (revenue). RIGHT of xtValue is ongoing value (Sword observes T, dT/dt).

### Three xtValue patterns

| Pattern         | xItem type  | What happens                                              | IFRS 15                  |
|-----------------|-------------|-----------------------------------------------------------|--------------------------|
| **Point**       | gItem       | Buyer receives physical thing. Value at delivery/unpack.  | Point-in-time            |
| **Progressive** | hItem       | Value accumulates as Σδᵢ (each day of work adds a delta). | Over-time (% completion) |
| **Continuous**  | vItem.e-svc | Value flows as stream while access active.                | Over-time (ratable)      |

### Three time natures in the value chain

| Nature           | What happens                                                    | Value?      | Example                                     |
|------------------|-----------------------------------------------------------------|-------------|---------------------------------------------|
| **Repose**       | Waiting. xItem in transit/queued. Time passes, nothing changes. | No          | Truck driving, customs, warehouse           |
| **Delta**        | Building. Each increment adds xtValue.                          | Progressive | Consultant working, mover carrying boxes    |
| **Product-time** | Time IS the value. Each unit is a δ.                            | Continuous  | SaaS day, insurance day, subscription month |

### Accounting activation test

IAS 38, IAS 2, IFRS 15 contract costs, IAS 36 all ask the same question: **"Can you Vector to xtValue?"** Cost sits on
balance sheet only while the chain is expected to reach xtValue. Tamagos dying = chain breaks = write off.

---

## 7. Four Concentric Sets — Black-Gray-White-BFFB

From EconSales W-H-S (revised session 34):

```
BLACK (dark matter): Completely unmeasured. Can't identify.
GRAY:                Would enjoy our xItem. Identifiable BY xItem profile. Addressable. No contact.
WHITE (visible):     Relationship born. T exists. Tamagos may be alive.
BFFB:                First Tamagos hatched. Permanent. T still fluctuates.
```

**Gray requires xItem definition** — the boundary between Black and Gray IS the xItem clarity. Sharper xItem → clearer
Gray → better Sword aim.

### Transition rates

| Rate           | What                                        | Measures                |
|----------------|---------------------------------------------|-------------------------|
| dBlack→Gray/dt | Identification (market research, profiling) | xItem clarity           |
| dGray→White/dt | First contact (targeted marketing)          | Marketing effectiveness |
| dWhite→BFFB/dt | First Tamagos hatching                      | Sales effectiveness     |

---

## 8. Rim Parameters — What Each Standard Looks At

Every Rim parameter is grounded in a specific location:

| Location            | What lives there                                                                               | Which Rim reads it                                           |
|---------------------|------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| **ON xItem**        | type (g/v/h), SSP, cost, vat_class, ifrs_standard, xtvalue_pattern, effector_mix               | IFRS 15, IAS 2, IAS 38, VAT, IFRS 8, TP                      |
| **ON xPackage**     | components, distinct_per_component, ssp_allocation                                             | IFRS 15 (performance obligations)                            |
| **ON edge:org-org** | price, TC (deal terms), Incoterms, principal/agent, variable_consideration, IC_flag, TP_method | IFRS 15, VAT, TP, ABL                                        |
| **ON ORG.seller**   | jurisdiction, effector_capacity, equity, share_capital                                         | ABL (KBR), Tax, Pillar Two                                   |
| **ON ORG.buyer**    | jurisdiction, type, size                                                                       | VAT (place of supply), IFRS 8 (segment), IAS 24 (RPT)        |
| **DERIVED**         | margin (edge.price - xItem.cost), reverse_charge, segment (cluster), cash_conversion, T/dT/dt  | All — each derived value read by S-R-S with different Intent |

---

## 9. IFRS Ergon Chains

Ergons = work that must be done for Rim compliance. Each maps to a specific IFRS standard.

### Master Chain (execution order per reporting period)

```
Phase 1: IFRS 10 (Scope)        → who is in the group
Phase 2: IFRS 3 (Acquisitions)  → new entities entering (parallel: IFRS 5 disposals)
Phase 3: IAS 21, IC Elimination, IAS 36, IAS 19  → adjustments (parallel)
Phase 4: IAS 12 (Tax)           → deferred tax on ALL adjustments (sequential — needs all above)
Phase 5: IAS 33, IFRS 8, IAS 24, ABL KBR         → completion (parallel)
Phase 6: Done2 complete          → consolidated trial balance
```

### Chains defined

| Chain                                       | Ergons                                                                                                | Status                        |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------|
| [IFRS 10](ergon-ifrs-10-chain_v1.0.md)      | Control assessment → Scope → NCI → BC Consolidation                                                   | Done                          |
| [IFRS 3](ergon-ifrs-3-chain_v1.0.md)        | Business-vs-asset → PPA → Goodwill → Measurement period → Contingent consideration                    | Done                          |
| [IFRS 5](ergon-ifrs-5-chain_v1.0.md)        | Classification → Monitor → Completion/Abandonment                                                     | Done                          |
| [IFRS 8](ergon-ifrs-8-chain_v1.0.md)        | Segment identification → Validation → Disclosure                                                      | Done                          |
| [IFRS 13](ergon-ifrs-13-fair-value_v1.0.md) | Fair value measurement (service ergon — invoked by IFRS 3, IAS 36, IFRS 9, etc.)                      | Done                          |
| [IFRS 15](ergon-ifrs-15-chain_v1.0.md)      | Contract → POs → Price → Allocate → Recognize (five-step model mapped to xItem/xtValue)               | Done                          |
| [IFRS 16](ergon-ifrs-16-chain_v1.0.md)      | Lease identification → Measurement (ROU as FA card) → Ongoing (depreciation, interest, modifications) | Done                          |
| [IFRS 17](ergon-ifrs-17-chain_v1.0.md)      | Insurance scope test + consolidation interface (specialist systems handle detail)                     | Done                          |
| [IAS 21](ergon-ias-21-chain_v1.0.md)        | FX rate policy (home central bank) → Functional currency → Translation → FCTR Ghost → Monitors        | Done                          |
| IAS 36 — Impairment                         | Pending                                                                                               | High priority                 |
| IAS 12 — Deferred Tax                       | Pending                                                                                               | High priority                 |
| IC Elimination                              | Pending                                                                                               | High priority                 |
| ABL KBR — Equity Monitor                    | Pending                                                                                               | Critical (personal liability) |
| IAS 19 — Employee Benefits                  | Pending                                                                                               | Depends on group profile      |
| IAS 24 — Related Party                      | Pending                                                                                               | Medium                        |
| IAS 33 — EPS                                | Pending                                                                                               | Medium                        |
| IAS 37 — Provisions                         | Pending                                                                                               | Medium                        |

---

## 10. Governance Philosophies

| Principle                              | Source        | FGGE Application                                          |
|----------------------------------------|---------------|-----------------------------------------------------------|
| Trust + incentive alignment            | Buffett       | Don't build bureaucracy; build guardrails                 |
| First-principles + delete unnecessary  | Musk          | Delete → Simplify → Automate (Shield)                     |
| Relative targets + autonomy            | Handelsbanken | Measure against peers, not budgets (Sword)                |
| Inversion ("what would destroy us?")   | Munger        | The Rim IS the inversion list (Shield)                    |
| Separation of 3 budget functions       | Bogsnes       | Rolling forecasts, not budget-vs-actual                   |
| Preserve core / stimulate progress     | Collins       | Shield preserves, Sword stimulates                        |
| Stockdale Paradox                      | Collins       | Shaw Lenses: brutal facts + Intent holds                  |
| Long-tail / barbell                    | Taleb         | Shield+Reserve for negative tail, Sword for positive tail |
| Averages lie                           | Taleb/Jensen  | Shaw Lenses show distributions, not point estimates       |
| Segments discovered, not assumed       | W-H-S         | Clusters from data correlations, not top-down assumption  |
| xtValue is the buyer's hatching moment | W-H-S         | Value chain cost LEFT of xtValue, ongoing value RIGHT     |

---

## 11. Ghost Terms (do NOT use)

| Ghost term                 | Why it's a ghost                               | Use instead                                                                          |
|----------------------------|------------------------------------------------|--------------------------------------------------------------------------------------|
| "Customer"                 | Undefined (EconSales dissolved it). Ghost.     | ORG.buyer + Relationship (edge:org-org) + T/BFFB                                     |
| "Delivery method"          | Not a thing. Steps in value chain.             | Value chain steps (each is Repose or Delta)                                          |
| "Firmness"                 | Not independent. Derived.                      | xtValue pattern + TC (deal terms on edge)                                            |
| "Channel"                  | Not a property. Graph topology.                | Value chain topology (ORG hops between creation and xtValue)                         |
| "Last mile"                | Vague.                                         | Where xtValue happens (at buyer / at seller)                                         |
| "Longevity"                | Dissolved.                                     | Three time natures: Repose / Delta / Product-time                                    |
| "Segment" (assumed)        | Assuming = hiding ugly books.                  | Segments DISCOVERED from xItem × ORG.buyer × edge correlations                       |
| "Margin" (as stored value) | Derived from two locations. Not a property.    | edge.price - xItem.cost (derived, not stored)                                        |
| "Cost-to-serve"            | Three-dimensional ghost.                       | xItem.cost (production) + edge topology cost (chain hops) + ORG.buyer geography cost |
| "Budget variance"          | Measures against your own guess, not R. Noise. | Compare to R directly (Shaw Lenses on actual T, dBFFB/dt, margin trend)              |

---

## 12. Cross-References

| Document                                  | What it defines                                                      |
|-------------------------------------------|----------------------------------------------------------------------|
| `FLIGHT-PLAN.md`                          | Root Intent + 11 Anchors (5 clusters)                                |
| `credo-avr-model_v1.1.md`                 | General AV-R model (universal, pre-FGGE)                             |
| `credo-choosable-properties_v1.0.md`      | V-P-C-T-TC (e-commerce layer — output feeds governance via C and TC) |
| `ai/prompts/xItem-view.md`                | xItem existence-to-xtValue chains (working notes)                    |
| `whs-srs-governance-2026-03-31.md`        | S-R-S governance W-H-S (18 anchors)                                  |
| `whs-thing-eidos-2026-03-31.md`           | xItem Eidos sub-Walk (22 anchors)                                    |
| `whs-econsales-2026-03-12.md`             | EconSales: Tamagos, Morphon, Black-Gray-White-BFFB (27 anchors)      |
| `dr-manhattan-financial-union-list_v1.md` | Raw union of all governance requirements (7 tracks, 800+ lines)      |
| `node-org-governance_v1.0.md`             | ORG node data model                                                  |
| `node-xitem_v1.0.md`                      | xItem node data model                                                |
| `edge-org-org-relationship_v1.0.md`       | Bilateral relationship data model                                    |
| `doc-tamagos_v1.0.md`                     | Pre-contract deal data model                                         |
| `ergon-ifrs-master-chain_v1.0.md`         | IFRS ergon execution ordering                                        |

---

## Version History

| Version | Date       | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1.0     | 2026-04-01 | Initial — assembled from W-H-S sessions. S-R-S, xItem g/v/h, xtValue, Black-Gray-White-BFFB, Rim parameters, ghost terms, governance philosophies.                                                                                                                                                                                                                                                                                                                                          |
| 1.1     | 2026-04-01 | xItem taxonomy refined after sharp stress-test (20+ cases). Added: vItem.e-svc sub-types (access/use/platform), vItem.svc (non-electronic: auto, transport), vItem.financial.lease, gItem.physical.raw, hItem.regulated. EU VAT Rim confirms vItem.e-svc vs vItem.svc split. BC mapping locked: Gen. Prod. Posting Group = xItem type, VAT Prod. Posting Group = vat_class. IFRS ergon chains expanded: 9 standards done (IFRS 10, 3, 5, 8, 13, 15, 16, 17, IAS 21). Model survived attack. |
