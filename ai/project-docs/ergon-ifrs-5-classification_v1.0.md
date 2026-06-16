# Ergon: IFRS 5 — Held-for-Sale Classification and Initial Measurement

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 5.6-8, 15-18, 30-36
**Intent**: Assess whether a subsidiary/disposal group meets held-for-sale criteria. If yes: stop depreciation, remeasure, change presentation.
**Chain**: ergon-ifrs-5-chain_v1.0.md (steps 1-3)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | Board/management decides to sell a subsidiary or major business line |
| **Event** | Disposal plan formalized (SPA process initiated, advisor appointed) |

---

## Input

| Source | What |
|---|---|
| Board minutes / management decision | Formal decision to dispose |
| `node:org` (entity to be sold) | Current carrying amounts, depreciation status |
| `edge:org-org` → owns | Ownership data, carrying amount of investment |
| External valuers (if needed) | FVLCD estimate |
| BC | Fixed asset register, trial balance of subsidiary |

---

## Sub-Ergons

### Step 1: Assess Held-for-Sale Criteria [IND — judgment]

```
IFRS 5.7-8 — ALL of the following must be met:

  [ ] Management committed to a plan to sell
      Evidence: board resolution, minutes, formal decision

  [ ] Available for immediate sale in present condition
      Not: "after we finish the restructuring" or "after we fix the IT system"
      Must be sellable NOW, subject only to terms customary for such sales

  [ ] Active programme to locate a buyer initiated
      Evidence: advisor appointed, marketing materials, buyer list

  [ ] Sale HIGHLY PROBABLE (stricter than "more likely than not")
      Evidence: serious buyer interest, active negotiations,
               realistic price relative to fair value

  [ ] Expected to complete within 12 MONTHS
      IFRS 5.8: "expected to qualify for recognition as a completed sale
      within one year from the date of classification"

  [ ] Marketed at a price reasonable in relation to fair value
      Not: fire-sale pricing OR unreasonably high asking price
      (Both suggest the sale isn't genuine)

  [ ] Unlikely that significant changes to the plan will be made
      or that the plan will be withdrawn

IF ALL criteria met:
  → Classify as held for sale
  → Record: node:org → held_for_sale.classified = true
  → Record: node:org → held_for_sale.classification_date = today
  → Record: node:org → held_for_sale.expected_sale_date
  → Record: node:org → held_for_sale.highly_probable_evidence
  → Record: edge:org-org → disposal.planned = true, disposal.status = "marketed"
  → Proceed to Step 2

IF NOT all criteria met:
  → Do NOT classify
  → Document: which criteria not met
  → Monitor for when criteria ARE met
```

### Step 2: Initial Measurement [MACH + IND]

```
IFRS 5.15:

At classification date, measure at LOWER of:
  a) Carrying amount (what's on the books now)
  b) Fair value less costs to sell (FVLCD)

Carrying amount = subsidiary's net assets as consolidated
  (including allocated goodwill from IFRS 3 PPA)

FVLCD = fair value (per IFRS 13) minus:
  - Incremental costs directly attributable to the sale
  - Legal fees, broker fees, transfer taxes
  - NOT: costs to restructure or "fix up" the business

IF FVLCD < carrying amount:
  → Recognize impairment loss
  → Allocate: first to goodwill, then pro rata to other assets (IAS 36 order)
  → Record: node:org → held_for_sale.impairment_on_classification

IF FVLCD ≥ carrying amount:
  → No impairment at classification
  → Carrying amount unchanged

CRITICAL: STOP DEPRECIATION from classification date.
  → All depreciable assets in the disposal group: depreciation ceases
  → This applies even if FVLCD > carrying amount
  → Interest on liabilities continues to be recognized

Record:
  node:org → held_for_sale.carrying_amount_at_classification
  node:org → held_for_sale.fair_value_less_costs_to_sell
  node:org → held_for_sale.impairment_on_classification (if any)
```

### Step 3: Presentation [MACH + IND]

```
BALANCE SHEET (IFRS 5.38):
  Assets of disposal group → single line: "Non-current assets held for sale"
  Liabilities of disposal group → single line: "Liabilities associated with
    assets held for sale"
  Presented in CURRENT section (sale expected within 12 months)
  NOT offset (gross presentation)

INCOME STATEMENT — depends on "discontinued operation" test:

  IS it a DISCONTINUED OPERATION? (IFRS 5.32)
  A discontinued operation is a component that:
    (a) represents a SEPARATE MAJOR LINE of business or geographical area, OR
    (b) is part of a single COORDINATED PLAN to dispose of a separate major
        line or geographical area, OR
    (c) is a subsidiary acquired EXCLUSIVELY with a view to resale

  IF YES → DISCONTINUED OPERATION:
    → Single line on face of P&L:
      "Profit/loss from discontinued operations (net of tax)"
    → In notes or on face: breakdown of revenue, expenses, pre-tax P&L,
      tax, gain/loss on disposal, net cash flows (operating/investing/financing)
    → RESTATE comparatives (prior period also shows the split)

  IF NO (held for sale but NOT discontinued):
    → No P&L reclassification
    → Results remain in normal line items
    → Balance sheet reclassification only
    → Disclose in notes

Record:
  node:org → held_for_sale.discontinued_operation = true/false
```

---

## Output

| Target | What |
|---|---|
| `node:org` → held_for_sale section | All classification and measurement data |
| `edge:org-org` → disposal section | Disposal plan, status, expected proceeds |
| BC consolidation | Presentation changes (reclassify BS lines, P&L single line for discontinued) |
| `node:anomaly` | If criteria borderline — "Held-for-sale classification uncertain for {org}" |
| `node:decision` | "Is this a discontinued operation?" (may require judgment) |

---

## Rim Consequence

| Risk | Consequence | Failure pattern |
|---|---|---|
| Premature classification | Depreciation stops too early → assets overstated | #3 Optimistic estimates |
| Late classification | Depreciation continues when it shouldn't → inconsistency | #3 Optimistic estimates |
| Not presenting discontinued ops separately | P&L misleads — continuing business looks different than it is | ESMA finding |
| FVLCD not updated | Carrying amount overstated → impairment missed | #3 Optimistic estimates |
| Classification used to "park" a subsidiary | Management classifies to stop depreciation with no real intent to sell | #1 Scope manipulation (using IFRS 5 to change numbers without substance) |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial |
