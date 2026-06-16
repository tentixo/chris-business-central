# Ergon: IFRS 10 — NCI Calculation

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 10.22-24, B94-B99
**Intent**: Calculate Non-Controlling Interest percentages for all subsidiaries, including chain and cross-ownership
**Chain**: ergon-ifrs-10-chain_v1.0.md (step 3 of 4)
**Depends on**: ergon-ifrs-10-scope-determination (scope must be finalized first)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting date, AFTER scope determination complete |
| **Event** | Any ownership % change within consolidation scope |

---

## Input

| Source | What |
|---|---|
| `ctx-v` "consolidation-scope-{period}" | Entities in scope with effective ownership % |
| `edge:org-org` → owns | Voting rights percentages per edge |

---

## Output

| Target | What |
|---|---|
| `edge:org-org` → owns.nci_pct | Effective NCI per entity |
| BC `business-unit.minority-pct` | Written to BC for consolidation engine |

---

## Sub-Ergons

### Step 1: Direct ownership NCI [MACH]

```
For each subsidiary with single-level ownership:
  nci_pct = 100 - voting_rights_pct

Example:
  Parent owns 80% of Sub → nci_pct = 20%
```

### Step 2: Chain ownership (multi-level) [MACH]

```
For subsidiaries owned through chains:

  A owns 80% of B
  B owns 60% of C

  A's effective ownership of C = 80% × 60% = 48%

  Consolidation:
    A controls B (80% > 50%) → consolidate B
    B controls C (60% > 50%) → consolidate C (through B)

  NCI allocation:
    NCI in B = 20% (direct minority)
    NCI in C = 52% from A's perspective
      But: 20% of C's NCI belongs to B's NCI shareholders
      Layered NCI: direct (B's 40%) + indirect (A's minority in B × B's share in C)

  Graph traversal computes effective % at each level.
  BC Business Unit receives the consolidation-relevant minority %.
```

### Step 3: Cross-holdings detection [MACH + IND if found]

```
Detect circular ownership: A → B → C → A

IF circular ownership detected:
  → Cannot use simple multiplication
  → Iterative algebraic solution required
  → Flag for IND review: "Cross-holding detected between {entities}"
  → Solve simultaneous equations for effective ownership

Cross-holdings are rare but exist (e.g., Japanese keiretsu, some European groups).
```

### Step 4: Write to graph + BC [MACH]

```
For each subsidiary in scope:
  Write nci_pct to edge:org-org → owns.nci_pct
  Write to BC: business-unit.minority-pct via API (bc.path reference)
```

### Step 5: Validate totals [MACH]

```
For each subsidiary:
  ASSERT: parent_effective_pct + nci_pct = 100%

For P&L attribution:
  ASSERT: parent_share + nci_share = total_net_income (per entity)

Note: NCI CAN be negative (deficit).
  IFRS 10.B94: "Total comprehensive income shall be attributed to the owners
  of the parent and to the non-controlling interests even if this results in
  the non-controlling interests having a deficit balance."
```

---

## Rim Consequence

- Incorrect NCI = misstated equity split between parent and minority shareholders
- P&L attribution wrong → EPS wrong (IAS 33) → misleading to market
- Common audit finding: NCI allocation errors in multi-level groups
- NCI must go into deficit if subsidiary has losses — cannot cap at zero

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — from W-H-S IFRS 10 Hammer-Walk |
