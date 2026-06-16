# Ergon: IFRS 3 — Business vs Asset Acquisition Test

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 3.3, B7-B12
**Intent**: Determine whether the acquired entity is a BUSINESS (IFRS 3 applies — goodwill possible) or an ASSET ACQUISITION (no goodwill — cost allocated by relative fair value)
**Chain**: ergon-ifrs-3-chain_v1.0.md (step 1)

---

## Why This Matters

The classification is load-bearing:

| | Business Combination (IFRS 3) | Asset Acquisition |
|---|---|---|
| Goodwill | Yes — residual recognized | No — cost allocated to assets by relative FV |
| Intangible identification | Required separately from goodwill | Allocated as part of cost |
| Acquisition costs | EXPENSED | CAPITALIZED into asset cost |
| Contingent consideration | Fair value → remeasured through P&L | Part of cost → adjusts asset carrying amount |
| Deferred tax | Yes (on FV uplifts) | Yes (on FV uplifts) but no goodwill DT issue |
| Transaction costs impact | P&L hit immediately | No P&L hit (capitalized) |

Getting this wrong: either overstates assets (calling an asset acquisition a business → creating goodwill that doesn't exist) or understates P&L (calling a business acquisition an asset → capitalizing costs that should be expensed).

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | IFRS 10 control gained — new acquisition detected |

---

## Input

| Source | What |
|---|---|
| `edge:org-org` → owns | The new acquisition (acquisition_date, consideration_paid) |
| `node:org` (acquired entity) | Entity properties — what does it contain? |
| Deal documentation | Share purchase agreement, due diligence reports |

---

## Sub-Ergons

### Step 1: Apply the Optional Concentration Test [IND — shortcut]

```
IFRS 3.B7A-B7B (added 2018):

IF substantially all of the fair value of the gross assets acquired
   is concentrated in a single identifiable asset or group of similar assets:
   → ASSET ACQUISITION (not a business)
   → Skip further analysis

Example: Buying a company that owns one building and nothing else.
         Fair value of building = 95% of total assets → asset acquisition.

Example: Buying a company with customers, employees, technology, IP.
         No single asset dominates → cannot use shortcut → proceed to step 2.

This is an OPTIONAL screen. If passed → asset acquisition. If not → must do full test.
```

### Step 2: Full Business Test [IND — judgment]

```
IFRS 3.B7-B12:

A business has three elements:
  1. INPUTS: Economic resources (employees, IP, access to materials/customers)
  2. PROCESSES: Applied to inputs to create outputs (organized workforce,
     operational processes, management processes, technology)
  3. OUTPUTS: Results of inputs + processes (revenue, dividends, lower costs)

The acquired set is a BUSINESS if it includes, at minimum:
  - An input AND
  - A substantive process that together significantly contribute to
    the ability to create outputs

Key indicator: Does the acquired set have an ORGANIZED WORKFORCE
that can apply a substantive process?

  YES → likely a BUSINESS (IFRS 3 applies)
  NO → likely an ASSET ACQUISITION (no goodwill)

Record:
  node:org → type_data.acquisition_history.business_or_asset
  = "business_combination" or "asset_acquisition"
  + rationale documented
```

---

## Output

| Target | What |
|---|---|
| `node:org` → acquisition_history.business_or_asset | Classification: business_combination / asset_acquisition |
| Next ergon | IF business → ergon-ifrs-3-business-combination. IF asset → simple cost allocation (no separate ergon chain needed). |

---

## Rim Consequence

- Misclassification as business when it's assets → goodwill created that shouldn't exist → future impairment needed → misstated P&L
- Misclassification as assets when it's business → acquisition costs capitalized instead of expensed → overstated assets
- ESMA finding: failure to correctly apply the concentration test
- Auditor focus: always challenge this classification, especially for holding company acquisitions and property acquisitions

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial |
