# Ergon: IAS 12 — Deferred Tax Calculation

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 12.5-88, IFRIC 23, IAS 12 Pillar Two amendments
**Intent**: For every asset and liability on the consolidated balance sheet: compare carrying amount to tax base, calculate deferred tax, apply exceptions, reconcile effective rate, disclose.
**Chain**: ergon-ias-12-chain_v1.0.md (all steps)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting period, AFTER all Phase 3 chains finalize (IAS 21, IAS 36, IC Elimination, IFRS 16, IAS 19, etc.) |

---

## Step 1: Identify Temporary Differences [MACH + IND]

```
IAS 12.5: Temporary difference = carrying amount of asset/liability
          MINUS tax base of that asset/liability.

For EVERY line on the consolidated balance sheet:
  carrying_amount (IFRS books) vs tax_base (what tax authority recognizes)

Two types:

  TAXABLE temporary difference (carrying > tax base for assets, or carrying < tax base for liabilities):
    → Future taxable amount when asset recovered / liability settled
    → Deferred Tax LIABILITY (DTL)
    → "We'll owe more tax later"

  DEDUCTIBLE temporary difference (carrying < tax base for assets, or carrying > tax base for liabilities):
    → Future deductible amount when asset recovered / liability settled
    → Deferred Tax ASSET (DTA)
    → "We'll owe less tax later"
```

### Systematic identification from each chain's output

```
FOR EACH SUBSIDIARY in consolidation scope:

  a) Entity-level temporary differences:
     Compare each BS line: IFRS carrying vs local tax base.
     Common sources:
       - PP&E: different depreciation rates (IFRS vs tax)
       - Intangibles: amortized for IFRS, maybe not for tax (or different rate)
       - Provisions (IAS 37): recognized for IFRS, deductible when paid for tax
       - Contract liabilities (IFRS 15): taxed on receipt, deferred for IFRS
       - Lease ROU/liability (IFRS 16): IFRS depreciation ≠ tax lease deduction
       - Pension deficit (IAS 19): recognized for IFRS, deductible when contributed for tax
       - Tax losses carried forward: no carrying amount, but has tax base → DTA

  b) Consolidation-level temporary differences:
     Created by consolidation adjustments, NOT in any single entity's books.
       - IFRS 3 PPA fair value uplifts: asset carrying > tax base → DTL
       - IC profit elimination: profit taxed in seller, eliminated at group → DTA
       - FCTR (IAS 21): translation reserve → deferred tax in OCI
       - Undistributed subsidiary profits: retained earnings → potential withholding tax on distribution → DTL

Output per temporary difference:
  { source, asset_or_liability, carrying_amount, tax_base,
    temp_diff, type: taxable/deductible, tax_rate, deferred_tax }
```

---

## Step 2: Calculate Deferred Tax [MACH + IND for DTA recoverability]

### DTL (Deferred Tax Liabilities) [MACH — mostly mechanical]

```
IAS 12.15: Recognize DTL for ALL taxable temporary differences.

  DTL = taxable_temp_diff × applicable_tax_rate

  Tax rate: enacted or substantively enacted at reporting date (IAS 12.46).
  Use the rate expected to apply when the asset is recovered / liability settled.

  Example:
    PPA uplift on customer relationships: IFRS carrying 10M, tax base 0 (not recognized for tax)
    Temp diff: 10M taxable
    Tax rate: 20.6% (Swedish corporate tax)
    DTL: 10M × 20.6% = 2.06M

EXCEPTIONS — do NOT recognize DTL for:
  a) Initial recognition of GOODWILL (IAS 12.15(a)) — THE famous exception
     Why: recognizing DTL on goodwill would increase goodwill → circular
  b) Initial recognition of asset/liability in a transaction that:
     - Is not a business combination, AND
     - Affects neither accounting profit nor taxable profit (IAS 12.15(b))
     (This exception is being narrowed — see Pillar Two below)
  c) Undistributed subsidiary profits WHERE parent controls timing
     AND reversal not probable in foreseeable future (IAS 12.39)
```

### DTA (Deferred Tax Assets) [IND — HitL for recoverability]

```
IAS 12.24: Recognize DTA for deductible temporary differences
  TO THE EXTENT THAT IT IS PROBABLE that future taxable profit
  will be available against which the deductible temp diff can be utilized.

  "Probable" = judgment. THE major HitL in IAS 12.

  DTA = deductible_temp_diff × applicable_tax_rate

  Sources of future taxable profit (IAS 12.28-29):
    a) Existing taxable temporary differences (that will reverse and create taxable income)
    b) Forecast taxable profit (management projections — same challenge as IAS 36 VIU)
    c) Tax planning opportunities (actions entity would take to create taxable profit)

  THE DANGER: companies recognize DTAs on losses to INFLATE equity.
    "We have losses of 50M, at 20.6% = DTA of 10.3M. Equity increases by 10.3M."
    But if the company can't generate future profits → DTA is worthless → write off.
    DTA write-off = equity drop = KBR headroom shrinks.

  IAS 12.37: Reassess unrecognized DTAs at EACH reporting date.
    If new evidence of future profitability → recognize.
    If profitability less likely → derecognize/reduce.

Tax losses carried forward:
  IAS 12.34-36: DTA recognized for unused tax losses IF:
    - Probable that future taxable profit will be available
    - Same entity (losses can't be used by a different group entity, unless group relief)
    - Consider expiry dates (losses may expire)
    - Consider tax authority's acceptance

  Evidence of recoverability is harder for losses than for temp differences.
  If entity has recent history of losses → IAS 12.35: "convincing other evidence"
  required that sufficient taxable profit will be available.
```

---

## Step 3: Exceptions and Special Rules [IND]

### No DT on initial goodwill (IAS 12.15(a))

```
When IFRS 3 creates goodwill:
  Goodwill carrying amount: 50M
  Tax base of goodwill: 0 (most jurisdictions don't recognize goodwill for tax)
  Taxable temp diff: 50M
  DTL would be: 50M × 20.6% = 10.3M

  BUT: IAS 12.15(a) PROHIBITS recognizing this DTL.
  Reason: recognizing DTL would increase the purchase price allocation residual
  → increasing goodwill → increasing DTL → infinite loop.

  HOWEVER: if goodwill is LATER IMPAIRED:
    Carrying: 30M (after 20M impairment)
    Tax base: 0
    Temp diff: 30M
    DTL: still prohibited on the ORIGINAL goodwill temp diff
    BUT: the impairment loss IS a deductible temp diff in some jurisdictions
    → DTA may arise on the impairment (jurisdiction-dependent)

  COMPLEX. Tax specialists required.
```

### Undistributed profits of subsidiaries (IAS 12.39)

```
Retained earnings in subsidiaries = potential taxable event on distribution.
  If subsidiary distributes dividend to parent:
    - Withholding tax in subsidiary's country
    - Dividend tax in parent's country (often exempt under participation exemption)

  IAS 12.39: Recognize DTL on undistributed profits UNLESS:
    a) Parent controls the timing of reversal (distribution), AND
    b) It is probable that the temp diff will NOT reverse in the foreseeable future

  For Swedish parent with Swedish subsidiaries:
    Participation exemption (näringsbetingade andelar) usually means
    dividends from Swedish subsidiaries are TAX EXEMPT → no DTL.

  For foreign subsidiaries:
    Withholding tax may apply. Treaty rates. Must assess per jurisdiction.
    If parent intends to permanently reinvest → exemption may apply.
    If parent plans to distribute → DTL required.
```

### Pillar Two — Global Minimum Tax (IAS 12 amendments)

```
IAS 12.4A (effective 2023): MANDATORY temporary exception:
  DO NOT recognize deferred tax arising from Pillar Two top-up tax.
  DO NOT disclose information about deferred tax related to Pillar Two.

  BUT MUST DISCLOSE:
    - That the exception has been applied
    - Current tax expense related to Pillar Two
    - Qualitative/quantitative info about Pillar Two exposure:
      jurisdictions where effective tax rate is below 15%
      aggregate profit in those jurisdictions
      aggregate Pillar Two tax expense

  This simplifies: no DTA/DTL for Pillar Two.
  But current Pillar Two tax IS recognized in current tax expense.

  Applies if: group has ≥EUR 750M consolidated revenue (2 of 4 years).
  node:org → type_data.tax.pillar_two_scope = true → this exception applies.
```

### IFRIC 23 — Uncertain Tax Positions [IND — HitL]

```
IFRIC 23 (effective 2019): How to account for uncertainty in income tax treatment.

  For each uncertain tax position:
    1. Assume the tax authority WILL examine the position
       AND has full knowledge of all relevant information.
       (No "audit lottery" — no probability of NOT being examined.)

    2. Determine: is it PROBABLE (>50%) the tax authority will accept the position?

    IF probable → measure at FILED amount (the position the entity took)
    IF NOT probable → measure using:
      a) Most likely amount (single best estimate), OR
      b) Expected value (probability-weighted)
      Choose whichever better predicts the resolution.

    3. Reassess at each reporting date if facts change.

  Common uncertain positions:
    - Transfer pricing: is the IC price arm's length?
    - R&D tax credits: do these activities qualify?
    - Permanent establishment: does our activity create a tax presence?
    - Interest deduction limitations (ATAD): does our structure comply?
    - Withholding tax treaty rates: correct treaty applied?

  Record:
    Provisions for uncertain tax positions (additional tax liability)
    OR reduced DTA recognition (if uncertainty about using the DTA)
```

---

## Step 4: Tax Rate Reconciliation [MACH + IND]

```
IAS 12.81(c): Reconcile the tax expense to the product of
accounting profit × applicable tax rate(s).

  Starting point: consolidated profit before tax × statutory rate
  Reconciling items (EVERY difference must be explained):

  | Reconciling item | Direction | Common? |
  |---|---|---|
  | Different tax rates in foreign jurisdictions | +/- | Yes — each sub at local rate |
  | Non-deductible expenses (fines, entertainment, goodwill amortization) | + (more tax) | Yes |
  | Tax-exempt income (participation exemption on dividends) | - (less tax) | Yes for Swedish groups |
  | DTA not recognized (losses where no probable profit) | + (more tax) | Yes for loss-making subs |
  | DTA previously unrecognized now recognized | - (less tax) | Occasional |
  | Tax rate changes (enacted during period) | +/- | Occasional |
  | Pillar Two top-up tax | + | If applicable |
  | Withholding taxes on dividends | + | If foreign subs distribute |
  | R&D tax credits / incentives | - | Jurisdiction-dependent |
  | Prior period adjustments (revised tax returns) | +/- | Occasional |

  The reconciliation must explain EVERY material item.
  Auditors check this line by line.
  ESMA reviews: is the effective tax rate plausible for this group structure?
```

---

## Step 5: Presentation and Disclosure [MACH + IND]

### P&L / OCI classification

```
IAS 12.58: Tax expense recognized WHERE the related item is recognized:

  Item in P&L → tax in P&L
  Item in OCI → tax in OCI
  Item directly in equity → tax directly in equity

  Examples:
    PPA fair value uplift → DTL recognized at acquisition (IFRS 3)
    FCTR (IAS 21) → deferred tax in OCI
    Pension remeasurement (IAS 19) → deferred tax in OCI
    Impairment loss (IAS 36) → deferred tax in P&L
    IC profit elimination → deferred tax in P&L (consolidation adjustment)
```

### Disclosure requirements (IAS 12.79-88)

```
  - Major components of tax expense (current + deferred, by P&L and OCI)
  - Tax rate reconciliation (step 4)
  - DTA and DTL by type of temporary difference
  - Amount of DTA recognized + evidence supporting recognition
  - Amount of unrecognized DTA + unrecognized temp differences
  - Tax losses: amount, expiry dates, utilized
  - Deferred tax on undistributed subsidiary profits (amount not recognized + reason)
  - Pillar Two: exception applied, current tax, exposure disclosure
  - Uncertain tax positions: nature, amount, significant judgments
```

---

## Node/Edge Properties

### On node:org → type_data.tax (additions to existing section)

| Field | Type | x-history | Why required | Ref |
|---|---|---|---|---|
| `current_tax_expense` | decimal | yes | Current period tax charge | IAS 12.5 |
| `deferred_tax_expense` | decimal | yes | Deferred tax charge/credit for the period | IAS 12.5 |
| `dta_balance` | decimal | yes | Total deferred tax assets. Ghost: inflates equity. Write-off → equity drop → KBR. | IAS 12.24 |
| `dtl_balance` | decimal | yes | Total deferred tax liabilities. Reduces equity. | IAS 12.15 |
| `dta_unrecognized` | decimal | yes | DTAs not recognized (no probable future profit). Disclose amount + nature. | IAS 12.81(e) |
| `tax_losses_available` | decimal | no | Unused tax losses carried forward. Per jurisdiction. Expiry dates tracked. | IAS 12.81(g) |
| `effective_tax_rate` | decimal | yes | Actual tax / pre-tax profit. Shield monitors vs statutory rate → reconciliation explains gap. | IAS 12.81(c) |
| `uncertain_tax_provision` | decimal | yes | IFRIC 23 provision for uncertain positions. | IFRIC 23 |
| `pillar_two_exposure` | object | no | { jurisdictions_below_15pct: [], aggregate_profit, aggregate_topup_tax }. Only if pillar_two_scope = true. | IAS 12.4A |

### Consolidation-level deferred tax (on group/parent node:org)

| Field | Type | x-history | Why |
|---|---|---|---|
| `dt_on_ppa_uplifts` | decimal | yes | DTL from IFRS 3 fair value adjustments across all acquisitions |
| `dt_on_ic_elimination` | decimal | yes | DTA from eliminating unrealized IC profit |
| `dt_on_fctr` | decimal | yes | Deferred tax on FX translation reserve (OCI item) |
| `dt_on_undistributed` | decimal | yes | DTL on subsidiary retained earnings planned for distribution |
| `goodwill_dt_exception_amount` | decimal | no | Amount of temp diff on goodwill where DTL NOT recognized (IAS 12.15(a)). Disclose. |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | DTA recognized only when probable? Tax rate reconciliation explains everything? Pillar Two exception applied? IFRIC 23 assessed? Correct P&L vs OCI classification? No DT on initial goodwill? | Tax compliance. ESMA checks reconciliation. Tax authority checks positions. |
| **Reserve** | DTA balance relative to equity: if DTA written off, how much does equity drop? Uncertain provisions: how much could tax authority demand? Pillar Two exposure: how much top-up? | Tax risk = cash risk (assessments) + equity risk (DTA write-off → KBR). |
| **Sword** | Effective tax rate by jurisdiction: where is tax low? Where can we structure better? R&D credits available? Tax incentives unused? | Tax optimization within the Rim (A1: hard rim is sacred — no aggressive planning, but use what's available). |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| DTA recognized without probable future profit | Equity inflated → KBR buffer illusory → board unaware of true position | #3 Optimistic |
| DTA written off suddenly | Equity drops → KBR headroom collapses → potential personal liability | Ghost trap |
| Tax rate reconciliation unexplained items | Auditor qualification. ESMA finding. "What are you hiding?" | Shield failure |
| DTL on initial goodwill recognized | IAS 12.15(a) violation → goodwill overstated (circular) | Shield bright-line |
| IFRIC 23 positions not assessed | Tax authority assessment → additional tax + penalties (skattetillägg 40%) | #4 Hidden positions |
| Pillar Two not disclosed | IAS 12.4A violation for in-scope groups | Shield compliance |
| IC elimination DTA not calculated | Consolidated tax provision wrong (double-taxation on IC profit not offset) | #5 IC concealment |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — accumulator pattern reading all chains. Temporary differences by source. DTA recoverability judgment. Exceptions (goodwill, undistributed, Pillar Two). IFRIC 23 uncertain positions. Tax rate reconciliation. Full S-R-S view. Node:org tax properties expanded. |
