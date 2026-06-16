# Ergon Chain: IFRS 8 — Operating Segments

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 8 (complete standard)
**Intent**: Identify, validate, and disclose operating segments. Two levels: Sword discovers clusters continuously, Shield formalizes for IFRS 8 disclosure with stability and comparability.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 5 — parallel with EPS, RPT)
**Data model**: Segments are ctx-v (views) over node:xitem × edge:org-org.sells_to × node:org.buyer

---

## Why Two Levels

```
SWORD (operational — continuous):
  Power BI discovers clusters from xItem × ORG.buyer × edge data
  Clusters shift as R changes (T, dBFFB/dt, margin)
  CODM steers by discovered clusters
  This IS the "internal reports" IFRS 8 asks about

SHIELD (compliance — stable):
  IFRS 8 segments = formalized version of what CODM reviews
  Changed only when CODM formally reorganizes
  Comparatives restated when changed (IFRS 8.29-30)
  Published quarterly/annually

LINK: When Sword discovery reveals current IFRS 8 segments
      no longer match what CODM reviews → trigger formal change.
```

ESMA checks consistency between the two. If CODM's Power BI shows 5 clusters but annual report shows 3 segments → flagged.

---

## Chain Overview

```
┌──────────────────────────────────────────────┐
│  STEP 1: IDENTIFY CODM                       │
│  Who makes resource allocation decisions?     │
│  HitL: CEO? Executive committee? Board?       │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 2: DOCUMENT CODM'S SHAW LENSES        │
│  What Power BI reports does CODM review?     │
│  How sliced? xItem type? Geography? Buyer?    │
│  These slices ARE the operating segments.      │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 3: QUANTITATIVE THRESHOLDS             │
│  ≥10% revenue, profit, or assets?             │
│  75% external revenue covered?                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 4: AGGREGATION CHALLENGE               │
│  If combining: ALL 5 criteria must pass       │
│  xItem type + effector + buyer + topology + Rim│
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 5: RECONCILE + DISCLOSE                │
│  Segment totals → consolidated amounts        │
│  Major customer. Entity-wide. Consistency.     │
└──────────────────────────────────────────────┘
```

---

## Chain Steps

| Step | Ergon | When | Effector | Output |
|---|---|---|---|---|
| 1 | [segment-identification](ergon-ifrs-8-segment-identification_v1.0.md) | Each reporting period (+ when CODM reorganizes) | IND (CODM identification) + MACH (data mapping) | Segment definitions as ctx-v |
| 2 | [segment-validation](ergon-ifrs-8-segment-validation_v1.0.md) | After identification | MACH (thresholds) + IND (aggregation challenge) | Validated reportable segments |
| 3 | [segment-disclosure](ergon-ifrs-8-segment-disclosure_v1.0.md) | After validation | MACH (reconciliation, entity-wide) + IND (consistency check) | IFRS 8 note content |

---

## Triggers

| From | Trigger | What happens |
|---|---|---|
| IFRS 10 scope change | New entity in/out of scope | Segment data changes — rerun thresholds |
| CODM reorganization | Internal reporting structure changed | Formal segment change + restate comparatives |
| Sword discovery | Clusters shifted materially from published segments | Flag inconsistency → CODM decision: reorganize or explain |
| M&A (IFRS 3) | New acquisition | New xItems/ORGs may create new segment or affect existing |
| Disposal (IFRS 5) | Entity leaving group | Segment may shrink below 10% threshold |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — grounded in xItem g/v/h + ORG.buyer + edge data model |
