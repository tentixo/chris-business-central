# Ergon: IFRS 16 — Ongoing: Depreciation, Interest, Modifications, Reassessment

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 16.29-46 (subsequent measurement), IFRS 16.36-46 (modifications)
**Intent**: Monthly depreciation of ROU asset, interest accrual on liability, handle modifications and lease term reassessment
**Chain**: ergon-ifrs-16-chain_v1.0.md (ongoing)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each month: depreciation + interest |
| **Event** | Lease modification (term change, payment change, scope change) |
| **Event** | Significant event requiring lease term reassessment |
| **Event** | Index/rate update (CPI, STIBOR → variable payment recalculation) |

---

## Monthly: Depreciation + Interest [MACH]

### ROU Asset Depreciation

```
BC Fixed Assets handles this automatically:

  Method: Straight-line (IFRS 16.31 — or other systematic basis if more appropriate)
  Period: shorter of lease term or useful life
    - If ownership transfers or purchase option certain → useful life
    - Otherwise → lease term

  Monthly: Dr Depreciation expense (P&L) / Cr Accumulated depreciation (BS)

  BC: "Calculate Depreciation" batch job includes ROU assets.
  FA Posting Group routes to correct GL accounts (7835 / 1259 accumulated).
```

### Lease Liability: Interest Accrual + Payment

```
Each period:

  1. Interest accrual:
     interest = opening_liability × IBR / 12 (monthly)
     Dr: Interest expense (P&L — financial cost, BAS 8410 or similar)
     Cr: Lease liability (increases the liability)

  2. Lease payment:
     Dr: Lease liability (reduces it)
     Cr: Cash/Bank

  Net effect on liability:
     closing = opening + interest - payment
     (liability reduces over time — like a loan amortization)

  P&L impact:
     Depreciation (operating expense) + Interest (financial expense)
     ≠ old operating lease expense (which was one straight-line number)
     EBITDA IMPROVES under IFRS 16 (no lease expense in EBITDA — it's split into D&A + interest)

  If using Bank Account Card (DBT):
     BC tracks balance, interest, payments automatically.
     bc.path: bc.bank_account_card.{no}
```

---

## Modifications [IND + MACH]

### What's a modification? (IFRS 16.44)

```
A change in scope or consideration NOT part of the original terms.

Examples:
  - Lease term extended (exercised option or new negotiation)
  - Lease term shortened (early termination)
  - Space added (lease additional floor)
  - Space reduced (give back one floor)
  - Payment changed (renegotiated rent)
```

### Two treatments

```
SEPARATE LEASE (IFRS 16.44):
  IF modification INCREASES scope (new asset or extended right)
  AND price increase is commensurate with standalone price for the increase
  → Treat as a NEW, SEPARATE lease.
  → New ROU + new liability for the incremental scope.
  → Existing lease unchanged.

  Example: lease one more floor at market rent → separate lease.

REMEASURE EXISTING LEASE (IFRS 16.45):
  IF modification does NOT qualify as separate lease:
  → Remeasure lease liability with revised payments at REVISED discount rate
  → Adjust ROU asset for the difference
  → If scope decreased: reduce ROU proportionally, recognize gain/loss in P&L
  → If scope unchanged (just payment change): adjust ROU by same amount as liability change

  Example: rent reduced due to renegotiation → remeasure liability at new payments,
           adjust ROU downward.
  Example: lease term extended → remeasure at new term + revised IBR.
```

---

## Reassessment [IND]

### Lease term reassessment (IFRS 16.20-21)

```
Reassess when SIGNIFICANT EVENT or CHANGE IN CIRCUMSTANCES:
  - That is within the lessee's control
  - That affects whether the lessee is reasonably certain to exercise
    an extension option or not exercise a termination option

Examples:
  - Significant leasehold improvements made → now reasonably certain to extend
  - Business restructuring → now reasonably certain to terminate early
  - Change in market conditions alone is NOT sufficient trigger

IF lease term changes:
  → Remeasure liability at revised payments + revised IBR
  → Adjust ROU asset
```

### IBR reassessment

```
New IBR used when:
  - Lease term reassessed (above)
  - Lease modified (remeasurement scenario)
  - Variable payments change due to floating rate change (e.g., STIBOR-linked rent)

New IBR NOT used for:
  - Regular index adjustments (CPI) — these use the ORIGINAL IBR
  - Market interest rate changes alone — original IBR continues
```

### Index/rate updates (IFRS 16.42)

```
For variable payments based on index or rate (e.g., CPI-linked rent):
  When the rate/index changes → recalculate future payments
  → Remeasure liability at ORIGINAL discount rate (not revised IBR)
  → Adjust ROU by same amount
```

---

## Impairment (IAS 36)

```
ROU assets are subject to impairment testing under IAS 36.
  - Test when indicators exist (same as any other asset)
  - Recoverable amount = higher of FVLCD and VIU
  - Impairment loss recognized in P&L

Practical: for individual ROU assets (office, car), impairment
is rare unless the asset becomes clearly unneeded (office vacated,
car sitting unused). More relevant for large/specialized leases.
```

---

## IC Lease Elimination (Consolidation)

```
When one group entity leases FROM another group entity:

  LESSEE (the entity that uses the asset):
    Has: ROU asset + lease liability

  LESSOR (the entity that owns and leases out):
    Has: finance lease receivable OR operating lease income
    (Lessor accounting: IFRS 16.61-97 — lessor classifies as finance or operating)

  ON CONSOLIDATION:
    Eliminate the ROU asset against the lessor's asset/receivable
    Eliminate the lease liability against the lessor's receivable
    Eliminate the depreciation against the lessor's lease income
    Eliminate the interest against the lessor's interest income

  The underlying asset appears at GROUP LEVEL as if owned
  (because within the group, it IS owned — the lease is internal).

  This must be done for EVERY IC lease. Can be many in a large group.
  FGGE: edge:org-org → ic section should flag IC lease relationships.
```

---

## Node/Edge Properties

### On node:org (lessee) — lease summary for governance

| Field | Type | x-history | Why |
|---|---|---|---|
| `lease_count` | integer | yes | Total non-exempt leases |
| `rou_total` | decimal | yes | Total ROU asset carrying amount. Depreciating. |
| `lease_liability_total` | decimal | yes | Total lease liability. Affects leverage + covenants. |
| `lease_liability_current` | decimal | yes | Portion due within 12 months. Current liability classification. |
| `weighted_avg_ibr` | decimal | no | Weighted average IBR across portfolio. Shield: is it defensible? |
| `lease_cash_outflow_annual` | decimal | yes | Total annual lease payments committed. Reserve: cash locked. |

### On edge:org-org — IC lease flag

| Field | Type | Why |
|---|---|---|
| `ic_lease` | boolean | In the common or directed section: does one ORG lease from the other? If yes → eliminate on consolidation. |

### BC references per lease

| BC entity | What | Path |
|---|---|---|
| Fixed Asset card | ROU asset (depreciation, carrying amount) | bc.fixed_asset.{fa_no} |
| Bank Account Card (DBT) | Lease liability (balance, payments, interest) | bc.bank_account_card.{no} |
| GL accounts | ROU asset class, depreciation, interest, liability current/non-current | BAS: 1259/7835/8410/2350/2359 |

---

## Rim Monitoring (Shield)

| Monitor | Threshold | Consequence | Cadence |
|---|---|---|---|
| `lease_count` vs known contracts | Mismatch | Missing leases (embedded in service contracts?) | Quarterly |
| `lease_liability_total` vs covenant limits | Approaching covenant threshold | Debt covenants often include lease liabilities post-IFRS 16 | Monthly |
| `weighted_avg_ibr` | Material change in market rates vs booked IBR | May indicate reassessment needed for modified/new leases | Quarterly |
| IC leases flagged | Any `ic_lease = true` in edge:org-org | Must eliminate on consolidation | Each reporting period |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — depreciation via FA, interest via Bank Account Card (DBT), modifications (separate vs remeasure), reassessment triggers, IC elimination, node:org lease summary |
