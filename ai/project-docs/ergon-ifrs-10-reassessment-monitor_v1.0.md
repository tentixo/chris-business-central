# Ergon: IFRS 10 — Reassessment Monitor

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 10.8 ("reassess when facts and circumstances indicate changes")
**Intent**: Detect trigger events requiring control reassessment — continuous Entropy Patrol for ownership graph
**Chain**: ergon-ifrs-10-chain_v1.0.md (step 0 — continuous, feeds into step 1)

---

## Trigger

| Type | Detail |
|---|---|
| **Continuous** | Monitors x-history events on ownership edges and governance data |
| **This is a Walker** | Reality Observer Path — detects anomalies independently of planned work |

---

## Input

| Source | What monitored |
|---|---|
| `edge:org-org` → _history | Changes to voting_rights_pct, economic_interest_pct, control_assessment |
| `edge:ind-org.board-member` → _history | Birth/death of board membership edges |
| `node:org` → _history | Changes to entity_type, registered_share_capital, governance properties |
| External sources (Walkers) | Bolagsverket filings, allabolag updates, news feeds |

---

## Output

| Anomaly | Trigger condition |
|---|---|
| "Voting rights changed: {parent}→{subsidiary} {old}%→{new}%" | x-history event on voting_rights_pct |
| "Board composition changed at {org} — reassess control" | Board-member edge born or died |
| "New shareholder agreement detected — reassess" | Contractual arrangement property changed |
| "Subsidiary share issue/buyback — dilution check" | registered_share_capital changed on subsidiary |
| "Entity type changed for {org}: {old}→{new}" | entity_type history event |
| "New ownership edge created: {org1}→{org2}" | New edge:org-org with owns section |
| "Ownership edge removed: {org1}→{org2}" | Edge:org-org owns section set to null |

Each anomaly → triggers `ergon-ifrs-10-control-assessment` for the affected ORG pair.

---

## Sub-Ergons

### Step 1: Monitor ownership percentage changes [MACH — Walker]

```
Watch: edge:org-org → _history WHERE field = "org*_to_org*.owns.voting_rights_pct"

On event:
  old_pct = event.from
  new_pct = event.to

  Classify:
    Crossed 50% threshold (up or down) → CRITICAL — control may have changed
    Crossed 20% threshold (up or down) → SIGNIFICANT — significant influence may have changed
    Within same band → INFORMATIONAL — update effective ownership, may affect NCI

  Raise anomaly with classification level.
```

### Step 2: Monitor board composition [MACH — Walker]

```
Watch: edge:ind-org.board-member → _history (birth/death events)

On event:
  Check: does this change who has power to direct relevant activities?

  Heuristic:
    IF parent-nominated directors now < 50% of board → flag
    IF key individual removed who was basis of power assessment → flag
    IF new independent directors shift balance → flag

  Raise anomaly if board change could affect control conclusion.
```

### Step 3: Monitor governance changes [MACH — Walker]

```
Watch: edge:org-org → _history WHERE field contains "contractual_arrangements"
       or "potential_voting_rights" or other governance properties

On event:
  New shareholder agreement → flag
  Management agreement changed → flag
  Veto rights added/removed → flag
  Put/call option on shares → flag
```

### Step 4: Raise anomaly and trigger reassessment [MACH]

```
For each anomaly raised:
  Create node:anomaly with:
    - Description of what changed
    - Reference to affected edge:org-org
    - Reference to affected node:org entities
    - Classification: CRITICAL / SIGNIFICANT / INFORMATIONAL
    - Spotter: "walker:ifrs-10-reassessment-monitor"

  Anomaly → addresses → ergon-ifrs-10-control-assessment (new instance)
  The control assessment ergon runs for the affected pair.
```

---

## Rim Consequence

Delayed reassessment:
- If control LOST but not recognized → overstating assets and revenue (still consolidating)
- If control GAINED but not recognized → understating the group (missing entity)
- IFRS 10.8 is explicit: "shall reassess" — not optional
- Failure pattern #1 (passive): not detecting that scope should change

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — from W-H-S IFRS 10 Hammer-Walk |
