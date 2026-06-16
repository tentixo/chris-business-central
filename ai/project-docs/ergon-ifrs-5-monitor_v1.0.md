# Ergon: IFRS 5 — Held-for-Sale Ongoing Monitor

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 5.9-14, 15, 20-25, 26-29
**Intent**: Reassess held-for-sale classification each period: still highly probable? Within 12 months? Remeasure FVLCD. Handle abandonment.
**Chain**: ergon-ifrs-5-chain_v1.0.md (ongoing)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting period while node:org → held_for_sale.classified = true |
| **Event** | Sale completes (disposal.status = completed) |
| **Event** | Plan abandoned (disposal.status = abandoned) |
| **Event** | 12-month deadline approaching or passed |

---

## Sub-Ergons

### Step 1: Reassess held-for-sale criteria [IND]

```
Each reporting period, reassess ALL original criteria:

  [ ] Still committed to sell?
  [ ] Still available for immediate sale?
  [ ] Still actively marketing?
  [ ] Still highly probable?
  [ ] Still expected within 12 months?
  [ ] Still at reasonable price?

IF all still met → continue as held for sale → proceed to Step 2

IF one or more criteria NO LONGER met → go to Step 4 (Abandonment)
```

### Step 2: Remeasure FVLCD [IND + external if needed]

```
IFRS 5.15:

Each period, remeasure at LOWER of:
  a) Carrying amount at classification (LESS any cumulative impairment recognized)
  b) Fair value less costs to sell (UPDATED)

IF FVLCD has declined since last period:
  → Additional impairment loss → P&L
  → Allocate: first to goodwill (if any remaining), then pro rata to other assets
  → Update: node:org → held_for_sale.fair_value_less_costs_to_sell

IF FVLCD has increased since last period:
  → Reversal of impairment loss → P&L
  → BUT: reversal cannot exceed cumulative impairment previously recognized
  → AND: never reverse goodwill impairment (IAS 36)
  → Update: node:org → held_for_sale.fair_value_less_costs_to_sell

REMEMBER: Depreciation still stopped. Do not resume.
```

### Step 3: Check 12-month deadline [MACH]

```
IFRS 5.8-9:

Calculate: months since classification_date

IF < 10 months → normal monitoring
IF 10-11 months → WARNING: "Approaching 12-month deadline for {org}"
IF = 12 months → CRITICAL: must complete or justify exception

EXCEPTIONS (IFRS 5.B1 — sale can extend beyond 12 months IF):
  (a) Delay caused by events beyond entity's control AND
  (b) Sufficient evidence that entity remains committed to its plan

  Specific exceptions:
    - Buyer imposes unexpected conditions → entity responding promptly
    - Regulatory approval delayed
    - Unexpectedly, only offers below reasonable FV received
      AND entity takes actions to respond to the low offers

  IF exception applies:
    → Document reason
    → node:org → held_for_sale.twelve_month_exception = true
    → node:org → held_for_sale.twelve_month_exception_reason = "..."
    → Continue as held for sale

  IF no exception applies AND 12 months passed:
    → Must reclassify OUT of held for sale → Step 4 (Abandonment)
    → Anomaly: "12-month deadline passed without sale or valid exception for {org}"
```

### Step 4: Abandonment / Reclassification [IND + MACH]

```
IFRS 5.26-29:

When held-for-sale classification is REVERSED (plan abandoned or criteria no longer met):

  1. RESUME DEPRECIATION from the date the criteria ceased to be met
     (or the 12-month expiry, whichever earlier)

  2. REMEASURE at the LOWER of:
     a) Carrying amount as if NEVER classified held for sale
        (what the carrying amount would have been if depreciation had continued)
     b) Recoverable amount (per IAS 36) at the date of the decision
        not to sell

  3. ADJUST through P&L
     The difference between the held-for-sale carrying amount
     and the remeasured amount → P&L

  This can result in a CATCH-UP depreciation charge — the accumulated
  depreciation that was skipped during the held-for-sale period.

Write to graph:
  node:org → held_for_sale.classified = false (x-history records the reversal)
  edge:org-org → disposal.status = "abandoned"
  edge:org-org → disposal.planned = false

Write to BC:
  Resume depreciation in Fixed Asset register
  Post catch-up depreciation entries
  Reverse BS reclassification (back to normal line items)
  If was discontinued operation: reverse P&L single-line presentation
```

### Step 5: Sale Completes [triggers master chain]

```
When disposal.status = "completed":

  This ergon's job is done. Completion triggers:
  → Master chain: IFRS 3 reverse (derecognition)
    - Derecognize all subsidiary assets/liabilities
    - Derecognize goodwill
    - Recognize gain/loss in P&L
    - Recycle FCTR from OCI to P&L (IAS 21)
    - If retained interest: remeasure at FV → equity method (IAS 28) or IFRS 9

  → IFRS 10 chain: remove from consolidation scope
  → IC Elimination chain: remove IC relationships with disposed entity

Write to graph:
  edge:org-org → disposal.completion_date = actual date
  edge:org-org → disposal.actual_proceeds
  edge:org-org → disposal.actual_gain_loss
  edge:org-org → owns.control_assessment.control_conclusion = false (control lost)
  node:org → held_for_sale.classified = false
```

---

## Output

| Target | What | Condition |
|---|---|---|
| `node:org` → held_for_sale | Updated FVLCD, impairment, exception flags | Each period |
| `edge:org-org` → disposal | Updated status, proceeds estimate | Each period |
| `node:anomaly` | "12-month deadline approaching for {org}" | At month 10 |
| `node:anomaly` | "12-month deadline passed without completion or exception" | At month 12 |
| `node:anomaly` | "FVLCD declined — additional impairment for {org}" | When FVLCD drops |
| `node:anomaly` | "Held-for-sale criteria no longer met — reclassify {org}" | When criteria fail |
| Master chain | Derecognition trigger | When sale completes |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Not monitoring the 12-month deadline | Held-for-sale classification stale → depreciation wrongly stopped → assets overstated |
| Not remeasuring FVLCD | Impairment missed → assets overstated |
| Abandoning plan but not reversing classification | Depreciation still stopped → catch-up charge building silently → future P&L shock |
| Not resuming depreciation on reversal | Carrying amount wrong going forward |
| ESMA common finding | Extending the 12-month period without meeting specific exception criteria |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial |
