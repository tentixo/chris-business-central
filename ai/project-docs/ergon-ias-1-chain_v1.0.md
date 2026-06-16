# Ergon Chain: IAS 1 — Presentation of Financial Statements

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 1 (complete standard). Being replaced by **IFRS 18** (effective 2027, early adoption from 2025).
**Intent**: The OUTPUT FORMAT specification. After Done2 delivers correct numbers, IAS 1 defines HOW they are presented. Going concern assessment. Current/non-current classification. Complete set of financial statements. Materiality.
**Master chain**: ergon-ifrs-master-chain_v1.0.md — IAS 1 is the PRESENTATION LAYER, not a calculation phase.

---

## What IAS 1 Defines

IAS 1 is the CONTAINER for all the numbers every other ergon chain produces. It doesn't calculate — it STRUCTURES.

```
Done2 produces: a correct consolidated trial balance (GL account balances).

IAS 1 says: present those balances as:
  1. Statement of financial position (balance sheet)
  2. Statement of profit or loss and OCI
  3. Statement of changes in equity
  4. Statement of cash flows (IAS 7)
  5. Notes (accounting policies + explanatory information)
  6. Comparative information (at least one prior period)

+ Going concern assessment
+ Current vs non-current classification
+ Fair presentation + IFRS compliance statement
+ Materiality-based presentation decisions
```

---

## Going Concern (IAS 1.25-26) — THE Board Responsibility

```
IAS 1.25: When preparing financial statements, management shall assess
the entity's ABILITY TO CONTINUE AS A GOING CONCERN.

  Period: at least 12 months from the reporting date (but consider beyond).
  "Going concern" = entity will continue in operation for the foreseeable future.
  The DEFAULT assumption unless management intends to liquidate or has no realistic alternative.

  Assessment must consider:
    - Cash flow forecasts (rolling forecast, not budget — Bogsnes)
    - Borrowing facilities (committed vs uncommitted)
    - Debt maturities (can we refinance?)
    - Covenant compliance (will we breach? → accelerated repayment?)
    - Profitability trends
    - Contingencies (IAS 37 — could a provision crystallize and drain cash?)
    - KBR status (equity vs share capital — ABL 25:13)

  OUTCOMES:

  a) No material uncertainty → going concern assumed. No special disclosure.
     (But auditor ISA 570 may still comment.)

  b) MATERIAL UNCERTAINTY exists but entity IS going concern:
     → Disclose: the uncertainty, the events/conditions, management's plans.
     → Auditor: "Material Uncertainty Related to Going Concern" paragraph.
     → Share price impact: market sees uncertainty disclosed.

  c) Entity is NOT a going concern:
     → Financial statements NOT on going concern basis.
     → Measure assets at liquidation values. Recognize ALL obligations.
     → This is rare for listed companies (usually triggers before reaching this point).

  Connection to our model:
    Reserve Shaw Lens: 13-week cash forecast + covenant headroom + KBR status
    = the DATA for the going concern assessment.
    FGGE doesn't make the going concern JUDGMENT (that's the board).
    FGGE provides the INFORMATION the board needs to make it.
```

---

## Current vs Non-Current Classification (IAS 1.66-76)

```
ASSETS:
  Current if:
    a) Expected to be realized within normal operating cycle, OR
    b) Held primarily for trading, OR
    c) Expected to be realized within 12 months, OR
    d) Cash or cash equivalent (not restricted)

  Otherwise → non-current.

LIABILITIES:
  Current if:
    a) Expected to be settled within normal operating cycle, OR
    b) Held primarily for trading, OR
    c) Due within 12 months, OR
    d) Entity does not have unconditional right to defer settlement ≥12 months

  Otherwise → non-current.

2024 AMENDMENTS (effective 1 Jan 2024):
  IAS 1.72A-76A: Classification of Liabilities with COVENANTS.

  Old rule: classify based on rights at the reporting date.
  New rule: if a liability's classification as non-current depends on
  covenant compliance → entity must COMPLY at or before the reporting date.

  If covenant breached at reporting date → classify as CURRENT
  (even if lender granted waiver AFTER the reporting date).

  If covenant compliance required within 12 months → disclose:
    - The carrying amount of the liability
    - The covenants and their thresholds
    - Circumstances that could cause breach

  Connection to our model:
    Reserve monitors: covenant headroom → classification impact.
    If headroom < threshold → liability reclassifies current → current ratio deteriorates
    → cascading: other covenants may trigger on current ratio → cross-default.
    THIS IS A RIM TRAP: covenant breach → reclassify → ratio worsens → more breaches.
```

---

## Complete Set of Financial Statements (IAS 1.10)

```
a) STATEMENT OF FINANCIAL POSITION (Balance Sheet)
   Minimum line items (IAS 1.54):
     PP&E, investment property, intangible assets, financial assets,
     equity-accounted investments, biological assets, inventories,
     trade receivables, cash, assets held for sale (IFRS 5),
     trade payables, provisions, financial liabilities, tax liabilities,
     NCI (in equity), issued capital + reserves.

   Presented: current/non-current distinction (IAS 1.60).
   Comparative: most recent annual year-end.

b) STATEMENT OF PROFIT OR LOSS AND OCI
   P&L minimum lines (IAS 1.82):
     Revenue, finance costs, share of profit of associates/JVs,
     tax expense, single amount for discontinued operations (IFRS 5),
     profit or loss.

   OCI items in TWO groups (IAS 1.82A):
     Items that WILL be reclassified to P&L (FCTR, cash flow hedges, FVOCI debt)
     Items that will NOT be reclassified (pension remeasurements, FVOCI equity, revaluation surplus)

   Classification: by NATURE or by FUNCTION (IAS 1.99-105).
     Nature: materials, employee costs, depreciation, other → what TYPE of cost.
     Function: cost of sales, selling expenses, admin → what PURPOSE.
     Most listed companies: function (shows gross margin).
     If function → must disclose nature in notes (IAS 1.104).

   IFRS 18 CHANGE (effective 2027):
     New mandatory subtotals: operating profit, operating profit + investing,
     profit before financing and tax.
     Management-defined performance measures: must reconcile to IFRS amounts.

c) STATEMENT OF CHANGES IN EQUITY
   For each component of equity:
     Opening balance → total comprehensive income → transactions with owners
     (dividends, share issues) → closing balance.
   NCI shown separately.

d) STATEMENT OF CASH FLOWS → IAS 7 (separate standard)

e) NOTES
   Significant accounting policies (only MATERIAL policies — 2023 amendment).
   Sources of estimation uncertainty (IAS 1.125-133):
     Key assumptions about the future with significant risk of material adjustment.
     Examples: goodwill impairment assumptions (IAS 36), pension discount rate (IAS 19),
     ECL forward-looking inputs (IFRS 9), provision estimates (IAS 37).
   ALL disclosures required by other IFRS standards.
```

---

## Materiality (IAS 1.29-31)

```
IAS 1.7: Information is material if omitting or misstating it could
influence the economic decisions of users.

Entity-specific. Not a fixed % threshold.

PRACTICAL: most groups set materiality as % of a benchmark:
  - 0.5-2% of revenue (for P&L items)
  - 1-5% of total assets (for BS items)
  - Lower for sensitive items (RPT, director compensation, fraud)

IAS 1.29: Don't aggregate material items with different nature/function.
IAS 1.30: Immaterial items CAN be aggregated with similar items.
IAS 1.31: Immaterial in statements → may still need note disclosure.

2023 AMENDMENT (Disclosure of Accounting Policies):
  Disclose MATERIAL accounting policies (not just "significant").
  Don't disclose boilerplate policies that just repeat IFRS text.
  Only disclose when: entity made a choice, or policy is entity-specific,
  or policy is relevant to understanding the financial statements.

Connection to our model:
  Shield: are material items separately presented?
  Materiality threshold documented and applied consistently?
  Immaterial items not buried inside material line items?
```

---

## Comparative Information (IAS 1.38-44)

```
IAS 1.38: Present comparative information for the PRECEDING PERIOD
for ALL amounts in the financial statements.

Minimum: one year of comparatives.
Some entities present: two years (US practice, voluntary under IFRS).

WHEN COMPARATIVES MUST BE RESTATED:
  - IAS 8: change in policy or error correction → restate.
  - IFRS 8.29: segment reorganization → restate.
  - IAS 1.40A: if reclassification of items in current period → reclassify prior period.

THIRD BALANCE SHEET (IAS 1.40A):
  If retrospective restatement or reclassification → present THREE balance sheets:
    - Current period end
    - Prior period end (restated)
    - Beginning of the prior period (the "opening" restated BS)
  This is the famous "third balance sheet" rule. Triggers when IAS 8 restatement occurs.
```

---

## IFRS 18 — What's Coming (effective 2027)

```
IFRS 18 REPLACES IAS 1. Major changes:

1. NEW INCOME STATEMENT SUBTOTALS (mandatory):
   Revenue
   − Cost of sales
   = Gross profit (if function classification)
   ...
   = OPERATING PROFIT ← new mandatory subtotal
   + Income/expenses from investments
   = OPERATING PROFIT AND INVESTING ← new mandatory subtotal
   − Financing costs
   = PROFIT BEFORE TAX

   Categories: OPERATING / INVESTING / FINANCING
   (similar to cash flow statement categories applied to P&L)

2. MANAGEMENT-DEFINED PERFORMANCE MEASURES (non-GAAP):
   If entity reports adjusted EBITDA, adjusted operating profit, or ANY
   non-GAAP measure in public communications:
   → Must disclose in the notes with RECONCILIATION to nearest IFRS subtotal.
   → Subject to audit.
   → Prevents: companies touting "adjusted earnings" that exclude inconvenient items
     without showing the bridge to IFRS.

3. DISAGGREGATION:
   More granular breakdown of expenses in notes.
   If P&L by function → must provide nature disaggregation in notes (enhanced from IAS 1.104).

FGGE implication:
  BC chart of accounts must support the new categorization (operating/investing/financing for P&L).
  Power BI Shaw Lenses must accommodate new subtotals.
  Management-defined measures must be reconciled → FGGE scripts can automate reconciliation.

Timeline:
  Effective: 1 Jan 2027 (financial years beginning on or after)
  Early adoption: permitted from 2025
  Comparatives: must restate prior period under IFRS 18 format.
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Going concern assessed? Current/non-current correctly classified? Covenant amendments (2024) applied? Materiality thresholds set? Comparatives consistent? Complete set of statements? IFRS compliance explicitly stated? | IAS 1 is the PRESENTATION Rim. Wrong classification = wrong ratios = wrong covenant assessment = cascade. |
| **Reserve** | Going concern data: 13-week cash forecast, covenant headroom, KBR status. Is the going concern assessment supported by data? Material uncertainty identified? | Going concern IS the Reserve question: "can we survive?" If the answer is uncertain → disclose. If no → not going concern. |
| **Sword** | P&L structure: where is gross margin? Which cost lines are growing? OCI: which Ghosts moved this period? IFRS 18 management-defined measures: what does the CODM track beyond IFRS? | P&L structure = the public face of what Sword is achieving. OCI shows the Ghosts. IFRS 18 exposes the CODM's actual steering metrics. |

---

## Node/Edge Properties

**No new properties.** IAS 1 is presentation — it reads from what's already there:

| What IAS 1 needs | Where it already lives |
|---|---|
| Going concern data | Reserve Shaw Lens: cash forecast, covenant headroom, KBR headroom |
| Current/non-current classification | BC: due dates on liabilities. Node:org: covenant data. |
| P&L by nature or function | BC: Gen. Prod. Posting Group (function) + BAS account ranges (nature) |
| OCI items | node:org: fctr, pension remeasurements, fvoci_reserve, cash_flow_hedge_reserve |
| Materiality threshold | Set per group (policy). Not a stored property — a governance parameter. |

One governance parameter to track:

| Field | Where | Why |
|---|---|---|
| `materiality_threshold` | Group-level governance setting (on parent node:org or as FGGE config) | Shield: is it set? Applied consistently? Appropriate for group size? |
| `going_concern_status` | node:org (parent) | enum: no_uncertainty / material_uncertainty_disclosed / not_going_concern. x-history tracked. |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Going concern not assessed | IAS 1.25 violation. Auditor MUST assess independently (ISA 570). If material uncertainty exists and not disclosed → auditor qualification or adverse opinion. |
| Material uncertainty not disclosed | Market not informed → surprise if entity fails. ABL + MAR: inside information? |
| Current/non-current classification wrong (covenant) | 2024 amendment: breach at reporting date → CURRENT. If misclassified as non-current → current ratio overstated → misleading. |
| Covenant reclassification cascade | Breach → reclassify current → ratio worsens → triggers other covenants → cross-default → going concern? |
| Comparatives not restated when required | IAS 8 restatement + IAS 1.40A: must present third BS. If missing → incomplete FS. |
| IFRS 18 not prepared for (2027) | Chart of accounts may not support new P&L categorization. Transition requires comparative restatement. Start planning NOW. |
| Management-defined measures not reconciled (IFRS 18) | Non-GAAP measures without reconciliation → regulatory enforcement. ESMA already watches this under IAS 1. |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — going concern, current/non-current (2024 covenant amendments), complete set of FS, materiality, comparatives, IFRS 18 preview (2027), S-R-S view. No new properties (presentation reads from existing data). |
