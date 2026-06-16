# Ergon Chain: IFRS 9 — Financial Instruments

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 9 (complete standard), IFRS 7 (disclosure companion), IAS 32 (presentation)
**Intent**: Classify, measure, impair, and hedge all financial instruments in the group. Two faces: (1) every company has receivables/payables/loans/investments → IFRS 9 governs them. (2) Financial companies selling vItem.financial → IFRS 9 IS the revenue standard.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — parallel)
**Companion standards**: IFRS 7 (disclosures: credit risk, liquidity risk, market risk), IAS 32 (liability vs equity classification, offsetting)

---

## What ARE Financial Instruments?

```
IAS 32.11: A financial instrument is any contract that gives rise to
a financial ASSET of one entity and a financial LIABILITY or EQUITY
instrument of another entity.

FINANCIAL ASSETS (what you HOLD):
  Cash, bank balances
  Trade receivables (from selling ANY xItem)
  Loans given (edge:org-org → lends_to where you are the lender)
  Debt investments (bonds, notes held)
  Equity investments (shares in non-consolidated entities)
  Derivatives with positive fair value (FX forwards, options in-the-money)
  Contract assets (IFRS 15 — accrued revenue)

FINANCIAL LIABILITIES (what you OWE):
  Trade payables
  Loans received (bank loans, bonds issued, IC loans received)
  Lease liabilities (IFRS 16 — measured under IFRS 16, but IFRS 9 derecognition applies)
  Derivatives with negative fair value
  Contingent consideration (IFRS 3 — if classified as liability)

NOT financial instruments:
  Inventory (IAS 2) — physical assets, not contracts
  PP&E (IAS 16) — physical assets
  Intangible assets (IAS 38) — not contractual financial rights
  Prepayments for goods/services — right to receive goods, not cash
  Tax receivables/payables — statutory, not contractual
```

---

## Chain Overview

```
┌──────────────────────────────────────────────┐
│  PILLAR 1: CLASSIFICATION & MEASUREMENT      │
│  Business model + SPPI test → category        │
│  Amortized cost / FVOCI / FVTPL              │
│  IFRS 9.4.1-4.4                              │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  PILLAR 2: IMPAIRMENT (ECL)                  │
│  Three-stage model for amortized cost + FVOCI │
│  Simplified approach for trade receivables    │
│  IFRS 9.5.5                                  │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  PILLAR 3: HEDGE ACCOUNTING                  │
│  FX hedges, interest rate hedges, commodity   │
│  Fair value / cash flow / net investment      │
│  IFRS 9.6.1-6.7                              │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  IAS 32: PRESENTATION                        │
│  Liability vs equity classification           │
│  Compound instruments (convertibles)          │
│  Offsetting rules                             │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  IFRS 7: DISCLOSURE                          │
│  Credit risk (ECL by stage, concentrations)   │
│  Liquidity risk (maturity analysis)           │
│  Market risk (sensitivity: FX, rate, price)   │
└──────────────────────────────────────────────┘
```

---

## Pillar 1: Classification & Measurement [IND + MACH]

### Financial Assets — Two Tests

```
IFRS 9.4.1: Classification based on TWO criteria:

  1. BUSINESS MODEL TEST: how does the entity manage the asset?
     a) Hold to collect contractual cash flows → may qualify for amortized cost
     b) Hold to collect AND sell → may qualify for FVOCI
     c) Other (trading, managing on fair value basis) → FVTPL

  2. SPPI TEST (Solely Payments of Principal and Interest):
     Are the contractual cash flows SOLELY principal + interest?
     Interest = compensation for time value + credit risk + basic lending margin.

     PASSES SPPI: standard loan, bond, trade receivable (fixed or floating rate)
     FAILS SPPI: convertible feature, leverage feature, equity-linked returns,
                  returns linked to commodity prices, inverse floaters

  DECISION MATRIX:

  Business Model: Hold to collect | Hold to collect & sell | Other/Trading
  SPPI passes:    AMORTIZED COST  | FVOCI (debt)           | FVTPL
  SPPI fails:     FVTPL           | FVTPL                  | FVTPL

  SPECIAL: Equity investments (shares in other entities):
    No SPPI (dividends ≠ interest) → would default to FVTPL.
    BUT: IRREVOCABLE election per instrument to designate as FVOCI.
    If FVOCI elected for equity: dividends → P&L, fair value changes → OCI.
    OCI amounts NEVER recycled to P&L (even on disposal). Permanent OCI.
```

### What This Means for Each Financial Asset Type

| Asset type | Typical classification | Measurement | Where gains/losses go |
|---|---|---|---|
| **Trade receivables** | Amortized cost (hold to collect, SPPI passes) | Initial: fair value + transaction costs. Subsequent: amortized cost minus ECL. | ECL → P&L. FX → P&L (IAS 21). |
| **Bank deposits** | Amortized cost | Same as receivables | Interest → P&L |
| **IC loans given** (edge:org-org → lends_to) | Amortized cost | Same | Interest → P&L. ECL → P&L. Eliminated on consolidation. |
| **Government bonds held** | Amortized cost OR FVOCI (depending on business model) | AC: amortized cost. FVOCI: fair value, changes in OCI (recycled on disposal). | AC: interest → P&L. FVOCI: FV changes → OCI → P&L on disposal. |
| **Corporate bonds held** | Same as government bonds | Same | Same |
| **Equity investments (non-consolidated)** | FVTPL (default) or FVOCI (irrevocable election) | Fair value | FVTPL: all changes → P&L. FVOCI: dividends → P&L, FV changes → OCI (NEVER recycled). |
| **Derivatives** (FX forward, interest rate swap) | FVTPL (unless in hedge relationship) | Fair value | FVTPL: changes → P&L. If hedging: see Pillar 3. |
| **vItem.financial products** (loans originated, securities created) | Depends on business model | Depends | THE business of a financial company. Classification drives entire P&L pattern. |

### Financial Liabilities — Simpler

```
IFRS 9.4.2: Most financial liabilities at AMORTIZED COST.

  Exceptions:
    - Derivatives with negative FV → FVTPL
    - Contingent consideration (IFRS 3) classified as liability → FVTPL
    - Liabilities DESIGNATED at FVTPL (fair value option — rare, special conditions)
    - Financial guarantee contracts → IFRS 9 or can elect IFRS 17

  For designated FVTPL liabilities:
    Fair value changes due to OWN CREDIT RISK → OCI (not P&L).
    This prevents the absurdity of "our creditworthiness declined → we profit"
    (because liability FV decreased).
```

### IAS 32: Liability vs Equity

```
CRITICAL for listed groups:

  A financial instrument is EQUITY only if:
    NO contractual obligation to deliver cash or another financial asset.
    If settled in own shares: FIXED number of shares for FIXED amount ("fixed-for-fixed").

  Everything else → FINANCIAL LIABILITY.

  Common traps:
    Redeemable preference shares → LIABILITY (mandatory redemption = cash obligation)
    Written put on NCI (obligation to buy minority shares) → LIABILITY
    Convertible bond → COMPOUND: liability component + equity component (split)
    Puttable instruments → usually LIABILITY (IAS 32.16A-D for limited exceptions)

  WHY this matters: liability classification → hits equity (reduces it) → KBR.
  A redeemable preference share classified as equity when it should be a liability
  → equity OVERSTATED → KBR buffer illusory.
```

---

## Pillar 2: Impairment — Expected Credit Loss (ECL) [IND + MACH]

### The Three-Stage Model

```
IFRS 9.5.5: Applies to financial assets at AMORTIZED COST and FVOCI (debt).
NOT to FVTPL (already at fair value — impairment embedded in FV changes).

                    ┌────────────────────────────────────────────┐
                    │  STAGE 1: PERFORMING                       │
                    │  No significant increase in credit risk     │
                    │  ECL = 12-MONTH expected loss               │
                    │  Interest: on GROSS carrying amount         │
                    └──────────────┬─────────────────────────────┘
                                   │ SICR detected
                                   ▼
                    ┌────────────────────────────────────────────┐
                    │  STAGE 2: UNDERPERFORMING                  │
                    │  Significant increase in credit risk (SICR) │
                    │  ECL = LIFETIME expected loss               │
                    │  Interest: still on GROSS carrying amount   │
                    └──────────────┬─────────────────────────────┘
                                   │ Credit-impaired
                                   ▼
                    ┌────────────────────────────────────────────┐
                    │  STAGE 3: CREDIT-IMPAIRED                  │
                    │  Objective evidence of impairment           │
                    │  ECL = LIFETIME expected loss               │
                    │  Interest: on NET carrying amount (after ECL)│
                    └────────────────────────────────────────────┘

SICR (Significant Increase in Credit Risk) — THE judgment call:
  IFRS 9.5.5.9: Compare credit risk at reporting date vs at initial recognition.
  If significantly worse → Stage 2.

  Quantitative: PD (probability of default) increased by X% or Xbps.
  Qualitative: customer in financial difficulty, industry downturn, payment delays.

  Rebuttable presumption (IFRS 9.5.5.11):
    30+ days past due → SICR exists (rebuttable).
    Can be rebutted if entity has reasonable, supportable information
    showing no SICR despite being past due.

  Credit-impaired (Stage 3) indicators (IFRS 9.B5.5.37):
    - Significant financial difficulty of debtor
    - Breach of contract (e.g., default or past due > 90 days)
    - Concessions granted due to debtor's difficulty
    - Probable bankruptcy or financial restructuring
    - Active market disappeared for the asset
```

### Simplified Approach for Trade Receivables

```
IFRS 9.5.5.15: For trade receivables (and contract assets) WITHOUT
a significant financing component:

  MUST use simplified approach: always LIFETIME ECL.
  No staging. No SICR assessment. Always lifetime.

  PRACTICAL: PROVISION MATRIX.

  Build a matrix from HISTORICAL loss data:

  | Age bucket     | Historical loss rate | Forward-looking adjustment | ECL rate |
  |---------------|---------------------|---------------------------|----------|
  | Current        | 0.5%                | +0.2% (economy weakening) | 0.7%     |
  | 1-30 days      | 1.5%                | +0.3%                     | 1.8%     |
  | 31-60 days     | 5%                  | +1%                       | 6%       |
  | 61-90 days     | 15%                 | +2%                       | 17%      |
  | 91-180 days    | 40%                 | +5%                       | 45%      |
  | 180+ days      | 80%                 | +5%                       | 85%      |

  Apply matrix to receivables aging → ECL = SUM(bucket_balance × ECL_rate).

  FORWARD-LOOKING: IFRS 9 requires forward-looking information.
  Can't just use historical rates. Must consider:
    - Economic outlook (GDP, unemployment, industry trends)
    - Customer-specific information (T and dT/dt from our model!)
    - Country risk (Reserve: buyer jurisdiction)

  Connection to our model:
    edge:org-org → sells_to creates receivables.
    ORG.buyer jurisdiction + type + size → credit risk profile.
    T and dT/dt on the relationship → leading indicator of credit risk!
      Falling T with late payments = SICR signal.
      High T with one late payment = probably just timing.

  The EconSales model PREDICTS credit risk better than aging alone.
```

### ECL for IC Loans

```
edge:org-org → lends_to: IC loans between group entities.

  Entity-level (separate FS): ECL applies to IC loans.
  A subsidiary lending to a struggling subsidiary → ECL required.

  Consolidation: IC loans ELIMINATED.
  → ECL on IC loans also eliminated on consolidation.
  → But: the entity-level ECL may signal a problem (the borrower is struggling).

  If IC borrower approaches insolvency → the IC loan may trigger KBR at the LENDER
  (write-down reduces lender's assets → equity → KBR).
```

---

## Pillar 3: Hedge Accounting [IND — specialist knowledge]

### Why Hedge?

```
Without hedge accounting:
  Entity hedges USD revenue with FX forward.
  Revenue recognized: USD 1M at average rate = SEK 10.5M
  FX forward gains: SEK 0.3M (because USD strengthened)
  P&L: revenue 10.5M + derivative gain 0.3M = 10.8M

  Problem: derivative gain in P&L but the HEDGED revenue is spread over months.
  TIMING MISMATCH → P&L volatility that doesn't reflect economic reality.

With hedge accounting:
  The derivative gain is deferred in OCI and released to P&L WHEN the revenue is recognized.
  P&L: revenue 10.5M + 0.3M (recycled from OCI when revenue recognized) = 10.8M
  But the 0.3M hits P&L at the SAME TIME as the revenue → matched → less volatility.

Hedge accounting REDUCES P&L volatility by matching the hedge with the hedged item.
```

### Three Types of Hedges

```
1. FAIR VALUE HEDGE:
   Hedging changes in fair value of a recognized asset/liability.
   Example: fixed-rate bond held → hedge interest rate risk with swap.
   Both hedged item AND hedge instrument → changes in P&L.
   They (mostly) offset → low P&L volatility.

2. CASH FLOW HEDGE:
   Hedging variability in future cash flows.
   Example: forecast USD revenue → hedge with FX forward.
   Hedge instrument FV change → OCI (cash flow hedge reserve).
   Recycled to P&L when hedged item affects P&L.
   THE GHOST: cash flow hedge reserve in OCI → equity → KBR.

3. HEDGE OF NET INVESTMENT IN FOREIGN OPERATION:
   Hedging FX risk on net investment in a foreign sub (IAS 21).
   Hedge gains/losses → OCI (alongside FCTR).
   Recycled to P&L on disposal of foreign operation.
   Reduces the FCTR Ghost (hedge offsets FCTR movement).
```

### Hedge Accounting Requirements (IFRS 9.6.4)

```
To QUALIFY for hedge accounting, must document:

  a) FORMAL DESIGNATION at inception:
     - Which hedging instrument (the derivative)
     - Which hedged item (the exposure)
     - Nature of the risk being hedged (FX, interest rate, commodity)
     - How effectiveness will be assessed

  b) ECONOMIC RELATIONSHIP:
     Hedging instrument and hedged item have values that move in
     OPPOSITE directions due to the hedged risk.
     (No need for 80-125% retrospective test from old IAS 39.)

  c) CREDIT RISK does not dominate:
     The effect of credit risk is not the dominant driver of value changes.

  d) HEDGE RATIO:
     Same as used for risk management purposes.
     Can't designate a different ratio for accounting than for RM.

  IF any condition no longer met → DISCONTINUE hedge accounting (prospective).
  Amounts in OCI from cash flow hedges → remain until hedged item affects P&L
  (or hedged future transaction is no longer expected to occur → reclassify to P&L).
```

### Common Hedges for a Swedish Listed Group

| What's hedged | Risk | Instrument | Hedge type | Where gains/losses go |
|---|---|---|---|---|
| Forecast USD revenue | FX | FX forward (sell USD, buy SEK) | Cash flow | OCI → P&L when revenue recognized |
| Forecast EUR purchases | FX | FX forward (buy EUR, sell SEK) | Cash flow | OCI → P&L when purchase expensed |
| USD receivable (recognized) | FX | FX forward | Fair value | Both in P&L (offset) |
| Variable rate loan | Interest rate | Interest rate swap (pay fixed, receive floating) | Cash flow | OCI → P&L over loan term |
| Net investment in EUR subsidiary | FX | EUR loan at parent (or FX forward) | Net investment | OCI (with FCTR) → P&L on disposal |

---

## IFRS 7: Disclosure [MACH + IND]

```
IFRS 7 requires disclosure of THREE risk categories:

1. CREDIT RISK:
   - Maximum exposure to credit risk (per class of financial asset)
   - ECL allowance by stage (Stage 1, 2, 3) with reconciliation (opening → movements → closing)
   - Significant concentrations of credit risk
   - Credit quality (aging analysis, past due analysis)
   - Forward-looking information used in ECL
   - Collateral held
   - Write-off policy

2. LIQUIDITY RISK:
   - Maturity analysis of financial liabilities (contractual undiscounted cash flows)
   - Buckets: <1 month, 1-3 months, 3-12 months, 1-5 years, >5 years
   - Include: trade payables, loans, lease liabilities (IFRS 16), derivatives
   - How liquidity risk is managed

3. MARKET RISK:
   - Sensitivity analysis for EACH type of market risk:
     a) FX risk: impact of ±10% on each significant currency
     b) Interest rate risk: impact of ±100bps on floating rate instruments
     c) Equity price risk: impact of ±10% on equity investments
   - How market risk is managed
   - If hedging: describe hedging strategy, instruments, amounts hedged

Connection to S-R-S:
  Credit risk disclosures → Shield (compliance) + Reserve (exposure sizing)
  Liquidity maturity → Reserve (cash planning, 13-week forecast alignment)
  Market risk sensitivity → Reserve (FX/rate stress matches our Ghost stress test)
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Classification correct per business model + SPPI? ECL calculated per three-stage model (or simplified for receivables)? Hedge documentation complete? IAS 32 liability/equity correct? IFRS 7 disclosures complete (credit, liquidity, market risk)? | Classification errors → wrong measurement → wrong P&L pattern. ECL too low → receivables overstated. Hedge documentation missing → can't use hedge accounting → P&L volatility. IAS 32 wrong → equity overstated → KBR. |
| **Reserve** | ECL adequacy: is the provision enough? Forward-looking info used? Concentration: is one debtor >10% of receivables? Liquidity: maturity profile → can we pay? FX/rate sensitivity: how much does ±10%/±100bps move equity? Hedge effectiveness: are hedges working? | Credit risk = cash risk (debtor doesn't pay). Liquidity = survival. Market risk → Ghost (FV changes in OCI → equity → KBR). |
| **Sword** | Credit terms offered to customers: competitive? Optimizable? Which ORG.buyer segments have lowest ECL? Where is cash conversion fastest (DSO from our model)? Hedging cost: is the hedge worth the premium? | Customer credit strategy. Cash conversion optimization. Hedging ROI. |

## Ghost Dimension

IFRS 9 creates multiple Ghosts:

| Ghost | Mechanism | Equity impact |
|---|---|---|
| **FVOCI debt instruments** | Fair value changes → OCI | Equity ± without P&L. Recycled on disposal. |
| **FVOCI equity investments** | Fair value changes → OCI | Equity ± without P&L. NEVER recycled (permanent OCI). |
| **Cash flow hedge reserve** | Effective hedge portion → OCI | Equity ± without P&L. Recycled when hedged item hits P&L. |
| **Own credit risk on FVTPL liabilities** | Own credit changes → OCI | Equity ± without P&L. |
| **ECL provisions** | Reduce asset carrying amount → reduce net assets | Equity ↓. P&L charge (not OCI — this one IS in P&L). |

All feed into ABL KBR equity monitoring.

## xItem Connection

| xItem type | IFRS 9 impact |
|---|---|
| **Any xItem sold on credit** (gItem, vItem, hItem) | Creates trade receivables → simplified ECL (provision matrix). ORG.buyer credit profile + T/dT/dt = leading indicators. |
| **vItem.financial** (loans, derivatives, payment platforms) | IFRS 9 IS the standard. Classification + measurement + ECL + hedge accounting. The WHOLE standard applies. |
| **vItem.financial.lease** (lessor) | Lease receivable (finance lease) → IFRS 9 ECL applies. |
| **xPackage with financing component** (IFRS 15.60-65) | Significant financing → separate interest component → IFRS 9 applies to the financing element. |

## Tamagos Connection

The ECL model connects to our EconSales pipeline:
- **T and dT/dt** on a relationship = leading indicator of credit risk. Falling T + late payments = SICR signal (Stage 1 → Stage 2).
- **BFFB matter** (existing customers) have credit history → better ECL estimation than new customers.
- **White matter** (new, no BFFB yet) → higher credit uncertainty → potentially higher ECL rate.
- **Tamagos pipeline** → receivables don't exist yet. But forecast receivables from near-hatching Tamagos feed into cash flow forecasting (Reserve: 13-week forecast).

---

## Node/Edge Properties

### On node:org → type_data.financial_instruments

| Field | Type | x-history | Why required | Ref |
|---|---|---|---|---|
| `ecl_allowance_total` | decimal | yes | Total ECL provision across all financial assets. Reduces net assets → equity → KBR. | IFRS 9.5.5 |
| `ecl_by_stage` | object | yes | { stage1: amount, stage2: amount, stage3: amount }. Shield: staging correct? Reserve: how much is deteriorating? | IFRS 7.35H |
| `ecl_receivables_simplified` | decimal | yes | Trade receivables ECL (provision matrix). The most common ECL for non-financial groups. | IFRS 9.5.5.15 |
| `fvoci_reserve` | decimal | yes | Accumulated fair value changes on FVOCI instruments in OCI. Ghost: equity moves without P&L. | IFRS 9.4.1.2A |
| `cash_flow_hedge_reserve` | decimal | yes | Effective portion of cash flow hedges in OCI. Ghost: equity moves without P&L. Recycled when hedged item hits P&L. | IFRS 9.6.5.11 |
| `has_active_hedges` | boolean | no | Does this entity use hedge accounting? If yes → documentation + effectiveness requirements. | IFRS 9.6.4 |
| `hedge_instruments_fv` | decimal | yes | Total fair value of hedging instruments. Net positive or negative. | IFRS 7.24A |
| `financial_assets_fvtpl` | decimal | yes | Total financial assets at FVTPL. FV changes → P&L directly. | IFRS 9.4.1.4 |
| `financial_liabilities_fvtpl` | decimal | yes | Total financial liabilities at FVTPL (including contingent consideration from IFRS 3). | IFRS 9.4.2.2 |

### On edge:org-org → sells_to (addition)

| Field | Type | x-history | Why |
|---|---|---|---|
| `receivable_ecl_rate` | decimal | yes | ECL rate applied to receivables from this buyer. Based on provision matrix bucket + buyer-specific adjustments. Shield validates. |
| `receivable_overdue_days` | integer | yes | Days overdue. >30 = rebuttable presumption of SICR. >90 = likely credit-impaired (Stage 3). |

### On edge:org-org → lends_to (addition)

| Field | Type | x-history | Why |
|---|---|---|---|
| `ecl_stage` | enum: 1/2/3 | yes | Which ECL stage is this IC loan in? Stage 2/3 = borrower deteriorating. |
| `ecl_amount` | decimal | yes | ECL provision on this specific IC loan. Entity-level (eliminated on consolidation). |

---

## Rim Monitoring

| Monitor | Threshold | Consequence | Cadence |
|---|---|---|---|
| `ecl_allowance_total` relative to receivables | Material change vs prior period | Sharp ECL increase = credit deterioration → P&L hit → equity → KBR | Each reporting date |
| Stage 2+3 as % of total financial assets | Increasing trend | Credit quality deteriorating across portfolio | Each reporting date |
| `receivable_overdue_days` on any edge:org-org | >30 days (SICR presumption) or >90 days (likely impaired) | SICR assessment required. Stage migration. | Monthly (part of IC matching / close) |
| `cash_flow_hedge_reserve` | Large absolute amount | Ghost: equity swing when hedges recycled or discontinued | Each reporting date |
| `fvoci_reserve` | Large swing | Ghost: equity moved without P&L | Each reporting date |
| IAS 32 classifications | Any redeemable preference shares, NCI puts, convertibles | Liability vs equity. Wrong classification → equity overstated → KBR illusion | At issuance + annual review |
| Hedge documentation | Incomplete or missing | Can't use hedge accounting → P&L volatility → equity volatility | At designation + each reporting date |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| ECL too low | Receivables overstated → equity overstated → KBR buffer illusory | #3 Optimistic |
| ECL not forward-looking | Using only historical rates violates IFRS 9. ESMA finding. | #3 + Shield |
| SICR not detected (Stage 1 when should be 2) | 12-month ECL instead of lifetime → underprovisioned | #3 Optimistic |
| Hedge documentation missing | Can't apply hedge accounting → sudden P&L volatility when hedges are already in place | Shield compliance failure |
| IAS 32 classification wrong | Redeemable pref shares as equity → equity overstated → KBR | #3 + HQ Bank pattern |
| FVOCI reserve large and volatile | Board doesn't understand OCI → equity swings surprise → KBR | Ghost trap |
| Concentration: one debtor >10% of receivables defaults | Material ECL charge + cash shortfall | Reserve failure — concentration not monitored |

---

## Connection to Other Chains

| Chain | Connection |
|---|---|
| **IFRS 15** | Revenue creates receivables → IFRS 9 ECL applies. Significant financing component → IFRS 9 governs the financing element. |
| **IFRS 3** | Contingent consideration (liability) → FVTPL (IFRS 9 measurement). Retained interest after loss of control → IFRS 9 or IAS 28. |
| **IFRS 13** | FVTPL and FVOCI measurements → invoke IFRS 13 service ergon. fv_meta on all fair-valued instruments. |
| **IAS 21** | FX on financial instruments → P&L (monetary items). FX hedges → IFRS 9 hedge accounting. Net investment hedges → OCI (with FCTR). |
| **IAS 12** | ECL provision → DTA (deductible temp diff: provision recognized, tax deduction when written off). FVOCI reserve → deferred tax in OCI. |
| **IC Elimination** | IC loans → IFRS 9 at entity level → eliminated on consolidation. IC receivables/payables → eliminated. |
| **ABL KBR** | ECL → equity ↓. FVOCI reserve → equity ±. Cash flow hedge reserve → equity ±. IAS 32 misclassification → equity overstated. ALL Ghosts feed KBR. |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — three pillars (classification/ECL/hedging), IAS 32 presentation, IFRS 7 disclosure, simplified ECL for trade receivables with provision matrix, hedge types, xItem connection (vItem.financial + receivables from any xItem), Tamagos connection (T/dT/dt as credit risk leading indicator), node:org + edge:org-org properties, Ghost dimension (FVOCI, hedge reserve, own credit), S-R-S view, Rim monitors |
