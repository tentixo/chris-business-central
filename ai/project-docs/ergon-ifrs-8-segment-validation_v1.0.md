# Ergon: IFRS 8 — Segment Validation (Thresholds + Coverage)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 8.13-19
**Intent**: Apply quantitative thresholds, ensure 75% coverage, handle below-threshold segments
**Chain**: ergon-ifrs-8-chain_v1.0.md (step 2)
**Depends on**: ergon-ifrs-8-segment-identification (segments must be identified first)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | After segment identification, each reporting period |

---

## Input

| Source | What |
|---|---|
| Segment definitions (ctx-v) | From identification ergon |
| `edge:org-org` → sells_to | Revenue per segment (SUM of sells_to.annual_volume × price, filtered by ctx-v) |
| Consolidated P&L | Total revenue, total profit/loss |
| Consolidated BS | Total assets |

---

## Sub-Ergons

### Step 1: Calculate segment metrics [MACH]

```
For each identified segment (ctx-v):

  Revenue = SUM(edge:org-org → sells_to.price × volume)
            WHERE sells_to matches segment ctx-v filter
            EXCLUDING intercompany (edge.IC_flag = true → eliminated)

  Profit/Loss = Revenue - attributed cost
                Cost attribution: SUM(xItem.cost_standard × volume)
                + allocated ORG.seller costs per segment

  Assets = SUM(node:org assets) allocated per segment
           (allocation method: by revenue, by headcount, or direct)

Store: segment.revenue, segment.profit, segment.assets
```

### Step 2: Apply 10% thresholds [MACH]

```
IFRS 8.13:

For each segment, test:

  a) segment.revenue ≥ 10% of combined revenue?
     Combined = SUM(all segment revenues) — includes intersegment
     Note: combined revenue includes BOTH external and intersegment

  b) segment.profit ≥ 10% of the GREATER of:
     - Total of all segments reporting profit, OR
     - Total of all segments reporting loss (in absolute terms)
     (Compare to the larger absolute number)

  c) segment.assets ≥ 10% of combined assets?

  IF ANY of a/b/c is true → REPORTABLE segment

  IF NONE → below threshold → can aggregate into "All other segments"
            OR can still report separately if management wants
```

### Step 3: Check 75% coverage [MACH]

```
IFRS 8.15:

  total_reported = SUM(revenue of all REPORTABLE segments)
  total_external = total external (non-intersegment) revenue

  IF total_reported / total_external ≥ 75% → PASS

  IF < 75% → must add more segments as reportable
    Add in order of size until 75% reached
    Even below-threshold segments must be added

  IFRS 8.15: "Additional operating segments should be identified as
  reportable segments even if they do not meet the quantitative criteria."
```

### Step 4: Handle "All other segments" [MACH]

```
IFRS 8.16:

  Remaining non-reportable segments → "All other segments" bucket

  Disclose:
    - Revenue (external + intersegment)
    - Profit/loss
    - Assets
    - Description of what's included

  "All other segments" should NOT be larger than any reportable segment.
  If it is → reconsider whether something should be split out.
```

### Step 5: Validate stability [MACH + IND]

```
Compare to prior period:

  For each segment:
    Prior revenue vs current → material change?
    Prior profit vs current → material change?
    Segment appeared or disappeared?

  IF segment dropped below 10% but was reportable last period:
    IFRS 8.17: May continue reporting separately if management judges
    it remains significant. Common practice: report for continuity.

  IF new segment crossed 10%:
    Must report. Restate prior period if data available.
```

---

## Output

| Target | What |
|---|---|
| Reportable segments list | With revenue, profit, assets per segment |
| 75% coverage confirmation | Pass/fail + additional segments if needed |
| "All other segments" | Residual bucket with disclosures |
| Stability flags | Segments crossing thresholds in/out |
| Ready for disclosure ergon | Validated segment data |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial |
