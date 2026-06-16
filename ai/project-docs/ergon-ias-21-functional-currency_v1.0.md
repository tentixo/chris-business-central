# Ergon: IAS 21 — Functional Currency Determination

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 21.9-14
**Intent**: Determine the functional currency for each entity in the group. Factual determination, not a policy choice. Get this wrong → entire translation method wrong → material misstatement.
**Chain**: ergon-ias-21-chain_v1.0.md (step 1)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | New entity enters the group (acquisition, incorporation) |
| **Event** | Entity's economic environment changes materially (new market, currency regime change, operations relocated) |
| **Periodic** | Annual confirmation that functional currency is still correct |

---

## Core Rule

IAS 21.9: Functional currency = the currency of the **primary economic environment** in which the entity operates. This is normally the currency in which the entity primarily generates and expends cash.

**This is a FACTUAL determination.** Management does not choose. They discover.

---

## Sub-Ergons

### Step 1: Apply primary indicators [IND — judgment]

```
IAS 21.9-10: Primary indicators (most weight):

a) Currency that mainly influences SALES PRICES
   → In which currency are goods/services priced and settled?
   → If a Swedish company prices everything in EUR for German market → EUR may be functional

b) Currency of the country whose competitive forces and regulations
   mainly determine sales prices
   → Where does the entity compete? Local market (SEK) or international (EUR/USD)?

c) Currency that mainly influences LABOUR, MATERIAL, and other costs
   → What currency are salaries paid in? Suppliers invoiced in?
   → If costs are 80% in SEK → SEK pulls strongly toward functional

Document per entity:
  revenue_currency_mix:  { SEK: 20%, EUR: 70%, USD: 10% }
  cost_currency_mix:     { SEK: 80%, EUR: 15%, USD: 5% }
  competitive_market:    "DACH region, prices set in EUR"
```

### Step 2: Apply secondary indicators (if primary is ambiguous) [IND]

```
IAS 21.11: Secondary indicators (additional evidence):

a) Currency of FINANCING activities
   → Debt raised in EUR? Equity in SEK? Intercompany loans in USD?

b) Currency in which OPERATING receipts are usually retained
   → Does the entity keep cash in EUR accounts or convert to SEK?

Document:
  financing_currency:    { loans: EUR, equity: SEK }
  cash_retention:        "Primarily EUR bank accounts"
```

### Step 3: Determine and record [IND + MACH]

```
Weigh all indicators. Primary indicators dominate.

Common patterns:

  Swedish operating company, Swedish customers, Swedish costs:
    → SEK. Clear.

  Swedish holding company with German subsidiary:
    → Holding: SEK (costs in SEK, financing in SEK)
    → Subsidiary: EUR (revenue in EUR, costs in EUR, operates in Germany)

  Swedish company, international sales, Swedish production:
    → Revenue: 60% EUR, 40% USD — international
    → Costs: 90% SEK — domestic
    → Competitive market: international
    → TENSION: costs say SEK, revenue says EUR/USD
    → Usually: SEK (costs are the primary economic environment — where you OPERATE)
    → But: judgment call. Document reasoning.

  Sales office in Denmark, part of Swedish group:
    → Revenue: DKK (Danish customers)
    → Costs: DKK (Danish staff, Danish office)
    → Functional: DKK (primary economic environment is Denmark)

Record:
  node:org → functional_currency = "{currency code}" (x-history tracked)
  node:org → functional_currency_rationale = "{documented reasoning}"
  node:org → functional_currency_assessed_date = "{date}"
```

### Step 4: Identify translation need [MACH]

```
Compare: entity.functional_currency vs group.presentation_currency

IF different → entity is a FOREIGN OPERATION → translation required (Step 4 of chain)
IF same → no translation needed (entity already in group currency)

For each foreign operation:
  Set up: BC Business Unit with correct consolidation currency
  Set up: reference rate feed for this currency pair
  node:org → fx_reference_source = "{central bank}" (from rate policy)
```

---

## Reassessment

```
IAS 21.13: Functional currency is reassessed only when there is a change
in the underlying transactions, events, and conditions.

NOT reassessed just because exchange rates move.
NOT reassessed annually as a matter of routine (but confirmed).

Triggers for genuine reassessment:
  - Entity relocates operations to different country
  - Revenue mix shifts materially (was 80% SEK, now 80% EUR)
  - Cost base shifts (moved manufacturing abroad)
  - New major customer in different currency
  - Currency regime change (country joins/leaves eurozone)
  - Hyperinflation in functional currency country (IAS 29 trigger)

IF functional currency changes:
  → Translate all items to new functional currency at rate on date of change
  → Prospective — no restatement of prior periods
  → IAS 21.35
  → This is rare and material — document thoroughly
```

---

## node:org Properties

| Field | Type | x-history | Set by this ergon |
|---|---|---|---|
| `functional_currency` | currency code | yes | Primary output |
| `functional_currency_rationale` | string | no | Documented reasoning |
| `functional_currency_assessed_date` | date | yes | When last assessed |
| `fx_reference_source` | string | no | Home central bank (from rate policy) |
| `presentation_currency` | currency code | no | Group presentation currency (set at group level) |
| `is_foreign_operation` | boolean | derived | functional_currency ≠ presentation_currency |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong functional currency | Entire translation method wrong. All FX gains/losses wrong. Material misstatement. ESMA finding. |
| Not reassessing when economic environment changes | Stale functional currency → wrong translation → accumulating error |
| Holding company assumed SEK when it should be EUR | Common error for holding companies that manage EUR subsidiaries and have EUR financing |
| No documented rationale | Auditor cannot verify the determination. Qualification risk. |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — primary + secondary indicators, reassessment triggers, node:org properties |
