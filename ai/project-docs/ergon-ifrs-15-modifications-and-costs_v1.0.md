# Ergon: IFRS 15 — Contract Modifications + Contract Cost Assets (Ongoing)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 15.18-21 (modifications), IFRS 15.91-104 (contract costs)
**Intent**: Handle changes to existing contracts (scope, price) and capitalize costs to obtain/fulfill contracts when recoverable
**Chain**: ergon-ifrs-15-chain_v1.0.md (ongoing)

---

## Contract Modifications [IND — HitL]

### When modifications occur

```
A modification = change in scope and/or price of an existing contract
approved by both parties.

Examples:
  - Customer adds more xItems to the deal (scope increase)
  - Customer removes xItems (scope decrease)
  - Price renegotiated (discount, escalation)
  - T&M engagement extended beyond original estimate
  - SaaS customer upgrades tier (changes TC in V-P-C-T-TC)
```

### Three treatments (this IS the HitL judgment)

```
IFRS 15.20-21:

TREATMENT 1: SEPARATE CONTRACT
  IF: added goods/services are DISTINCT
  AND: price increase reflects SSP of the additional goods/services
  → Treat as a brand new, separate contract.
  → Existing contract unaffected.
  → The simplest outcome.

  Example: SaaS customer at EUR 1,000/month adds a new module
           priced at EUR 300/month (its standalone price).
           → New contract for the module. Original continues unchanged.

TREATMENT 2: PROSPECTIVE (terminate old + create new)
  IF: added goods/services are DISTINCT
  BUT: price does NOT reflect SSP (e.g., customer gets discount on addition)
  → Terminate old contract.
  → Create new contract combining:
     remaining POs from old + new POs from modification
     at reallocated transaction price.
  → Recognize prospectively from modification date.

  Example: Customer on a 3-year Fixed Price consulting project
           adds new workstream (distinct) at discounted rate.
           → Combine remaining original work + new workstream.
           → Reallocate total remaining price by relative SSP.
           → Recognize from modification date forward.

TREATMENT 3: CUMULATIVE CATCH-UP
  IF: added goods/services are NOT DISTINCT
  (modification is essentially part of the original PO)
  → Update the transaction price and measure of progress.
  → Cumulative catch-up: adjust revenue recognized to date
     as if the modified terms had existed from the start.
  → Recognize adjustment in period of modification.

  Example: Fixed Price implementation project where customer adds
           scope that is deeply interrelated with original scope
           (not distinct — same integrated output).
           → Recalculate % complete with new total scope.
           → Adjust cumulative revenue in this period.

Decision tree:
  Is the new scope DISTINCT?
  ├── YES → Is the new price at SSP?
  │         ├── YES → Treatment 1 (separate contract)
  │         └── NO  → Treatment 2 (prospective)
  └── NO  → Treatment 3 (cumulative catch-up)

Record:
  edge:org-org → sells_to.contract_modification[]:
    date, scope_change, price_change,
    treatment: separate_contract / prospective / cumulative_catchup,
    rationale (HitL documented)
```

---

## Contract Cost Assets [IND + MACH]

### Costs to obtain a contract (IFRS 15.91-94)

```
Incremental costs of obtaining a contract:
  Costs that would NOT have been incurred if contract not obtained.
  → Sales commissions paid specifically for winning THIS deal.

Capitalize as asset IF:
  Entity expects to recover the costs through contract performance.

Amortize:
  Over the period of benefit — usually the contract term.
  IF commission paid on renewal AND renewal commission NOT commensurate
  with initial → amortize over expected customer relationship (longer than contract).

Practical expedient (IFRS 15.94):
  IF amortization period ≤ 12 months → expense immediately.
  Most small deal commissions: expense as incurred.

Record:
  node:org → contract_cost_assets (x-history tracked)
  BC: prepaid expense or deferred commission asset, amortized monthly
```

### Costs to fulfill a contract (IFRS 15.95-98)

```
Costs directly related to a contract that:
  a) Relate directly to a specific contract (or anticipated contract)
  b) Generate or enhance resources used to satisfy POs
  c) Expected to be recovered

Examples:
  - Setup costs for a SaaS customer (one-time, recovered over subscription)
  - Direct labor costs for a project not yet started
  - Materials allocated to a specific contract

NOT capitalized:
  - General and administrative costs (not directly related)
  - Wasted materials, labor (abnormal waste)
  - Costs relating to satisfied POs (past performance)
  - Costs that can't be distinguished between satisfied and unsatisfied POs

This is the "can you Vector to xtValue?" test:
  Will these costs reach xtValue (be recovered through the contract)?
  IF yes → capitalize. IF no → expense immediately.

Amortize:
  On same basis as revenue recognition for the PO these costs relate to.
  (Point-in-time → expense at delivery. Over-time → amortize over service period.)

Impairment:
  Each period: is carrying amount > remaining consideration expected
  minus remaining costs? If yes → impair. (Onerous contract territory — IAS 37.)
```

---

## Output

| Target | What |
|---|---|
| `edge:org-org → sells_to.contract_modification[]` | Each modification with treatment and rationale |
| `xPackage.performance_obligations[]` | Updated POs after modification (new POs, revised allocation, adjusted progress) |
| `node:org → contract_cost_assets` | Capitalized obtainment/fulfillment costs |
| BC GL | Commission asset, setup cost asset, amortization entries |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong modification treatment | Revenue shifted between periods. Cumulative catch-up in wrong period. |
| Modification not identified (verbal scope change not documented) | POs not updated → revenue recognized on wrong base |
| Commission costs expensed when should be capitalized | Understated assets, overstated expenses in current period |
| Fulfillment costs capitalized when contract is onerous | Asset that won't be recovered → should be expensed + onerous contract provision (IAS 37) |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — three modification treatments (decision tree), contract cost assets (obtain + fulfill), practical expedients, Vector-to-xtValue test for capitalization. |
