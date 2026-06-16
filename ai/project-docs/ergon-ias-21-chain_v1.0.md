# Ergon Chain: IAS 21 — Effects of Changes in Foreign Exchange Rates

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 21 (complete standard), IAS 29 (hyperinflationary economies)
**Intent**: Determine functional currency per entity, translate foreign subsidiaries for consolidation, handle FX gains/losses, manage the FCTR Ghost
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — parallel with IC elimination, IAS 36, IAS 19)
**Trigger**: IFRS 10 scope includes foreign subsidiaries (functional currency ≠ presentation currency)

---

## Chain Overview

```
┌──────────────────────────────────────────────────┐
│  STEP 0: FX RATE POLICY (set once, apply always) │
│  Each entity uses home central bank as reference  │
│  Consolidation uses parent's reference source     │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  STEP 1: FUNCTIONAL CURRENCY DETERMINATION       │
│  Per entity. Factual, not a choice.              │
│  IAS 21.9-14                                     │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  STEP 2: TRANSACTION RECORDING                   │
│  Foreign currency transactions → functional at    │
│  reference rate on transaction date               │
│  IAS 21.21-22                                    │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  STEP 3: MONTH-END REVALUATION                   │
│  Monetary items at closing reference rate         │
│  FX gain/loss → P&L                              │
│  IAS 21.23-28                                    │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  STEP 4: CONSOLIDATION TRANSLATION               │
│  BS at closing rate, P&L at average/daily rate    │
│  Difference → FCTR in OCI (the Ghost)            │
│  IAS 21.39-43                                    │
└──────────────┬───────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────┐
│  ONGOING: MONITORS                               │
│  Reference rate divergence (Entropy Patrol)       │
│  Hyperinflation detection (IAS 29)               │
│  FCTR headroom for KBR impact                    │
│  Functional currency reassessment triggers       │
└──────────────────────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 0 | [fx-rate-policy](ergon-ias-21-fx-rate-policy_v1.0.md) | Set once, maintained | IND (policy decision) + MACH (rate feeds) | Rate source per entity, rate table in BC |
| 1 | [functional-currency](ergon-ias-21-functional-currency_v1.0.md) | At entity creation + reassess on trigger | IND (factual determination) | node:org → functional_currency |
| 2-3 | BC standard functionality | Each transaction + month-end | MACH (BC) | Booked at reference rate, revalued at closing |
| 4 | [consolidation-translation](ergon-ias-21-consolidation-translation_v1.0.md) | Each reporting period | MACH (BC consolidation) | Translated financials, FCTR in OCI |
| Ongoing | [fx-monitors](ergon-ias-21-fx-monitors_v1.0.md) | Continuous + monthly | MACH (Walker) | Anomalies: divergence, hyperinflation, FCTR impact |

---

## Dependencies

```
IFRS 10 scope → determines WHICH entities need translation (foreign functional currency)
IAS 21 Step 1 → functional currency must be determined before any translation
IFRS 3 → goodwill + PPA from foreign acquisition = assets of foreign op → closing rate
IAS 21 Step 4 → produces FCTR → Ghost that affects equity → KBR (ABL chain)
IFRS 5 / IFRS 3 reverse → disposal of foreign sub = FCTR recycled from OCI to P&L
```

---

## Triggers to Other Chains

| To | Trigger | What happens |
|---|---|---|
| IAS 12 (Deferred Tax) | FX translation creates temporary differences | Deferred tax on FCTR and translation adjustments |
| ABL KBR | FCTR movement affects equity | Large FX move → equity drops → KBR headroom shrinks |
| IFRS 3 reverse (disposal) | Foreign sub disposed | ENTIRE accumulated FCTR recycled to P&L — can be massive |
| IAS 36 (Impairment) | Goodwill translated at closing rate | FX weakening → goodwill in presentation currency drops → may trigger impairment |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — rate policy (home central bank per entity), functional currency, translation, FCTR Ghost, monitors |
