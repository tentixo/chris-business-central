# Ergon: IFRS 16 — Lease Measurement + Fixed Asset Recording (Steps 3-4)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 16.22-28 (measurement), IFRS 16.29-33 (subsequent)
**Intent**: Calculate ROU asset and lease liability at commencement. Record ROU as Fixed Asset card in BC. Track liability in GL or Bank Account Card.
**Chain**: ergon-ifrs-16-chain_v1.0.md (steps 3-4)
**Depends on**: Lease identified and not exempt (steps 1-2)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | Lease commencement date (when asset available for use — not signing date) |
| **Event** | Lease modification requiring remeasurement |

---

## Step 3: Initial Measurement [MACH + IND for IBR/term]

### Lease Liability (IFRS 16.26-28)

```
Lease liability = present value of lease payments not yet paid at commencement.

Lease payments include:
  a) Fixed payments (less any lease incentives receivable)
  b) Variable payments based on an INDEX or RATE (CPI, STIBOR)
     (Variable payments NOT based on index/rate → expense as incurred, NOT in liability)
  c) Exercise price of PURCHASE OPTION (if reasonably certain to exercise)
  d) Penalties for TERMINATION (if lease term reflects termination)
  e) Residual value guarantees (expected amount payable)

DISCOUNT RATE (the HitL):
  Best: rate IMPLICIT in the lease (if determinable)
  Usually: not determinable → use INCREMENTAL BORROWING RATE (IBR)

  IBR = the rate the lessee would have to pay to borrow
        over similar term, with similar security,
        the funds necessary to obtain an asset of similar value
        in a similar economic environment.

  In practice:
    - Start with entity's actual borrowing rate (if recent loans exist)
    - Adjust for: lease term (longer = higher rate), currency, security
    - IBR may differ per entity in the group (different credit quality, jurisdiction)
    - This is THE major judgment call in IFRS 16

  Record: rate used, source, methodology

Calculate:
  liability = PV(payments, discount_rate, term)
```

### Lease Term (HitL — IFRS 16.18-21)

```
Lease term = non-cancellable period
           + periods covered by EXTENSION option (if reasonably certain to exercise)
           + periods after TERMINATION option (if reasonably certain NOT to exercise)

"Reasonably certain" = judgment. Consider:
  - Economic incentive to extend (significant leasehold improvements → likely extend)
  - Past practice (always renewed office leases → likely extend)
  - Importance to operations (HQ → likely extend. Storage room → maybe not)
  - Cost to relocate (high → likely extend)
  - Remaining useful life of leasehold improvements

ESMA focus: "reasonably certain" for extension options.
  Too aggressive → overstate lease term → overstate asset + liability
  Too conservative → understate → understate
```

### ROU Asset (IFRS 16.23-25)

```
ROU asset at commencement =
  Lease liability (as calculated above)
  + Lease payments made at or before commencement (prepayments)
  + Initial direct costs (incremental costs of obtaining the lease)
  + Estimated costs to dismantle/restore (IAS 37 provision)
  - Lease incentives received

This IS the cost of the "purchased" asset — as if you bought it with a loan.
```

---

## Step 4: Record in BC [MACH]

### ROU Asset → Fixed Asset Card

```
Create Fixed Asset card in BC:

  FA No: auto-generate (or policy-based numbering)
  Description: "ROU — {asset description} — {lessor}"
  FA Class: "Right-of-Use" (separate from owned PP&E — for disclosure)
  FA Subclass: by asset type (Buildings, Vehicles, Equipment, IT)

  Acquisition Cost: = ROU asset amount from Step 3
  Acquisition Date: = lease commencement date
  Depreciation Method: Straight-line
  Depreciation Period: shorter of lease term OR useful life of asset
    (If ownership transfers or purchase option reasonably certain → useful life)
  Salvage Value: typically 0 (lease returns the asset)

  FA Posting Group: determines which GL accounts for:
    - BS: ROU asset (e.g., 1259 Right-of-Use Assets)
    - P&L: Depreciation (e.g., 7835 Depreciation ROU)

BC path: bc.fixed_asset.{fa_no}
```

### Lease Liability → GL or Bank Account Card

```
Option A — GL only:
  Cr: Lease liability account (e.g., 2359 Lease Liabilities, Non-current)
  Split: current portion (next 12 months payments) on 2350 (current liabilities)
  Track: payment schedule manually or via recurring journal

Option B — Bank Account Card (your AST/DBT pattern):
  Create Bank Account Card with type DBT (debt)
  Description: "Lease — {asset description}"
  Track: balance, payments, interest component
  Advantage: uses existing BC infrastructure for loan tracking
  bc.path: bc.bank_account_card.{no}

Either way, track:
  Opening balance = lease liability from Step 3
  Interest accrual each period = opening balance × discount rate / periods
  Payment each period = fixed lease payment
  Liability reduction = payment - interest
  Closing balance = opening - reduction
```

### Journal Entries at Commencement

```
Dr: ROU Asset (Fixed Asset)         = ROU amount
Dr: Prepaid lease (if any)
Cr: Lease Liability                  = PV of payments
Cr: Cash (if initial direct costs or prepayments from cash)
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | All leases identified? ROU correctly measured? IBR defensible? Depreciation running? | IFRS 16 compliance. Understated leases = understated assets + liabilities. |
| **Reserve** | Total lease liability = committed cash outflow. How much of future cash is locked in leases? | Lease commitments affect liquidity. Cash is committed whether business grows or shrinks. Covenant impact. |
| **Sword** | Lease vs buy analysis. Are we leasing things we should own? Overpaying? | Cost optimization. Lease consolidation opportunities. |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Missing leases (especially embedded) | Understated BS. ESMA common finding. |
| Wrong IBR | ROU + liability wrong. Material if rate significantly off. |
| Wrong lease term (extension options) | Same — material impact on BS. ESMA focus. |
| Not splitting current/non-current liability | Classification error → IAS 1 covenant amendment implications |
| IC leases not eliminated | Double-counting in consolidated BS |
| Lease modifications not remeasured | Stale liability carrying amount |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — measurement (PV of payments, IBR, lease term), ROU as Fixed Asset card, liability as GL or Bank Account Card (AST/DBT pattern), S-R-S view |
