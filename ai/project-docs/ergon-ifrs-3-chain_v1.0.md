# Ergon Chain: IFRS 3 — Business Combinations

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 3 (complete standard)
**Intent**: When control is gained over another entity, account for the acquisition correctly — identify what was bought at fair value, calculate goodwill, track measurement period
**Master chain**: ergon-ifrs-master-chain_v1.0.md (triggered by IFRS 10 control gained)
**Trigger**: IFRS 10 control assessment concludes control_conclusion = true WHERE previously false (new acquisition)

---

## Chain Overview

```
IFRS 10: Control GAINED (new edge or control_conclusion changed to true)
    │
    ▼
┌─────────────────────────────────────────┐
│  STEP 1: BUSINESS vs ASSET ACQUISITION  │
│  Is this a business or just assets?      │
│  IFRS 3.3, B7-B12                        │
│  (Determines entire accounting treatment)│
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │ BUSINESS            │ ASSET ACQUISITION
    │ (IFRS 3 applies)    │ (no goodwill, allocate
    ▼                     │  cost by relative FV)
┌──────────────────────┐  │ → separate simple ergon
│  STEP 2: IDENTIFY    │  │
│  THE ACQUIRER        │  │
│  (usually obvious)   │  │
│  IFRS 3.6-7          │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────┐  │
│  STEP 3: PPA         │  │
│  Fair value ALL      │  │
│  identifiable assets │  │
│  + liabilities       │  │
│  Identify intangibles│  │
│  Measure NCI         │  │
│  IFRS 3.10-31        │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────┐  │
│  STEP 4: GOODWILL    │  │
│  = Consideration     │  │
│  + NCI               │  │
│  - Net identifiable  │  │
│    assets at FV      │  │
│  IFRS 3.32-36        │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────┐  │
│  STEP 5: BOOK IT     │  │
│  Journal entries      │  │
│  Write to BC + graph  │  │
└──────────┬───────────┘  │
           ▼              │
┌──────────────────────────────────────────┐
│  ONGOING: MEASUREMENT PERIOD MONITOR     │
│  12 months to finalize PPA               │
│  After: adjustments through P&L          │
│  IFRS 3.45-50                            │
├──────────────────────────────────────────┤
│  ONGOING: CONTINGENT CONSIDERATION       │
│  Remeasure at fair value each period     │
│  Changes → P&L (if liability)            │
│  IFRS 3.58                               │
└──────────────────────────────────────────┘
           │
           │ triggers downstream chains
           ├──► IAS 36: Goodwill allocated to CGU, annual test
           ├──► IAS 21: Foreign sub → set up FX translation
           ├──► IAS 12: Deferred tax on PPA fair value uplifts
           └──► IAS 24: New related party relationships
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 1 | [business-vs-asset](ergon-ifrs-3-business-vs-asset_v1.0.md) | At acquisition | IND (judgment) | business_or_asset classification on node:org |
| 2-5 | [business-combination](ergon-ifrs-3-business-combination_v1.0.md) | At acquisition | Mixed (IND + external valuers + MACH) | PPA on edge:org-org, goodwill, intangibles, journal entries |
| Ongoing | [measurement-period-monitor](ergon-ifrs-3-measurement-period-monitor_v1.0.md) | Continuous for 12 months | MACH (monitor) + IND (adjustments) | PPA adjustments or finalization |
| Ongoing | [contingent-consideration](ergon-ifrs-3-contingent-consideration_v1.0.md) | Each reporting period | IND (valuation) | Fair value remeasurement → P&L |

---

## Dependencies

```
IFRS 10 (control gained) → Step 1 (business vs asset?)
Step 1 (= business) → Steps 2-5 (full IFRS 3 PPA)
Step 1 (= asset) → Simple cost allocation (no goodwill)
Steps 2-5 complete → Measurement Period Monitor starts (12 months)
Steps 2-5 complete → Contingent Consideration remeasurement starts (each period)
Steps 2-5 complete → IAS 36 chain (goodwill → CGU → annual test)
Steps 2-5 complete → IAS 12 chain (deferred tax on PPA fair value uplifts)
Steps 2-5 complete → IAS 21 chain (if foreign subsidiary)
```

---

## Reverse: Control LOST (Derecognition)

When IFRS 10 concludes control is LOST:

```
1. Derecognize all assets and liabilities of the subsidiary
2. Derecognize goodwill related to the subsidiary
3. Recognize fair value of any retained interest (→ IAS 28 equity method or IFRS 9)
4. Recognize gain or loss in P&L
5. Recycle FCTR from OCI to P&L (IAS 21)
6. Recycle any other OCI items per applicable standards

This is NOT a separate ergon chain — it's the REVERSE of this chain,
triggered by IFRS 10 control assessment concluding control_conclusion = false
where previously true.
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | PPA complete and correct? All intangibles identified (not lumped into goodwill)? Acquisition costs expensed (not capitalized)? Contingent consideration classified correctly (liability vs equity)? Measurement period tracked? fv_meta recorded per IFRS 13? | Under-identification of intangibles = ESMA's #1 IFRS 3 finding. Every dollar in goodwill instead of intangible = future profit overstated (goodwill not amortized). |
| **Reserve** | Goodwill created = Ghost on the balance sheet. Contingent consideration (earn-out) = P&L volatility each period. How much goodwill at risk across all acquisitions? | Goodwill Ghost: doesn't generate cash but hits equity on impairment (IAS 36). Earn-out remeasurement creates unpredictable P&L swings. |
| **Sword** | Did we overpay? Lookback: compare acquisition business case to actual performance. What xItems does the acquired entity sell? Do they strengthen our xItem portfolio? Which xItem types drove the acquisition rationale? | M&A post-acquisition review: did the Tamagos deliver what the Morphon promised? |

## Ghost Dimension

IFRS 3 CREATES Ghosts:
- **Goodwill** = the biggest Ghost. Sits on BS forever (never amortized). Only moves DOWN (impairment, IAS 36). One-way ratchet → equity erodes over impairment cycles. No cash impact.
- **PPA intangibles** = slowly unwinding Ghost. Amortized over useful life → P&L charge → equity gradually decreases. But this IS a real economic effect (value consumed).
- **Contingent consideration** (liability) = volatile Ghost. Remeasured at fair value each period → P&L swings. Not cash until settled.
- **FCTR on foreign acquisition** (IAS 21) = FX Ghost. Goodwill + PPA adjustments treated as assets of the foreign operation → translated at closing rate → FX moves change their SEK value → FCTR → equity → KBR.

All feed into ABL KBR equity monitoring.

## Tamagos Connection

An acquisition IS a hatched Tamagos — at the M&A level:
- **Pre-acquisition**: the deal forming between buyer group and target (or seller). The M&A Tamagos: bField (buyer's strategic need) + sField (target's capabilities/value). Vector Events: due diligence, management meetings, negotiations, board approvals.
- **Hatching**: control obtained (IFRS 10 trigger). The Morphon emerges: legal agreements, share purchase, regulatory approvals. The IFRS 3 PPA = opening the hatched Morphon and identifying what's inside.
- **Post-hatching**: the acquired entity's xItems flow into the group. Its Tamagos pipeline (doc:tamagos) becomes the group's pipeline. Its IC relationships (edge:org-org) activate.

## xItem Connection

The acquired entity sells xItems. IFRS 3 PPA identifies:
- **Customer relationships** (intangible) = the acquired entity's White + BFFB matter. The value of existing relationships with T > 0.
- **Technology** (intangible) = the capability behind vItem.e-svc or the process behind gItem.physical.
- **Brand** (intangible) = market recognition that improves Gray→White conversion (dGray→White/dt).
- **Order backlog** (intangible) = alive Tamagos at advanced Ladder Gates (near-certain hatching).

PPA intangibles MAP to our EconSales model: they're the acquired entity's relationship graph + capability + pipeline, measured at fair value.

## fv_meta

All PPA fair value measurements should carry `fv_meta` (from ergon-ifrs-13-fair-value):
- edge:org-org → ppa.intangibles[] → each with fv_meta (hierarchy level, technique, key inputs, sensitivity)
- edge:org-org → ppa.consideration_contingent → fv_meta
- Level 3 for most PPA intangibles (no market for customer relationships) → full sensitivity disclosure required

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — IFRS 3 chain with 4 ergons |
| 1.1 | 2026-04-02 | Added S-R-S view, Ghost dimension (goodwill, PPA intangibles, contingent consideration, FCTR), Tamagos connection (acquisition = M&A-level Tamagos), xItem connection (PPA intangibles map to EconSales model), fv_meta reference. Aligned with FGGE taxonomy. |
