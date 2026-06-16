# Ergon: IFRS 13 — Fair Value Measurement

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 13 (complete standard)
**Intent**: Measure fair value correctly wherever another standard requires it. Classify in hierarchy. Document inputs. Disclose sensitivity for Level 3.
**Nature**: SERVICE ergon — not a chain of its own. Invoked BY other chains (IFRS 3, IAS 36, IFRS 9, IAS 19, IFRS 5).

---

## When This Ergon Is Invoked

| Calling chain | What needs fair value | Typical hierarchy level |
|---|---|---|
| **IFRS 3** (PPA) | Identifiable assets, liabilities, NCI, contingent consideration | Level 2-3 (intangibles always Level 3) |
| **IAS 36** (Impairment) | FVLCD for CGU or individual asset | Level 2-3 |
| **IFRS 9** (Financial instruments) | FVTPL and FVOCI instruments | Level 1 (quoted) or Level 2-3 (complex) |
| **IAS 19** (Pensions) | Plan assets | Level 1 (quoted securities) to Level 3 (property) |
| **IFRS 5** (Held for sale) | FVLCD for disposal group | Level 2-3 |
| **IFRS 16** (Leases) | Fair value in sale-and-leaseback | Level 2-3 |
| **IFRS 3** (Contingent consideration remeasurement) | Current fair value of earn-out | Level 3 (usually) |

---

## Core Concept: Exit Price

```
Fair value = the price that would be received to SELL an asset
             or paid to TRANSFER a liability
             in an ORDERLY transaction
             between MARKET PARTICIPANTS
             at the MEASUREMENT DATE

NOT: what you paid (historical cost)
NOT: what it's worth to you (entity-specific value)
NOT: a fire-sale price (distressed transaction)
NOT: a forced transaction

IS: what an informed, willing market participant would pay/receive
    in the principal market (most volume) or most advantageous market
```

---

## The Hierarchy

| Level | Input | Subjectivity | Disclosure burden |
|---|---|---|---|
| **Level 1** | Quoted prices in active markets for IDENTICAL items | None | Light — state the market, state the price |
| **Level 2** | Observable inputs other than Level 1 quotes | Low | Medium — describe inputs, describe adjustments |
| **Level 3** | Unobservable inputs (management assumptions) | **High** | **Heavy** — full reconciliation, sensitivity analysis, input description |

### Hierarchy Classification Rules

```
Classify based on the LOWEST LEVEL INPUT that is SIGNIFICANT to the measurement.

Example: DCF valuation using:
  - Risk-free rate (Level 1 — observable)
  - Credit spread (Level 2 — observable)
  - Revenue growth forecast (Level 3 — management assumption)

  Revenue growth is SIGNIFICANT to the output → entire measurement = Level 3

Common mistake (ESMA finding): Calling a measurement Level 2
when a significant input is actually Level 3 (unobservable).
```

### Transfers Between Levels

```
Transfers happen when:
  - An active market becomes inactive (Level 1 → Level 2 or 3)
  - Previously observable inputs become unobservable (Level 2 → Level 3)
  - New market data becomes available (Level 3 → Level 2 or 1)

Must disclose: transfers between Level 1 and Level 2, with reasons.
Must disclose: transfers into and out of Level 3, with reasons.
```

---

## Valuation Techniques

| Technique | When used | How it works |
|---|---|---|
| **Market approach** | Comparable transactions exist | Prices from similar transactions, adjusted for differences. Multiples (EV/EBITDA, P/E). |
| **Income approach** | Future cash flows estimable | DCF: forecast cash flows, discount at risk-adjusted rate. Also: option pricing models, multi-period excess earnings (MEEM). |
| **Cost approach** | Replacement or reproduction cost relevant | What it would cost to replace the asset's service capacity. Used for specialized PP&E, some intangibles. |

**Must use technique(s) that maximize observable inputs and minimize unobservable inputs.**

Multiple techniques can (should) be used as cross-checks. If they give materially different answers → investigate why.

---

## Sub-Ergons

### Step 1: Determine what needs fair value [MACH]

```
Triggered by calling ergon (IFRS 3 PPA, IAS 36 impairment, etc.)

Input: specific asset, liability, or unit requiring fair value measurement
  - node:xitem (inventory at NRV? → IAS 2, not IFRS 13)
  - edge:org-org → ppa.intangibles[] (each identified intangible)
  - edge:org-org → ppa.consideration_contingent (earn-out)
  - node:org → cgu (goodwill impairment FVLCD)
  - vItem.financial (IFRS 9 instruments)

For each item: determine unit of account (individual asset? CGU? portfolio?)
```

### Step 2: Identify the principal market [IND + MACH]

```
IFRS 13.16-18:

  Principal market = market with greatest VOLUME and LEVEL OF ACTIVITY
  If no principal market → most advantageous market (highest net price)

  For quoted securities: the exchange where most volume trades
  For real estate: local property market
  For intangibles (PPA): hypothetical market of market participants

  Market participants = buyers/sellers who are:
    - Independent (not related parties)
    - Knowledgeable (reasonable understanding)
    - Able (financially capable)
    - Willing (not forced)
```

### Step 3: Select valuation technique [IND — judgment]

```
Based on what's available:

  Quoted price available for identical item? → Level 1. Done.

  Observable market data for similar items? → Market approach (Level 2)
    Adjust for differences. Document adjustments.

  No market data? → Income approach (DCF) or Cost approach (Level 3)
    MUST use market participant assumptions, NOT entity-specific.

    Market participant assumptions:
      - What would a buyer of this business assume for growth?
      - What discount rate would a buyer apply?
      - NOT: what does OUR management forecast

    In practice: management forecasts are often used as starting point,
    then adjusted to market participant view. Auditors challenge
    whether adjustments are sufficient.
```

### Step 4: Perform measurement [IND + external valuers for Level 3]

```
Level 1:
  Read quoted price at measurement date. Done.
  Record: market, date, price, volume.

Level 2:
  Identify observable inputs (quotes for similar, yield curves, credit spreads)
  Apply adjustments for differences
  Record: inputs, adjustments, technique, result

Level 3:
  Develop unobservable inputs:
    Revenue growth rate: X% (source: management forecast adjusted for market view)
    Discount rate: Y% (source: WACC + specific risk premium)
    Customer attrition: Z% (source: historical data + market comparable)
    Terminal growth: W% (must not exceed long-term GDP growth — ESMA focus)

  Run the model (DCF, MEEM, option pricing)

  Cross-check: does another technique give a similar answer?
  If materially different → investigate, document why.

  Record: ALL inputs, sources, technique, model, sensitivities, result.

  For PPA intangibles → usually requires EXTERNAL VALUATION SPECIALIST
  For complex derivatives → usually requires EXTERNAL VALUATION SPECIALIST
```

### Step 5: Classify in hierarchy [IND]

```
What is the LOWEST LEVEL significant input?

  All significant inputs Level 1 → measurement is Level 1
  Lowest significant input is Level 2 → measurement is Level 2
  ANY significant input is Level 3 → measurement is Level 3

"Significant" = judgment. Would a reasonable change in this input
materially change the fair value? If yes → significant.

Record: hierarchy level + rationale for classification
```

### Step 6: Record and document [MACH + IND]

```
For EVERY fair value measurement, record:

  fair_value: decimal
  measurement_date: date
  hierarchy_level: 1 / 2 / 3
  valuation_technique: market / income / cost
  key_inputs: [{ name, value, observable: boolean, source }]
  unit_of_account: description
  principal_market: description

  IF Level 3:
    sensitivity_analysis: [{ input_name, base_value, change, fair_value_impact }]
    reconciliation: opening → gains/losses → purchases → sales → transfers → closing

  measured_by: IND ref (who) or "external: {valuer name}"
  reviewed_by: IND ref (who reviewed — should be different from measurer)
```

---

## Where Fair Value Properties Live in Our Data Model

| Location | Fair value property | Example |
|---|---|---|
| `edge:org-org → ppa.intangibles[]` | Each intangible has: fair_value, hierarchy_level, technique, key_inputs | Customer relationships valued at EUR 5M, Level 3, MEEM |
| `edge:org-org → ppa.goodwill` | Goodwill itself is a residual, but FVLCD of the CGU uses IFRS 13 | CGU FVLCD = EUR 20M, Level 3, DCF |
| `edge:org-org → ppa.consideration_contingent` | Fair value of earn-out | EUR 3M, Level 3, probability-weighted |
| `node:org → cgu.headroom_latest` | Based on FVLCD (IFRS 13) or VIU (IAS 36 — not IFRS 13) | |
| `node:org → held_for_sale.fair_value_less_costs_to_sell` | FVLCD at classification and each period | Level 2-3 |
| `node:xitem (vItem.financial)` | Fair value per IFRS 9 classification | Level 1 (quoted bond) to Level 3 (complex derivative) |

### Fair value measurement metadata (attach to any fair-value field)

```json
{
  "fair_value": 5000000,
  "fv_meta": {
    "measurement_date": "2025-12-31",
    "hierarchy_level": 3,
    "technique": "income_meem",
    "key_inputs": [
      { "name": "revenue_growth", "value": 0.05, "observable": false, "source": "management_forecast_adjusted" },
      { "name": "discount_rate", "value": 0.12, "observable": true, "source": "wacc_plus_premium" },
      { "name": "customer_attrition", "value": 0.08, "observable": false, "source": "historical_3yr_avg" }
    ],
    "sensitivity": [
      { "input": "discount_rate", "change": "+1%", "fv_impact": -400000 },
      { "input": "revenue_growth", "change": "-2%", "fv_impact": -800000 }
    ],
    "measured_by": "node:ind:v:1:{valuer}",
    "reviewed_by": "node:ind:v:1:{reviewer}"
  }
}
```

This `fv_meta` structure can attach to ANY field that carries a fair value. Standardized across all IFRS standards that invoke IFRS 13.

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | hierarchy_level: is it classified correctly? key_inputs: are they market participant, not entity-specific? sensitivity: is it disclosed? | Rim compliance — ESMA focuses here |
| **Reserve** | sensitivity: how much could this move? Which inputs are most dangerous? | Fair value volatility → equity → KBR headroom. Level 3 measurements are volatile by nature. |
| **Sword** | fair_value of acquired intangibles: what did we actually buy? Fair value trends: is our portfolio appreciating? | Understanding the value of what we own. Informing future acquisition decisions. |

---

## Rim Consequence

| Risk | Consequence | Failure pattern |
|---|---|---|
| Level 3 classified as Level 2 | Understated disclosure. ESMA's most common IFRS 13 finding. | #3 Optimistic estimates (hiding subjectivity) |
| Entity-specific inputs used instead of market participant | Fair value biased (usually upward). Goodwill not impaired when it should be. | #3 Optimistic estimates (Carillion) |
| Insufficient sensitivity disclosure | Market can't assess downside risk. Auditor qualification. | #3 Optimistic estimates |
| Not reconciling Level 3 movements | Can't trace opening → closing. Audit trail broken. | Shield failure |
| Single technique without cross-check | One model, one answer, no validation. | #6 Auditor complacency (accept management's model without challenge) |
| HQ Bank pattern | Internal valuation models for derivatives deviated from market prices. No independent price verification. | #3 Optimistic estimates + #2 Fictitious (mispriced assets) |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — service ergon invoked by IFRS 3, IAS 36, IFRS 9, IAS 19, IFRS 5. Fair value hierarchy, valuation techniques, fv_meta structure for data model, S-R-S view, HQ Bank reference. |
