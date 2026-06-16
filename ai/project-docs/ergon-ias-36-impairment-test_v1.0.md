# Ergon: IAS 36 — Impairment Test (Steps 2-4)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 36.18-57 (recoverable amount), IAS 36.59-64 (recognition), IAS 36.104-105 (allocation), IAS 36.109-125 (reversal)
**Intent**: When indicators are found (or annual test due): determine recoverable amount, compare to carrying amount, recognize impairment loss if needed, check for reversal of prior impairments.
**Chain**: ergon-ias-36-chain_v1.0.md (steps 2-4)
**Uses**: IFRS 13 service ergon (for FVLCD)
**Depends on**: Indicators assessed (step 1), CGU allocation in place (step 0)

---

## Step 2: Determine Recoverable Amount [IND + external valuers + MACH]

```
IAS 36.18: Recoverable amount = HIGHER of:
  a) Fair Value Less Costs of Disposal (FVLCD) — what the market would pay
  b) Value in Use (VIU) — what the asset generates by using it

Only need to calculate BOTH if the first one calculated exceeds carrying amount
(then no impairment — skip the second). If first < carrying, must check the other.
```

### FVLCD — Fair Value Less Costs of Disposal [invoke IFRS 13]

```
FVLCD = fair value (per IFRS 13) minus costs of disposal.

Costs of disposal: legal fees, broker fees, dismantling costs, transfer taxes.
NOT: restructuring costs, redundancy costs (those are the BUYER's problem).

For CGUs with goodwill:
  FVLCD is often Level 3 (no market for a CGU as a whole).
  Methods:
    - Comparable transactions (if recent M&A in the sector)
    - Market multiples (EV/EBITDA × EBITDA of CGU)
    - DCF (same as VIU but with market participant assumptions)

  Key distinction from VIU:
    FVLCD uses MARKET PARTICIPANT assumptions (what would a buyer assume?)
    VIU uses ENTITY-SPECIFIC assumptions (what does management project?)

Invoke ergon-ifrs-13-fair-value for the measurement.
Record: fv_meta on the CGU/asset (hierarchy level, inputs, sensitivity).
```

### VIU — Value in Use [IND — THE judgment call]

```
IAS 36.30-57: VIU = present value of future cash flows expected from the asset/CGU.

CASH FLOW PROJECTIONS:
  IAS 36.33(a): Based on REASONABLE AND SUPPORTABLE assumptions.
  IAS 36.33(b): Based on MANAGEMENT'S MOST RECENT financial budgets/forecasts.
  IAS 36.33(b): Maximum projection period: 5 YEARS (unless longer is justified).
  IAS 36.33(c): Beyond 5 years: EXTRAPOLATE using steady or declining growth rate.
  IAS 36.33(c): Growth rate shall NOT exceed long-term average for the market/industry/country.

  THE HOCKEY STICK PROBLEM:
    Management projects: Year 1 down, Year 2 flat, Years 3-5 exponential growth.
    This is the most common manipulation. Auditors must challenge.
    Lookback test: compare LAST YEAR's projections to what actually happened.
    If last year's projections were 30% too optimistic → this year's probably are too.

CASH FLOWS INCLUDE:
  a) Cash inflows from continuing use
  b) Cash outflows necessary to generate those inflows (including maintenance capex)
  c) Net cash flows from disposal at end of useful life (if any)

CASH FLOWS EXCLUDE:
  a) Financing activities (interest, debt repayment — these are in the discount rate)
  b) Income tax (pre-tax cash flows, pre-tax discount rate) — IAS 36.50
  c) Future restructuring not yet committed (IAS 36.44)
  d) Future capex that will enhance the asset beyond its current performance (IAS 36.44)

DISCOUNT RATE (the second major judgment):
  IAS 36.55-56: PRE-TAX rate reflecting:
    - Current market assessment of time value of money
    - Risks SPECIFIC to the asset/CGU
    - NOT risks already adjusted in cash flow estimates (avoid double-counting)

  In practice:
    - Start with WACC (Weighted Average Cost of Capital)
    - Adjust for CGU-specific risks
    - MUST be PRE-TAX (IAS 36.BCZ85 — iterate to find pre-tax rate
      that gives same VIU as post-tax rate applied to post-tax cash flows)
    - This pre-tax/post-tax conversion is technically complex

  ESMA focus: discount rate too low = VIU too high = no impairment = #3 Optimistic.

TERMINAL VALUE:
  After the explicit projection period (typically 5 years):
    Terminal value = Year 5 cash flow × (1 + terminal growth rate) / (discount rate - terminal growth rate)

  Terminal growth rate:
    IAS 36.33(c): steady or DECLINING. NOT increasing.
    Must NOT exceed long-term GDP growth for the market.
    Typical: 0-2% for mature markets. 0% if conservative.

  ESMA focus: terminal growth rate exceeding GDP growth without justification.
```

---

## Step 3: Compare Carrying to Recoverable [MACH]

```
For an individual asset:
  IF carrying_amount > recoverable_amount → impairment = difference

For a CGU:
  Carrying amount of CGU = SUM of all assets in the CGU
    INCLUDING: allocated goodwill
    INCLUDING: allocated corporate assets (proportionally)
    EXCLUDING: liabilities (unless needed to determine recoverable amount)

  Recoverable amount of CGU = higher of FVLCD and VIU (as calculated above)

  IF carrying > recoverable → impairment loss = difference
  IF carrying ≤ recoverable → NO impairment. Record headroom.

  HEADROOM = recoverable - carrying
    This is what Shield monitors: how close are we to impairment?
    node:org → cgu.headroom_latest = recoverable - carrying

    IF headroom > 0 but small → DISCLOSE sensitivity:
      IAS 36.134(f): "a reasonably possible change in a key assumption
       that would cause the carrying amount to exceed recoverable amount"
      Auditors and ESMA ALWAYS check this disclosure.
```

---

## Step 4: Allocate Impairment Loss [MACH + IND]

```
IAS 36.104-105: When a CGU is impaired:

  1. FIRST: reduce GOODWILL allocated to the CGU → to zero
     (goodwill absorbs impairment first)

  2. THEN: reduce OTHER ASSETS in the CGU pro rata by carrying amount
     BUT: do NOT reduce any individual asset below the HIGHEST of:
       a) Its FVLCD (IFRS 13)
       b) Its VIU
       c) Zero

  Example:
    CGU carrying: Goodwill 50M + PP&E 80M + Intangibles 30M = 160M
    Recoverable: 120M
    Impairment: 40M

    Step 1: Reduce goodwill: 50M → 10M (absorb 40M) → all absorbed. Done.
    OR if impairment = 70M:
    Step 1: Reduce goodwill: 50M → 0 (absorb 50M). Remaining: 20M.
    Step 2: Reduce others pro rata:
      PP&E: 80/110 × 20M = 14.5M → PP&E now 65.5M
      Intangibles: 30/110 × 20M = 5.5M → Intangibles now 24.5M
      Check: neither below their individual FVLCD. If so, cap and reallocate remainder.

Journal entries:
  Dr: Impairment loss (P&L — separate line or within depreciation, disclosed)
  Cr: Goodwill (BS)
  Cr: Accumulated impairment on PP&E / Intangibles (BS)

GOODWILL IMPAIRMENT IS NEVER REVERSED. IAS 36.124.
Other asset impairment CAN be reversed in later periods if indicators change.
```

---

## Reversal of Impairment (for assets other than goodwill) [IND + MACH]

```
IAS 36.109-123:

At EACH reporting date, assess whether indicators exist that
a previously recognized impairment loss may have DECREASED.

Same indicators as step 1, but in REVERSE:
  - Market value increased
  - Favorable changes in technology/markets
  - Interest rates decreased
  - Economic performance improved

IF reversal indicators exist:
  Recalculate recoverable amount.
  IF recoverable > carrying:
    Reverse the impairment loss (back to P&L as income).
    BUT: carrying amount after reversal shall NOT EXCEED
    the carrying amount that would have been determined
    (net of depreciation) had NO impairment been recognized.
    (You can't reverse MORE than you impaired.)

  GOODWILL: NEVER REVERSE. IAS 36.124. Period.
  This asymmetry matters: goodwill goes down but never back up.
  One-way ratchet → equity erodes over time through impairment cycles.
```

---

## Data Model Properties

### On node:org → cgu (already defined, confirming)

| Field | Type | x-history | Purpose |
|---|---|---|---|
| `cgu_id` | string | yes | Which CGU this entity belongs to |
| `cgu_name` | string | no | Human-readable |
| `goodwill_allocated` | decimal | yes | Goodwill from IFRS 3 allocated to this CGU |
| `headroom_latest` | decimal | yes | Recoverable - carrying. THE Shield metric. |

### New: impairment test record (on node:org → cgu or on CGU register)

| Field | Type | x-history | Purpose |
|---|---|---|---|
| `last_test_date` | date | yes | When was this CGU last tested? Shield monitors: annual test done? |
| `test_trigger` | enum: annual / indicator / both | no | What triggered the test |
| `recoverable_amount` | decimal | yes | Result of the test |
| `recoverable_basis` | enum: fvlcd / viu | no | Which was higher? |
| `key_assumptions` | object | no | Growth rate, discount rate, terminal growth, projection period. For audit trail + disclosure. |
| `sensitivity` | array | no | [{ assumption, change, headroom_impact }]. IAS 36.134(f) disclosure. |
| `impairment_recognized` | decimal | yes | Amount recognized this period (if any). Hits P&L → equity → KBR. |
| `cumulative_impairment` | decimal | yes | Total impairment recognized to date on this CGU's goodwill. |
| `fv_meta` | object | no | IFRS 13 measurement metadata (if FVLCD used). |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Annual test done? Indicators assessed? Key assumptions defensible (not hockey stick)? Sensitivity disclosed? Goodwill never reversed? | IAS 36 compliance. ESMA's most scrutinized standard after IFRS 15. |
| **Reserve** | Headroom per CGU: how close to impairment? Sensitivity: what rate/growth change triggers impairment? FX impact on translated goodwill (IAS 21 Ghost)? Market cap vs book value? | Impairment = sudden equity drop = KBR danger. Reserve must anticipate. |
| **Sword** | Which CGUs underperform? Which acquisitions haven't delivered? Where is goodwill at risk? | Strategic: fix the CGU (improve performance), restructure, or exit. Lookback on M&A: did we overpay? |

---

## The Carillion Warning

```
Carillion (2018):
  Goodwill: GBP 1.57B (half of total assets)
  Impairment recognized: 0
  Auditor (KPMG for 19 years): accepted management's projections
  July 2017: GBP 845M provision = proof profits were overstated for years
  January 2018: liquidation

What went wrong:
  1. CGU boundaries too high (whole business segments)
  2. Cash flow projections consistently optimistic (hockey stick)
  3. Discount rates too low
  4. Terminal growth rates too high
  5. No lookback testing (prior projections vs actual)
  6. Auditor complacency (19-year tenure, no rotation)

What would have caught it:
  - Lookback: compare Year-1 projection to Year-0 actual. If 30% off → challenge Year-2.
  - Market cap test: market cap < book value for YEARS before collapse.
  - CGU at lower level: individual contracts showed losses that were masked at segment level.
  - Sensitivity: "a 1% change in discount rate would trigger impairment" → alarm bell.
```

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Goodwill not impaired when it should be | Assets overstated → equity overstated → KBR buffer illusory → board unaware of true position | #3 Optimistic (Carillion — THE case) |
| CGU too large | Profitable parts mask losses → impairment hidden → same as above | #3 Optimistic — ESMA #1 IAS 36 finding |
| Hockey stick projections accepted | VIU inflated → no impairment recognized → deferred pain → eventual big write-down | #3 + #6 Auditor complacency |
| Discount rate too low | Same effect as optimistic projections: VIU too high | #3 Optimistic |
| Terminal growth > GDP growth | Mathematically aggressive → VIU inflated | #3 Optimistic — ESMA focus |
| Sensitivity not disclosed | Investors can't assess how close to impairment → surprise when it happens | Shield disclosure failure |
| Goodwill impairment reversed | IAS 36.124 violation — NEVER reverse goodwill impairment | Shield bright-line violation |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — FVLCD vs VIU, hockey stick problem, allocation order (goodwill first), reversal (never goodwill), headroom monitoring, Carillion warning, full S-R-S view, sensitivity disclosure |
