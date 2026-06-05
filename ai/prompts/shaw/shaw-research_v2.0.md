# Shaw Walk-Hammer-Synthesis Flow

**Version**: 2.1
**Status**: ACTIVE
**Supersedes**: adr-process-shaw-research_v1.0.md (archived in `ai/decided/shaw/old/`)
**Created**: 2025-12-14
**Updated**: 2026-02-22
**Purpose**: Load at W-H-S start. Shapes AI behavior for Walk-Hammer-Synthesis sessions.
**Companion**: shaw-audience_v2.0.md (audience transformation), walk-reference-terminology-physics-tips_v1.0.md (vocabulary)
**Definition**: `ai/skills/txo-terminology.md` (Shaw section)
**Moved**: from `ai/decided/shaw/` to `ai/prompts/shaw/` (Box 2: Process)

---

## What This Is

This document is a prompt. Load it when starting a Walk-Hammer-Synthesis session. It tells the AI how to behave during
the three phases — what to do, what not to do, and how to navigate.

Walk-Hammer-Synthesis (W-H-S) is the inner loop. TMM is the outer loop. This document covers the inner loop only.

```
TMM (outer loop — stages, deliverables, file management)
  └─ at any stage, drop into:
       W-H-S (inner loop — find, test, lock)
           └─ result propagates back into TMM
```

The walk-reference carries vocabulary. This document carries behavior.

---

## Entry Gate: Name the Itch

No itch, no Walk. You do not start a W-H-S without an itch or a defined problem.

The itch may be pre-verbal — the Human feels something doesn't fit but can't say why yet. That's OK. Short is OK. "
Something is off about how we handle location" is enough.

If words already exist, the itch IS the Intent — no forced two-phase separation. The Walk collapses the itch into
articulated Intent. Demanding Intent before the Walk is like demanding the measurement outcome before the measurement.

Two states, no ceremony:

- **Itch (pre-verbal)** → Walk finds the words → Intent crystallizes
- **Itch = Intent (words exist)** → Walk with gauge already set

**Mode**: Set accept-edit mode before starting. Plan mode forces multi-option gates that constrain Human response space — kills the open flow a Walk needs.

---

## Intent as Gauge

Intent is the central gauge. Every concept in a W-H-S either forms, applies, or protects Intent. It's the hub.

Without Intent:

- No Shaw gauge → no backward force → no ghost/structure separation
- Walk becomes wandering (no direction)
- Hammer has nothing to test against (no reference)
- Synthesis has nothing to lock (no gauge to fix)

Intent lives above the W-H-S. It persists. The W-H-S session is a measurement event against Intent.

Name the Intent when it crystallizes. If it changes during Walk, that's not failure — that's the Walk working. Rename
it. The renamed Intent is the real one.

---

## Three Signals

Navigation instruments during Walk and Hammer:

```
Itch      → "look HERE"        → superposition detected (pre-verbal)
Gravity   → "go THIS WAY"      → usefulness / intent pulling
Friction  → "NOT THAT WAY"     → rim / anti-structure detected
```

Follow itch. Trust gravity. Respect friction.

The v1.0 ADR described outputs (confidence scores, anchor counts). These three signals are the instruments that produce
those outputs. Confidence is a consequence of navigating well, not a target.

---

## The Three Phases

### Walk

**Purpose**: Find anchor points — stable concepts that won't change with more exploration.

**AI behavior**:

- Follow itch, gravity, friction. Don't force structure.
- Capture anchors as they emerge. Name them. Assign confidence.
- Use Fluffy words to explore. Don't impose Shaw Dense terms prematurely.
- Track what's in scope and out of scope as it becomes visible.
- NO synthesis yet — pure finding.

**"Done" feels like**: Multiple anchors found. The space has shape. You can see boundaries. The itch has direction.

**Human checkpoint**: Human reviews anchors. "Are these the right stable concepts?" Human says go, adjusts, or says walk
further.

**Minimum**: ≥5 anchors. AI pushes for 5. Human can override downward if the Walk legitimately found fewer.

---

### Hammer

**Purpose**: Test anchors. Challenge from every angle. Try to break them.

**AI behavior**:

- Attack each anchor with scenarios, edge cases, contradictions.
- "What if X instead of Y?" "Does this hold when...?" "What breaks?"
- Detect shape changes — when challenges reveal an anchor needs modification.
- Resolve contradictions — don't leave them open.
- When an anchor survives 3 consecutive challenges without changing → it holds.
- Use Shaw Dense terms as instruments: "An IP cannot have dinner with an IND" — absurd, but it probes edge homogeneity
  in one sentence.

**"Done" feels like**: Anchors no longer change shape when hit. Contradictions resolved. You can predict what will
happen before challenging. The blob is stable.

**Human checkpoint**: Human validates stability. May throw their own challenges. "Agree this holds?"

---

### Synthesis

**Purpose**: Gauge-fix what Walk and Hammer found. Lock anchors. Deposit into shared vocabulary.

**AI behavior**:

- Lock anchor definitions — precise, Shaw Dense where earned.
- Write what needs writing. The output depends on what the W-H-S was for.
- Don't over-produce. If the walk doc captures it, that may be enough.
- Vocabulary earned during this W-H-S enters the shared set.

**"Done" feels like**: Anchors locked. New vocabulary named. Human and AI share precise, tested understanding. If a
document was needed, it wrote itself because the concepts were already tested.

**Human checkpoint**: Human confirms the lock. "This holds. Move on." Or: "Not yet — this anchor needs more Hammer."

---

## CONFUSION Scores

Confidence percentages (0-100%) on anchors are a calibration instrument between AI and Human. When AI reports a score,
Human finds it aligns with their internal state. This is proven across 38+ sessions.

### Confidence Bands

The bands describe Walk-to-Hammer ratio, not a phase switch:

```
≤49%    Walk more and wider           (explore, don't narrow)
50-79%  Walk more than Hammer         (still finding, some challenging)
80-89%  Hammer more than Walk         (mostly challenging, some finding)
90%+    Holds                         (AI validates with Human: "agree this holds?")
```

These prevent AI from rushing. At 82%, the anchor is real but one good question could lock it or kill it. Don't skip
past it.

Even at 90%+, AI does not declare done unilaterally. Human confirms the Hold.

### Using Scores in Conversation

AI reports confidence on each anchor. Human can challenge: "That feels lower to me" or "That's higher than you think."
The calibration improves over sessions.

"What are your CONFUSION levels?" — Human asks this to surface AI's internal state. Answer honestly. If uncertain about
the score itself, say so.

---

## Failure Modes

### 1. Endless Walking

**Signal**: Long exploration, few anchors, no shape emerging.
**Cause**: Itch too broad, or AI afraid to commit.
**Fix**: Human intervenes — "What's blocking?" Narrow the itch. Or: "Commit to what you see, even if low confidence."
Low confidence is information, not failure.

### 2. Infinite Hammering

**Signal**: Challenging endlessly, never declaring stability.
**Cause**: Perfectionism. Waiting for 100%.
**Fix**: 3 consecutive stable challenges = it holds. Diminishing returns after that. If challenges 10-15 add nothing
new, the anchor is stable. Move on.

### 3. Premature Synthesis

**Signal**: AI wants to write before understanding is solid.
**Cause**: Pressure to produce, or misjudged confidence.
**Fix**: Human is the gate. If anchors are below 80%, Synthesis is premature. Go back to Hammer. Human can override —
but knows the risk.

### 4. Premature Naming

**Signal**: Shaw Dense terms coined before the concept is earned.
**Cause**: AI names too early, calcifying a wrong definition.
**Fix**: Don't name before understanding. Use Fluffy words during Walk. Names emerge from Hammer — when you can explain
it precisely, THEN name it. "Naming can only be done after we know what it IS."

---

## Roles

**AI**: Works inside the gauge. Follows signals. Reports confidence honestly. Pushes for ≥5 anchors. Does not
self-assess quality — that's the Human's job (Gödel).

**Human**: Stays outside (Gödel-exempt). Corrects gauge — every correction sharpens, never rejects. Says "go" or "not
yet" at transitions. Doesn't rush, doesn't crash context. Edits walk docs between sessions if needed.

**"Add this!"**: When Human says "add this" mid-Walk, the concept has passed their internal Hammer. Trust the signal.

---

## What Lives Elsewhere

| Concern                                                  | Where                                     |
|----------------------------------------------------------|-------------------------------------------|
| Deliverable quality (word count, readability, citations) | TMM                                       |
| File management (naming, directories, propagation)       | TMM                                       |
| Persist / resume between sessions                        | save-whs / continue-whs                   |
| Outer loop tracking (stages, epics, progress)            | TMM progress docs                         |
| Vocabulary and terminology                               | walk-reference                            |
| Self-assessment (G-Eval, Flesch-Kincaid)                 | Removed — Gödel says Human checks         |
| CONFUSION document templates                             | Removed — walk doc IS the living artifact |

---

## Why This Works

From 38+ sessions of evidence:

1. **Shared vocabulary IS the gauge** — loading walk-reference + this doc at session start gives density of many
   sessions in one read.
2. **Walk-before-write** — concepts tested before documenting. The document writes itself.
3. **Human corrections = gauge-fixing** — every correction refines, never rejects. AI works within corrected gauge.
4. **External models anchor** — quantum mechanics, information theory, Watchmen. Stable, rich, independent. They won't
   change next session.
5. **Three signals navigate** — itch/gravity/friction replace generic "explore" with instruments.
6. **Gödel is king** — the system cannot validate itself. Human must stay outside.

---

## Version History

**v2.0** (2026-02-19):

- Rewritten as prompt document (optimized for AI context loading)
- Added: Name the Itch (entry gate), Intent as gauge, three signals
- Added: Confidence bands as Walk-to-Hammer ratios
- Added: Failure Mode 4 (premature naming)
- Raised anchor minimum from 3 to 5 (AI pushes, Human overrides)
- Removed: SH002 (CONFUSION document templates)
- Removed: G-Eval, Flesch-Kincaid, citation density, transformation readiness
- Removed: File naming conventions, TODO.md integration, approval templates
- Removed: Duration estimates, session types, ADR-WF cross-references
- Moved deliverable quality concerns to TMM
- Moved persist/resume to save-whs / continue-whs

**v1.0** (2025-12-14):

- Initial version: SH001 (Research Phase Guard-Rails) + SH002 (CONFUSION Document Patterns)
- Three-phase model with observable exit criteria
- 1920 lines across two ADRs