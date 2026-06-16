# Ergon Chain: IFRS 17 — Insurance Contracts

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 17 (complete standard, effective 2023-01-01)
**Intent**: Identify when IFRS 17 applies within the group. Ensure correct measurement and consolidation treatment. Most detail lives in specialist insurance systems — this ergon handles the FGGE governance interface.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — if applicable)
**Scope**: Only relevant if group ISSUES insurance contracts (captive, extended warranties, financial services)

---

## When Does IFRS 17 Apply?

### The test: significant insurance risk

```
IFRS 17.2-8:

A contract IS an insurance contract if:
  Entity accepts SIGNIFICANT INSURANCE RISK from the policyholder
  by agreeing to COMPENSATE the policyholder
  if a SPECIFIED UNCERTAIN FUTURE EVENT
  ADVERSELY AFFECTS the policyholder.

  Significant = there is a scenario (commercially realistic, not trivially unlikely)
  where the entity pays MORE than it would if the insured event had NOT occurred.
```

### What IS and what ISN'T IFRS 17

| Contract type | IFRS 17? | Why | Standard instead |
|---|---|---|---|
| Insurance policy (life, property, health) | **YES** | Core insurance. Significant insurance risk. | — |
| Reinsurance (held or issued) | **YES** | Insurance of insurance. | — |
| Captive insurance (intra-group) | **YES** in captive's own books. **Eliminated** on consolidation. | Entity issues insurance contracts even if policyholders are group entities. | — |
| Extended warranty SOLD SEPARATELY | **Maybe** | If covers risks beyond manufacturing defects → significant insurance risk → IFRS 17. | If assurance-type (normal defects) → IFRS 15 |
| Standard product warranty (assurance-type) | **NO** | Part of selling the product. No separate insurance risk accepted. | IFRS 15 (part of transaction price) |
| Fixed-fee service contract | **NO** | Service, not insurance. Even if entity takes on risk of cost overrun. | IFRS 15 |
| Financial guarantee contract | **Choice** | IFRS 17.7(e): issuer can ELECT to apply IFRS 17 or IFRS 9 (irrevocable choice per contract) | IFRS 9 if not elected |
| Investment contract with DPF | **YES** | Discretionary participation features → IFRS 17.71 | — |
| Credit card with insurance element | **Separate** | Separate the insurance component → IFRS 17. Rest → IFRS 15/IFRS 9. | — |

### xItem mapping

```
vItem.financial.insurance → IFRS 17 (this ergon)
vItem.financial.debt/equity/derivative → IFRS 9
vItem.e-svc (subscription) → IFRS 15
gItem/hItem with assurance warranty → IFRS 15 (part of the xItem sale)
gItem/hItem with insurance warranty sold separately → IFRS 17 (separate contract)
```

---

## The Three Measurement Models (overview — detail in specialist systems)

### General Measurement Model (GMM / Building Block Approach)

```
Default model. Used for most insurance contracts.

Insurance contract liability =
  Fulfilment cash flows:
    a) Estimates of future cash flows (probability-weighted)
    b) Discounted at current rates (not historical)
    c) Risk adjustment for non-financial risk (uncertainty buffer)
  + Contractual Service Margin (CSM):
    Unearned profit. Released to P&L over the coverage period.

CSM = total expected profit on the contract at inception.
  → Recognized in P&L as insurance services are provided.
  → Like deferred revenue but for insurance.
  → If contract is ONEROUS at inception → no CSM, loss in P&L immediately.

Each period:
  1. Accrete interest on CSM (discount unwinding)
  2. Update fulfilment cash flows for changes in estimates
  3. Release CSM to P&L (as coverage provided)
  4. Recognize insurance service expenses
```

### Premium Allocation Approach (PAA) — simplified

```
IFRS 17.53-59: Permitted for contracts with coverage period ≤ 12 months
(or if it gives similar results to GMM).

Simpler: measure liability = unearned premium (like IFRS 15 deferred revenue).
  Revenue = premium allocated to each period of coverage.
  No CSM calculation needed.
  No discount required (unless significant financing).

Most non-insurance companies' insurance-like contracts (extended warranties)
qualify for PAA because coverage is typically ≤ 12 months.
```

### Variable Fee Approach (VFA) — for participating contracts

```
IFRS 17.B101-B118: For direct participating contracts
(policyholder shares in the return on underlying items).

Investment-linked products: the policyholder's share of returns
is treated as a "variable fee" to the insurer.

Mostly relevant for life insurance with investment components.
Unlikely for non-insurance groups.
```

---

## Contract Grouping (IFRS 17.14-24) [IND — HitL]

```
CRITICAL: contracts must be grouped into PORTFOLIOS and COHORTS.

Portfolio = contracts with similar risks, managed together.

Within each portfolio, group into ANNUAL COHORTS:
  - Contracts issued within the SAME 12-month period
  - Cannot group contracts issued more than 12 months apart
  - Must separate: onerous at inception / no significant possibility of becoming onerous / remaining

This cohort requirement is the MOST CONTROVERSIAL aspect of IFRS 17.
Auditors check it rigorously. It prevents companies from masking
new unprofitable contracts within a pool of old profitable ones.
```

---

## Consolidation Interface (what FGGE needs)

### If group has captive insurance subsidiary

```
CAPTIVE ENTITY (node:org with entity_type = operating, insurer):
  Own books: IFRS 17 applies fully.
  Uses specialist insurance system (not BC).
  Produces trial balance with IFRS 17 line items:
    - Insurance contract liabilities (fulfilment CF + CSM)
    - Insurance contract assets (reinsurance held)
    - Insurance revenue
    - Insurance service expenses
    - Insurance finance income/expenses

ON CONSOLIDATION:
  IC insurance contracts must be ELIMINATED:
    - Captive's insurance liability vs group entity's prepaid insurance asset
    - Captive's premium revenue vs group entity's insurance expense
    - The underlying risk transfers within the group cancel out
    - Result: as if the group self-insures (which it does, through the captive)

  edge:org-org → common.ic_insurance = true (flag for elimination)
```

### If group sells extended warranties (IFRS 17 scope)

```
Extended warranty sold separately (not assurance-type):
  → Classified as insurance contract
  → PAA likely applicable (coverage ≤ 12 months typical, or if longer then GMM)
  → Track in BC: deferred warranty revenue (contract liability)
  → Release to P&L over coverage period

  This CAN be handled in BC:
    - Use Subscription Billing for warranty contracts
    - Contract Deferrals handle the deferral/release
    - PAA measurement ≈ unearned premium ≈ deferred revenue
```

---

## Node/Edge Properties

### On node:org (if entity issues insurance contracts)

| Field | Type | x-history | Why required |
|---|---|---|---|
| `issues_insurance_contracts` | boolean | yes | Flags that IFRS 17 applies to this entity |
| `ifrs17_measurement_model` | enum: gmm / paa / vfa | no | Which model is used (may vary by portfolio) |
| `insurance_contract_liability` | decimal | yes | Total IFRS 17 liability (fulfilment CF + CSM). For consolidation. |
| `csm_balance` | decimal | yes | Contractual Service Margin — unearned profit. Shield: is it releasing correctly? |
| `insurance_system_ref` | string | no | Reference to specialist insurance system (not BC) |

### On edge:org-org (IC insurance)

| Field | Type | Why |
|---|---|---|
| `ic_insurance` | boolean | In common section: does captive insure this group entity? → eliminate on consolidation |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | `issues_insurance_contracts` = true → IFRS 17 applies, not IFRS 15. Correct standard used? CSM releasing over coverage? Cohort grouping correct? IC insurance eliminated? | Wrong standard = wrong revenue recognition pattern entirely |
| **Reserve** | Insurance liabilities = claims risk. How much could claims exceed estimates? Reinsurance coverage adequate? | Insurance risk IS the Reserve question — the captive's whole purpose |
| **Sword** | Is captive saving the group money vs external insurance? What risks are worth self-insuring? | Cost optimization: captive vs market insurance |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| IFRS 17 contract classified as IFRS 15 | Wrong measurement model. Revenue recognized differently. Material misstatement. |
| IFRS 15 warranty classified as IFRS 17 | Unnecessary complexity. Over-engineering. But less risky than the reverse. |
| Cohort grouping wrong (mixing >12-month vintages) | ESMA enforcement. Most scrutinized aspect of IFRS 17. |
| CSM not released correctly | Revenue timing wrong. Profit recognized too early or too late. |
| IC insurance not eliminated | Double-counting: captive shows premium revenue, group entity shows insurance expense. Both in consolidated P&L. |
| Captive's specialist system not reconciled to consolidation | Trial balance from insurance system doesn't match what feeds into BC consolidation → reconciliation breaks |

---

## Practical for Most Non-Insurance Groups

```
IF group has NO captive and NO insurance products:
  → IFRS 17 does NOT apply.
  → Only check: are any extended warranties insurance-like?
  → If all warranties are assurance-type (normal defects) → IFRS 15. Done.

IF group has captive insurance:
  → Captive uses specialist system for IFRS 17.
  → Captive feeds trial balance into BC consolidation.
  → IC insurance eliminated.
  → FGGE: flag the captive entity + IC insurance edges.

IF group sells extended warranties meeting IFRS 17:
  → Use PAA (simplified). BC Subscription Billing can handle.
  → Treat like deferred revenue with insurance-specific disclosure.
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — scope test (what's IFRS 17 vs IFRS 15 vs IFRS 9), three models (overview), consolidation interface (captive elimination, IC insurance), xItem mapping (vItem.financial.insurance), practical guidance for non-insurance groups. |
