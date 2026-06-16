# Ergon Chain: IAS 8 — Accounting Policies, Changes in Estimates and Errors

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 8 (complete standard)
**Intent**: When accounting changes or errors occur — classify correctly (policy change, estimate change, or error), apply correct treatment (retrospective or prospective), disclose. The META-standard governing how changes flow through the financial statements.
**Master chain**: ergon-ifrs-master-chain_v1.0.md — IAS 8 is not a phase. It's a RULE that applies whenever any other chain produces a change.

---

## Why This Matters

Every ergon chain can produce an IAS 8 event:

| Source chain | Example of change | IAS 8 classification |
|---|---|---|
| **IAS 36** | Revised useful life of intangible → changes depreciation | Change in ESTIMATE → prospective |
| **IAS 36** | Switch from cost model to revaluation model for PP&E | Change in POLICY → retrospective |
| **IFRS 15** | Discovered revenue was recognized in wrong period last year | ERROR → retrospective restatement |
| **IFRS 16** | Revised lease term (extension option reassessed) | Change in ESTIMATE → prospective (remeasure) |
| **IAS 19** | Updated mortality table → changes pension obligation | Change in ESTIMATE → prospective (but goes through OCI as remeasurement) |
| **IAS 12** | New tax law changes the rate → recalculate deferred tax | Change in ESTIMATE → current period |
| **IFRS 9** | Revised ECL model methodology | Change in POLICY (if model framework changes) or ESTIMATE (if just inputs change) |
| **IFRS 8** | CODM reorganizes → segments change | Not IAS 8 per se, but IFRS 8.29 requires restating comparatives → same effect as retrospective |
| **New IFRS standard** (e.g., IFRS 18 effective 2027) | Adopt new standard | Change in POLICY → apply transition provisions of the NEW standard (may override IAS 8 general rule) |

---

## The Three Scenarios

### 1. Change in Accounting Policy (IAS 8.14-27)

```
WHAT: A different accounting principle is applied to the same type of transaction.

  Examples:
    - Switch inventory method (FIFO → weighted average)
    - Switch PP&E model (cost → revaluation)
    - Adopt a new IFRS standard (mandatory change)
    - Voluntary change to more relevant/reliable method

  WHEN ALLOWED:
    a) REQUIRED by a new or revised IFRS standard, OR
    b) VOLUNTARY: results in more relevant and reliable information.
    Cannot change just because management prefers a different number.

  TREATMENT: RETROSPECTIVE
    → Adjust opening balances of the EARLIEST prior period presented.
    → Restate ALL comparative periods as if the new policy had ALWAYS been applied.
    → Cumulative effect of change recognized in opening retained earnings
      of the earliest period presented.

  EXCEPTION: impracticable to determine the cumulative effect →
    Apply from the earliest date practicable (IAS 8.24).

  For new IFRS standards:
    The NEW standard's transition provisions take PRECEDENCE over IAS 8.
    Many new standards offer simplified transition (e.g., IFRS 16 allowed
    modified retrospective with cumulative catch-up, no restatement).

  DISCLOSURE (IAS 8.28-31):
    - Nature of the change
    - Reasons (if voluntary)
    - Amount of adjustment for current and each prior period presented
    - Amount of adjustment to periods before those presented
    - If impracticable: explain why, describe how the change was applied
```

### 2. Change in Accounting Estimate (IAS 8.32-40)

```
WHAT: New information or developments cause a revision of a previous estimate.

  Examples:
    - Revised useful life of PP&E or intangible → future depreciation changes
    - Revised ECL rate for receivables → provision changes
    - Revised warranty claim rate → provision changes
    - Revised discount rate for pensions → DBO changes (but this goes OCI per IAS 19)
    - Revised expected cost for onerous contract → provision changes
    - Revised probability for contingent liability → reclassify or adjust
    - Revised impairment assumptions → headroom changes

  TREATMENT: PROSPECTIVE
    → Adjust in the CURRENT period and FUTURE periods affected.
    → Do NOT restate prior periods.
    → The prior estimate was NOT wrong — it was the best estimate
      with the information available at the time.

  DISCLOSURE (IAS 8.39-40):
    - Nature of the change
    - Amount of the effect in current period
    - Expected effect in future periods (if practicable to estimate)

  THE DISTINCTION TEST:
    Is this a change in METHOD (policy) or a change in AMOUNT (estimate)?

    Change in depreciation METHOD (straight-line → reducing balance) → POLICY
    Change in useful LIFE (10 years → 7 years) → ESTIMATE
    Change in ECL MODEL framework (new model) → POLICY
    Change in ECL INPUT data (updated PD/LGD) → ESTIMATE

    If HARD TO DISTINGUISH (IAS 8.35):
      Treat as change in estimate (prospective).
      This is the SAFER default — no restatement.
```

### 3. Correction of Prior Period Error (IAS 8.41-49)

```
WHAT: Omission or misstatement in prior period financial statements
      due to failure to use, or misuse of, RELIABLE INFORMATION that:
      a) Was available when those FS were authorized for issue, AND
      b) Could reasonably be expected to have been obtained and considered.

  This is NOT: a change in estimate based on new information.
  This IS: information that WAS available but was not used (or was used incorrectly).

  Examples:
    - Mathematical error in depreciation calculation
    - Revenue recognized in wrong period (cut-off error)
    - Inventory count error discovered after FS issued
    - Fraud (fictitious transactions booked — Wirecard, Prosolvia)
    - Misapplication of an accounting standard (e.g., classified operating lease
      when it should have been finance lease)

  TREATMENT: RETROSPECTIVE RESTATEMENT
    → Restate comparative amounts for the PRIOR PERIOD(S) in which the error occurred.
    → If error occurred BEFORE the earliest period presented:
      adjust opening balances of the earliest period presented.
    → Disclose the nature of the error.

  EXCEPTION: impracticable → same as policy change exception.

  DISCLOSURE (IAS 8.49):
    - Nature of the error
    - Amount of correction for each prior period (each line item affected)
    - Amount of correction at the beginning of the earliest prior period
    - If impracticable: explain

  THE REPUTATIONAL BOMB:
    A restatement = public admission that prior FS were WRONG.
    → Share price impact (market loses trust)
    → Auditor scrutiny (how did we miss this?)
    → Regulatory attention (ESMA, FI)
    → Personal liability exposure (ABL 29:1 — board signed wrong FS)
    → MAR: restatement may be inside information → immediate disclosure

  FGGE's role: PREVENT errors through the ergon chains (correct process = correct numbers).
  If error IS discovered: classify it correctly (error, not "change in estimate")
  and disclose properly. Trying to disguise an error as an estimate change = worse.
```

---

## The Classification Decision Tree [IND — HitL]

```
Something changed in the numbers. What is it?

  Was the INFORMATION available when prior FS were prepared?
  ├── YES → was it used correctly?
  │         ├── NO → PRIOR PERIOD ERROR → retrospective restatement
  │         └── YES → not an error (the estimate was correct at the time)
  │
  └── NO → new information
          │
          Did the ACCOUNTING METHOD change?
          ├── YES → CHANGE IN POLICY → retrospective
          │         (unless mandated by new standard → follow standard's transition)
          │
          └── NO → the method is the same, only the AMOUNT changed
                    → CHANGE IN ESTIMATE → prospective

  HARD TO TELL? → treat as ESTIMATE (prospective). IAS 8.35.
```

---

## Connection to Our Model

### How IAS 8 events flow through FGGE

```
When any ergon produces a change:

  1. CLASSIFY: policy change, estimate change, or error?
     → ergon-ias-8: apply the decision tree above.

  2. TREAT:
     Policy change or error → RETROSPECTIVE
       → Restate comparatives
       → Adjust opening retained earnings
       → Affects PRIOR PERIOD numbers → ALL downstream chains must be re-run
         for the restated periods (tax, EPS, segments — everything changes)
       → KBR: was KBR headroom DIFFERENT in prior period after restatement?
         If restatement shows equity was below 50% BACK THEN → ?
         (This is legally complex — the board BELIEVED equity was fine,
          but the RESTATED numbers show it wasn't.)

     Estimate change → PROSPECTIVE
       → Current + future periods only
       → Prior periods unchanged
       → Less disruptive but must disclose

  3. DISCLOSE:
     All three scenarios require specific disclosure.
     The ergon that caused the change references IAS 8 in its documentation.
```

### IAS 8 events on node:org

```
When a material IAS 8 event occurs:

  node:anomaly created:
    "IAS 8 event: {type: policy_change | estimate_change | error_correction}
     Source: {ergon that triggered it}
     Description: {what changed}
     Treatment: {retrospective | prospective}
     Periods affected: {list}
     Amount: {material? quantify}"

  If RESTATEMENT:
    → All affected ergon chains re-run for restated periods
    → Updated consolidated trial balance for prior periods
    → Comparative information in ALL future reports reflects the restatement
    → MAR assessment: is this inside information? (likely yes if material)
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Is every change correctly classified? Policy vs estimate vs error? Retrospective applied when required? Disclosures complete? No disguised errors ("we changed our estimate" when it was really an error)? | Misclassification = wrong treatment = misstated comparatives or wrong current period. ESMA checks. |
| **Reserve** | Restatements: how much did prior equity change? Does restated prior equity breach KBR retroactively? What's the magnitude of the error — does it signal systemic problems? | Restatement = trust damage + regulatory risk + potential MAR disclosure. |
| **Sword** | Estimate changes: are they improving accuracy? Is our forecasting getting better (lookback: estimates vs actuals converging)? | Quality improvement: fewer estimate changes over time = better initial estimates = better Shaw Lenses. |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Error disguised as estimate change | Avoid restatement → prior periods remain misstated → auditor catches eventually → worse restatement later | #3 Optimistic + cover-up |
| Material error discovered, not restated | IAS 8.41 violation. Prior periods remain wrong. Auditor qualification. | Shield failure |
| Policy change without retrospective restatement | IAS 8.22 violation (unless new standard's transition overrides). Comparatives misleading. | Shield compliance |
| Restatement triggers MAR disclosure | Inside information: material error corrected → must disclose immediately (MAR Art 17). Failure → FI sanctions. | Swedish Rim |
| Restatement reveals prior KBR breach | Board was unaware equity was below 50% in a prior period. Retroactive personal liability? (Legally complex — NJA case law applies.) | ABL 25:18 + Ghost trap |
| Frequent estimate changes | Market questions: "do they know what they're doing?" Signal of poor estimation quality. | Reputational |

---

## No New Node/Edge Properties

IAS 8 doesn't create new data fields. It creates **node:anomaly** events when changes occur, with classification (policy/estimate/error) and treatment (retrospective/prospective). The anomaly references the source ergon chain that produced the change.

The only tracking needed:

| What | Where | Why |
|---|---|---|
| IAS 8 event log | node:anomaly (type: ias8_event) | Audit trail: what changed, why, how treated, who decided |
| Restatement flag on affected periods | Consolidation records | Which prior periods have been restated (for comparative tracking) |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — three scenarios (policy/estimate/error), decision tree, retrospective vs prospective, IFRIC 10 cross-reference (interim impairment), connection to all other ergon chains, MAR disclosure trigger, KBR retroactive risk |
