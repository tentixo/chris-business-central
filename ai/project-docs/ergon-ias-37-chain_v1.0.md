# Ergon Chain: IAS 37 — Provisions, Contingent Liabilities and Contingent Assets

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 37 (complete standard)
**Intent**: Recognize provisions when obligations exist. Disclose contingent liabilities. Catch onerous contracts. Prevent both under-provisioning (Rim danger) and over-provisioning (cookie jar reserves).
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — parallel)

---

## Three Categories, Three Treatments

```
                    Present obligation?
                    ├── YES → Probable outflow (>50%)?
                    │         ├── YES → Reliable estimate?
                    │         │         ├── YES → PROVISION (recognize on BS)
                    │         │         └── NO  → Extremely rare. Contingent liability (disclose).
                    │         └── NO (possible, not probable) → CONTINGENT LIABILITY (disclose only)
                    └── NO  → Possible obligation?
                              ├── YES → CONTINGENT LIABILITY (disclose only)
                              └── NO  → Nothing. Not remote = disclose. Remote = nothing.

CONTINGENT ASSET: inflow probable? Disclose. Never recognize until virtually certain.
```

---

## Chain Overview

```
┌──────────────────────────────────────────────┐
│  STEP 1: IDENTIFY OBLIGATIONS                │
│  Legal claims, onerous contracts, warranties, │
│  restructuring, environmental, tax disputes   │
│  IAS 37.10-13                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 2: CLASSIFY                            │
│  Provision (recognize) vs                     │
│  Contingent liability (disclose only) vs      │
│  Remote (nothing)                             │
│  IAS 37.14-26                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 3: MEASURE PROVISIONS                  │
│  Best estimate. Discount if long-term.        │
│  Expected value or most likely amount.         │
│  IAS 37.36-52                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 4: SPECIFIC TYPES                      │
│  Onerous contracts (IFRS 15 connection)       │
│  Restructuring (detailed plan required)       │
│  Warranties (assurance-type)                  │
│  Environmental / decommissioning              │
│  IAS 37.66-83                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  ONGOING: REASSESS EACH PERIOD               │
│  Still probable? Estimate changed?            │
│  New obligations? Resolved?                   │
│  IAS 37.59-60                                │
└──────────────────────────────────────────────┘
```

---

## Step 1: Identify Obligations [IND + MACH]

```
For each entity in the group, identify ALL potential obligations:

SOURCES:

  a) Legal claims / litigation:
     Pending lawsuits, regulatory proceedings, arbitration.
     Source: legal counsel, in-house legal register.
     Each claim: nature, amount claimed, probability assessment.

  b) Onerous contracts:
     Contracts where unavoidable cost of fulfilling > expected economic benefits.
     Source: project managers (xPackage.project where cost > price),
             procurement (unfavorable long-term supply contracts),
             leases (vacant leased space — IFRS 16 handles the lease,
                     but onerous beyond IFRS 16 scope if additional costs exist).
     IFRS 15 connection: contract cost assets → if costs > remaining consideration → onerous.

  c) Warranties (assurance-type):
     Standard product warranties for defects within normal warranty period.
     NOT extended warranties sold separately (those are IFRS 15 or IFRS 17).
     Source: warranty claims history per xItem.type.
     gItem.physical → warranty provision based on historical claim rates.

  d) Restructuring:
     Plans to close operations, exit markets, reduce headcount.
     Source: board decisions, management plans.
     ONLY if detailed formal plan + valid expectation raised (IAS 37.72).

  e) Environmental / decommissioning:
     Cleanup obligations, asset retirement obligations.
     Source: environmental assessments, regulatory requirements.
     Long-term → discount to present value.

  f) Tax disputes (overlap with IFRIC 23):
     Uncertain tax positions → provision under IFRIC 23.
     Already covered in IAS 12 ergon, but IAS 37 applies to
     non-income-tax disputes (VAT disputes, customs, social contributions).

  g) Other:
     Product liability, contract penalties, guarantees given to third parties,
     regulatory fines expected.
```

---

## Step 2: Classify [IND — HitL]

```
For each identified obligation:

  Is there a PRESENT obligation (legal or constructive)?
    Legal: law, contract, regulation creates the obligation.
    Constructive: past practice, published policy, or specific statement
                  creates valid expectation that entity will honor it.

  IF yes → is outflow PROBABLE (>50%)?
    "Probable" = more likely than not (IAS 37.23).
    This is THE judgment call. Legal counsel advises on litigation.
    Project managers advise on onerous contracts.

    IF probable → can you RELIABLY ESTIMATE?
      Almost always yes (IAS 37.25 — "extremely rare" that you can't).
      → PROVISION. Recognize on balance sheet.

    IF not probable but not remote (possible) →
      CONTINGENT LIABILITY. Disclose in notes. Do NOT recognize.

  IF no present obligation → possible obligation →
    CONTINGENT LIABILITY. Disclose if not remote.

  IF remote (very unlikely) → NOTHING. No provision, no disclosure.

  SPECIAL: "serious prejudice" exemption (IAS 37.92):
    In extremely rare cases, disclosure can be omitted if it would
    seriously prejudice the entity's position in a dispute.
    Must still disclose the GENERAL nature.
    Auditors challenge this exemption — it's rarely justified.
```

---

## Step 3: Measure Provisions [IND + MACH]

```
IAS 37.36-52:

BEST ESTIMATE = the amount entity would rationally pay to settle
the obligation at the reporting date (or to transfer to a third party).

Two methods:

  a) MOST LIKELY AMOUNT (single obligation):
     What is the single most likely outcome?
     Example: litigation — most likely outcome is lose and pay EUR 5M.
     → Provision = EUR 5M.

  b) EXPECTED VALUE (large population):
     Probability-weighted average of all possible outcomes.
     Example: warranty claims — 60% chance of EUR 1M cost, 30% of EUR 3M, 10% of EUR 5M.
     → Provision = 0.6×1 + 0.3×3 + 0.1×5 = EUR 2M.

DISCOUNT TO PRESENT VALUE (IAS 37.45-47):
  If time value of money is MATERIAL (long-term obligations):
    Discount at PRE-TAX rate reflecting current market risk assessment.
    Environmental cleanup in 10 years → discount.
    Litigation expected to settle in 6 months → don't bother.

  Unwinding of discount → P&L as financial expense (not operating).

REIMBURSEMENT (IAS 37.53-58):
  If entity expects to recover some of the provision (insurance, counter-claim):
    Recognize reimbursement as SEPARATE ASSET (not offset against provision).
    Only if VIRTUALLY CERTAIN of receiving it.
    Asset ≤ provision amount.
```

---

## Step 4: Specific Types [IND + MACH]

### Onerous Contracts (IAS 37.66-69) — connects to IFRS 15

```
A contract is onerous when unavoidable costs of meeting the obligations
EXCEED the economic benefits expected from it.

Unavoidable costs (2022 amendment — IAS 37.68A):
  = LOWER of:
    a) Cost of fulfilling the contract (DIRECT costs: labor, materials,
       directly attributable overhead — NOT general overhead)
    b) Cost of terminating the contract (penalties, compensation)

Connection to xPackage.project:
  For each xPackage.project in edge:org-org → sells_to:
    estimated_cost = SUM(xItem.cost_standard × planned quantity) + direct overhead
    contract_price = edge:org-org → sells_to.transaction_price_total

    IF estimated_cost > contract_price → ONEROUS
    → Provision = estimated_cost − contract_price (the expected loss)
    → Recognize IMMEDIATELY (don't wait for the loss to materialize)

  MONITOR: each period, reassess ongoing projects.
    hItem.consulting fixed-price engagement → hours exceeding estimate?
    xPackage.project → scope creep without price increase?

Journal:
  Dr: Onerous contract expense (P&L — operating)
  Cr: Provision for onerous contract (BS — current or non-current)
```

### Restructuring Provisions (IAS 37.70-83)

```
Recognize ONLY when entity has:
  a) A DETAILED FORMAL PLAN identifying at least:
     - The business or part concerned
     - Principal locations affected
     - Location, function, approximate number of employees to be compensated
     - Expenditures to be undertaken
     - When the plan will be implemented

  b) Raised a VALID EXPECTATION in those affected:
     - Started implementing the plan, OR
     - Announced main features to those affected

  CANNOT provision for:
    - "We might restructure" (no plan)
    - Board decision only (not yet communicated)
    - Future operating losses (NEVER provision for — IAS 37.63)

  Provision includes ONLY DIRECT costs:
    - Redundancy payments
    - Lease termination penalties (to extent not IFRS 16)
    - Contract cancellation costs
    NOT: retraining, relocation of continuing staff, future losses

  "Big bath" warning:
    Massive restructuring provision in a bad year → release excess in future
    → smooths earnings. Auditors and ESMA watch for this pattern.
```

### Warranty Provisions (assurance-type)

```
Standard product warranties: customer has RIGHT to repair/replacement
if product is defective within warranty period.

This is ASSURANCE (not a separate performance obligation under IFRS 15).
→ IAS 37 provision, not IFRS 15 revenue deferral.

Measurement:
  Expected value method (large population of similar warranties):
    Historical claim rate × average cost per claim × units sold under warranty

  Example: gItem.physical sold 10,000 units, 2% historical claim rate,
           average repair cost SEK 500.
           → Provision = 10,000 × 2% × 500 = SEK 100,000

  Update each period based on actual claims vs estimate → adjust provision.
```

### Environmental / Decommissioning

```
Obligation to clean up contamination, restore sites, decommission assets.
  Often VERY long-term (10-30+ years).
  → Discount to present value (material time value).
  → Unwinding of discount each period → financial expense.

  Initial recognition: capitalize as part of the related asset's cost
  (IAS 16.16(c) — estimated dismantling costs added to PP&E cost, then depreciated).

  Changes in estimate → adjust the asset cost (prospective depreciation change).
```

---

## Ongoing: Reassess Each Period [IND + MACH]

```
IAS 37.59-60:

Each reporting date:
  a) Review EXISTING provisions:
     Still probable? → if not → reverse.
     Estimate changed? → adjust (increase or decrease).
     Resolved? → use (settle) or reverse (no longer needed).

  b) Identify NEW obligations:
     New litigation? New onerous contracts? New restructuring decisions?

  c) Review CONTINGENT LIABILITIES:
     Has probability increased to "probable"? → Upgrade to provision.
     Has it become remote? → Remove from disclosure.

  d) Disclosure update:
     For each provision: opening → additional → used → reversed → unwinding → closing.
     For each contingent liability: nature, estimate (if possible), uncertainties.

Track:
  Movement schedule (opening → movements → closing) for each provision class.
  Required disclosure (IAS 37.84-85).
```

---

## Node Properties

### On node:org → type_data.provisions

| Field | Type | x-history | Why required | Ref |
|---|---|---|---|---|
| `provisions_balance` | decimal | yes | Total provisions on BS. Reduces equity → KBR. | IAS 37.84 |
| `provisions_breakdown` | object | no | By type: { litigation, onerous_contracts, restructuring, warranties, environmental, other } | IAS 37.84 |
| `contingent_liabilities_disclosed` | decimal | no | Estimated amount of contingent liabilities (not on BS, in notes). | IAS 37.86 |
| `onerous_contract_count` | integer | yes | How many contracts are onerous? Shield: are all identified? | IAS 37.66 |
| `restructuring_provision` | decimal | yes | Active restructuring provision. Auditor watches for "big bath." | IAS 37.70 |
| `warranty_provision` | decimal | yes | Assurance warranty provision. Based on claim rates per xItem. | IAS 37 |
| `long_term_provisions_discounted` | decimal | no | Provisions discounted to PV (environmental, decommissioning). Unwinding → financial expense. | IAS 37.45 |

---

## Rim Monitoring

| Monitor | Threshold | Consequence | Cadence |
|---|---|---|---|
| `provisions_balance` relative to equity | Material (>5% of equity) | Direct equity reduction → KBR headroom | Each reporting date |
| `onerous_contract_count` vs xPackage.project count | Any xPackage.project where cost > price | Onerous contract not provisioned = liability understated | Each reporting date (project review) |
| `restructuring_provision` | Large + subsequently reversed | "Big bath" pattern — over-provisioned then released for earnings smoothing | Annual (look-back: provision → release pattern) |
| `contingent_liabilities_disclosed` | Material | Not on BS but could crystallize → Reserve must anticipate | Each reporting date |
| Litigation developments | Legal counsel updates | Probability may have changed (contingent → provision, or vice versa) | Quarterly + when events occur |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | All obligations identified? Provisions measured? Contingent liabilities disclosed? Onerous contracts caught? Restructuring provision only when detailed plan + communicated? | IAS 37 compliance. Under-provisioning = liability gap. Over-provisioning = cookie jar. |
| **Reserve** | Provisions + contingent liabilities = potential cash outflow. How much could crystallize? When? What's the worst case? | Cash risk: provisions settle in cash. Contingent liabilities may become provisions. |
| **Sword** | Onerous contracts: which xPackage.projects are losing money? Can we fix scope, renegotiate, or exit? Warranty rates: which xItems have quality problems? | Operational: fix the contracts. Improve the products. Don't enter similar deals. |

---

## Connection to Other Chains

| Chain | Connection |
|---|---|
| **IFRS 15** | Onerous contract test on xPackage.project: cost > transaction_price_total → provision. Contract cost assets impairment test. |
| **IAS 12** | Provisions create deductible temporary differences → DTA (provision recognized for IFRS, tax deduction when paid). |
| **IFRS 3** | Contingent liabilities of acquiree recognized at FAIR VALUE in PPA (even if < 50% probable — different from IAS 37's >50% threshold). |
| **IFRS 5** | Disposal group may have provisions that transfer with it. |
| **ABL KBR** | Provisions reduce equity → KBR headroom. Large provision = sudden equity drop. |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Onerous contract not provisioned | Losses not recognized until they materialize → equity overstated → KBR | #3 Optimistic |
| Restructuring provisioned too early (no detailed plan) | Premature provision → released later → earnings smoothing | Cookie jar reserves |
| Restructuring provisioned too generously ("big bath") | Excess released in future periods → artificial P&L improvement | Cookie jar + #3 |
| Litigation contingent liability not disclosed | Market doesn't know about potential exposure → surprise | Shield disclosure failure |
| "Serious prejudice" exemption overused | Material litigation hidden from users | Shield — ESMA scrutinizes |
| Provision for future operating losses | IAS 37.63 explicitly PROHIBITS this. Any such provision = error. | Shield bright-line |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — provisions (onerous, restructuring, warranty, environmental), contingent liabilities, classification tree, IFRS 15 onerous connection to xPackage.project, big bath warning, cookie jar monitoring |
