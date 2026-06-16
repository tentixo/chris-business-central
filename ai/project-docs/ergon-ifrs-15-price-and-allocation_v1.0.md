# Ergon: IFRS 15 — Transaction Price + Allocation (Steps 3-4)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 15.47-86
**Intent**: Determine total transaction price (including variable, financing, non-cash), then allocate to each performance obligation by relative SSP
**Chain**: ergon-ifrs-15-chain_v1.0.md (steps 3-4)
**Depends on**: Performance obligations identified (steps 1-2)

---

## Step 3: Determine Transaction Price [IND + MACH]

```
IFRS 15.47: Transaction price = amount entity expects to be ENTITLED TO
            (not what entity expects to RECEIVE — subtle difference:
             agent receives cash but is only entitled to commission)

Components:

  TRANSACTION PRICE = fixed consideration
                    + variable consideration (constrained)
                    + non-cash consideration (at fair value, IFRS 13)
                    - consideration payable to customer
                    ± significant financing component
```

### 3a: Fixed consideration [MACH]

```
The stated contract price. Most straightforward.
Read from: edge:org-org → sells_to.transaction_price_fixed
BC source: Sales Order / Subscription Contract → total amount
```

### 3b: Variable consideration [IND — HitL]

```
IFRS 15.50-59:

Variable consideration exists when:
  - Volume discounts / rebates (buy 100, get 10% off)
  - Performance bonuses / penalties (hit target → extra payment)
  - Price concessions / credits (expected returns, refunds)
  - Usage-based fees (metered consumption)
  - Earn-outs (revenue sharing)

Estimation methods (choose most predictive):
  a) Expected value: probability-weighted (sum of outcomes × probabilities)
     → Best when large number of similar contracts (portfolio)
  b) Most likely amount: single most likely outcome
     → Best when only two possible outcomes (bonus or no bonus)

THE CONSTRAINT (IFRS 15.56-58):
  Include variable consideration ONLY to the extent it is
  HIGHLY PROBABLE that a significant reversal will NOT occur.

  "Highly probable" is stricter than "probable" (>50%).
  Must consider:
    - Amount is highly susceptible to external factors?
    - Long resolution period?
    - Entity's experience with similar contracts is limited?
    - Broad range of possible outcomes?
    - Entity has practice of offering price concessions?

  PRACTICAL: many companies include 0% variable until they have
  enough history to estimate reliably. Conservative but safe.

EXCEPTION — sales/usage-based royalties on IP:
  Recognize ONLY when: later of sale/usage occurring OR PO satisfied.
  Do NOT estimate in advance. IFRS 15.B63.

Record:
  edge:org-org → sells_to.transaction_price_variable = estimated (constrained) amount
  edge:org-org → sells_to.variable_constraint_applied = true
```

### 3c: Significant financing component [IND]

```
IFRS 15.60-65:

IF payment timing differs materially from delivery timing AND
   the financing benefit is significant:
  → Separate the financing component
  → Revenue at "cash selling price" (what customer would pay for immediate delivery)
  → Interest revenue/expense recognized separately over the financing period

Practical expedient (IFRS 15.63):
  IF transfer → payment ≤ 12 months → NO adjustment needed.
  Most contracts: payment within 30-90 days. No financing component.

When it matters:
  - Construction: deliver building in 24 months, customer pays 50% upfront
    → Customer financing the entity → interest expense to adjust revenue DOWN
  - Subscription: customer pays 12 months upfront, service delivered monthly
    → Entity financing the customer? Usually ≤12 months → practical expedient applies

Record:
  edge:org-org → sells_to.significant_financing = true/false
  edge:org-org → sells_to.financing_adjustment = amount (if applicable)
```

### 3d: Consideration payable to customer [IND]

```
IFRS 15.70-72:

If entity pays the CUSTOMER (rebates, slotting fees, coop advertising):
  → REDUCE transaction price (not a separate expense)
  → UNLESS payment is for a DISTINCT good or service from the customer

Common in: retail (slotting fees to retailers), distribution (coop advertising),
           platform (referral credits to users)

Record:
  edge:org-org → sells_to.consideration_payable_to_customer = amount
```

---

## Step 4: Allocate to Performance Obligations [MACH + IND for SSP]

```
IFRS 15.73-86:

Allocate transaction_price_total to each PO based on RELATIVE
standalone selling price (SSP).

  For each PO:
    allocation = (PO.ssp / total_ssp_all_POs) × transaction_price_total
```

### SSP Determination [IND — HitL for items never sold separately]

```
IFRS 15.77-79:

Best evidence: observable price when entity sells that xItem separately.
  → xItem.SSP if sold standalone → use directly.

If NOT observable (never sold separately):
  a) Adjusted market assessment: what would market pay? Competitor pricing.
  b) Expected cost plus margin: entity's cost + appropriate margin.
  c) Residual approach (LAST RESORT, only if SSP highly variable or uncertain):
     Total transaction price minus observable SSPs of other POs = residual.

For each PO, record:
  xPackage.performance_obligations[].ssp = amount
  xPackage.performance_obligations[].ssp_method = observable / adjusted_market /
                                                   expected_cost_plus_margin / residual
```

### Discount allocation [MACH]

```
IFRS 15.81-83:

If total transaction price < total SSP → there's a discount.

Default: allocate discount proportionally across ALL POs.

Exception: allocate entirely to SPECIFIC POs if:
  a) Entity regularly sells each PO separately
  b) Prices vary significantly
  c) Observable evidence that discount relates to specific PO(s)

Record:
  xPackage.performance_obligations[].allocated_price = amount per PO
  Validate: SUM(allocated_price) = transaction_price_total
```

---

## Output

| Target | What |
|---|---|
| `edge:org-org → sells_to.transaction_price_*` | All components: fixed, variable, financing, non-cash, payable, total |
| `xPackage.performance_obligations[]` | SSP per PO, SSP method, allocated price |
| `node:anomaly` | "Variable consideration material — constraint assessment needed" |
| `node:decision` | "SSP for {xItem} — never sold separately, estimation required" |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Variable consideration not constrained | Revenue overstated → reversal later → volatile P&L | #3 Optimistic (Prosolvia) |
| SSP allocation wrong | Revenue shifted between POs → recognized in wrong pattern/period | #3 Optimistic |
| Financing component ignored | Revenue includes interest → overstated | ESMA finding |
| Consideration payable booked as expense instead of revenue reduction | Revenue overstated, expenses overstated, net may be same but gross misleading | ESMA finding (agent/principal related) |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — transaction price components, variable constraint, SSP methods, allocation. Connected to edge and xPackage properties. |
