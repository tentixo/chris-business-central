# Ergon Chain: IFRS 15 — Revenue from Contracts with Customers

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 15 (complete standard)
**Intent**: Recognize revenue correctly — when, how much, for what. The five-step model applied to every customer contract. Connected to xItem taxonomy (g/v/h), xtValue patterns, and V-P-C-T-TC output.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — adjustment, parallel with others)
**NOT applicable to**: vItem.financial (IFRS 9 Rim), insurance (IFRS 17), leases (IFRS 16), government grants (IAS 20)

---

## Chain Overview

```
TAMAGOS HATCHES (IFRS event — contract born)
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 1: IDENTIFY THE CONTRACT          │
│  Enforceable? Commercial substance?      │
│  = Tamagos hatching criteria             │
│  IFRS 15.9-16                            │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 2: IDENTIFY PERFORMANCE           │
│  OBLIGATIONS                             │
│  Each xItem in xPackage: distinct?       │
│  gi-Eidos test                           │
│  IFRS 15.22-30                           │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 3: DETERMINE TRANSACTION PRICE    │
│  Fixed + variable (constrained) +        │
│  non-cash - payable to customer          │
│  ± financing component                   │
│  IFRS 15.47-72                           │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 4: ALLOCATE TO OBLIGATIONS        │
│  By relative SSP per performance         │
│  obligation                              │
│  IFRS 15.73-86                           │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 5: RECOGNIZE REVENUE              │
│  Per xtValue pattern:                    │
│  Point (gItem) / Progressive (hItem) /   │
│  Continuous (vItem)                      │
│  IFRS 15.31-45                           │
└──────────────┬──────────────────────────┘
               ▼
┌──────────────────────────────────────────┐
│  ONGOING: CONTRACT MODIFICATIONS         │
│  New contract / prospective / catch-up    │
│  ONGOING: CONTRACT COST ASSETS           │
│  Capitalize if recoverable, amortize     │
│  ONGOING: CONTRACT BALANCE MONITORING    │
│  Receivable / contract asset / liability  │
└──────────────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 1-2 | [contract-and-obligations](ergon-ifrs-15-contract-and-obligations_v1.0.md) | At Tamagos hatching (contract inception) | IND (judgment on distinct) + MACH (xItem classification) | Contract identified, POs mapped |
| 3-4 | [price-and-allocation](ergon-ifrs-15-price-and-allocation_v1.0.md) | At contract inception + when modified | IND (variable estimation, SSP) + MACH (allocation math) | Transaction price allocated per PO |
| 5 | [recognition](ergon-ifrs-15-recognition_v1.0.md) | Ongoing per xtValue pattern | MACH (time-based, milestone) + IND (% completion judgment) | Revenue recognized in P&L |
| Ongoing | [modifications-and-costs](ergon-ifrs-15-modifications-and-costs_v1.0.md) | When contract changes or costs incurred | IND (modification treatment) + MACH (amortization) | Updated POs, contract cost assets |

---

## Connection to xItem Taxonomy

| xItem type | Typical PO pattern | Recognition | xtValue |
|---|---|---|---|
| gItem.physical | Single PO per item. Transfer at delivery. | Point-in-time | Point |
| gItem.energy | Single PO. Transfer as consumed (metered). | Over-time (simultaneous receive/consume) | Continuous |
| vItem.e-svc (one-time) | Single PO. Transfer at download/access grant. | Point-in-time | Point |
| vItem.e-svc (subscription) | Single stand-ready PO per period. | Over-time (time-elapsed) | Continuous |
| vItem.financial | NOT IFRS 15 — goes to IFRS 9 | N/A | N/A |
| hItem.consulting (T&M) | Single PO (or per-period). Right to invoice practical expedient. | Over-time (simultaneous receive/consume) | Progressive |
| hItem.consulting (Fixed) | Single PO (or per deliverable if distinct). | Over-time (no alternative use + right to payment) OR point-in-time (at acceptance) | Progressive |
| hItem.labor | Per-task or per-period PO. | Over-time (simultaneous receive/consume) | Progressive |
| xPackage.project | Multiple POs — one per distinct xItem. | Mixed: each PO per its own pattern. | Mixed |
| xPackage.continuous | Stand-ready + specific services. | Over-time + per-event. | Continuous + Progressive |

---

## Dependencies

```
Tamagos hatching → IFRS 15 starts (Steps 1-4 at inception)
IFRS 15 Step 5 → Revenue in P&L → feeds IFRS 10 consolidation
IFRS 15 allocation → needs xItem.SSP → may need IFRS 13 (fair value for SSP estimation)
IFRS 15 variable consideration → may interact with IFRS 3 (contingent consideration on acquisition)
IFRS 15 per entity → must use uniform policies across group (IFRS 10.19)
Contract modification → may trigger re-assessment of all 5 steps
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — five-step model mapped to xItem/xPackage/edge/xtValue. Connected to Tamagos hatching, V-P-C-T-TC, gi-Eidos test. |
