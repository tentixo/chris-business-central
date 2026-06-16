# Ergon Chain: IFRS 10 — Consolidated Financial Statements

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 10 (complete standard)
**Intent**: The complete chain of tasks required to determine WHO is consolidated, at WHAT percentage, under WHAT method
**Parent**: ai/reports/dr-manhattan-financial-union-list_v1.md (Track 1, IFRS 10)

---

## Chain Overview

```
                    ┌─────────────────────────────────┐
                    │  REASSESSMENT MONITOR            │
                    │  (continuous — Walker)            │
                    │  Detects ownership/governance     │
                    │  changes between reporting dates  │
                    └──────────────┬──────────────────┘
                                   │ raises anomaly
                                   ▼
                    ┌─────────────────────────────────┐
                    │  CONTROL ASSESSMENT              │
                    │  (per entity pair)                │
                    │  Power + Returns + Link = Control │
                    │  HitL for de facto + SPE          │
                    └──────────────┬──────────────────┘
                                   │ control_conclusion per edge
                                   ▼
                    ┌─────────────────────────────────┐
                    │  SCOPE DETERMINATION             │
                    │  (per reporting period)           │
                    │  Graph traversal → ctx-v          │
                    │  Validate dates + policies        │
                    └──────────────┬──────────────────┘
                                   │ consolidation scope (ctx-v)
                                   ▼
                    ┌─────────────────────────────────┐
                    │  NCI CALCULATION                  │
                    │  (per reporting period)           │
                    │  Direct + chain + cross-holdings  │
                    │  Write to graph + BC              │
                    └──────────────┬──────────────────┘
                                   │ nci_pct per entity
                                   ▼
                    ┌─────────────────────────────────┐
                    │  BC CONSOLIDATION ENGINE          │
                    │  (BC performs the mechanics)       │
                    │  Elimination, translation,        │
                    │  aggregation using scope + NCI    │
                    └─────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | Trigger | Effector | Output |
|---|---|---|---|---|
| 0 | [reassessment-monitor](ergon-ifrs-10-reassessment-monitor_v1.0.md) | Continuous (x-history events) | MACH (Walker) | Anomalies triggering reassessment |
| 1 | [control-assessment](ergon-ifrs-10-control-assessment_v1.0.md) | Periodic + event (from step 0) | Mixed (MACH + IND for HitL) | control_conclusion on each edge |
| 2 | [scope-determination](ergon-ifrs-10-scope-determination_v1.0.md) | After all step 1 complete | MACH + IND (exceptions) | ctx-v consolidation scope |
| 3 | [nci-calculation](ergon-ifrs-10-nci-calculation_v1.0.md) | After step 2 complete | MACH | nci_pct per entity → graph + BC |
| 4 | BC Consolidation | After step 3 writes to BC | MACH (BC engine) | Consolidated financial statements |

---

## Dependencies

```
Step 0 → Step 1:  Anomaly triggers reassessment for specific entity pair
Step 1 → Step 2:  ALL control assessments must complete before scope is determined
Step 2 → Step 3:  Scope must be finalized before NCI can be calculated
Step 3 → Step 4:  NCI must be written to BC before consolidation engine runs
Step 4 → Done:    BC produces consolidated trial balance
```

**Step 0 runs continuously.** Steps 1-4 run sequentially per reporting period.

**Step 1 can run in parallel** for different entity pairs (each pair's control assessment is independent). Steps 2-4 are sequential and require all prior step instances to complete.

---

## Data Flow

| From | To | What flows |
|---|---|---|
| External sources (Walkers) | Step 0 | Ownership changes, governance events |
| Graph (edge:org-org) | Step 0 | x-history events |
| Step 0 | Step 1 | Anomaly → triggers assessment for specific pair |
| Graph (edge:org-org) | Step 1 | Ownership data, prior control assessment |
| Step 1 | Graph (edge:org-org) | Updated control_conclusion |
| Graph (all edges in scope) | Step 2 | Complete ownership graph with control conclusions |
| Step 2 | Graph (ctx-v) | Consolidation scope view |
| Step 2 | Anomalies | Scope changes, date/policy misalignments |
| Graph (ctx-v + edges) | Step 3 | Scope + ownership percentages |
| Step 3 | Graph (edge:org-org) | nci_pct per entity |
| Step 3 | BC (business-unit.minority-pct) | NCI for consolidation engine |
| BC | Step 4 | Business Unit setup, GL data, IC data |
| Step 4 | BC | Consolidated trial balance, elimination entries |

---

## Nodes and Edges Touched

### Nodes

| Node type | Role in chain |
|---|---|
| `node:org` | The entities being assessed. Properties read: governance (entity_type, reporting_date, accounting_policy_set, materiality) |
| `node:ind` | Board members (for power assessment). CFO/Controller (as HitL effector) |
| `node:anomaly` | Raised by monitor (step 0) and scope determination (step 2) |
| `node:decision` | Created when HitL required (de facto control, SPE, investment entity) |
| `node:pragma` (ergon instances) | One Pragma per ergon execution (per period, per entity pair for step 1) |

### Edges

| Edge type | Role in chain |
|---|---|
| `edge:org-org` | The ownership relationship — primary data source and write target |
| `edge:ind-org.board-member` | Board composition — monitored for power assessment |
| `effector` | IND cast on Pragma for HitL steps |
| `addresses` | Anomaly → Pragma (triggered work) |
| `achieves` | Pragma → Goal (IFRS 10 compliance) |

---

## Failure Patterns Addressed

| Pattern | How this chain prevents it |
|---|---|
| #1 Consolidation scope manipulation | Control assessment (step 1) + scope determination (step 2) ensure all controlled entities are consolidated |
| #1 (passive) Failure to detect change | Reassessment monitor (step 0) detects trigger events continuously |
| #4 Related-party/IC errors | NCI calculation (step 3) ensures correct equity attribution |
| #6 Auditor complacency | Documented assessment trail (x-history on control conclusions) supports audit |

---

## Cadence

| Context | Frequency |
|---|---|
| Listed company (NASDAQ Stockholm) | Quarterly (Q1, H1, Q3, Annual) |
| Non-listed group | Annual minimum |
| Between periods | Continuous monitoring (step 0 only) |
| M&A event | Immediate trigger for steps 1-3 |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Is every controlled entity consolidated? Are control assessments current? De facto control for <50% cases documented? SPEs assessed? NCI correctly calculated? | Scope = the foundation. Wrong scope → everything downstream is wrong. Enron: 3000 SPEs off-balance-sheet. |
| **Reserve** | NCI concentration: is the group dependent on one subsidiary? Foreign sub scope → creates FX Ghost (FCTR via IAS 21). Goodwill Ghost (via IFRS 3 → IAS 36). | Scope determines WHICH Ghosts exist. Each foreign sub = an FCTR Ghost. Each acquisition = a goodwill Ghost. |
| **Sword** | What xItems does each entity in scope sell? Where is xtValue being created? Which entities are the Sword (growth engines) vs Shield (stable, cash-generating)? | Scope shows the group's portfolio. Sword identifies which entities to invest in vs maintain vs exit. |

## Ghost Dimension

Scope determination creates the Ghost inventory:
- Each **foreign subsidiary** in scope creates an FCTR Ghost (IAS 21) — equity moves without cash.
- Each **acquisition** with goodwill creates a goodwill Ghost (IAS 36) — impairment hits equity without cash.
- Each subsidiary with **defined benefit pensions** creates a pension Ghost (IAS 19) — remeasurements hit OCI → equity.
- Each subsidiary with **DTA** creates a tax Ghost (IAS 12) — write-off hits equity.

**IFRS 10 scope = the register of all Ghosts.** ABL KBR monitors the combined effect.

## Tamagos Connection

- **Control gained** (new subsidiary): often triggered by an M&A Tamagos hatching. The buying group's Tamagos (the deal forming between buyer and target) hatches → control obtained → IFRS 10 triggers → IFRS 3 follows.
- **Control lost** (disposal): the reverse. An IFRS 5 held-for-sale classification may precede. The disposal IS a Tamagos from the buyer's perspective.
- **Scope determines which entities' xItem revenue flows into the group.** Each entity sells xItems (gItem/vItem/hItem). The scope determines which xItems' revenue consolidates.

## xItem Connection

Each entity in consolidation scope sells xItems. The scope determines:
- Which xItem revenue is in the group's consolidated P&L
- Which IC xItem transactions require elimination (edge:org-org → sells_to with xitem_refs)
- Which xItem types drive segment reporting (IFRS 8 → discovered from xItem × ORG.buyer)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — IFRS 10 complete chain with 4 ergons + monitor |
| 1.1 | 2026-04-02 | Added S-R-S view, Ghost dimension (FCTR, goodwill, pensions, DTA), Tamagos connection (M&A trigger), xItem connection (scope determines which xItem revenue consolidates). Aligned with FGGE taxonomy. |
