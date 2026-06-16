# Ergon: IFRS 10 — Scope Determination

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 10.4, 10.19-26, IFRS 12
**Intent**: Determine the complete list of entities in consolidation scope — who's in, who's out, what method
**Chain**: ergon-ifrs-10-chain_v1.0.md (step 2 of 4)
**Depends on**: ergon-ifrs-10-control-assessment (all assessments must complete first)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting date, AFTER all control assessments complete |
| **Event** | Any control_conclusion change (anomaly from control assessment ergon) |

---

## Input

| Source | What |
|---|---|
| ALL `edge:org-org` where owns section populated | Ownership graph with control conclusions |
| ALL `node:org` in the group | Entity properties (entity_type, reporting_date, accounting_policy_set, materiality) |
| `ergon-ifrs-10-control-assessment` results | control_conclusion per edge |

---

## Output

| Target | What | Condition |
|---|---|---|
| `ctx-v` "consolidation-scope-{period}" | Filtered view: entities in scope + method per entity | Always |
| `node:org` → materiality_assessment | Confirmed/updated per entity | Always |
| `node:anomaly` | "New entity in scope since last period" | Scope changed |
| `node:anomaly` | "Entity dropped from scope — investigate" | Scope changed |
| `node:anomaly` | "Reporting date misalignment > 3 months for {org}" | Validation failure |
| `node:anomaly` | "Accounting policy deviation: {org} uses {policy}, group uses {group_policy}" | Policy mismatch |

---

## Sub-Ergons

### Step 1: Traverse ownership graph from ultimate parent [MACH]

```
Start: node:org where entity is the ultimate parent (no incoming owns edge)

Recursive traversal:
  For each edge:org-org where this ORG is in the owns.source position:
    Read control_conclusion
    Read relationship_type
    Build tree: parent → children with effective ownership %

Output: Complete ownership tree with:
  - Every ORG reachable from ultimate parent
  - Effective ownership % per entity (chain multiplication)
  - Control conclusion per entity
  - Relationship type per entity
```

### Step 2: Classify each entity [MACH + IND]

```
For each entity in the ownership tree:

  IF control_conclusion = true:
    method = "full_consolidation"
    → Entity is SUBSIDIARY

  ELIF voting_rights_pct ≥ 20% AND significant_influence:
    method = "equity_method"
    → Entity is ASSOCIATE (IAS 28)

  ELIF joint_control (per IFRS 11 assessment):
    IF joint_operation → recognize own share of assets/liabilities
    IF joint_venture → method = "equity_method"

  ELSE:
    method = "financial_investment"
    → IFRS 9 classification

Record: entity + method on the scope output
```

### Step 3: Check investment entity exception [IND — HitL]

```
IF ultimate parent entity_type = "investment_entity":

  For each subsidiary:
    IF subsidiary provides investment management services:
      → STILL consolidated (exception to the exception)
    ELSE:
      → NOT consolidated
      → Measured at FVTPL
      → Record: method = "fvtpl_investment_entity"

  HitL: Confirm investment entity status still holds
  (Self-assessment: provides investment management services?
   Measures at fair value? Multiple investments? Unrelated investors?)
```

### Step 4: Check held-for-sale (IFRS 5) [IND]

```
For each subsidiary:
  IF materiality_assessment = "held_for_sale":
    Validate IFRS 5 criteria:
      - Available for immediate sale in present condition?
      - Sale highly probable (committed plan, active program, reasonable price)?
      - Expected to complete within 12 months?

    IF criteria met:
      method = "held_for_sale"
      → Measured at lower of carrying amount and FVLCD
      → Presented separately
      → Depreciation ceases

    IF criteria NOT met:
      → Anomaly: "Held-for-sale classification not supported for {org}"
      → Revert to full_consolidation
```

### Step 5: Validate reporting dates [MACH]

```
parent_reporting_date = ultimate parent node:org → reporting_date

For each subsidiary in scope:
  subsidiary_date = node:org → reporting_date
  difference = |parent_reporting_date - subsidiary_date|

  IF difference > 3 months:
    → Anomaly: "Reporting date misalignment > 3 months for {org}.
       Cannot consolidate without interim financial statements.
       Subsidiary year-end: {subsidiary_date}, Parent: {parent_reporting_date}"

  ELIF difference > 0 AND difference ≤ 3 months:
    → Flag: "Adjust for significant transactions between {subsidiary_date}
       and {parent_reporting_date}"
```

### Step 6: Validate accounting policies [MACH + IND]

```
group_policy = ultimate parent node:org → accounting_policy_set

For each subsidiary in scope:
  sub_policy = node:org → accounting_policy_set

  IF sub_policy != group_policy:
    → Anomaly: "Accounting policy deviation for {org}.
       Group: {group_policy}, Subsidiary: {sub_policy}.
       Consolidation adjustment required."

    Specific deviations to check:
    - Revenue recognition method
    - Depreciation method / useful lives
    - Inventory valuation (FIFO vs weighted average)
    - Financial instrument classification
    - Lease accounting approach
```

### Step 7: Generate consolidation scope [MACH]

```
Output ctx-v "consolidation-scope-{period}":

  For each entity:
    - org_id
    - org_name
    - method (full_consolidation / equity_method / fvtpl / held_for_sale / financial_investment)
    - effective_ownership_pct
    - nci_pct
    - reporting_date_aligned (true/false)
    - accounting_policy_aligned (true/false)
    - flags (anomalies raised)

  Compare to prior period scope:
    - NEW entities → anomaly: "New in scope"
    - REMOVED entities → anomaly: "Dropped from scope — why?"
    - METHOD changes → anomaly: "Method changed from {old} to {new}"
```

---

## Rim Consequence

- Incorrect scope = misstated consolidated financial statements
- ESMA common finding: failure to consolidate where de facto control exists
- Wirecard: fabricated entities included in scope
- Enron: real entities excluded from scope
- ABL 29:1: Board liable for damage from misstated annual report

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — from W-H-S IFRS 10 Hammer-Walk |
