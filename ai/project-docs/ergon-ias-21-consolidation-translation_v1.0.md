# Ergon: IAS 21 — Consolidation Translation

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 21.39-43, IAS 29 (hyperinflation)
**Intent**: Translate each foreign subsidiary's financial statements from functional currency to group presentation currency for consolidation. Manage the FCTR Ghost.
**Chain**: ergon-ias-21-chain_v1.0.md (step 4)
**Depends on**: Functional currency determined (step 1), rate policy in place (step 0), entity-level close complete (Done1)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting period, after foreign subsidiaries have closed their books (Done1) |

---

## Input

| Source | What |
|---|---|
| Foreign subsidiary trial balance | Entity-level financials in functional currency (Done1 output) |
| `node:org` → functional_currency | What currency to translate FROM |
| Group presentation currency | What currency to translate TO (typically SEK) |
| Rate table (from rate policy) | Closing rate + daily/average rates from home central bank |
| Prior period FCTR | Opening balance of Foreign Currency Translation Reserve |

---

## Sub-Ergons

### Step 1: Determine translation rates [MACH]

```
From the rate policy (ergon-ias-21-fx-rate-policy):

  Closing rate = reference rate on last business day of the period
    Source: parent's home central bank (e.g., Riksbanken for SEK group)

  Average rate = average of daily reference rates for the period
    OR: if subsidiary posted each transaction at daily rate,
    the sum in presentation currency already approximates the average.

  Historical rate = rate on specific past dates (for equity items)

For a SEK group translating EUR subsidiary:
  Closing: Riksbanken EUR/SEK on Dec 31 (or last business day)
  Average: average of Riksbanken EUR/SEK for Jan-Dec (or quarter)
```

### Step 2: Translate the balance sheet [MACH]

```
IAS 21.39(a): ALL assets and liabilities at CLOSING rate.

  Every BS line item × closing rate = SEK amount

  This includes:
    - Current assets (cash, receivables, inventory)
    - Non-current assets (PP&E, intangibles, goodwill)
    - Current liabilities (payables, accruals, short-term debt)
    - Non-current liabilities (long-term debt, provisions, pensions)

  GOODWILL and PPA FAIR VALUE ADJUSTMENTS from IFRS 3:
    IAS 21.47: Treated as assets/liabilities of the FOREIGN OPERATION
    → Translated at CLOSING rate (not historical rate of acquisition)
    → FX movement on goodwill affects FCTR → equity → KBR

  This is a Ghost trap: goodwill doesn't generate cash in any currency,
  but its SEK value changes with the EUR/SEK rate → equity moves → KBR.
```

### Step 3: Translate the P&L [MACH]

```
IAS 21.39(b): Income and expenses at rates at the DATES OF THE TRANSACTIONS.

  Practical expedient (IAS 21.40): average rate for the period
  UNLESS rates fluctuate significantly → must use transaction-date rates.

  Two approaches in BC:

  Approach A — Average rate:
    Each P&L line item × average rate for the period = SEK amount
    Simpler. One rate per period per currency. Common practice.

  Approach B — Daily rates via ACY:
    Each transaction already has a parallel SEK record (Additional Reporting Currency)
    posted at the daily reference rate. The SUM of these IS the translated P&L.
    No separate average-rate calculation needed.
    More precise. More data. BC handles automatically if ACY configured.

  Both are acceptable under IAS 21. Approach B is preferred if ACY is set up.
```

### Step 4: Calculate FCTR [MACH]

```
IAS 21.39(c): The FCTR is the translation difference.

  It arises because:
    BS is translated at CLOSING rate (one rate)
    P&L is translated at AVERAGE rate (different rate)
    Equity at HISTORICAL rates (yet another rate)

  FCTR = balancing figure in equity that makes the translated BS balance.

  Calculation:
    Opening net assets at opening rate
    + P&L at average rate
    + Other equity movements at transaction-date rates
    = Expected closing net assets
    vs
    Actual closing net assets at closing rate
    → Difference = FCTR movement for the period

  Record in OCI (Other Comprehensive Income).
  ACCUMULATES over time — can become very large for long-held foreign subs.

  The FCTR is a GHOST:
    - Doesn't affect cash (no currency was actually converted)
    - DOES affect equity → directly impacts KBR headroom
    - On disposal of foreign sub: ENTIRE accumulated FCTR recycled to P&L
      This can be a massive P&L hit (positive or negative)
```

### Step 5: Handle special cases [IND + MACH]

```
a) GOODWILL translation:
   IAS 21.47: Goodwill from acquiring a foreign operation → asset of foreign operation
   → Closing rate each period
   → FX change on goodwill → FCTR (not P&L)
   → If EUR weakens vs SEK → goodwill in SEK drops → equity drops → KBR tighter

b) INTRAGROUP MONETARY ITEMS (IAS 21.32):
   Long-term loans between group entities where settlement is neither planned nor likely:
   → In substance, part of the net investment in the foreign operation
   → FX differences on these loans → OCI (FCTR), NOT P&L
   → Must assess: is this truly "part of net investment" or a normal receivable?

c) HYPERINFLATIONARY ECONOMY (IAS 29):
   If subsidiary's functional currency is hyperinflationary:
   → FIRST: restate subsidiary's financials under IAS 29 (price-level adjustment)
   → THEN: translate ALL items (BS + P&L) at CLOSING rate (exception to normal rules)
   → No average rate for P&L — everything at closing rate
   → Comparatives: prior period at prior closing rate (not restated unless same hyperinfl.)

   Hyperinflation indicator: cumulative inflation ≈100% over 3 years
   Recent examples: Turkey (TRY), Argentina (ARS)
   Monitor via: ergon-ias-21-fx-monitors

d) STEP ACQUISITION of foreign operation:
   Previously held equity interest → remeasured at acquisition-date fair value (IFRS 3)
   Accumulated FCTR on the previously held interest → recycled to P&L at acquisition date

e) PARTIAL DISPOSAL:
   IAS 21.48A: proportionate share of FCTR reclassified to P&L
   Based on the ownership percentage disposed
```

### Step 6: Record and reconcile [MACH]

```
Write to consolidation:
  Translated BS at closing rate
  Translated P&L at average rate (or ACY daily accumulation)
  FCTR movement for the period → OCI
  Prior period FCTR brought forward
  Closing FCTR balance

Reconcile:
  Opening FCTR + movement = closing FCTR
  Closing translated net assets = (opening + P&L + other movements) at closing rate

  IF reconciliation doesn't balance → investigate:
    - Rate error in table?
    - Transaction posted at wrong rate?
    - Intragroup monetary item not treated correctly?
    - Goodwill translation not at closing rate?
```

---

## Data Model Properties

### On node:org (foreign subsidiary)

Already defined in node-org-governance_v1.0.md:
- `functional_currency`: the entity's functional currency
- `reporting_date`: alignment with parent (IAS 21 + IFRS 10)

Additional for translation tracking:

| Field | Type | x-history | Purpose |
|---|---|---|---|
| `fctr_balance` | decimal | yes | Accumulated FCTR for this entity. Ghost that affects equity → KBR. |
| `fctr_movement_period` | decimal | yes | FCTR movement this period (for OCI disclosure). |
| `goodwill_translated` | decimal | yes | Goodwill in presentation currency (at closing rate). Compare to prior period. |

### On edge:org-org → owns

| Field | Type | x-history | Purpose |
|---|---|---|---|
| `net_investment_loans` | array of { amount, currency, bc.path } | yes | Intragroup monetary items treated as net investment (IAS 21.32). FX diff → FCTR not P&L. |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Are all foreign subs translated at correct rates? FCTR reconciliation balances? Goodwill at closing rate? Intragroup loans correctly classified? | Translation errors = misstated consolidated FS |
| **Reserve** | FCTR balance and sensitivity: how much does a 10% FX move change equity? Goodwill FX sensitivity. KBR impact. | FCTR is a Ghost that eats KBR headroom. Must size Reserve for FX exposure. |
| **Sword** | Currency exposure by subsidiary. Natural hedging (revenue and cost in same currency?). Which markets' FX risk is worth taking? | Strategic currency decisions. Where to expand considering FX risk. |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong translation rates | Misstated consolidated BS and P&L. ESMA common finding. |
| Goodwill not at closing rate | Goodwill translated at historical rate = understated/overstated in presentation currency. Affects impairment test. |
| FCTR not recycled on disposal | Missing P&L gain/loss on sale of foreign sub. Can be massive. |
| Intragroup loan FX in P&L instead of OCI | P&L volatility that should be in OCI. Or vice versa. |
| Hyperinflation not detected | Wrong translation method (average instead of all-closing). IAS 29 not applied. Turkey/Argentina trap. |
| FCTR erodes equity without anyone noticing | Ghost dimension: no cash impact but equity drops → KBR headroom shrinks → personal liability approaches silently |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — translation mechanics, FCTR Ghost, goodwill at closing, hyperinflation, intragroup net investment, S-R-S view |
