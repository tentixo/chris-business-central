# Ergon: IFRS 3 — Measurement Period Monitor

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 3.45-50
**Intent**: Track the 12-month measurement period after acquisition. During: adjustments are retrospective (restate opening BS). After: adjustments through P&L.
**Chain**: ergon-ifrs-3-chain_v1.0.md (ongoing)

---

## Why This Matters

The 12-month measurement period is a window where the acquirer can finalize the PPA. During this period, new information about facts and circumstances that existed at the acquisition date can adjust the initial PPA retrospectively. After the window closes, ANY changes go through P&L — no more goodwill adjustments.

Companies sometimes game this deadline — rushing adjustments in before 12 months, or "discovering" information conveniently within the window.

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | PPA completed (ergon-ifrs-3-business-combination step 7) → monitor starts |
| **Deadline** | acquisition_date + 12 months = measurement_period_end |

---

## Sub-Ergons

### Step 1: Set deadline and begin monitoring [MACH]

```
Read: edge:org-org → ppa.measurement_period_end
Set: status = "in_measurement_period"

Create scheduled checks:
  - Monthly: "Any new information about acquisition-date facts?"
  - At month 10: "WARNING: 2 months remaining in measurement period"
  - At month 11: "CRITICAL: 1 month remaining — finalize PPA"
  - At month 12: "DEADLINE: Measurement period ends. Finalize NOW."
```

### Step 2: Process measurement period adjustments [IND + MACH]

```
IF new information discovered about facts/circumstances at acquisition date:

  During measurement period (IFRS 3.45):
    → RETROSPECTIVE adjustment
    → Restate the opening balance sheet AS IF the new information was known at acquisition
    → Adjust: identifiable assets/liabilities at FV → recalculate goodwill
    → Comparatives restated
    → Record: what changed, why, evidence it relates to acquisition-date facts

  After measurement period (IFRS 3.50):
    → PROSPECTIVE through P&L
    → No goodwill adjustment
    → Changes in estimates → P&L
    → Changes in contingent consideration → P&L (if liability) or equity (if equity)

  ALWAYS:
    → Record adjustment in x-history on edge:org-org → ppa
    → Document rationale (auditor will challenge)
```

### Step 3: Finalize PPA [IND]

```
At or before measurement_period_end:
  Review all PPA components:
    - Are all identifiable assets/liabilities at final fair value?
    - Are external valuations complete and documented?
    - Is goodwill calculation final?
    - Are intangible useful lives confirmed?
    - Is contingent consideration at current fair value?

  IF all finalized:
    edge:org-org → ppa.status = "finalized"
    No further retrospective adjustments possible.

  IF not fully finalized at deadline:
    → Must finalize with best available information
    → edge:org-org → ppa.status = "finalized" (forced)
    → Any future changes → P&L only
    → Anomaly: "PPA finalized at deadline with incomplete information"
```

---

## Rim Consequence

- Adjustments after measurement period that should have been within = restatement risk
- Audit focus: were adjustments genuinely about acquisition-date facts, or management trying to manage goodwill?
- ESMA finding: measurement period adjustments made after the 12-month window

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial |
