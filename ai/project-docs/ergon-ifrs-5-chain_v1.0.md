# Ergon Chain: IFRS 5 — Non-current Assets Held for Sale and Discontinued Operations

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 5 (complete standard)
**Intent**: When the group decides to sell a subsidiary or major business line, classify correctly, change measurement, change presentation, monitor until completion or abandonment
**Master chain**: ergon-ifrs-master-chain_v1.0.md

---

## Chain Overview

```
BOARD DECISION: "We will sell subsidiary X"
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 1: CLASSIFICATION ASSESSMENT      │
│  Does it meet held-for-sale criteria?    │
│  IFRS 5.6-8                             │
│  HitL: "highly probable" is judgment     │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │ YES (criteria met)  │ NO (criteria not met)
    ▼                     │ → No reclassification
┌──────────────────────┐  │   Monitor for when criteria ARE met
│  STEP 2: RECLASSIFY  │  │
│  + INITIAL MEASURE    │  │
│  Stop depreciation    │  │
│  Measure at lower of  │  │
│  CA or FVLCD          │  │
│  IFRS 5.15-18         │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────┐  │
│  STEP 3: PRESENT     │  │
│  Discontinued op?    │  │
│  → Single line P&L    │  │
│  → Separate BS        │  │
│  IFRS 5.30-36        │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────────────────────────┐
│  ONGOING: MONITOR                        │
│  Each period:                            │
│  - Still highly probable?                │
│  - Still within 12 months?               │
│  - Remeasure FVLCD                       │
│  - Impairment or reversal?               │
│  IFRS 5.9-12, 15                         │
└──────────────┬───────────────────────────┘
               │
    ┌──────────┴──────────┐
    │ SALE COMPLETES      │ SALE ABANDONED
    ▼                     ▼
┌──────────────────┐  ┌─────────────────────────┐
│ DERECOGNITION    │  │ REVERSE CLASSIFICATION   │
│ (master chain    │  │ Resume depreciation      │
│  IFRS 3 reverse) │  │ Remeasure: lower of      │
│ Gain/loss → P&L  │  │  adjusted CA or          │
│ Recycle FCTR     │  │  recoverable amount      │
│ Remove from scope│  │ IFRS 5.26-29             │
└──────────────────┘  └─────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 1 | [classification](ergon-ifrs-5-classification_v1.0.md) | When disposal plan exists | IND (judgment on "highly probable") | classified = true/false on node:org |
| 2-3 | [classification](ergon-ifrs-5-classification_v1.0.md) (same ergon) | Immediately after classification | MACH + IND | Measurement change, presentation change |
| Ongoing | [monitor](ergon-ifrs-5-monitor_v1.0.md) | Each reporting period while classified | MACH + IND | Remeasurement, 12-month check, impairment/reversal |
| Completion | Master chain → IFRS 3 reverse | When sale completes | Mixed | Derecognition, gain/loss |
| Abandonment | [monitor](ergon-ifrs-5-monitor_v1.0.md) (triggers reversal) | When plan abandoned | IND | Reverse classification, resume depreciation |

---

## Triggers from Other Chains

| From | Trigger | What happens |
|---|---|---|
| Board decision / management plan | Disposal plan created | IFRS 5 classification assessment starts |
| IFRS 10 scope determination | Entity flagged `held_for_sale` | Consolidation treatment changes |
| IAS 36 impairment | Impairment on held-for-sale asset | FVLCD already lower — additional write-down |

## Triggers to Other Chains

| To | Trigger | What happens |
|---|---|---|
| IFRS 10 | Classification as held for sale | Scope unchanged BUT presentation changes |
| IFRS 3 reverse (master chain) | Sale completed | Full derecognition |
| IAS 21 | Foreign sub disposed | FCTR recycled from OCI to P&L |
| IAS 12 | Measurement changes | Deferred tax recalculation on new carrying amounts |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Correctly classified? Criteria genuinely met (not just to stop depreciation)? 12-month deadline tracked? FVLCD remeasured each period? Discontinued operation presented separately on P&L? Comparatives restated? | Classification abuse: stop depreciation → assets overstated. ESMA checks premature classification. |
| **Reserve** | Expected disposal proceeds → cash inflow timing. Post-disposal group: is the remaining group viable? Does disposal reduce reserve needs (less risk) or increase them (lost diversification)? | Disposal = cash event. Reserve must model: what does the group look like AFTER the sale? KBR impact of gain/loss on disposal. |
| **Sword** | WHY are we selling? Is this an underperforming segment (discovered via IFRS 8 Shaw Lens)? What xItems does this entity sell — are we exiting a xItem category? Does the disposal align with Flywheel direction or is it a doom-loop lurch? | Strategic: disposal should serve Intent, not be reactive. Collins: consistent Flywheel push, not panic selling. |

## Ghost Dimension

IFRS 5 changes the Ghost landscape:
- **Depreciation stops** at classification → the depreciation Ghost (gradual equity reduction) PAUSES. Equity stops declining from this source. But FVLCD measurement may create a DIFFERENT equity hit (impairment to FVLCD if lower than carrying).
- **On disposal completion**: FCTR Ghost RECYCLES — the entire accumulated FCTR for a foreign sub goes from OCI to P&L in ONE hit. This can be massive (years of FX accumulation → single period P&L). Goodwill Ghost also derecognized. Pension Ghost (IAS 19) if entity had DB plans → plan may transfer or settle.
- **Abandonment reversal**: if plan abandoned → depreciation RESUMES → catch-up depreciation charge → equity drops → KBR impact.

## Tamagos Connection

Disposal is a **reverse-Tamagos** from the seller's perspective:
- The GROUP is the seller. The Tamagos sits between the group and potential BUYERS of the subsidiary.
- Ladder Gate progression: marketing the entity (awareness → interest → proposal → negotiation → IFRS event = sale completion)
- T between group and buyers is measured during the process (active engagement, competitive bids, etc.)
- **Annihilation** = disposal abandoned. The sell-side Tamagos dies. Entity stays in the group.
- **Hatching** = sale completes. The buyer's Tamagos hatches. For the buyer: IFRS 3 PPA. For the seller: IFRS 5 → IFRS 3 reverse (derecognition).

The edge:org-org → disposal section tracks this sell-side Tamagos lifecycle (status: planned → marketed → under_negotiation → conditionally_agreed → completed/abandoned).

## xItem Connection

The entity being sold sells xItems. IFRS 5 classification affects:
- **Discontinued operation test** (IFRS 5.32): does this entity represent a "separate major line of business"? This maps to: does it sell a DISTINCT xItem category (e.g., all gItem.physical vs the group's vItem.e-svc)? If it sells the same xItems as other entities → probably NOT a discontinued operation. If it's the ONLY entity selling a particular xItem type → probably IS.
- **Segment impact** (IFRS 8): disposal may remove an entire discovered segment. The CODM's Shaw Lens changes — the segment disappears. Comparative data must show the discontinued segment separately.
- **IC elimination impact**: disposal removes IC trading relationships (edge:org-org with sells_to → no longer eliminated post-disposal).

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — IFRS 5 chain with 2 ergons |
| 1.1 | 2026-04-02 | Added S-R-S view, Ghost dimension (depreciation pause, FCTR recycling on disposal, abandonment catch-up), Tamagos connection (disposal = reverse-Tamagos, sell-side lifecycle on edge:org-org.disposal), xItem connection (discontinued operation test maps to xItem category distinctness). Aligned with FGGE taxonomy. |
