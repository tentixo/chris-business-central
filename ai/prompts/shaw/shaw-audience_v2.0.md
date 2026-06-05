# Shaw Audience Transformation

**Version**: 2.0
**Purpose**: Load when transforming a document for a specific audience. Shapes AI behavior for audience adaptation.
**Companion**: `shaw-research_v2.0.md` (produces the Synthesis document that feeds into this)
**Definition**: `ai/skills/txo-terminology.md` (Shaw section)

---

## What This Is

This document is a prompt. Load it when transforming a Synthesis document (from W-H-S) or any source document into an audience-specific version. It tells the AI how to think about audiences as Intent-carriers.

The pipeline:

```
Research (W-H-S) → Synthesis document → THIS WORKFLOW → Audience documents
```

---

## Core Principle: Audience = Intent

Each audience type carries a different active Intent. The same source material has different Shaw-resolution for each audience — not because the information changes, but because the measurement basis changes.

This is not summarization. Summarization compresses uniformly. Audience transformation re-resolves through a different Intent.

---

## Five Audience Types

### Boss

**Intent**: WHY — strategic rationale, decision enablement.

**What they need**: Rationale, cost, timeline, risk, decision options. One page.

**Transformation pattern**: Aggressive compression (10:1). Extract WHY statements only. Add decision framework (Approve/Defer/Reject with trade-offs). Lead with recommendation (inverse pyramid). Bold key numbers.

**Shaw characteristics**: High Concentration (Sw/Sh). Every word earns its place. Remove HOW entirely. Keep WHAT only if decision-relevant.

**Structure**:

```
Recommendation (one sentence)
Cost | Timeline | Risk (one line)
Why This Matters (2-3 paragraphs)
Options with trade-offs
Decision Needed (what, by when)
Link to FOCUS doc (optional depth)
```

---

### Lead

**Intent**: WHAT — tactical plan, team coordination.

**What they need**: Context + action plan + dependencies + risks + success criteria.

**Transformation pattern**: Medium compression (3:1). Keep WHY (context) + WHAT (all). Remove deep theory and detailed HOW. Add phase breakdown, task assignments, timeline, risk table.

**Shaw characteristics**: Medium Concentration. Maintain technical depth (leads are technical). Include architecture diagrams. Map sections to work phases.

**Structure**:

```
Context & Rationale (WHY — brief)
Approach (WHAT — phased)
  Phase 1: Goal, tasks, dependencies, estimate
  Phase 2: ...
Architecture (diagram)
Risks & Mitigations (table)
Success Criteria (checklist)
Link to full research (optional)
```

---

### Worker

**Intent**: HOW — step-by-step implementation.

**What they need**: Instructions they can follow. Code examples. Troubleshooting. Checklists.

**Transformation pattern**: Expansion OK (1:1 or more). Keep all content. Add operational detail: numbered steps, copy-paste code blocks, expected outputs, error handling. More examples (principle → concrete instances).

**Shaw characteristics**: Full depth. High Perceptibleness (Sw/s) matters more than Concentration — worker needs to STUDY, not scan. Numbered steps, not prose.

**Structure**:

```
Prerequisites (checklist)
Background (WHY — one paragraph)
Overview (WHAT — one paragraph)
Step-by-Step Instructions (HOW — detailed)
  Step 1: Goal, instructions, expected output, troubleshooting
  Step 2: ...
Validation Checklist
```

---

### User

**Intent**: USE — get it working.

**What they need**: Enough to operate the thing. Not architecture (Boss), not implementation (Worker), not planning (Lead). "Install, configure, run, verify."

**Transformation pattern**: Selective extraction. Pull only what a user touches. Hide internals. Optimize for first-time success — the user has one chance before they give up.

**Shaw characteristics**: High Perceptibleness. Every sentence must move the user closer to a working state. If a paragraph doesn't help them USE it, cut it. Examples must be copy-paste runnable.

**Structure**:

```
What this is (one sentence)
Quick Start (install → configure → run → verify)
Configuration (what knobs exist, what they do)
Common Tasks (how to do X, Y, Z)
Troubleshooting (symptom → fix)
```

**Note**: This is the README.md audience. We have been creating READMEs implicitly without declaring what this audience needs. This definition makes it explicit.

---

### Student

**Intent**: BUILD codebook — construct understanding through effort.

**What they need**: Deliberate gaps. Not a complete answer — a structured path to discover the answer. Low accessible Shaw, high potential Shaw.

**Transformation pattern**: Anti-compression. Remove conclusions. Keep the questions that lead to conclusions. Present evidence without interpretation. Leave the synthesis as an exercise.

**Shaw characteristics**: Shaw Sequence applies — each pass through the material, the student's state (ρ) evolves, and marginal Shaw per pass diminishes as codebook builds. The transformation optimizes for CODEBOOK GROWTH, not information transfer.

**Structure**:

```
Context (enough to understand the problem space)
Key Observations (evidence, not conclusions)
Questions to Consider (Socratic prompts)
Exercise: [gap for student to fill]
Further Reading (for self-directed depth)
```

**The formal connection**: The student audience maps to Section 7 of the Shaw hypothesis paper (Codebook Dynamics and Gradual Shaw Extraction). Potential Shaw is fixed. Accessible Shaw rises per pass. The transformation controls how much is accessible on first read — deliberately less than full, forcing codebook construction.

---

## OVERVIEW + FOCUS Structure

For aggressive compression (>5:1), use progressive disclosure:

```
OVERVIEW.md (high Concentration — essential statements only)
├── Links to FOCUS docs:
│   ├── FOCUS-technical.md (deep dive — optional)
│   └── FOCUS-implementation.md (deep dive — optional)
```

- Boss reads OVERVIEW only (5 min)
- Lead reads OVERVIEW + relevant FOCUS docs (20 min)
- Worker reads everything (40 min)
- User reads Quick Start section only (2 min)
- Student works through exercises across all docs

---

## Entry Gate

Before transforming, gather:

1. **Source document** — path to Synthesis or source doc
2. **Target audience** — which of the five types (can be multiple)
3. **Constraints** — reading time, max length, specific needs
4. **Current problems** — what's wrong with the source for this audience (optional)

These parameters set the gauge for transformation.

---

## AI Behavior

**AI MUST**:

- Identify target audience Intent before writing
- Report before/after: word count, reading time, content mix (WHY/WHAT/HOW/USE)
- Validate against constraints (if "5 min read" was requested, output must fit)
- Preserve source accuracy — transformation changes FORM, not TRUTH

**AI MUST NOT**:

- Treat transformation as uniform summarization
- Invent information not in the source (except audience-specific framing: cost estimates, decision options)
- Skip the entry gate questions

**AI SHOULD**:

- Offer OVERVIEW+FOCUS for >5:1 compression
- Suggest multi-audience generation when appropriate
- Ask Human to validate: "Does this feel right for a Boss/Lead/Worker/User/Student?"

---

## Roles

**AI**: Performs the transformation within the declared audience Intent. Reports metrics. Does not decide which audience — Human chooses.

**Human**: Chooses target audience. Validates the transformation feels right for that audience. May override: "This is too sparse for a Lead" or "A User doesn't need this section."

---

## Version History

**v2.0** (2026-02-22):

- Rewritten from adaptation v1.0. Intent-driven audience model replaces metrics-heavy approach.
- Five audience types: Boss, Lead, Worker (carried from v1.0), User and Student (new).
- Removed: Statement counting, Shaw number calculations, calibration workflows, large document strategies.
- Kept: OVERVIEW+FOCUS progressive disclosure, audience transformation patterns, entry gate.
- Moved from `ai/decided/shaw/` to `ai/prompts/shaw/` (Box 2: Process).
- Concentration (Sw/Sh) and Perceptibleness (Sw/s) referenced as ratios, not computed.

**v1.0** (2025-12-25):

- Original adaptation flow (1230 lines). Boss/Lead/Worker only. Statement-counting metrics. Archived to `ai/decided/shaw/old/`.
