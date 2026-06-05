# Upstream-Downstream Flow

**Version**: 1.3
**Created**: 2026-02-19
**Purpose**: How FLIGHT-PLAN, Credo, MVA, W-H-S, TMM, and Coding relate. Load for orientation.

---

```mermaid
graph TD
    bootstrap(["<b>Bootstrap</b><br/><i>manual: copy files,<br/>install beads, git</i>"])
    init["<b>txo-init</b><br/>validate files<br/><i>offer /txo-intent<br/>if no FLIGHT-PLAN</i>"]
    intent["<b>txo-intent</b><br/>W-H-S with Human<br/><i>creates FLIGHT-PLAN.md</i>"]
    fp["<b>FLIGHT-PLAN.md</b><br/>Intent + Anchors<br/><i>L0 — gauge for all work</i>"]
    credo["<b>Credo</b><br/>MAY/SHOULD<br/><i>load-bearing positions<br/>in project-docs/credo-*.md</i>"]
    mva["<b>MVA</b><br/>WHY: absorb complexity when cheap<br/><i>load-bearing vs decorative</i>"]
    whs["<b>W-H-S</b><br/>Walk-Hammer-Synthesis<br/><i>find, test, lock</i>"]
    tmm["<b>TMM</b><br/>outer loop<br/><i>stages, deliverables, 4BM</i>"]
    docs["<b>4BM Docs</b><br/>decided/ + project-docs/<br/><i>locked artifacts</i>"]
    code["<b>Coding</b><br/>EXECUTION<br/><i>build from specs</i>"]

    bootstrap -->|" one-time "| init
    init -->|" no FLIGHT-PLAN? "| intent
    intent -->|" W-H-S produces "| fp
    fp -->|" anchors graduate<br/>when they generate<br/>design questions "| credo
    fp -->|" Intent + Anchors<br/>read by "| tmm
    credo -->|" constrain "| tmm
    credo -->|" constrain "| docs
    fp -->|" Anchors inform "| whs
    fp -->|" Anchors inform "| code
    start(["<b>Start</b><br/><i>txo-takeoff</i>"])
    start -->|" loads Intent +<br/>Anchors as gauge "| fp
    mva -->|" starts W-H-S<br/>(find what's load-bearing) "| whs
    whs -->|" results propagate<br/>into TMM stage "| tmm
    whs -->|" position crystallizes<br/>into credo "| credo
    tmm -->|" drop into W-H-S<br/>at any stage "| whs
    tmm -->|" produces "| docs
    docs -->|" re-hammer when<br/>downstream contradicts "| whs
    tmm -->|" Stage EXECUTION "| code
    whs -.->|" synthesis may<br/>produce specs "| code
```

---

## Reading the Graph

- **Bootstrap** is manual and one-time: copy files from txo-ai, install beads, set up git.
- **txo-init** validates bootstrap. If no FLIGHT-PLAN.md exists, offers `/txo-intent`.
- **txo-intent** runs a W-H-S process with the Human to extract Intent and Anchors, producing FLIGHT-PLAN.md.
- **FLIGHT-PLAN.md** is the L0 Anchor document — carries Intent (the gauge) and Anchors (load-bearing philosophical
  positions). Anchors inform all downstream work: TMM stage decisions, W-H-S direction, and coding choices.
- **Credo** (MAY/SHOULD) — a load-bearing philosophical position that constrains downstream design. Appears when
  ontological ambiguity exists (things shift shape, Eidos must be found). An anchor in FLIGHT-PLAN *graduates* into a
  credo when it generates enough design questions to fill a document. W-H-S may also crystallize positions directly into
  credos. AV-R serves as compass — separating AV vs R so the designer knows which realm they're in. Lives in
  `project-docs/credo-*.md`. See tmm-0-foundation §5 for full explanation.
- **MVA** motivates W-H-S — you walk to find what's load-bearing before it calcifies.
- **W-H-S** and **TMM** are circular: TMM is the outer loop (stages), W-H-S is the inner loop (measurement events). At
  any TMM stage, drop into W-H-S. Results flow back.
- **4BM Docs** are TMM's locked artifacts. When downstream work (coding, new W-H-S) contradicts them, they get
  re-hammered.
- **Coding** is downstream of TMM EXECUTION stage. W-H-S synthesis may also produce specs directly (dashed line — less
  common).

## The Circular Relationship

```
TMM Stage N → itch detected → W-H-S begins
    Walk → Hammer → Synthesis → result
        → propagates back into TMM Stage N (or earlier — backward force)
            → may invalidate 4BM docs → re-hammer
```

This is the upstream effect problem (Anchor 5, task v86). Currently handled manually by Human noticing.

---

## TMM Stage Flow (outer loop)

```mermaid
graph TD
    S00["<b>00. INTENT</b><br/><i>declare Intent<br/>narrow from Root Intent</i>"]
    S0["<b>0. FOUNDATION</b><br/><i>tech stack, patterns</i>"]
    S1["<b>1. DUMP</b><br/><i>capture everything</i>"]
    S2["<b>2. CATEGORIZE</b><br/><i>sort into 4 boxes</i>"]
    S3["<b>3. SCOPE</b><br/><i>inside / edge / external</i>"]
    S4["<b>4. DECISIONS</b><br/><i>ADRs, hard-rules</i>"]
    S5["<b>5. TESTS</b><br/><i>test cases, smoke tests</i>"]
    S6["<b>6. SKILLS</b><br/><i>dev-order, features</i>"]
    S7["<b>7. VALIDATE</b><br/><i>completeness check</i>"]
    exec["<b>EXECUTION</b><br/><i>build one module, return</i>"]
    whs_inner(["<b>W-H-S</b><br/><i>inner loop</i>"])

    S00 --> S0
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 -->|" all boxes filled "| exec
    S7 -->|" boxes missing "| S2

    S0 -.->|" itch? "| whs_inner
    S1 -.->|" itch? "| whs_inner
    S2 -.->|" itch? "| whs_inner
    S3 -.->|" itch? "| whs_inner
    S4 -.->|" itch? "| whs_inner
    S5 -.->|" itch? "| whs_inner
    S6 -.->|" itch? "| whs_inner
    whs_inner -.->|" result back<br/>to stage "| S0
```

At any stage, an itch triggers a W-H-S (dashed lines). The W-H-S result propagates back — possibly to the same stage, possibly to an earlier one (backward force). Stage 00 (Intent Declaration) added in TMM v0.7.

---

## Document Map

| Position | Document                     | What it carries                                     |
|----------|------------------------------|-----------------------------------------------------|
| -1       | bootstrap-ai-in-repo v1.2    | Manual setup steps (one-time)                       |
| 0a       | txo-init (skill)             | Validate bootstrap, offer /txo-intent               |
| 0b       | txo-intent (skill)           | W-H-S process to create/improve FLIGHT-PLAN.md      |
| 0c       | FLIGHT-PLAN.md               | Intent + Anchors (L0 gauge for all work)            |
| 0d       | Credo docs (MAY/SHOULD)      | Load-bearing positions, graduated anchors            |
| 1a       | Shaw Research v2.0           | W-H-S process behavior (prompt for AI)              |
| 1b       | MVA v2.0                     | WHY — motivation, load-bearing vs decorative        |
| 1c       | Walk Reference v1.0          | Shaw Dense terminology + tips                       |
| 2        | TMM Process v0.7             | Outer loop stages with Intent + W-H-S awareness     |
| 3        | 4BM Docs                     | decided/ + project-docs/ (locked per stage)         |
| 4        | Code                         | src/ (EXECUTION)                                    |

---

**Version History**

**v1.3** (2026-03-06):

- Re-added Credo as separate node between FLIGHT-PLAN and TMM/4BM docs
- v1.2 absorption was premature — credos are distinct from FLIGHT-PLAN anchors (they graduate when generating design questions)
- Added W-H-S → Credo edge (positions crystallize into credos)
- Added Credo → TMM and Credo → 4BM Docs edges (credos constrain downstream)
- Document Map: added position 0d for Credo docs
- Full credo explanation in tmm-0-foundation v0.9 §5

**v1.2** (2026-02-21):

- Removed Credo as separate node — absorbed into FLIGHT-PLAN.md Intent (reversed in v1.3)
- FLIGHT-PLAN.md now shows "Intent + Anchors" (L0 Anchor document)
- Added txo-intent node (W-H-S skill that produces FLIGHT-PLAN.md)
- Updated txo-init to offer /txo-intent instead of template copy
- txo-takeoff loads Intent + Anchors as gauge
- Anchors feed into TMM, W-H-S, and Code (replaced Credo vocabulary role)
- Document map updated with txo-intent at position 0b

**v1.1** (2026-02-19):

- Added Bootstrap → txo-init → FLIGHT-PLAN.md init chain to main diagram
- Added FLIGHT-PLAN.md as Root Intent carrier in document map
- Updated "Reading the Graph" with init layer
- Document map expanded with positions -1, 0a, 0b

**v1.0** (2026-02-19):

- Initial flow diagram from session 4 of Post Quantum-Eidos Upstream walk
- Shows Credo → W-H-S/TMM circular → 4BM → Code pipeline
- Documents the upstream effect problem (TMM ↔ W-H-S circular, 4BM re-hammer)