# Ergon: IAS 36 — CGU Identification + Goodwill Allocation (Step 0)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 36.65-73 (CGU identification), IAS 36.80-87 (goodwill allocation)
**Intent**: Identify Cash-Generating Units (CGUs) and allocate goodwill from acquisitions (IFRS 3) to them. This is the SETUP that determines how impairment testing works. Get the CGU wrong → test at wrong level → mask impairment.
**Chain**: ergon-ias-36-chain_v1.0.md (step 0)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | New acquisition with goodwill (IFRS 3 PPA complete → goodwill exists → must allocate) |
| **Event** | Group restructuring (business units reorganized → CGU boundaries may change) |
| **Periodic** | Annual review: are CGU boundaries still appropriate? |

---

## What is a CGU?

```
IAS 36.6: A Cash-Generating Unit is the SMALLEST identifiable group of assets
that generates cash inflows that are LARGELY INDEPENDENT of
cash inflows from other assets or groups of assets.

Key word: SMALLEST. Not the biggest convenient grouping.
Auditor challenge: is this REALLY the smallest independent cash-generating group?
ESMA challenge: companies aggregate CGUs to mask impairment at lower levels.
```

### How to identify CGUs [IND — judgment]

```
Questions to determine CGU boundaries:

1. Does this group of assets generate revenue independently?
   Can you trace customer revenue to THIS specific group?

2. Would you continue to operate this group on its own?
   If the rest of the business disappeared, would this group survive?

3. Does management monitor this as a separate unit?
   Internal reporting structure is evidence (but not determinative).

4. Is there an active market for output of this group?
   If you could sell the output separately → likely a CGU.

Common patterns:
  - Each legal entity (node:org) = one CGU (simplest, often correct for acquired entities)
  - A product line within an entity = one CGU (if independent revenue)
  - A geographic region = one CGU (if independent market)
  - A retail store = one CGU (each store generates independent cash flows)
  - A factory = may NOT be a CGU if its output is sold by a sales unit
    (factory + sales together = CGU)

Using our model:
  CGU boundary often aligns with:
    - An ORG (one entity = one CGU)
    - A cluster of xItems serving an independent market
    - A segment (IFRS 8) — but CGU can be SMALLER than a segment

  IAS 36.80: CGU for goodwill allocation shall NOT be larger
  than an OPERATING SEGMENT (before aggregation, per IFRS 8.5).
```

### Goodwill allocation to CGUs [IND + MACH]

```
IAS 36.80-87:

Goodwill from IFRS 3 acquisitions must be allocated to the CGU(s)
expected to BENEFIT from the synergies of the combination.

At acquisition:
  Identify which CGU(s) benefit from acquiring this entity.
  Allocate goodwill to those CGUs.

  Simple case: acquired entity = one CGU → all goodwill to that CGU.
  Complex case: acquired entity's synergies benefit multiple existing CGUs
                → allocate goodwill across them (by expected benefit).

Record:
  node:org → cgu.cgu_id = "{identifier}"
  node:org → cgu.cgu_name = "{description}"
  node:org → cgu.goodwill_allocated = amount allocated to this entity's CGU
  edge:org-org → ppa.goodwill = total goodwill from this acquisition

Constraint: CGU ≤ operating segment (before IFRS 8 aggregation).
  If goodwill can only be allocated to a group of CGUs larger than one segment
  → something is wrong with the CGU identification.
```

### CGU restructuring [IND]

```
IAS 36.87: If group reorganizes and CGU boundaries change:

  Goodwill must be REALLOCATED to the new CGUs.
  Method: relative value of the portions transferred.

  Example: CGU-North (with goodwill 100M) split into CGU-Nordics (60%)
           and CGU-Baltics (40%) → goodwill 60M and 40M.

  This is material and must be documented.
  Auditor checks: was the reallocation reasonable?
```

---

## Output

| Target | What |
|---|---|
| `node:org → cgu` | CGU identification per entity: cgu_id, cgu_name, goodwill_allocated |
| CGU register (documentation) | For each CGU: boundary rationale, entities included, goodwill amount, date allocated |
| `node:anomaly` | "CGU larger than operating segment — review boundary" |
| `node:decision` | "How to allocate goodwill from {acquisition} across CGUs?" |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| CGU too large (aggregated to mask impairment) | Profitable parts hide loss-making parts → goodwill not impaired when it should be | #3 Optimistic — ESMA's MOST common IAS 36 finding (Carillion) |
| CGU larger than operating segment | Violates IAS 36.80 bright-line rule | ESMA enforcement |
| Goodwill not allocated within 12 months of acquisition | Must allocate by end of measurement period (IFRS 3). Testing goodwill at group level is prohibited. | Shield compliance failure |
| CGU changed without reallocating goodwill | Old goodwill allocation doesn't match new structure → testing at wrong level | Shield |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — CGU = smallest independent cash-generating group. Goodwill allocation. Restructuring reallocation. ≤ operating segment constraint. |
