# FGGE Role Credo

**Status**: DECIDED  
**Version**: 1.0  
**Purpose**: Define what FGGE does and why — separate from how it is implemented  
**Scope**: FGGE as perception infrastructure for S-R-S governance  
**Depends on**: `credo-srs-governance_v1.0.md`, `credo-avr-model_v1.1.md`  

---

## 1. What FGGE Is

FGGE (Financial Governance & Guidance Engine) builds Shaw Lenses for each cell in the S-R-S × xItem grid.

Sharp, clean, ruthless lenses that show R as it IS. When humans from each S-R-S zone meet in the Room, each brings high
Shaw-resolution from their specific lens. The Group Shaw resolution is maximized.

FGGE is **perception infrastructure**. Not a governance model (that's S-R-S). Not a compliance system (that's one lens
among three). Not a budgeting tool (budgets are the thing it replaces).

---

## 2. What FGGE Does

### Builds lenses

One Shaw Lens per cell in the grid:

```
              gItem.physical         vItem.e-svc           hItem
Shield        [lens]                 [lens]                [lens]
Reserve       [lens]                 [lens]                [lens]
Sword         [lens]                 [lens]                [lens]
```

Each lens resolves R through the cell's Intent. Shield × gItem.physical sees: "What Rim applies to our physical goods?"
Sword × vItem.e-svc sees: "What xtValue field can we extend in digital services?"

The lenses are built from:

- **BC** — captures R events (transactions, contracts, compliance status). Reality Collectors.
- **IFRS ergon chains** — process R events into structured data per standard. Shield's operational backbone.
- **Power BI + columnar DB** — surface Shaw-resolved views per cell, per Intent. The seeing layer.

### Reveals diagnostics

The lenses don't tell the ORG what to do. They show R so clearly that what to do becomes visible to the humans in the
Room.

What the lenses may reveal:

| Diagnostic             | What it shows                                                         | Visible in                                                                          |
|------------------------|-----------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| **Intent not locked**  | Vectors inconsistent across zones or time periods                     | Sword lens: Vectors scatter. Reserve lens: capacity deployed without pattern.       |
| **xItem saturation**   | Current visible xItem's Gray pool shrinking, dGray→White/dt declining | Sword lens: BFFB flow slowing. Need xItem' or new geography.                        |
| **xItem' opportunity** | xtValue field extendable with different g/v/h mix                     | Sword lens: adjacent Gray pool visible with different xItem composition.            |
| **Wrong segments**     | Value flows across segment boundaries, not within                     | All lenses: metrics improve when viewed across segments, degrade within.            |
| **Approaching Rim**    | Shield metrics trending toward regulatory boundaries                  | Shield lens: covenant headroom shrinking, compliance margins thinning.              |
| **Reserve depletion**  | Capacity declining without replenishment after shocks                 | Reserve lens: policy thresholds approached. Response time increasing.               |
| **Dark tetrad signal** | Reported R diverging from observed R                                  | Shield lens: IFRS event timing mismatches, ghost entities, unexplained adjustments. |

### Maximizes Group Shaw in the Room

FGGE's lenses are designed so that when S-R-S zone holders meet:

- Each participant arrives with high Shaw-resolution for their zone × xItem cells
- The lenses present R, not opinions about R
- The Room can synthesize because each lens is sharp, not because a dashboard averaged everything into one number

---

## 3. What FGGE Is NOT

| FGGE is NOT             | Because                                                                                                                                  |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| A governance model      | That's S-R-S. FGGE provides perception for whatever governance the ORG needs.                                                            |
| A budget system         | Budgets allocate on prediction. FGGE shows R so allocation follows observation.                                                          |
| A strategy tool         | Strategy-as-prediction is a ghost. FGGE shows R. Intent + clear R = correct Vectors.                                                     |
| Prescriptive            | FGGE doesn't tell the ORG what to do. It shows what IS.                                                                                  |
| Implementation-specific | This credo defines WHAT and WHY. HOW is separate — BC configuration, Power BI design, ergon chain implementation are execution concerns. |

---

## 4. The IFRS Foundation

IFRS is not bureaucracy. IFRS is the Rim that forces honest R reporting.

Every IFRS standard demands that financial reporting reflects **events in Reality**, not events in Agency:

- Revenue when control transfers, not when invoiced (IFRS 15)
- Losses when expected, not when realized (IFRS 9)
- Fair value from market data, not internal models (IFRS 13)
- Consolidation when control exists, not when convenient (IFRS 10)

This is dark tetrad defense. ORGs with unhealthy Intent present false R to stakeholders. IFRS forces Shield to see and
report R as it IS.

FGGE's Shield lenses are built ON IFRS — not as compliance checkboxes but as perception infrastructure. The 24 ergon
chains (`ergon-ifrs-master-chain_v1.0.md`) are the operational backbone that processes R events into structured, honest
financial data.

---

## 5. The Stack

```
Layer          What                           Function
─────────────────────────────────────────────────────────────
Intent         ORG's locked Intent            The gauge for everything
S-R-S          Three focus zones on R         Governance model
xItem grid     What is sold × how governed    Resolution space
─────────────────────────────────────────────────────────────
FGGE lenses    Shaw-resolved views of R       Perception infrastructure
IFRS chains    Process R events               Data backbone
BC             Capture R events               Reality Collectors
Power BI       Surface Shaw-resolved R        Seeing layer
─────────────────────────────────────────────────────────────
```

Above the line: the model (domain-independent).
Below the line: the tool (implementation-specific, replaceable).

FGGE lives below the line. S-R-S lives above. The model doesn't depend on the tool. A different tool stack could serve
the same model. But THIS tool stack (BC + FGGE + Power BI) is what we build.

---

## 6. Connection to FLIGHT-PLAN.md

From Root Intent:

> Make the economy engine (Business Central) work correctly from day one for any ORG — by dragging complexity into the
> architect's now so the user gets correct numbers without consulting hours.

FGGE serves this by building the perception infrastructure that lets any ORG — from sole proprietor to listed global
group — see its R clearly through S-R-S lenses. The complexity is absorbed at build time (MVA). The user gets correct
numbers. The Shaw Lenses show what matters.

---

## Version History

**Version**: 1.0  
**Created**: 2026-04-03  
**Author**: Morre + Claude (W-H-S)  
**Provenance**: Derived from S-R-S governance credo + FLIGHT-PLAN.md Root Intent  
