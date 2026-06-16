# Ergon Chain: IAS 12 — Income Taxes (Deferred Tax)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 12 (complete standard), IFRIC 23 (uncertain tax positions), IAS 12 Pillar Two amendments
**Intent**: Calculate current and deferred tax for the group. Catch ALL temporary differences created by every other chain. The last Phase 3 step — must run AFTER all adjustments are known.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 4 — sequential, needs all Phase 3 complete)
**Nature**: ACCUMULATOR — reads outputs from every other chain and calculates the tax effect

---

## Why Phase 4 (Last Before Completion)

Every other chain creates temporary differences that IAS 12 must capture:

| Source chain | What it creates | Deferred tax consequence |
|---|---|---|
| **IFRS 3** (PPA) | Fair value uplifts on acquired assets | DTL: carrying > tax base (asset worth more in IFRS than for tax) |
| **IFRS 3** (Goodwill) | Goodwill recognized | **NO deferred tax on INITIAL goodwill** (IAS 12.15 exception). But impairment creates DTA. |
| **IAS 36** (Impairment) | Asset written down | DTA: carrying < tax base (tax still allows old value). Recognize only if probable taxable profit. |
| **IAS 21** (FX translation) | FCTR in OCI | Deferred tax on FCTR — recognized in OCI (not P&L). Affects equity → KBR. |
| **IFRS 16** (Leases) | ROU asset + lease liability | Temporary difference: ROU depreciation ≠ lease payment tax deduction. Net may be small. |
| **IFRS 15** (Revenue) | Contract liabilities (deferred revenue) | DTA: taxed when cash received, revenue deferred for IFRS → tax base > carrying of liability. |
| **IC Elimination** | Unrealized profit eliminated | DTA: profit eliminated for IFRS but taxed in selling entity → tax paid on profit that doesn't exist at group level. |
| **IAS 19** (Pensions) | Pension deficit/surplus | DTL on surplus, DTA on deficit. Remeasurements in OCI → deferred tax in OCI. |
| **IAS 37** (Provisions) | Provisions recognized | DTA: provision recognized for IFRS, tax deduction only when paid. |
| **Undistributed profits** | Subsidiary retained earnings | DTL on planned distributions (withholding tax, dividend tax). Exemption if parent controls timing AND no distribution planned. |

**IAS 12 must run AFTER all the above are finalized.** It reads their outputs and calculates the tax layer.

---

## Chain Overview

```
ALL PHASE 3 CHAINS COMPLETE
    │
    ▼
┌──────────────────────────────────────────────┐
│  STEP 1: IDENTIFY TEMPORARY DIFFERENCES      │
│  For every asset/liability on consolidated BS │
│  Compare: carrying amount vs tax base         │
│  IAS 12.5, 15-25                             │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 2: CALCULATE DEFERRED TAX              │
│  Taxable temp diff → DTL                     │
│  Deductible temp diff → DTA (if recoverable) │
│  Tax losses carried forward → DTA (if recov.) │
│  IAS 12.15-45                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 3: EXCEPTIONS + SPECIAL RULES          │
│  No DT on initial goodwill. Undistributed    │
│  profits. Pillar Two exception. IFRIC 23.    │
│  IAS 12.15, 39, 46A, IFRIC 23               │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 4: TAX RATE RECONCILIATION             │
│  Statutory rate → effective rate              │
│  Explain EVERY difference                     │
│  IAS 12.81(c)                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 5: DISCLOSURE + PILLAR TWO             │
│  DTA/DTL by type. Tax losses. Pillar Two     │
│  exposure. Uncertain positions (IFRIC 23).   │
│  IAS 12.79-88                                │
└──────────────────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 1-3 | [deferred-tax-calculation](ergon-ias-12-deferred-tax_v1.0.md) | Each reporting period, AFTER all Phase 3 chains | IND (judgment on DTA recoverability, uncertain positions) + MACH (temp diff identification, calculation) | DTL, DTA, current tax, exceptions applied |
| 4-5 | [deferred-tax-calculation](ergon-ias-12-deferred-tax_v1.0.md) (same ergon, steps 4-5) | Same | MACH (reconciliation) + IND (explain differences, Pillar Two assessment) | Tax rate reconciliation, disclosures |

Single comprehensive ergon — IAS 12 is one big calculation, not a sequence of independent tasks.

---

## Dependencies (reads from ALL other chains)

```
IFRS 3 PPA → fair value uplifts → DTL on each uplift (except goodwill)
IFRS 3 goodwill → NO DT on initial recognition (exception)
IAS 36 impairment → write-down → DTA (if recoverable)
IAS 21 translation → FCTR in OCI → DT on FCTR (in OCI, not P&L)
IFRS 16 leases → ROU ≠ tax deduction → temporary difference
IFRS 15 contract liabilities → deferred revenue → DTA
IC elimination → unrealized profit → DTA
IAS 19 pensions → deficit/surplus → DTA/DTL (remeasurements in OCI → DT in OCI)
IAS 37 provisions → recognized but not yet tax-deductible → DTA
Undistributed profits of subsidiaries → DTL (unless exemption)
Tax losses carried forward → DTA (if probable future taxable profit)
```

---

## Triggers to Other Chains

| To | Trigger | What happens |
|---|---|---|
| ABL KBR | DTA write-off → equity drops. DTL increase → equity drops. | KBR headroom check after tax calculation complete |
| IFRS 8 | Tax by segment (if CODM reviews) | Segment tax disclosure |
| IAS 33 | Tax expense finalized → net income → EPS | EPS calculation needs final tax |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — accumulator pattern (reads all other chains), temporary differences by source, exceptions (goodwill, undistributed, Pillar Two), IFRIC 23 |
