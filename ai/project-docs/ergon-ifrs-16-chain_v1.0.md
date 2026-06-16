# Ergon Chain: IFRS 16 — Leases

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 16 (complete standard)
**Intent**: Identify all leases, recognize ROU assets + lease liabilities on balance sheet, depreciate, handle modifications. Track in Fixed Assets register.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — parallel with IAS 21, IC elimination, IAS 36)
**NOT xItem**: Leases are Agency infrastructure (what you USE), not what you SELL. Lives on node:org, not node:xitem.

---

## Why Leases Are Not xItems

| | xItem | Lease |
|---|---|---|
| What | What you SELL to create xtValue for buyer | What you USE in your Agency to PRODUCE xItems |
| S-R-S | Sword (offering, revenue) | Shield (cost, asset/liability) + Reserve (cash commitment) |
| Node | node:xitem | node:org (the lessee) → tracked in Fixed Assets register |
| Example | SaaS subscription (vItem.e-svc) | Office where developers work, cars consultants drive |

A lease is EFFECTOR infrastructure. The office enables hItem.consulting. The servers enable vItem.e-svc. The cars enable hItem.labor (field service). They're cost, not revenue.

---

## Chain Overview

```
┌─────────────────────────────────────────┐
│  STEP 1: IDENTIFY LEASES                │
│  Is there an identified asset?           │
│  Does lessee control use?                │
│  IFRS 16.9-11, B9-B31                   │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 2: EXEMPTIONS                     │
│  Short-term (≤12 months)?               │
│  Low-value (<~$5,000 new)?              │
│  → If exempt: expense, don't capitalize  │
│  IFRS 16.5-8                            │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 3: MEASURE                        │
│  ROU asset = PV of lease payments        │
│  Lease liability = same PV               │
│  Discount at IBR (or implicit rate)      │
│  IFRS 16.23-28                          │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│  STEP 4: RECORD IN FIXED ASSETS         │
│  ROU asset → FA card (depreciate)        │
│  Lease liability → GL (or Bank Account)  │
│  IFRS 16.29-33                          │
└──────────────┬──────────────────────────┘
               ▼
┌──────────────────────────────────────────┐
│  ONGOING: DEPRECIATE + UNWIND            │
│  ROU asset: straight-line over lease term │
│  Liability: interest accrual + payments   │
│  ONGOING: MODIFICATIONS                  │
│  Scope/term/consideration changes         │
│  ONGOING: IMPAIRMENT (IAS 36)            │
│  ONGOING: REASSESS lease term + IBR       │
└──────────────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 1-2 | [lease-identification](ergon-ifrs-16-lease-identification_v1.0.md) | At contract inception + when new contracts entered | IND (is it a lease?) + MACH (exemption check) | Lease register: what's a lease, what's exempt |
| 3-4 | [lease-measurement](ergon-ifrs-16-lease-measurement_v1.0.md) | At commencement + on modification | MACH (PV calculation) + IND (IBR, lease term judgment) | ROU asset + liability on BS, FA card created |
| Ongoing | [lease-ongoing](ergon-ifrs-16-lease-ongoing_v1.0.md) | Each period | MACH (depreciation, interest) + IND (modifications, reassessment) | P&L: depreciation + interest. BS: updated asset + liability. |

---

## Connection to Consolidation

| Issue | What happens |
|---|---|
| **IC leases** (one group entity leases from another) | ELIMINATE on consolidation. The ROU asset in the lessee and the lease receivable in the lessor cancel out. |
| **ROU assets of foreign subsidiaries** | Translated at closing rate (IAS 21) like any other asset. FX movement → FCTR. |
| **Lease liabilities affect leverage ratios** | Covenant compliance: do debt covenants include lease liabilities? Post-IFRS 16, most do. Reserve monitors. |
| **ROU depreciation + interest ≠ old lease expense** | P&L pattern changes: front-loaded (interest higher early) vs. straight-line (old operating lease). EBITDA improves (lease payments no longer in operating expenses — split into depreciation + interest). |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — leases as Agency infrastructure (not xItem), FA register, ROU + liability, IC elimination, covenant impact |
