# Ergon: IFRS 10 — Control Assessment

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 10.5-18, B34-B72
**Intent**: Determine whether Parent controls Investee — the gate to consolidation
**Chain**: ergon-ifrs-10-chain_v1.0.md (step 1 of 4)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting date (quarterly for listed, annual minimum) |
| **Event** | Ownership % change, board composition change, new shareholder agreement, governance restructuring, share issue/buyback by investee |

---

## Input

| Source | What | Reference |
|---|---|---|
| `edge:org-org` | Ownership data (voting_rights_pct, economic_interest_pct) | org1_to_org2.owns / org2_to_org1.owns |
| `node:org` | Both parent and investee entity data | type_data.governance |
| `edge:ind-org.board-member` | Board composition of investee | For power assessment |
| BC | Business Unit card data | bc.business-unit.{company} |

---

## Output

| Target | What | Condition |
|---|---|---|
| `edge:org-org` → owns.control_assessment | Updated control conclusion + evidence | Always |
| `node:anomaly` | "Control may have changed for {org}" | When trigger event detected |
| `node:anomaly` | "De facto control inconclusive — HitL required" | When voting < 50% and evidence ambiguous |
| `node:decision` | "Does Parent have de facto control over {org}?" | When voting < 50% |
| `node:decision` | "Is this SPE controlled in substance?" | When entity_type = spe |

---

## Effector

| Role | Type | Why |
|---|---|---|
| Primary (steps 1, 6) | MACH | Graph read/write is mechanical |
| HitL (steps 2-5) | IND (CFO/Controller) | IFRS 10.B38-46 requires judgment on power, returns, link |

---

## Sub-Ergons

### Step 1: Verify voting rights percentage [MACH]

```
Read edge:org-org → owns.voting_rights_pct

IF ≥ 50%:
  has_power = true (presumed — IFRS 10.B34)
  power_evidence = "voting_majority"
  → Skip to Step 4

IF < 50%:
  → Proceed to Step 2 (de facto control assessment)

IF = 0 or null:
  Check: entity_type = spe?
  IF yes → Proceed to Step 2 (SPE substance assessment)
  IF no → No control. Record and exit.
```

### Step 2: Gather de facto control evidence [MACH gathers]

```
Collect from graph and BC:

a) largest_other_block_pct
   Query: all edge:org-org where target = this investee AND owns != null
   Find: largest voting block that is NOT this parent

b) shareholder_dispersion
   Count: number of other shareholders, distribution of blocks
   Concentrated (few large blocks) vs Dispersed (many small)

c) potential_voting_rights
   Read: options, convertibles, warrants that could give additional votes
   Calculate: voting_rights_pct IF exercised

d) contractual_arrangements
   Read: management agreements, veto rights, put/call options
   Source: may need manual input (not always in graph)

e) historical_voting_patterns
   Read: prior AGM outcomes — does parent consistently control?
   Source: may need manual input

Output: de_facto evidence template populated with available data
        Flag fields requiring manual input from IND
```

### Step 3: Evaluate de facto control [IND — HitL Decision]

```
Present evidence template to CFO/Controller:

  "Parent holds {voting_rights_pct}% of {investee}.
   Largest other block: {largest_other_block_pct}%.
   Shareholders: {shareholder_dispersion}.
   Potential voting rights if exercised: {potential_pct}%.
   Contractual arrangements: {description}.
   Historical voting: {description}.

   DECISION REQUIRED: Does Parent have de facto control?"

Record on edge:org-org → owns.de_facto:
  All evidence fields + conclusion + assessed_by + assessed_date

IF de facto control = true:
  has_power = true
  power_evidence = "de_facto"
  → Proceed to Step 4

IF de facto control = false:
  → No control (may still be associate if ≥ 20%). Exit.
```

### Step 4: Assess variable returns exposure [IND — judgment]

```
Evaluate exposure to variable returns from the investee:

Checklist:
  [ ] Dividends (current and expected)
  [ ] Management fees / service charges
  [ ] Synergies (cost savings, revenue enhancement)
  [ ] Residual interests (liquidation value)
  [ ] Loss exposure (guarantees, subordinated debt)
  [ ] Tax benefits (group relief, consolidated tax)

IF any checked:
  exposed_to_variable_returns = true
  returns_evidence = [list of checked items]
  → Proceed to Step 5

IF none checked:
  → Unusual. Power without returns exposure = possible agent relationship.
  Flag for additional review.
```

### Step 5: Assess link between power and returns [IND — judgment]

```
Question: Can the investor USE its power to AFFECT the returns it's exposed to?

Key distinction: Principal vs Agent (IFRS 10.B58-B72)

Agent indicators:
  - Scope of decision-making authority is narrow/predefined
  - Other parties can remove the decision-maker
  - Remuneration is fixed/formulaic (not variable with performance)
  - Exposure to variability is limited relative to other parties

Principal indicators:
  - Broad decision-making authority
  - Cannot be easily removed
  - Variable returns linked to performance
  - Significant exposure to variability

Record:
  can_affect_returns = true/false
  acting_as = "principal" / "agent"
```

### Step 6: Conclude and record [MACH]

```
control_conclusion = has_power AND exposed_to_variable_returns AND can_affect_returns

Write to edge:org-org → owns.control_assessment:
  has_power
  power_evidence
  exposed_to_variable_returns
  returns_evidence
  can_affect_returns
  acting_as
  control_conclusion
  assessed_date = now
  assessed_by = IND who performed assessment

IF control_conclusion CHANGED from prior assessment:
  Raise anomaly: "Control conclusion changed for {parent} → {investee}: {old} → {new}"
  This triggers ergon-ifrs-10-scope-determination to re-run
```

---

## Rim Consequence

Failure to correctly assess control:
- **Overstate scope** (consolidate entity you don't control) → misstated revenue, assets
- **Understate scope** (don't consolidate entity you DO control) → hidden debt, off-balance-sheet risk
- **ESMA enforcement**: Common finding — failure to consolidate structured entities
- **Failure pattern #1**: Consolidation scope manipulation (Enron — 3000 SPEs, Wirecard — fictitious entities)
- **ABL 29:1**: Board liable for damage caused by IFRS violation in consolidated statements
- **Auditor**: ISA 700 qualification if scope is wrong

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-03-31 | Initial — from W-H-S session on IFRS 10 Hammer-Walk |
