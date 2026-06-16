# Ergon: IFRS 3 — Contingent Consideration Remeasurement

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 3.39-40, 3.58
**Intent**: Remeasure contingent consideration (earn-outs) at fair value each reporting period. Changes through P&L (if liability).
**Chain**: ergon-ifrs-3-chain_v1.0.md (ongoing, each reporting period)

---

## What is Contingent Consideration?

"We'll pay an extra EUR 10M if the acquired company's revenue exceeds EUR 50M in the first two years." This is a contingent consideration — additional payment dependent on future events or performance.

At acquisition date: measured at fair value and included in total consideration.
After acquisition date: remeasured each period.

---

## Classification (set at acquisition date, never changed)

| Type | Treatment after acquisition | When used |
|---|---|---|
| **Liability** | Remeasured at fair value each period → changes through P&L | Cash payment dependent on performance/events |
| **Equity** | NOT remeasured. Stays at initial amount. | Settlement by issuing a FIXED number of shares |

Most contingent consideration is classified as LIABILITY (cash earn-outs linked to revenue/EBITDA targets).

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting period where contingent consideration is outstanding |
| **Event** | Target milestone approaching, performance data available |

---

## Input

| Source | What |
|---|---|
| `edge:org-org` → ppa.consideration_contingent | Current fair value |
| `edge:org-org` → ppa.consideration_contingent_type | liability / equity |
| Acquisition agreement | Earn-out terms, milestones, cap, floor |
| Acquired entity financials | Actual performance vs targets |
| External valuers (if complex) | Option pricing models for complex earn-outs |

---

## Sub-Ergons

### Step 1: Assess whether remeasurement needed [MACH]

```
IF consideration_contingent_type = "equity":
  → NO remeasurement. Exit.
  → (Settlement within equity when earn-out is settled)

IF consideration_contingent_type = "liability":
  → Remeasure at fair value. Proceed to step 2.

IF contingent consideration fully settled:
  → Remove from ppa. Record final settlement amount. Exit.
```

### Step 2: Estimate current fair value [IND + external if complex]

```
Simple earn-out (binary: target met or not):
  Probability × amount = fair value
  Example: 70% chance of hitting EUR 50M revenue → 0.7 × EUR 10M = EUR 7M

Complex earn-out (tiered, capped, collared):
  May require Monte Carlo simulation or option pricing model
  External valuation specialist recommended

Inputs to valuation:
  - Updated performance forecasts for the acquired entity
  - Updated probability of hitting milestones
  - Time value of money (discount rate)
  - Any new information about conditions

Record: new fair value estimate + methodology + key assumptions
```

### Step 3: Book the remeasurement [MACH]

```
Change in fair value:
  Dr/Cr: Contingent consideration liability (balance sheet)
  Cr/Dr: Fair value change — contingent consideration (P&L)

Example:
  Acquisition date: EUR 7M fair value (liability)
  Q4: Revenue strong, probability up to 90%
  New fair value: EUR 9M
  Journal: Dr P&L EUR 2M, Cr Liability EUR 2M (P&L charge)

  Q2 next year: Revenue misses, probability drops to 30%
  New fair value: EUR 3M
  Journal: Dr Liability EUR 6M, Cr P&L EUR 6M (P&L benefit)

These P&L swings can be MATERIAL and volatile.
Investors and analysts watch this — non-recurring but real.

Write to graph:
  edge:org-org → ppa.consideration_contingent = new fair value (x-history)
```

### Step 4: Settlement [IND + MACH]

```
When earn-out period ends:

IF target met:
  Pay the earn-out
  Dr: Contingent consideration liability
  Cr: Cash

IF target not met:
  Release the liability
  Dr: Contingent consideration liability
  Cr: P&L (gain)

IF partially met (tiered):
  Pay partial amount
  Release remainder

After settlement:
  edge:org-org → ppa.consideration_contingent = 0
  Record: final settlement amount vs original estimate
```

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Not remeasuring liability-classified earn-outs | Misstated liabilities + misstated P&L |
| Remeasuring equity-classified earn-outs | P&L volatility that shouldn't be there |
| Optimistic/pessimistic probability estimates | P&L manipulation — auditor focus |
| Complex earn-outs without proper valuation | Material misstatement, ESMA finding |
| Not disclosing earn-out terms and sensitivity | IFRS 3.B64(g) disclosure failure |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial |
