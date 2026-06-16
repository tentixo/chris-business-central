# Ergon: IFRS 3 — Business Combination (PPA)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 3.4-31, 32-40, B13-B63
**Intent**: Perform the Purchase Price Allocation — identify everything acquired at fair value, calculate goodwill, book it
**Chain**: ergon-ifrs-3-chain_v1.0.md (steps 2-5)
**Depends on**: ergon-ifrs-3-business-vs-asset (must conclude = business_combination)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | Business-vs-asset test concluded: business_combination |

---

## Input

| Source | What |
|---|---|
| `edge:org-org` → owns | Acquisition date, consideration, NCI measurement election |
| `node:org` (acquired entity) | Entity data, financial statements at acquisition date |
| Deal documentation | SPA, DD reports, legal opinions |
| External valuers | Fair value reports for intangibles, property, contingent consideration |
| BC | Acquired entity's trial balance at acquisition date |

---

## Sub-Ergons

### Step 1: Identify the Acquirer [IND]

```
IFRS 3.6-7:

Usually obvious: the entity that obtains control (per IFRS 10).
The entity that PAYS is normally the acquirer.

TRICKY CASES:
- Reverse acquisition: legal acquirer issues so many shares
  that the legal acquiree's shareholders end up with majority control.
  → Legal acquiree is the ACCOUNTING acquirer.
  → IFRS 3.B19-B27 applies.
  → Common in backdoor listings.

- Share-for-share: larger entity is usually the acquirer,
  but assess who controls the combined entity.

Record:
  node:org (acquirer) → acquisition_history.acquirer_org_id = self (normal)
  node:org (acquired) → acquisition_history.reverse_acquisition = true (if applicable)
  edge:org-org → owns section confirms direction
```

### Step 2: Determine Acquisition Date [IND]

```
IFRS 3.8-9:

Acquisition date = the date the acquirer obtains CONTROL.

This is NOT necessarily:
  - Signing date (contract signed but conditions not met)
  - Closing date (legal transfer but control already passed)
  - Payment date (payment may be deferred)

It IS: the date the IFRS 10 control model is satisfied.

For most acquisitions: closing date = acquisition date.
For some: control passes earlier (voting agreement) or later (regulatory approval pending).

Record:
  edge:org-org → owns.acquisition_date
  edge:org-org → ppa.measurement_period_end = acquisition_date + 12 months
```

### Step 3: Measure Consideration [IND + external valuers]

```
IFRS 3.37-40:

Total consideration = sum of:

  a) Cash paid
     Straightforward. Record at amount paid.

  b) Shares issued
     At acquisition-date fair value (usually market price for listed acquirer).
     For unlisted: valuation required.

  c) Contingent consideration (earn-outs)
     At acquisition-date FAIR VALUE.
     Classify as LIABILITY or EQUITY (IFRS 3.40):
       Liability → remeasured each period → P&L (ergon-ifrs-3-contingent-consideration)
       Equity → NOT remeasured → stays at initial amount

  d) Previously held interest (step acquisition)
     If acquirer already held 30% (associate) and now buys to 80% (subsidiary):
       Remeasure the 30% at acquisition-date fair value
       Gain/loss → P&L
     IFRS 3.42

SEPARATELY:
  Acquisition costs (advisory, legal, DD, stamp duty):
  → EXPENSED in P&L as incurred. NOT part of consideration.
  → IFRS 3.53
  → Track for audit trail: edge:org-org → ppa.acquisition_costs_expensed

  Pre-existing relationships settled:
  → Accounted for separately from the business combination.
  → IFRS 3.B51-B53
  → Track: edge:org-org → ppa.pre_existing_relationship

Record:
  edge:org-org → ppa.consideration_cash
  edge:org-org → ppa.consideration_shares
  edge:org-org → ppa.consideration_contingent
  edge:org-org → ppa.consideration_contingent_type (liability / equity)
  edge:org-org → ppa.consideration_total
  edge:org-org → ppa.acquisition_costs_expensed
  edge:org-org → ppa.step_acquisition_gain_loss (if applicable)
  edge:org-org → ppa.pre_existing_relationship (if applicable)
```

### Step 4: Identify and Fair-Value Everything [IND + external valuers]

```
IFRS 3.10-31:

THE BIG STEP. Open the box and identify everything at fair value.

TANGIBLE ASSETS:
  - Property, plant, equipment → fair value (market approach or cost approach)
  - Inventory → fair value (selling price minus costs to complete and sell)
  - Cash and receivables → usually close to carrying amount

INTANGIBLE ASSETS (identify SEPARATELY from goodwill):
  Must meet identifiability criterion (IFRS 3.B31-B34):
    - Separable (can be sold, licensed, transferred), OR
    - Arises from contractual/legal rights

  Common intangibles to identify:
  ┌─────────────────────────────────┬──────────────┬─────────────────┐
  │ Intangible                      │ Typical life │ Valuation method│
  ├─────────────────────────────────┼──────────────┼─────────────────┤
  │ Customer relationships          │ 5-15 years   │ MEEM or excess  │
  │ Technology / know-how           │ 3-10 years   │ Relief from     │
  │ Brand / trademark               │ Indefinite   │ royalty          │
  │ Patents                         │ Remaining    │ Relief from     │
  │ Order backlog                   │ < 1 year     │ royalty          │
  │ Favorable contracts             │ Contract     │ MEEM            │
  │ Non-compete agreements          │ Agreement    │ With/without    │
  │ Licenses / permits              │ License term │ Cost approach   │
  │ Software                        │ 3-7 years    │ Cost or income  │
  └─────────────────────────────────┴──────────────┴─────────────────┘

  MEEM = Multi-period Excess Earnings Method
  These usually require EXTERNAL VALUATION SPECIALISTS.

  AUDITOR FOCUS: Under-identification of intangibles is ESMA's #1 finding
  for IFRS 3. Every dollar not identified → goes to goodwill → never amortized
  → overstates future profits.

LIABILITIES ASSUMED:
  - Financial liabilities (debt, payables) → fair value
  - Provisions (IAS 37) → fair value of obligation
  - Contingent liabilities → fair value (even if < 50% probable — IFRS 3.23)
    This is DIFFERENT from IAS 37 (which requires > 50%).
  - Deferred revenue → fair value (often less than carrying amount)
  - Employee obligations → fair value
  - Deferred tax → IAS 12 (on temporary differences from FV adjustments)

Record:
  edge:org-org → ppa.identifiable_net_assets_fv (total)
  edge:org-org → ppa.intangibles[] (each identified intangible)
```

### Step 5: Measure NCI [IND]

```
IFRS 3.19:

Per-acquisition election (choice available for EACH acquisition):

  OPTION A: NCI at FAIR VALUE (full goodwill method)
    Goodwill includes NCI's share of goodwill.
    Requires: valuing NCI at fair value (market price if listed,
              valuation if not).

  OPTION B: NCI at PROPORTIONATE SHARE of identifiable net assets
    Goodwill includes ONLY parent's share of goodwill.
    Simpler. More conservative. Most common.

Record:
  edge:org-org → owns.nci_measurement (full_goodwill / proportionate)
```

### Step 6: Calculate Goodwill [MACH]

```
IFRS 3.32:

Goodwill = Consideration paid
         + NCI (at fair value OR proportionate, per election)
         - Net identifiable assets at fair value

IF positive → Goodwill (asset on balance sheet, never amortized, tested annually IAS 36)
IF negative → Bargain purchase (IFRS 3.34-36):
  1. First: RE-ASSESS. Recalculate. Have you correctly identified all assets and liabilities?
     Bargain purchases are SUSPICIOUS. Auditors will challenge.
  2. If confirmed negative after re-assessment: recognize GAIN in P&L immediately.

Record:
  edge:org-org → ppa.goodwill (if positive)
  edge:org-org → ppa.bargain_purchase_gain (if negative)
  node:org (acquired) → type_data.cgu.goodwill_allocated = goodwill amount
```

### Step 7: Book It [MACH — write to BC]

```
Journal entries in the CONSOLIDATION COMPANY (not the acquired entity's own books):

  Dr: Identifiable tangible assets (at fair value)
  Dr: Identified intangible assets (at fair value)
  Dr: Goodwill
  Cr: Liabilities assumed (at fair value)
  Cr: Deferred tax liability (on FV uplifts — IAS 12)
  Cr: Consideration paid / payable / shares issued
  Cr: NCI (at FV or proportionate)
  Cr: Contingent consideration liability (at FV)

  Separately:
  Dr: Acquisition costs (P&L)
  Cr: Cash / payable

Write to BC:
  Fixed Assets: goodwill, identified intangibles
  GL: PPA adjustment entries in consolidation company
  Business Unit: NCI percentage updated (via IFRS 10 NCI chain)

Write to graph:
  edge:org-org → ppa section fully populated
  edge:org-org → ppa.status = "in_measurement_period"
  node:org → acquisition_history populated
  node:org → cgu allocated
```

---

## Rim Consequence

| Risk | Consequence | Failure pattern |
|---|---|---|
| Under-identification of intangibles | Goodwill overstated → future profits overstated (no amortization) | #3 Optimistic estimates |
| Incorrect fair values | Misstated balance sheet from day one, cascades through all future periods | #3 Optimistic estimates |
| Acquisition costs capitalized | Assets overstated, P&L understated | #3 Optimistic estimates |
| Contingent consideration misclassified (equity vs liability) | P&L volatility hidden or created | #3 Optimistic estimates |
| Bargain purchase not re-assessed | Gain recognized that shouldn't be | #2 Fictitious items |
| Step acquisition remeasurement missed | Gain/loss on previously held interest not recognized | #4 Related party errors |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — full PPA ergon from W-H-S IFRS 3 session |
