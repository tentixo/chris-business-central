# Ergon: IFRS 8 — Segment Identification

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 8.5-10, 12
**Intent**: Identify CODM, document what they review, map to segment definitions grounded in xItem × ORG.buyer × edge data
**Chain**: ergon-ifrs-8-chain_v1.0.md (step 1)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting period (confirm segments still match CODM view) |
| **Event** | CODM reorganizes internal reporting. New Shaw Lenses in Power BI. M&A changes business structure. |

---

## Input

| Source | What |
|---|---|
| Management structure | Who is the CODM? Organizational chart. |
| Power BI reports / management packs | What the CODM actually reviews. Which slices. Which metrics. |
| `node:xitem` | xItem taxonomy (g/v/h, sub-types) |
| `edge:org-org` → sells_to | Revenue per xItem per direction, volumes |
| `node:org.buyer` | Buyer properties: jurisdiction, type, size |
| Prior period segments | What was reported last time |

---

## Sub-Ergons

### Step 1: Identify the CODM [IND — HitL]

```
IFRS 8.7: The CODM is a FUNCTION, not necessarily a person.

Who allocates resources to operating segments?
Who assesses segment performance?

Common patterns:
  Simple company: CEO = CODM
  Matrix organization: Executive committee collectively = CODM
  Holding company: Board or investment committee = CODM

Document:
  Who (name/role/committee)
  Evidence: meeting minutes showing resource allocation decisions

NOTE: Getting CODM wrong changes everything downstream.
  If CEO reviews by geography but executive committee reviews by product line
  → which is the CODM? The one who ALLOCATES RESOURCES.
```

### Step 2: Document CODM's Shaw Lenses [IND + MACH]

```
IFRS 8.5-6: Segments based on internal reports regularly reviewed by CODM.

Gather:
  a) What Power BI dashboards does the CODM use?
  b) What management packs are prepared for CODM meetings?
  c) How are they sliced?

Map each CODM report to our data model:

  Sliced by xItem type?
    → Segment per xItem.sub_type (e.g., "SaaS products", "Consulting", "Hardware")

  Sliced by geography?
    → Segment per ORG.buyer.jurisdiction cluster (e.g., "Nordics", "DACH", "UK")

  Sliced by buyer type?
    → Segment per ORG.buyer.type (e.g., "Enterprise", "SMB", "Public Sector")

  Sliced by business unit / ORG.seller?
    → Segment per ORG.seller (legal entity or group of entities)

  Mixed?
    → Matrix segments (xItem × geography, etc.)

Each slice = a ctx-v (view/filter) over the data model:

  ctx-v "segment-nordics-saas":
    filter: ORG.buyer.jurisdiction IN (SE, NO, DK, FI)
            AND xItem.sub_type = "vItem.e-svc"
    metrics: revenue (from edge.sells_to), cost (from xItem.cost), margin (derived)
```

### Step 3: Validate against prior period [MACH + IND]

```
Compare identified segments to prior period:

IF same segments → confirm, proceed to validation ergon.

IF different segments:
  WHY changed?

  a) CODM genuinely reorganized (new Power BI structure, new management approach)
     → Valid change. Restate comparatives (IFRS 8.29).
     → Document: what changed, why, when.

  b) Business structure changed (M&A, disposal, new xItem types)
     → Valid change if CODM now reviews differently as a result.
     → Document: which event triggered the change.

  c) No genuine change — cosmetic reclassification
     → NOT valid. Auditor will challenge.
     → Anomaly: "Segment change without genuine CODM reorganization"

IF changed → restate comparatives. IFRS 8.29-30:
  Prior period segment data recalculated under new structure.
  Unless: information not available AND cost to develop excessive (rare defense).
```

### Step 4: Test aggregation criteria [IND — HitL]

```
IFRS 8.12: May aggregate segments with SIMILAR ECONOMIC CHARACTERISTICS
if they are similar in ALL of:

Using our data model:

1. Nature of products/services
   → xItem.type (g/v/h) + xItem.sub_type
   Same? gItem.physical in both → YES. gItem vs hItem → NO.

2. Nature of production processes
   → xItem.effector_mix (machine % + person % + infrastructure %)
   Similar composition? Both 70% person → YES. 80% machine vs 80% person → NO.

3. Type or class of customer
   → ORG.buyer.type + ORG.buyer.size
   Same buyer profile? Both enterprise > 1000 employees → YES. Enterprise vs SMB → NO.

4. Methods of distribution
   → Value chain topology: edge hops (direct / partner / online)
   Same path to xtValue? Both direct → YES. Direct vs multi-hop partner → NO.

5. Nature of regulatory environment
   → xItem.ifrs_standard + xItem.vat_class + industry-specific regulation
   Same Rim? Both IFRS 15 + 25% VAT → YES. IFRS 15 vs IFRS 9 → NO.

ALL FIVE must pass. Any failure → cannot aggregate → separate segments.

The on-premises vs SaaS test (from our earlier Walk):
  1. Nature: both vItem.e-svc → PASS
  2. Process: on-prem = person-heavy (install), SaaS = infra-heavy → FAIL
  3. Customer: often different profiles → likely FAIL
  4. Distribution: on-prem = partner/direct install, SaaS = direct/online → FAIL
  5. Regulatory: both IFRS 15 → PASS

  2 PASS, 3 FAIL → CANNOT aggregate. Separate segments. Hiding underperformance blocked.
```

---

## Output

| Target | What |
|---|---|
| Segment definitions (ctx-v per segment) | Filter criteria grounded in xItem × ORG.buyer × edge |
| CODM documentation | Who, what they review, evidence |
| Aggregation assessment | Per combination: all 5 criteria documented (pass/fail with data model references) |
| Anomaly (if applicable) | "Segments changed without genuine reorganization" or "Aggregation criteria not met but segments combined" |
| Comparative restatement flag | If segments changed: trigger restatement of prior period |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong CODM identified | Entire segment structure wrong. ESMA enforcement. |
| Segments don't match internal reports | ESMA's most common IFRS 8 finding. Inconsistency = credibility loss. |
| Aggregation without meeting all 5 criteria | Hiding underperformance. Carillion pattern. ESMA finding. |
| Cosmetic segment change | Auditor challenge. Restatement risk if reversed. |
| Not restating comparatives after change | IFRS 8.29 violation. Non-comparable periods. |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — grounded in xItem + ORG.buyer + edge data model. Aggregation test mapped to 5 criteria using FGGE fields. |
