# Ergon: IFRS 8 — Segment Disclosure

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 8.20-34
**Intent**: Produce the segment note — reconciliation to consolidated amounts, entity-wide disclosures, major customer, consistency check
**Chain**: ergon-ifrs-8-chain_v1.0.md (step 3)
**Depends on**: ergon-ifrs-8-segment-validation (reportable segments must be validated)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | After segment validation, each reporting period |

---

## Sub-Ergons

### Step 1: Segment information per reportable segment [MACH]

```
IFRS 8.23-24: For each reportable segment, disclose:

  a) Measure of profit or loss

  b) IF reported to CODM:
     - Segment assets
     - Segment liabilities
     - Revenue from external customers
     - Intersegment revenue
     - Interest revenue
     - Interest expense
     - Depreciation and amortization
     - Material items of income/expense (IAS 1.97)
     - Share of profit of associates/JVs (equity method)
     - Income tax expense
     - Material non-cash items other than depreciation

  Source: all derivable from edge:org-org.sells_to (revenue per xItem per segment)
          + xItem.cost_standard (costs) + node:org (assets, liabilities, depreciation)
          filtered by segment ctx-v

  ONLY disclose what CODM actually reviews. Don't add data the CODM doesn't see.
```

### Step 2: Reconciliation [MACH]

```
IFRS 8.28: Reconcile segment totals to consolidated amounts:

  Segment revenue total → consolidated revenue
    Difference = intersegment eliminations + unallocated items

  Segment profit total → consolidated profit before tax
    Difference = corporate costs + unallocated items + eliminations

  Segment assets total → consolidated total assets
    Difference = corporate/unallocated assets + eliminations

  Each reconciling item EXPLAINED:
    "Corporate overhead not allocated to segments: SEK X"
    "Intersegment elimination: SEK Y"
    "Holding company assets not in any segment: SEK Z"
```

### Step 3: Entity-wide disclosures [MACH]

```
IFRS 8.32-34: Required REGARDLESS of segment structure:

  a) Revenue by xItem type (IFRS 8.32)
     → SUM(revenue) per xItem.type: gItem, vItem, hItem
     → Further: per xItem.sub_type if useful (gItem.physical, vItem.e-svc, etc.)
     → Source: edge:org-org → sells_to.xitem_refs → group by xItem.type

  b) Revenue by geography (IFRS 8.33)
     → SUM(revenue) per ORG.buyer.jurisdiction (grouped into regions)
     → Non-current assets per ORG.seller.jurisdiction
     → Country of domicile separately if material
     → Source: edge → sells_to, grouped by buyer/seller jurisdiction

  c) Major customer (IFRS 8.34)
     → Any single ORG.buyer providing ≥10% of total revenue?
     → Disclose: the FACT, the AMOUNT, which SEGMENT(s)
     → Do NOT name the customer
     → Source: edge:org-org → sells_to, aggregated per buyer ORG

  NOTE: Entity-wide disclosures required EVEN IF the entity has only ONE segment.
```

### Step 4: Consistency check [MACH + IND]

```
a) Compare IFRS 8 segments to CODM Power BI reports
   IF CODM sees 5 clusters but IFRS 8 shows 3 segments
   → MUST explain (aggregation) or anomaly (inconsistency)

b) Compare IFRS 8 segments to investor presentations
   IF IR materials slice differently → ESMA flags
   → Anomaly: "Investor presentation shows different business structure than IFRS 8"

c) Compare IFRS 8 segments to management commentary (förvaltningsberättelse)
   IF the directors' report discusses the business by geography
   but segments are by xItem type → inconsistency
   → Not necessarily wrong (narrative vs formal segments)
   → But must be explainable

d) Compare to prior period
   IF segments changed → have comparatives been restated?
   IF not → IFRS 8.29 violation
```

### Step 5: Assemble note [MACH]

```
Output: structured data for the segment note in the financial statements:

  1. Basis of segmentation (how segments identified, who is CODM)
  2. Per-segment table (revenue, profit, assets, reconciling items)
  3. Reconciliation tables (segments → consolidated)
  4. Entity-wide: revenue by xItem type
  5. Entity-wide: revenue by geography
  6. Entity-wide: non-current assets by geography
  7. Major customer disclosure
  8. Changes from prior period (if any, with explanation)
```

---

## Output

| Target | What |
|---|---|
| Segment note content | Structured data ready for annual report / quarterly report |
| Reconciliation | Segments → consolidated, all differences explained |
| Entity-wide disclosures | xItem type revenue, geography revenue/assets, major customer |
| Consistency report | Comparison: IFRS 8 vs Power BI vs IR materials vs management commentary |
| Anomalies (if any) | Inconsistencies flagged for IND review |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Missing reconciliation | IFRS 8.28 violation. Auditor qualification. |
| Missing entity-wide disclosures | IFRS 8.32-34 violation. Even single-segment entities must disclose. |
| Major customer not disclosed | IFRS 8.34 violation. Market doesn't see concentration risk. |
| Inconsistency with IR materials | ESMA finding. Credibility damage. "Are you showing the market a different story than what management sees?" |
| Not restating comparatives after change | IFRS 8.29 violation. Non-comparable periods. |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — reconciliation, entity-wide, major customer, consistency check. All grounded in xItem × ORG × edge data model. |
