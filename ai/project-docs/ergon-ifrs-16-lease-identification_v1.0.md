# Ergon: IFRS 16 — Lease Identification + Exemptions (Steps 1-2)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 16.9-11, B9-B31 (identification), IFRS 16.5-8 (exemptions)
**Intent**: Find all leases in every contract. Some are obvious (office lease). Some are hidden inside service contracts (dedicated server, dedicated vehicle in a logistics contract). Apply exemptions.
**Chain**: ergon-ifrs-16-chain_v1.0.md (steps 1-2)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | New contract signed (any contract — not just ones labeled "lease") |
| **Periodic** | Annual sweep of service contracts for embedded leases |
| **Event** | Contract modification (scope change may create/remove a lease) |

---

## Step 1: Does the Contract Contain a Lease? [IND — judgment]

```
IFRS 16.9: A contract IS (or contains) a lease if it conveys the right
to CONTROL THE USE of an identified asset for a period of time
in exchange for consideration.

Three questions:

  1. IS THERE AN IDENTIFIED ASSET? (IFRS 16.B13-B20)
     ├── Explicitly specified (e.g., "Building at Storgatan 5, Floor 3")? → YES
     ├── Implicitly specified (only one asset can fulfill the contract)? → YES
     ├── Supplier has SUBSTANTIVE right to substitute? → NO identified asset
     │   Substantive = supplier can AND benefits from substituting
     │   NOT substantive if: substitution costly, impractical, or customer must agree
     └── A PORTION of an asset can be identified (one floor of a building) → YES

  2. DOES LESSEE CONTROL THE USE? (IFRS 16.B21-B30)
     ├── Right to obtain substantially all ECONOMIC BENEFITS? → YES
     │   (Use, sublease, hold, consume the asset for the period)
     └── Right to DIRECT THE USE? → YES
         ├── Lessee decides HOW and FOR WHAT PURPOSE asset is used? → YES
         ├── Decisions predetermined (vending machine, pipeline) →
         │   Does lessee OPERATE the asset? → YES (lease)
         │   Did lessee DESIGN the asset? → YES (lease)
         │   Neither → NO (service, not lease)
         └── Supplier decides how/purpose → NO (service)

  3. FOR A PERIOD OF TIME?
     → Must be more than just a single use / spot transaction
```

### Common hidden leases

| Contract type | Obvious? | Lease inside? |
|---|---|---|
| Office rental agreement | YES | The office space |
| Car fleet agreement | YES | Each vehicle |
| Copier/printer contract | Maybe | If specific machines assigned and you control use |
| Dedicated server hosting | Maybe | If specific servers identified (not shared cloud) |
| Logistics contract with dedicated trucks | Maybe | If specific trucks assigned to your routes |
| Cloud computing (AWS, Azure) | Usually NO | Shared infrastructure, no identified asset. Service, not lease. |
| Warehouse space | YES if specific area | The warehouse or specific zone |
| Equipment maintenance with replacement unit | Maybe | If replacement unit is yours during service |

**ESMA focus**: Incomplete lease identification — companies miss embedded leases in service contracts.

---

## Step 2: Apply Exemptions [MACH + IND]

```
IFRS 16.5-8: Two exemptions (ELECTION, not mandatory):

  a) SHORT-TERM LEASE (IFRS 16.5(a)):
     Lease term ≤ 12 months (including extension options reasonably certain to exercise)
     AND: no purchase option
     → ELECT to expense on straight-line basis (or other systematic basis)
     → No ROU asset, no lease liability
     → Election made BY CLASS of underlying asset (e.g., all short-term car leases)

  b) LOW-VALUE ASSET (IFRS 16.5(b)):
     Underlying asset has LOW VALUE when NEW (not just low remaining value)
     → IASB guidance: approximately USD 5,000 or less when new
     → Examples: tablets, laptops, small office furniture, phones
     → NOT: cars (too expensive new), NOT: aggregated items (each assessed individually)
     → Election made LEASE BY LEASE (not by class)
     → Expense on straight-line or other systematic basis

  IF exempt:
    → Don't capitalize. Expense the payments.
    → STILL disclose: total expense for short-term leases + total for low-value leases (IFRS 16.55)

  IF NOT exempt:
    → Proceed to Step 3 (measurement)
```

---

## Output

| Target | What |
|---|---|
| Lease register | List of ALL identified leases: asset description, lessor, term, exempt (yes/no + reason) |
| BC | Non-exempt leases → proceed to FA card creation. Exempt → expense coding in GL. |
| `node:org → lease_summary` | Count of leases, total ROU, total liability (summary for governance) |
| `node:anomaly` | "Potential embedded lease in service contract {X} — HitL review needed" |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Missing an embedded lease | Understated assets AND liabilities. Balance sheet wrong. ESMA finding. |
| Applying exemption incorrectly (e.g., calling a 3-year lease "short-term") | Understated assets/liabilities. Auditor qualification. |
| Not reassessing when service contract changes | New identified asset may have appeared → lease not captured |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — identified asset test, control test, hidden leases in service contracts, exemptions |
