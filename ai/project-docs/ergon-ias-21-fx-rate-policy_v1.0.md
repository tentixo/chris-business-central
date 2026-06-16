# Ergon: IAS 21 — FX Rate Policy

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 21.8 (spot rate definition), IAS 21.21-22 (transaction recording)
**Intent**: Establish the group's FX rate policy — which reference source per entity, how rates flow into BC, how bank rates are handled
**Chain**: ergon-ias-21-chain_v1.0.md (step 0 — set once, maintain always)

---

## The Policy (Locked from W-H-S)

### Principle: Always reference rate. One source per entity.

Each entity uses its **home central bank** as reference source. The central bank is the most authoritative rate source for its own currency.

| Entity functional currency | Reference source | Published as |
|---|---|---|
| SEK | **Riksbanken** (Sveriges Riksbank) | SEK per unit of foreign currency, daily |
| EUR | **ECB** (European Central Bank) | EUR per unit of foreign currency, daily ~14:15 CET |
| NOK | **Norges Bank** | NOK per unit of foreign currency, daily |
| GBP | **Bank of England** | GBP per unit of foreign currency, daily |
| DKK | **Danmarks Nationalbank** | DKK per unit of foreign currency, daily |
| USD | **Federal Reserve** | Various, daily |

### How it works across layers

```
ENTITY LEVEL (each entity's own books):
  German sub (EUR functional):
    Uses ECB for all FX: USD→EUR, GBP→EUR, SEK→EUR, etc.

  Swedish parent (SEK functional):
    Uses Riksbanken for all FX: EUR→SEK, USD→SEK, GBP→SEK, etc.

CONSOLIDATION LEVEL (translating sub → group):
  Group presentation currency: SEK
  Translation EUR→SEK: uses RIKSBANKEN (parent's reference source)

  The subsidiary's internal FX (USD→EUR using ECB) is already resolved
  into EUR. Consolidation only sees EUR → translates to SEK at Riksbanken rate.
```

### Rate types needed per period

| Rate | When used | Source |
|---|---|---|
| **Daily reference rate** | Transaction booking (IAS 21.21) | Home central bank daily fixing |
| **Closing rate** | Month-end revaluation of monetary items (IAS 21.23). BS translation (IAS 21.39). | Home central bank rate on last business day of period |
| **Average rate** | P&L translation for consolidation (IAS 21.39 — practical expedient) | Average of daily reference rates for the period. OR: if each P&L transaction posted at daily rate, the sum approximates the average naturally. |
| **Bank rate** | Actual cash conversion events only | Bank's rate at conversion — difference from reference goes to FX P&L (BAS 8230). No per-transaction split required. |

### Bank rate handling

```
Booking:       ALWAYS at reference rate on transaction date
Month-end:     ALWAYS at closing reference rate (revaluation)
Cash convert:  Bank rate is what happens → total difference to FX P&L

  The difference includes:
    - FX rate movement (reference rate changed since booking)
    - Bank spread (bank rate vs reference at conversion date)

  NO SPLIT REQUIRED. Both are financial items. No VAT difference.
  Combined into BAS 8230 (Valutakursdifferenser) or equivalent.

  Bank fee analysis: done at AGGREGATE level from bank statements.
  Sword information (cost optimization), not Shield requirement.
```

### BC Implementation

```
BC Currency Exchange Rate table:
  - Populated from home central bank feed (daily)
  - ONE rate per currency pair per date (reference rate)
  - No separate buy/sell rates needed (mid-market reference)

  For SEK entity: Riksbanken feed → BC rate table
  For EUR entity: ECB feed → BC rate table

Additional Reporting Currency (ACY):
  - Uses same reference rate table
  - Parallel SEK record created for each EUR transaction
  - Month-end: BC "Adjust Exchange Rates" batch job revalues at closing rate
```

---

## Monitoring: Reference Rate Divergence

```
Monthly Walker check:

  Compare: Riksbanken EUR/SEK vs ECB EUR/SEK (inverted from ECB's SEK/EUR)

  Expected: within 0.01-0.02 SEK (negligible)

  IF divergence > 0.05 SEK on any day:
    → Anomaly: "Reference rate divergence Riksbanken vs ECB on {date}: {diff}"
    → Investigate: market stress? Fixing time difference? Data feed error?

  This validates that using different sources per entity doesn't create
  material inconsistency at consolidation.
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Are all entities using their designated reference source? Are rates populated for all trading days? Are revaluations at correct closing rate? | Rate errors → misstated FX gains/losses → misstated P&L |
| **Reserve** | FX sensitivity: how much does a 10% move in each currency affect the group? | Size Reserve per currency exposure. FCTR impact on equity → KBR headroom. |
| **Sword** | Currency exposure by market (ORG.buyer.jurisdiction). Natural hedging opportunities. | Which markets create FX risk? Does revenue currency match cost currency? |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong reference source or missing rates | Transactions booked at stale/incorrect rate → misstated revenue/cost |
| Bank rate used for bookkeeping (mixed with reference for revaluation) | Inconsistent FX base → bank spread contaminates revaluation → messy audit |
| Rate feed failure (no rate for a currency on a date) | Transactions can't be posted. Close delayed. |
| Divergence between Riksbanken and ECB not monitored | Consolidation translation may differ from entity-level FX → unexplained differences |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — home central bank per entity, always reference rate, bank rate only at cash conversion, no per-transaction split, divergence monitoring |
