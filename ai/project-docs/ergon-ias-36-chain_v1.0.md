# Ergon Chain: IAS 36 — Impairment of Assets

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 36 (complete standard)
**Intent**: Ensure assets are not carried above their recoverable amount. Test goodwill annually. Detect impairment indicators. The Ghost that silently eats KBR.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — parallel with IAS 21, IC elimination, IFRS 16)
**Uses**: IFRS 13 service ergon (for FVLCD measurement)

---

## Two Regimes

| Regime | Assets | When to test | Frequency |
|---|---|---|---|
| **Mandatory annual** | Goodwill (IFRS 3), indefinite-life intangibles (IAS 38) | At the same time each year + when indicators | Annual minimum + trigger |
| **Indicator-triggered** | PP&E, finite-life intangibles, ROU assets (IFRS 16), investments in associates (IAS 28) | Only when indicators of impairment exist | Check indicators at each reporting date |

---

## Chain Overview

```
┌──────────────────────────────────────────────┐
│  STEP 0: CGU IDENTIFICATION + GOODWILL       │
│  ALLOCATION (set up, maintained)              │
│  What are the CGUs? Where does goodwill sit?  │
│  IAS 36.65-73, 80-87                         │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 1: INDICATOR ASSESSMENT                │
│  External + internal indicators checked       │
│  Each reporting date                          │
│  IAS 36.12-14                                │
└──────────────┬───────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │ INDICATORS FOUND    │ NO INDICATORS
    │ (or annual test due)│ (and no annual test due)
    ▼                     │ → Done for this period
┌──────────────────────┐  │
│  STEP 2: DETERMINE   │  │
│  RECOVERABLE AMOUNT  │  │
│  Higher of FVLCD     │  │
│  and VIU             │  │
│  IAS 36.18-57        │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────┐  │
│  STEP 3: COMPARE     │  │
│  Carrying > Recoverable? │
│  YES → impairment loss│  │
│  NO → no impairment   │  │
│  IAS 36.59-64        │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────┐  │
│  STEP 4: ALLOCATE    │  │
│  IMPAIRMENT LOSS     │  │
│  First to goodwill    │  │
│  Then pro rata others │  │
│  IAS 36.104-105      │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────────────────────────────┐
│  ONGOING: REVERSAL CHECK                     │
│  Indicators that impairment decreased?        │
│  Reverse for other assets (NOT goodwill)      │
│  IAS 36.109-125                              │
└──────────────────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 0 | [cgu-allocation](ergon-ias-36-cgu-allocation_v1.0.md) | At acquisition + when structure changes | IND (judgment on CGU boundaries) + MACH (allocation math) | node:org → cgu populated |
| 1 | [indicator-assessment](ergon-ias-36-indicator-assessment_v1.0.md) | Each reporting date | MACH (external data) + IND (internal assessment) | Test triggered or not |
| 2-4 | [impairment-test](ergon-ias-36-impairment-test_v1.0.md) | When indicators found or annual test due | IND (projections, discount rate) + MACH (DCF calculation) + external valuers (FVLCD) | Impairment loss or headroom confirmed |

---

## Dependencies

```
IFRS 3 → Goodwill created → must be allocated to CGU(s) (step 0)
IFRS 10 → Consolidation scope → which entities/CGUs to test
IAS 21 → Foreign sub goodwill translated at closing rate → FX affects carrying amount
IFRS 13 → FVLCD measurement (service ergon invoked for fair value)
IFRS 5 → Held-for-sale entities → measured at FVLCD under IFRS 5, not IAS 36
IFRS 16 → ROU assets subject to IAS 36 impairment
IAS 12 → Deferred tax on impairment losses (reversal creates deferred tax asset question)
ABL KBR → Impairment reduces equity → headroom shrinks → personal liability approaches
```

---

## Triggers to Other Chains

| To | Trigger | What happens |
|---|---|---|
| ABL KBR | Goodwill impairment → equity drops | KBR headroom check: did we cross 50%? |
| IAS 12 | Impairment loss recognized | Deferred tax impact: loss creates temporary difference |
| IFRS 8 | Impairment in a segment | Segment profit affected, may change segment economics |
| IAS 1 | Material impairment | Separate disclosure on face of P&L or in notes |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — two regimes, CGU allocation, indicator assessment, impairment test, reversal, Ghost/KBR connection |
