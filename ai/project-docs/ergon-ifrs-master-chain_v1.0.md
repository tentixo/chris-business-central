# Ergon Master Chain: IFRS Consolidation

**Version**: 1.0
**Status**: Draft
**Intent**: Capture inter-standard triggers — when one IFRS chain's output becomes another chain's input
**Parent**: ai/reports/dr-manhattan-financial-union-list_v1.md (Track 1)

---

## Why This Exists

Each IFRS standard has its own ergon chain (IFRS 10, IFRS 3, IAS 21, etc.). But the standards don't exist in isolation — they trigger each other. IFRS 10 "control gained" triggers IFRS 3 "business combination." IFRS 3 "goodwill created" triggers IAS 36 "annual impairment test." Missing a trigger = missing a required accounting treatment.

This master chain maps the triggers between chains so nothing falls through the cracks.

---

## Master Chain Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  EVENT LAYER (what happens in Reality)                               │
│                                                                      │
│  Acquisition ── Ownership change ── Disposal ── New IC trading ──   │
│  FX rate move ── Impairment indicator ── Period end                  │
└────────┬────────────────┬──────────────┬────────────────────────────┘
         │                │              │
         ▼                ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  IFRS 10 CHAIN (WHO is in the group?)                                │
│  Control assessment → Scope → NCI → BC Consolidation                 │
└────┬──────────┬──────────┬──────────┬───────────────────────────────┘
     │          │          │          │
     │ control  │ control  │ scope    │ scope
     │ GAINED   │ LOST     │ set      │ set
     ▼          ▼          ▼          ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌───────────┐
│ IFRS 3  │ │IFRS 3  │ │IAS 21  │ │IC ELIM    │
│ chain   │ │reverse │ │chain   │ │chain      │
│(acquire)│ │(dispose)│ │(FX)   │ │           │
└────┬────┘ └───┬────┘ └───┬────┘ └─────┬─────┘
     │          │          │             │
     │ goodwill │ gain/    │ FCTR        │ elimination
     │ + PPA    │ loss     │ movements   │ entries
     │ created  │ + FCTR   │             │
     │          │ recycled │             │
     ▼          │          ▼             ▼
┌─────────┐    │    ┌──────────────────────────┐
│ IAS 36  │    │    │  IAS 12 CHAIN            │
│ chain   │    │    │  (Deferred tax on ALL    │
│(impair) │    │    │   consolidation           │
└────┬────┘    │    │   adjustments)            │
     │         │    └──────────────────────────┘
     │ impair- │              ▲
     │ ment    │              │ PPA fair value uplifts
     │ loss    │              │ IC profit elimination
     ▼         ▼              │ Goodwill (no DT!)
┌─────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│  DONE2: GROUP NUMBERS COMPLETE                                       │
│  Consolidated trial balance with all adjustments                     │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  SUPPORTING CHAINS (run in parallel with above)                      │
│                                                                      │
│  IAS 24 chain ─── Related party identification + disclosure          │
│  IFRS 8 chain ─── Segment reporting (management approach)            │
│  IAS 33 chain ─── EPS calculation                                    │
│  IAS 19 chain ─── Pension obligations                                │
│  IAS 37 chain ─── Provisions + contingent liabilities                │
│  IFRS 15 chain ── Revenue recognition (group-wide policy)            │
│  IFRS 16 chain ── Lease identification + ROU assets                  │
│  IFRS 9 chain ─── Financial instruments + ECL                        │
│  ABL KBR chain ── Equity monitoring (Swedish Rim)                    │
│  CSRD chain ───── Sustainability reporting                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Inter-Standard Triggers

### Acquisition Triggers (control GAINED)

| Event | Source chain | Triggers | Target chain | Why |
|---|---|---|---|---|
| Control obtained over new entity | IFRS 10 (control assessment) | **IFRS 3** | Business Combination chain | Must perform PPA, recognize goodwill, measure NCI |
| Foreign subsidiary acquired | IFRS 3 (acquisition complete) | **IAS 21** | FX Translation chain | Must determine functional currency, set up translation |
| Goodwill recognized | IFRS 3 (PPA complete) | **IAS 36** | Impairment chain | Goodwill must be allocated to CGU, tested annually |
| PPA fair value uplifts | IFRS 3 (PPA complete) | **IAS 12** | Deferred Tax chain | Deferred tax on temporary differences from fair value adjustments |
| New entity in scope | IFRS 10 (scope determination) | **IC Elimination** | IC chain | New IC relationships may exist |
| New entity in scope | IFRS 10 (scope determination) | **IAS 24** | Related Party chain | New RPT disclosure requirements |
| New entity in scope | IFRS 10 (scope determination) | **IFRS 8** | Segment chain | May affect segment reporting |

### Disposal Triggers (control LOST)

| Event | Source chain | Triggers | Target chain | Why |
|---|---|---|---|---|
| Control lost over entity | IFRS 10 (control assessment) | **IFRS 3 (reverse)** | Derecognition | Derecognize assets/liabilities, recognize gain/loss |
| Retained interest | IFRS 3 (reverse) | **IAS 28 or IFRS 9** | Remeasure | Retained interest at fair value → equity method or IFRS 9 |
| Foreign sub disposed | IFRS 3 (reverse) | **IAS 21** | FCTR recycling | Cumulative FX translation reserve → P&L |
| Goodwill derecognized | IFRS 3 (reverse) | **IAS 36** | Remove from CGU | Goodwill no longer tested |
| Entity removed from scope | IFRS 10 (scope) | **IC Elimination** | Remove IC | IC with disposed entity no longer eliminated |

### Periodic Triggers (each reporting date)

| Event | Source | Triggers | Target chain | Why |
|---|---|---|---|---|
| Period end | Calendar | **IAS 21** | FX Translation | Translate all foreign subs at closing rate |
| Period end | Calendar | **IAS 36** | Impairment test | Annual test for goodwill + indefinite-life intangibles |
| Period end | Calendar | **IC Elimination** | Full IC elim | Recalculate all eliminations from scratch |
| Period end | Calendar | **IAS 12** | Deferred tax | Recalculate all consolidated deferred tax positions |
| Period end | Calendar | **IAS 33** | EPS | Calculate basic + diluted EPS |
| Period end | Calendar | **ABL KBR** | Equity check | Monitor equity vs. share capital threshold |
| Contingent consideration | IFRS 3 (ongoing) | **P&L** | Remeasure | Fair value change through P&L each period |

### Event Triggers (between reporting dates)

| Event | Source | Triggers | Target chain | Why |
|---|---|---|---|---|
| Ownership % changes (no control change) | IFRS 10 monitor | **NCI recalc** | IFRS 10 step 3 | Equity transaction (NCI changes within equity, no P&L) |
| Impairment indicator detected | IAS 36 monitor | **IAS 36** | Interim impairment test | Can't wait for annual test |
| Significant FX rate movement | IAS 21 monitor | **Risk assessment** | Sensitivity update | May affect covenant headroom, KBR |
| Step acquisition (increase %) | IFRS 10 | **IFRS 3** | Additional PPA? | Only if control gained at this step; if already controlled = equity transaction |
| Hyperinflation detected | IAS 29 monitor | **IAS 29 + IAS 21** | Restate + translate | All items at closing rate (exception) |

---

## Execution Order per Reporting Period

The master chain has a required ordering. Some chains can run in parallel, others must be sequential.

### Phase 1: Scope (must complete first)

```
1. IFRS 10 chain: Control assessment → Scope → NCI
   Output: Who is in the group, at what %, under what method
```

### Phase 2: Acquisition/Disposal accounting (if events occurred)

```
2a. IFRS 3 chain: PPA for new acquisitions (if any)
2b. IFRS 3 reverse: Derecognition for disposals (if any)
    These can run in parallel with each other.
    Output: Goodwill, intangibles, gains/losses, contingent consideration
```

### Phase 3: Translation + Adjustments (after scope and PPA settled)

```
3a. IAS 21 chain: FX translation of all foreign subsidiaries
3b. IC Elimination chain: Eliminate all intercompany transactions
3c. IAS 36 chain: Impairment testing (goodwill + indefinite-life intangibles)
3d. IAS 19 chain: Pension obligation remeasurement
3e. IFRS 15/16/9 chains: Standard-specific adjustments
    These can run in parallel with each other.
    Output: Translated balances, elimination entries, impairment charges
```

### Phase 4: Tax (after all adjustments known)

```
4. IAS 12 chain: Deferred tax on ALL consolidation adjustments
   Depends on: Phase 2 (PPA creates temporary differences)
               Phase 3a (FX translation creates deferred tax)
               Phase 3b (IC profit elimination creates deferred tax)
               Phase 3c (Impairment may reverse deferred tax)
   NOTE: No deferred tax on initial goodwill recognition (IAS 12.15)
   Output: Group deferred tax positions
```

### Phase 5: Completion (after all adjustments + tax)

```
5a. IAS 33: EPS calculation (needs final net income attributable to parent)
5b. IFRS 8: Segment reporting (needs final segment allocations)
5c. IAS 24: Related party disclosures (needs final transaction data)
5d. ABL KBR: Equity check (needs final equity figure)
    These can run in parallel.
    Output: EPS, segment note, RPT note, Rim status
```

### Phase 6: Done2 complete

```
6. Consolidated trial balance with all adjustments
   → Feeds into Done2→Done3 (report production)
```

---

## Parallel vs Sequential

```
Phase 1 ──────────────────────── SEQUENTIAL (must complete first)
    │
Phase 2a ──┐
Phase 2b ──┤── PARALLEL (independent acquisitions/disposals)
    │      │
    ▼      ▼
Phase 3a ──┐
Phase 3b ──┤
Phase 3c ──┤── PARALLEL (independent adjustments)
Phase 3d ──┤
Phase 3e ──┘
    │
Phase 4 ──────────────────────── SEQUENTIAL (needs all adjustments)
    │
Phase 5a ──┐
Phase 5b ──┤── PARALLEL (independent completion tasks)
Phase 5c ──┤
Phase 5d ──┘
    │
Phase 6 ──────────────────────── DONE2 COMPLETE
```

---

## Nodes and Edges Across All Chains

| Document type | Role in master chain |
|---|---|
| `node:org` | The entities being consolidated. Carries governance properties. |
| `edge:org-org` | Bilateral relationship. Carries ownership (IFRS 10), IC data (elimination), lending (IAS 24). |
| `edge:ind-org.board-member` | Board composition. Monitored for control (IFRS 10) and RPT (IAS 24). |
| `edge:ind-org.kmp` | KMP relationships. IAS 24 disclosure. |
| `node:anomaly` | Raised by any chain when something needs attention. |
| `node:decision` | HitL judgment calls (de facto control, CGU allocation, impairment assumptions). |
| `node:pragma` (ergon) | One instance per ergon execution per period per entity. |
| `node:goal` | "Consolidated FS are IFRS compliant for period {X}" |
| `ctx-v` | Consolidation scope, segment views, CGU views. |

---

## Connection to S-R-S

| Phase | S-R-S zone | Why |
|---|---|---|
| Phases 1-4 | **Shield** | Rim compliance — these MUST be done correctly or personal liability |
| Phase 5d (KBR) | **Shield** (critical Rim) | Direct personal liability trigger for board |
| Impairment sensitivity | **Reserve** lens | Headroom between carrying amount and recoverable amount |
| Segment reporting | **Sword** lens | Management's view of the business (CODM approach) |
| EPS | **Market** output | What shareholders and analysts see |

---

## Connection to Done1 → Done2 → Done3

| Done phase | Master chain coverage |
|---|---|
| **Done1** (entity-level close) | Each subsidiary produces IFRS-compliant trial balance. Prerequisite for all chains. |
| **Done2** (group numbers) | Phases 1-5 = the complete Done2 process. This master chain IS Done2. |
| **Done3** (report production) | Phase 6 output feeds into report production (notes, commentary, audit). |

---

## Future Chains to Define

| Chain | Status | Priority |
|---|---|---|
| [IFRS 10](ergon-ifrs-10-chain_v1.0.md) | Defined (v1.0) | Done |
| [IFRS 3](ergon-ifrs-3-chain_v1.0.md) — Business Combinations | Defined (v1.0) | Done |
| [IFRS 5](ergon-ifrs-5-chain_v1.0.md) — Held for Sale / Discontinued Ops | Defined (v1.0) | Done |
| [IFRS 8](ergon-ifrs-8-chain_v1.0.md) — Operating Segments | Defined (v1.0) | Done |
| [IFRS 13](ergon-ifrs-13-fair-value_v1.0.md) — Fair Value Measurement | Defined (v1.0) | Done (service ergon — invoked by others) |
| [IAS 21](ergon-ias-21-chain_v1.0.md) — FX Translation | Defined (v1.0) | Done |
| [IFRS 15](ergon-ifrs-15-chain_v1.0.md) — Revenue from Contracts | Defined (v1.0) | Done |
| [IFRS 16](ergon-ifrs-16-chain_v1.0.md) — Leases | Defined (v1.0) | Done |
| [IFRS 17](ergon-ifrs-17-chain_v1.0.md) — Insurance Contracts | Defined (v1.0) | Done (scope test + consolidation interface, specialist systems handle detail) |
| IAS 21 — FX Translation | Pending | High — affects every foreign sub |
| [IAS 36](ergon-ias-36-chain_v1.0.md) — Impairment | Defined (v1.0) | Done |
| [IAS 12](ergon-ias-12-chain_v1.0.md) — Deferred Tax | Defined (v1.0) | Done |
| [IC Elimination](ergon-ic-elimination-chain_v1.0.md) — Intercompany | Defined (v1.0) | Done |
| [IAS 24](ergon-ias-24-chain_v1.0.md) — Related Party Disclosures | Defined (v1.0) | Done |
| IFRS 8 — Segments | Pending | Medium — management approach |
| [IAS 33](ergon-ias-33-chain_v1.0.md) — Earnings Per Share | Defined (v1.0) | Done |
| [ABL KBR](ergon-abl-kbr-chain_v1.0.md) — Equity Monitor (Kontrollbalansräkning) | Defined (v1.0) | Done — THE critical Rim |
| [IFRS 9](ergon-ifrs-9-chain_v1.0.md) — Financial Instruments | Defined (v1.0) | Done |
| [IAS 34](ergon-ias-34-chain_v1.0.md) — Interim Financial Reporting | Defined (v1.0) | Done — the flight schedule |
| [IAS 8](ergon-ias-8-chain_v1.0.md) — Accounting Policies, Estimates, Errors | Defined (v1.0) | Done — the meta-standard |
| [IAS 1](ergon-ias-1-chain_v1.0.md) — Presentation of Financial Statements | Defined (v1.0) | Done — output format + going concern + IFRS 18 preview |
| [IAS 7](ergon-ias-7-chain_v1.0.md) — Statement of Cash Flows | Defined (v1.0) | Done — the reality check + fractal problem |
| [IAS 2](ergon-ias-2-chain_v1.0.md) — Inventories | Defined (v1.0) | Done — gItem territory, BC setup critical |
| [IAS 19](ergon-ias-19-chain_v1.0.md) — Employee Benefits / Pensions | Defined (v1.0) | Done |
| [IAS 37](ergon-ias-37-chain_v1.0.md) — Provisions + Contingent Liabilities | Defined (v1.0) | Done |
| IFRS 15 — Revenue | Pending | Depends on group profile |
| IFRS 16 — Leases | Pending | Depends on group profile |
| [IFRS 9](ergon-ifrs-9-chain_v1.0.md) — Financial Instruments | Defined (v1.0) | Done |
| CSRD — Sustainability | Pending | Phasing in 2024-2027 |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — master chain with inter-standard triggers, execution ordering, parallel/sequential mapping |
