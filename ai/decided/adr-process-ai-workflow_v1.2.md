# AI-Human Workflow Architecture Decision Record v1.2

**Status**: ACTIVE
**Purpose**: Define tactical and strategic AI-Human collaboration patterns for multi-session work
**Companion To**: [Beads](https://github.com/steveyegge/beads) (operational task tracking with Epic/Task/Sub-task hierarchy)
**Audience**: AI assistants, human developers, framework maintainers
**RFC 2119**: This document uses MUST, SHOULD, MAY, MUST NOT, SHOULD NOT per [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt)
**Created**: 2025-10-01
**Updated**: 2026-02-21  

---

## Introduction and Scope

This ADR defines the tactical and strategic layers of AI-human collaboration. It complements Beads, which handles
operational-level task tracking.

### ADR Format Standard

This document
follows [Michael Nygard's ADR format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) with
adaptations:

**Standard sections we follow**:

- **Status**: MANDATORY / RECOMMENDED / OPTIONAL / DEPRECATED
- **Context**: Why this decision is needed
- **Decision**: What we decided
- **Consequences**: Positive, Negative, Mitigation

**Our additions**:

- **Implementation**: How-to guidance and examples
- **Version History**: Change tracking (see ADR-WF002)
- **Metadata footer**: Version, Domain, Purpose

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ ANCHOR       │ Project identity, Intent, load-bearing Anchors   │ ← FLIGHT-PLAN.md (WHY and WHAT)
├──────────────┼──────────────────────────────────────────────────┤
│ STRATEGIC    │ Multi-session planning, Architecture decisions   │ ← PROJECT-STATUS.md, TODO.md
├──────────────┼──────────────────────────────────────────────────┤
│ TACTICAL     │ Session management, Risk assessment, Sync points │ ← THIS ADR (HOW)
├──────────────┼──────────────────────────────────────────────────┤
│ OPERATIONAL  │ Individual tasks, Dependencies, `bd ready`       │ ← BEADS
└─────────────────────────────────────────────────────────────────┘
```

**This ADR Covers**:

- When and how to checkpoint work for session resume
- Risk classification and human approval requirements
- Document lifecycle and naming conventions
- Integration with Beads for operational tracking

**Beads Covers**:

- Individual task creation and tracking (`bd create`, `bd update`)
- Task dependencies (blocks, parent, related, discovered-from)
- Finding next actionable work (`bd ready`)
- Git-based sync across sessions

---

## ADR-WF000: Work Hierarchy Terminology

**Status**: MANDATORY

### Context

AI-human collaboration requires clear terminology for work levels. Terms like "epic", "task", "story" are overloaded and
carry baggage from various frameworks. We need unambiguous terms that integrate with Beads operational tracking.

### Decision

Use **Bead-extended terminology** with five levels:

| Level  | Term         | Scope                                  | Tracked In                                | Duration     |
|--------|--------------|----------------------------------------|-------------------------------------------|--------------|
| **L0** | **Anchor**   | Project identity, Intent, Anchors      | `FLIGHT-PLAN.md` (Intent + Anchors)       | Project life |
| **L1** | **Strand**   | Full project or initiative             | `ai/PROJECT-STATUS.md`                    | Weeks-months |
| **L2** | **Cluster**  | Phase, milestone, or major deliverable | `ai/TODO.md` + Beads Epic                 | Days-weeks   |
| **L3** | **Bead**     | Individual actionable task             | Beads Task (`bd`)                         | Hours-days   |
| **L4** | **Sub-bead** | Complex task breakdown                 | Beads Sub-task                            | Hours        |

#### Beads Hierarchy Mapping

Beads supports hierarchical IDs that map to TXO levels:

| TXO Level | Beads Level | ID Format     | Example                       |
|-----------|-------------|---------------|-------------------------------|
| Anchor    | -           | -             | FLIGHT-PLAN.md                |
| Strand    | -           | -             | ai/PROJECT-STATUS.md          |
| Cluster   | Epic        | `bd-xxxx`     | `txo-ai-htr` and `ai/TODO.md` |
| Bead      | Task        | `bd-xxxx.N`   | `txo-ai-htr.1`                |
| Sub-bead  | Sub-task    | `bd-xxxx.N.M` | `txo-ai-htr.1.1`              |

**Creating hierarchical Beads:**

```bash
# Create Epic (Cluster level)
bd create --title="Feature X" --type=feature

# Create Task under Epic (Bead level)
bd create --title="Implement component" --type=task --parent=bd-xxxx

# Create Sub-task (Sub-bead level, for complex Tasks)
bd create --title="Add validation" --type=task --parent=bd-xxxx.1
```

#### Definitions

**Strand** (L1 - Strategic):

- A complete project or significant initiative
- Has defined start and end
- Contains multiple Clusters
- Documented in `FLIGHT-PLAN.md` (workflow) and `ai/PROJECT-STATUS.md` (status)
- Example: "AI Workflow Framework v1.0", "Database Migration"

**Cluster** (L2 - Tactical):

- A phase, milestone, or coherent group of work
- Achieves a meaningful intermediate goal
- Contains multiple Beads
- Tracked in `ai/TODO.md` (prose) and Beads Epic (operational)
- Example: "Resume Protocol Implementation", "Hard Rules Enforcement"

**Bead** (L3 - Operational):

- Individual actionable task
- Can be completed in one session
- Managed by Beads tool (`bd create`, `bd ready`)
- Example: "Create /nudge command", "Update CLAUDE.md"

**Sub-bead** (L4 - Breakdown):

- Breakdown of complex Beads
- Used when a Bead turns out to be larger than expected
- Managed by Beads tool with hierarchical IDs
- Example: "Add input validation", "Write unit tests"

#### Layer Mapping

```
┌─────────────────────────────────────────────────────────────────────────┐
│ STRAND    │ Full project          │ FLIGHT-PLAN.md + PROJECT-STATUS.md  │
├───────────┼───────────────────────┼─────────────────────────────────────┤
│ CLUSTER   │ Phase/milestone       │ TODO.md + Beads Epic (bd-xxxx)      │
├───────────┼───────────────────────┼─────────────────────────────────────┤
│ BEAD      │ Individual task       │ Beads Task (bd-xxxx.N)              │
├───────────┼───────────────────────┼─────────────────────────────────────┤
│ SUB-BEAD  │ Complex breakdown     │ Beads Sub-task (bd-xxxx.N.M)        │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Communication Patterns

When transitioning between levels, AI MUST clearly signal:

**Starting a new Strand:**

```
Starting new Strand: "AI Workflow Framework v1.0"
This will involve multiple Clusters over several sessions.
```

**Starting a new Cluster:**

```
Starting Cluster: "Hard Rules Enforcement"
Part of Strand: "AI Workflow Framework v1.0"
This Cluster contains ~5 Beads.
```

**Completing a Cluster:**

```
Cluster complete: "Hard Rules Enforcement"
- 5/5 Beads done
- Deliverables: ADR-WF016, /nudge command, global hard-rules.md
Next Cluster: [name] or Strand complete
```

### Implementation

AI MUST:

1. Use Strand/Cluster/Bead/Sub-bead terminology consistently
2. Signal when transitioning between levels
3. Track Strands in FLIGHT-PLAN.md (workflow) and PROJECT-STATUS.md (status)
4. Track Clusters in TODO.md (prose) and reference Beads Epic ID
5. Track Beads and Sub-beads in Beads tool with hierarchical IDs

AI SHOULD:

1. Estimate number of Clusters in a Strand at start
2. Estimate number of Beads in a Cluster at start
3. Update estimates as work progresses
4. Create Sub-beads when a Bead becomes unexpectedly complex
5. Use `bd show <epic-id>` to view Epic with all Tasks

### Consequences

**Positive**:

- Unambiguous hierarchy (no "task" confusion)
- Extends Beads metaphor naturally
- Clear layer separation
- Easy to communicate level transitions

**Negative**:

- New terminology to learn
- Not industry-standard (intentional)

---

## ADR-WF001: Risk Classification

**Status**: MANDATORY

### Context

AI-human collaboration involves varying levels of risk. Without clear classification, teams either over-approve (slowing
progress) or under-approve (risking mistakes).

### Decision

Projects and tasks MUST be classified into three risk levels based on three factors:

| Factor            | Description                          |
|-------------------|--------------------------------------|
| **Reversibility** | How easily can changes be undone?    |
| **Messiness**     | How much cleanup if things go wrong? |
| **Uncertainty**   | How much is unknown or ambiguous?    |

### Risk Matrix

| Level      | Reversibility | Messiness | Uncertainty | Examples                                                |
|------------|---------------|-----------|-------------|---------------------------------------------------------|
| **LOW**    | High          | Low       | Low         | Documentation, schemas, config files                    |
| **MEDIUM** | Medium        | Medium    | Medium      | Feature additions, refactoring, known-bad external docs |
| **HIGH**   | Low           | High      | High        | Architecture changes, migrations, messy legacy cleanup  |

### Human Experience Modifiers

The human MAY adjust risk level based on experience:

- **Familiar domain**: Consider -1 risk level
- **Unfamiliar domain**: Consider +1 risk level
- **Time pressure**: Consider +1 risk level
- **Clear prior art**: Consider -1 risk level

### Implementation

AI MUST:

1. Assess risk level at session start (if not already classified)
2. State the assessed risk level to the human
3. Follow approval requirements per ADR-WF004

Human SHOULD:

1. Confirm or adjust the risk classification
2. Provide context for adjustments

### Consequences

**Positive**:

- Clear expectations for approval cadence
- Appropriate oversight without bottlenecks
- Shared vocabulary for discussing risk

**Negative**:

- Initial assessment takes time
- Risk may change mid-project (re-assessment needed)

---

## ADR-WF002: Document Lifecycle

**Status**: MANDATORY

### Context

AI-human collaboration produces many documents with different lifespans. Without clear lifecycle rules, temporary
documents persist and permanent documents get lost.

### Decision

Documents fall into four categories with distinct lifecycles:

#### 1. Session Notes (Temporary, AI-focused)

- **Location**: `ai/working/`
- **Format**: `UPPERCASE_YYYY-MM-DD.md`
- **Examples**: `SESSION-NOTES_2025-12-05.md`, `CONFUSION_2025-12-05.md`
- **Created**: Start of session (or when needed)
- **Updated**: Throughout session
- **Archived**: After content captured in permanent docs or no longer needed

#### 2. Session Reports (Permanent, Human-readable)

- **Location**: `ai/reports/`
- **Format**: `kebab-case_YYYY-MM-DD.md`
- **Examples**: `session-summary_2025-12-05.md`, `gap-analysis_2025-12-05.md`
- **Created**: End of session
- **Updated**: Rarely (corrections only)
- **Archived**: Move to `ai/reports/old/` when superseded

#### 3. Working Documents (Temporary, Session state)

- **Location**: `ai/` (root level)
- **Format**: `UPPERCASE.md` (no date for frequently-updated)
- **Examples**: `TODO.md`, `PROJECT-STATUS.md`, `READY-FOR-NEXT-SESSION.md`
- **Created**: When multi-session work begins
- **Updated**: Continuously
- **Archived**: After project completion

#### 4. Decided Documents (Permanent, Versioned)

- **Location**: `ai/decided/`, `ai/prompts/`
- **Format**: `kebab-case_vX.Y.md`
- **Examples**: `workflow-patterns_v1.0.md`, `refactoring-prompt_v2.1.md`
- **Created**: When decision is made
- **Updated**: New version created (old moved to `old/`)
- **Archived**: Move to `old/` subdirectory when superseded

### Version History Pattern

**Filename versioning** (major.minor only):

- Filename includes major.minor: `doc_v3.2.md`
- Patch versions (3.2.1) do NOT change filename
- Patch changes tracked in internal Version History section

**Internal Version History** (required in permanent docs):

```markdown
## Version History

### v3.2 (Current)

- Added [new feature]
- Enhanced [existing feature]

### v3.1.1

- Fixed [bug]
- Clarified [section]

### v3.1

- Initial version for this major release

---

**Version:** v3.2
**Last Updated:** YYYY-MM-DD
**Domain:** [Domain]
**Purpose:** [Purpose]
```

**Versioning rules**:

- **Major** (v1 → v2): Breaking changes, incompatible updates
- **Minor** (v1.0 → v1.1): New content, backward-compatible additions
- **Patch** (v1.1 → v1.1.1): Corrections, typo fixes, clarifications

**Version synchronization**:

- All project docs SHOULD use same version as git tag
- At release: `doc_v3.1.md` → `doc_v3.2.md` (rename file)
- Patch during release: Update internal Version History only

### Implementation

AI MUST:

1. Use correct naming format for document type
2. Place documents in correct directory
3. Update `READY-FOR-NEXT-SESSION.md` at session end (if multi-session)

Human SHOULD:

1. Archive completed working documents
2. Review session reports for accuracy

### Consequences

**Positive**:

- Clear visual distinction (UPPERCASE = temporary, kebab-case = permanent)
- Easy to find current vs historical documents
- Predictable locations

**Negative**:

- Requires discipline to archive
- Date suffix requires updates if work spans days

---

## ADR-WF003: Resume Protocol

**Status**: MANDATORY

### Context

Restarting a Claude Code session loses all in-memory context. Without a resume protocol, AI must re-read everything (
wasting tokens) or miss critical context (causing errors).

### Decision

AI MUST follow this hierarchical resume protocol:

#### Level 1: Quick Context (30 seconds - ALWAYS)

```
IF ai/READY-FOR-NEXT-SESSION.md exists:
    Read it first (contains compressed state)
ELSE IF ai/PROJECT-STATUS.md exists:
    Read it (contains high-level state)
ELSE:
    Ask human: "Is this a new project or resuming existing work?"

ALSO check for FLIGHT-PLAN.md in project root:
    If exists, read for mission context and current workflow step
```

#### Level 2: Current State (1-2 minutes - IF multi-session)

```
Read ai/TODO.md (task status, what's next)
Run `bd ready` (operational tasks from Beads)
Scan ai/working/CONFUSION-*.md (open questions)
```

#### Level 3: Deep Context (only if needed)

```
Read ai/reports/session-summary_*.md (latest)
Read relevant ai/decided/*.md documents
```

#### Level 4: Verify & Confirm

```
State to human: "Last session ended at [X], next task is [Y]"
Ask: "Continue from here, or reassess?"
```

### Token Optimization Rules

AI SHOULD:

1. Read hierarchically (quick → current → deep), stop when sufficient
2. Reference documents by filename rather than re-reading content
3. Use `READY-FOR-NEXT-SESSION.md` as compressed state
4. Read `FLIGHT-PLAN.md` for mission context if it exists

AI MUST NOT:

1. Read entire codebase on resume
2. Re-read documents already summarized in session notes
3. Read files in `old/` directories (unless explicitly instructed)

### READY-FOR-NEXT-SESSION.md Template

```markdown
# Ready for Next Session

**Last Updated**: YYYY-MM-DD HH:MM
**Risk Level**: LOW|MEDIUM|HIGH

## Where We Left Off

[1-2 sentences: last completed task, current state]

## Next Task

[Specific next action to take]

## Key Files to Read (if needed)

- [path/to/file1.md] - [why]
- [path/to/file2.md] - [why]

## Open Questions

- [Question needing human input]

## Beads Status

- Run `bd ready` for operational tasks
- [N] tasks in progress
```

### Consequences

**Positive**:

- Resume in < 2 minutes vs 10+ minutes
- Token-efficient (hierarchical reading)
- Human always knows current state

**Negative**:

- Requires discipline to create READY-FOR-NEXT-SESSION.md
- May miss context if documents not updated

---

## ADR-WF004: AI-Human Sync Points

**Status**: MANDATORY

### Context

AI needs human input at certain points, but over-asking slows progress and under-asking risks mistakes.

### Decision

Sync points are categorized by type and required based on risk level:

#### Sync Point Types

| Type             | Behavior                    | Examples                                 |
|------------------|-----------------------------|------------------------------------------|
| **APPROVAL**     | Blocking - AI waits         | Architecture decisions, breaking changes |
| **NOTIFICATION** | Non-blocking - AI continues | Task completion, document creation       |
| **VALIDATION**   | Async - Human reviews later | Confusion documents, deliverables        |

#### Sync Points by Risk Level

| Action                | LOW                  | MEDIUM               | HIGH                   |
|-----------------------|----------------------|----------------------|------------------------|
| Start work            | MAY notify           | SHOULD seek approval | MUST seek approval     |
| Phase transition      | MAY notify           | SHOULD seek approval | MUST seek approval     |
| Breaking change       | SHOULD seek approval | MUST seek approval   | MUST seek approval     |
| Architecture decision | SHOULD seek approval | MUST seek approval   | MUST seek approval     |
| Create confusion doc  | MUST notify          | MUST notify          | MUST notify            |
| Complete deliverable  | MAY notify           | SHOULD notify        | MUST notify + validate |

### Implementation

AI MUST:

1. Identify sync point type for current action
2. Check risk level for required behavior
3. Follow the required sync pattern

AI SHOULD:

1. Batch notifications where practical (end of phase vs every task)
2. Provide context in approval requests (not just "can I proceed?")

### Approval Request Format

```
## Approval Needed: [Action Type]

**Risk Level**: [LOW|MEDIUM|HIGH]
**Action**: [What AI wants to do]
**Impact**: [What will change]
**Alternatives**: [Other options considered]
**Recommendation**: [AI's suggested approach]

Proceed with this approach?
```

### Consequences

**Positive**:

- Right level of oversight for risk
- Clear expectations both ways
- Documented decision points

**Negative**:

- May feel bureaucratic for LOW risk
- Requires human availability for HIGH risk

---

## ADR-WF005: Beads Integration

**Status**: MANDATORY

### Context

Beads provides excellent operational task tracking. This ADR must complement, not duplicate, that functionality.

### Decision

Clear separation of concerns between Beads and this workflow:

#### Beads Handles (Operational)

- Epics (Cluster level) with hierarchical IDs
- Tasks and Sub-tasks (Bead level)
- Task dependencies (blocks, parent, related, discovered-from)
- Finding next work (`bd ready`)
- Task status (open, in_progress, closed)
- Hierarchical IDs: `bd-xxxx` (Epic), `bd-xxxx.N` (Task), `bd-xxxx.N.M` (Sub-task)

#### This ADR Handles (Tactical/Strategic)

- Session management and checkpoints
- Risk classification and approval workflows
- Document lifecycle and naming
- Resume protocols
- Meta-work tracking (done-done)

#### When to Use Each

| Scenario                   | Use Beads | Use ai/TODO.md | Use FLIGHT-PLAN.md |
|----------------------------|-----------|----------------|--------------------|
| Project mission/workflow   | MAY       | MAY            | SHOULD             |
| Cluster/Epic               | SHOULD    | SHOULD         | SHOULD (list)      |
| Individual coding task     | MUST      | MAY            | -                  |
| Multi-step feature         | MUST      | SHOULD         | -                  |
| Session tracking           | MAY       | MUST           | -                  |
| Task dependencies          | MUST      | SHOULD NOT     | -                  |
| Meta-work (docs, versions) | MAY       | MUST           | -                  |
| Resume context             | MAY       | MUST           | -                  |
| Human workflow steps       | MAY       | -              | MUST               |

#### Epic Sync Strategy (Loose)

Epics are tracked in **both** TODO.md (prose) and Beads (state), with loose coupling:

- TODO.md contains Epic **narrative** (why, context, rationale)
- Beads Epic contains **operational state** (status, tasks, dependencies)
- Reference Epic ID in TODO.md: `Epic: txo-ai-htr - AI Workflow v1.1`
- No strict validation required (loose sync)

#### Integration Pattern

```
Session Start:
1. Read ai/TODO.md (tactical state)
2. Run `bd ready` (operational tasks)
3. Combine for complete picture

During Work:
1. Update Beads for individual tasks (`bd update`, `bd close`)
2. Update TODO.md for phase/session progress

Session End:
1. Update TODO.md with session summary
2. Create READY-FOR-NEXT-SESSION.md
3. Beads auto-syncs via Git
```

#### Claude Code and Beads

Beads is a CLI tool. Claude Code can execute Beads commands directly via Bash - no separate terminal needed for basic
operations.

**Commands Claude Code can run**:

```bash
# Check actionable tasks
bd ready

# Create Epic (Cluster level)
bd create --title="Feature X" --type=feature

# Create Task under Epic (Bead level)
bd create --title="Implement component" --type=task --parent=bd-xxxx

# Create Sub-task (Sub-bead level)
bd create --title="Add validation" --type=task --parent=bd-xxxx.1

# View Epic with all children
bd show bd-xxxx

# Update task status
bd update bd-xxxx.1 --status in_progress

# Close a task with reason
bd close bd-xxxx.1 --reason "Implemented in commit abc123"

# Close multiple tasks at once
bd close bd-xxxx.1 bd-xxxx.2 bd-xxxx.3

# Add dependency
bd dep add bd-xxxx.2 bd-xxxx.1  # Task 2 depends on Task 1

# List all tasks
bd list
```

**Setup requirement**: Run `bd init` once in your project (creates `.beads/` directory).

**What requires separate terminal**:

- Beads daemon for continuous auto-sync (optional)
- Interactive commands (if any)
- Monitoring/watching task changes in real-time

**Practical workflow**:

| Action            | Who runs it | Where                        |
|-------------------|-------------|------------------------------|
| `bd init`         | Human       | Terminal (once)              |
| `bd ready`        | AI or Human | Claude Code or Terminal      |
| `bd create`       | AI          | Claude Code (during work)    |
| `bd update`       | AI          | Claude Code (during work)    |
| `bd close`        | AI          | Claude Code (task complete)  |
| Daemon monitoring | Human       | Separate terminal (optional) |

### Consequences

**Positive**:

- No duplication of task tracking
- Right tool for right level
- Clear integration points

**Negative**:

- Two systems to learn
- Must keep both in sync

---

## ADR-WF006: Skills Recommendations

**Status**: RECOMMENDED

### Context

Claude Code Skills enable reusable workflows. AI should help identify when Skills would be valuable.

### Decision

AI SHOULD recommend Skill creation when detecting these patterns:

#### Trigger Patterns

1. **Repeated workflow** (3+ times same steps)
2. **Complex multi-file operation**
3. **Domain-specific expertise required**
4. **Context-heavy operation** (needs significant setup)

#### Recommendation Format

```
I notice we've done [X] several times. Consider creating a Skill:

**Skill Name**: [suggested-name]
**Trigger**: [when it should activate]
**Files/Context Needed**: [list]

Would you like me to help draft a skill definition?
```

#### Skill vs Slash Command Decision

| Feature        | Slash Command   | Skill               |
|----------------|-----------------|---------------------|
| Invocation     | Manual (`/cmd`) | Can be automatic    |
| Complexity     | Simple prompt   | Multi-step workflow |
| Context needed | Minimal         | Extensive           |
| Files          | Single .md      | Can be directory    |

### Skill Discovery Process

Use `/discover-skill` command to initiate conversational discovery:

1. AI asks about workflow frequency
2. AI asks about trigger conditions
3. AI asks about required context
4. Together, draft skill definition

### Consequences

**Positive**:

- Captures repeated workflows
- Reduces future token usage
- Builds project-specific tooling

**Negative**:

- Overhead to create and maintain
- May create too many Skills

---

## ADR-WF007: Directory Structure

**Status**: MANDATORY

### Context

Consistent directory structure enables predictable document locations across projects.

### Decision

Standard `ai/` subdirectory structure:

```
ai/
├── decided/           # Permanent decisions (kebab-case_vX.md)
│   └── old/          # Archived versions
├── prompts/           # AI prompt templates (kebab-case_vX.md)
│   └── old/          # Archived versions
├── reports/           # Permanent reports (kebab-case_YYYY-MM-DD.md)
│   └── old/          # Archived reports
├── working/           # Temporary session files (UPPERCASE_YYYY-MM-DD.md)
│   └── old/          # User-archived session files
├── TODO.md            # Current task list
├── PROJECT-STATUS.md  # High-level status
└── READY-FOR-NEXT-SESSION.md  # Resume helper
```

### Directory Purposes

| Directory  | Purpose                     | Naming                   | Lifecycle            |
|------------|-----------------------------|--------------------------|----------------------|
| `decided/` | Approved decisions, ADRs    | kebab-case_vX.Y.md       | Permanent, versioned |
| `prompts/` | AI prompt templates         | kebab-case_vX.Y.md       | Permanent, versioned |
| `reports/` | Session summaries, analyses | kebab-case_YYYY-MM-DD.md | Permanent            |
| `working/` | Session notes, drafts       | UPPERCASE_YYYY-MM-DD.md  | Temporary            |
| `old/`     | Superseded documents        | Original name            | Archive              |

### Implementation

AI MUST:

1. Create directories as needed (with `.gitkeep`)
2. Place documents in correct directory
3. Never read from `old/` without explicit instruction

Human SHOULD:

1. Periodically archive working documents
2. Clean up old/ directories

### Consequences

**Positive**:

- Predictable locations
- Clear lifecycle by location
- Easy to ignore old/

**Negative**:

- Initial setup required
- Must remember structure

---

## ADR-WF008: Pre/Post Coding Workflow

**Status**: RECOMMENDED

### Context

AI collaboration includes architecture, design, ERD creation, and documentation—not just coding. These phases need the
same workflow patterns.

### Decision

All phases use the same workflow patterns:

#### Phase Types

| Phase           | Examples                       | Typical Risk |
|-----------------|--------------------------------|--------------|
| **Pre-coding**  | Architecture, ERD, API design  | MEDIUM-HIGH  |
| **Coding**      | Implementation, refactoring    | MEDIUM       |
| **Post-coding** | Review, documentation, release | LOW-MEDIUM   |

#### Phase-Specific Documents

**Pre-Coding**:

- `DESIGN-NOTES_YYYY-MM-DD.md` (working/)
- `{project}-architecture-adr_vX.md` (decided/, after approval)
- Format: `txo-{context}-adr_vX.md` where context = workflow, python, architecture, etc.
- `erd-draft_YYYY-MM-DD.md` (working/, until approved)

**Post-Coding**:

- `REVIEW-NOTES_YYYY-MM-DD.md` (working/)
- `release-notes_vX.md` (reports/)
- `migration-guide_vX.md` (decided/)

### Same Patterns Apply

- Risk classification (ADR-WF001)
- Resume protocol (ADR-WF003)
- Sync points (ADR-WF004)
- Document lifecycle (ADR-WF002)

### Consequences

**Positive**:

- Consistent workflow across phases
- No context-switching for different work types
- Architecture decisions tracked same as code decisions

**Negative**:

- May feel heavyweight for simple docs

---

## ADR-WF009: Done Levels

**Status**: MANDATORY

### Context

"Done" is ambiguous. Code working is not the same as code reviewed, documented, and released.

### Decision

Three explicit completion levels:

#### Level 1: Done (Work Product Level)

- Work product complete (code, doc, design)
- Tests pass (if applicable)
- Tracked in: `ai/TODO.md`, Beads

#### Level 2: Done-Done (Meta Level)

- All work products complete
- Documentation updated
- ADRs updated if needed
- Versions synchronized
- Session summary created
- Tracked in: `ai/PROJECT-STATUS.md`

#### Level 3: Done-Done-Done (Published Level)

- Git commit with comprehensive message
- Merged to main branch (if using feature branches)
- Git tag (if release) - applied to main branch after merge
- GitHub Release (if applicable) - uses release-notes as description
- Working files archived/deleted
- Pushed to remote (if applicable)
- `READY-FOR-NEXT-SESSION.md` cleared or removed

**Git Tag vs GitHub Release**:

- **Git tag**: Lightweight marker on commit (`git tag v1.0`)
- **GitHub Release**: Rich UI with release notes, assets, downloads
- **Workflow**: Merge → Tag on main → Create GitHub Release from tag
- **Release notes**: Use `ai/reports/release-notes_vX.Y.md` as GitHub Release description

### Implementation

AI MUST NOT:

- Claim work complete until Level 1 (Done) confirmed
- Skip reminding human about Levels 2-3

AI SHOULD:

- Track which level is current in PROJECT-STATUS.md
- Provide checklist for Level 2 and 3 items

### Done-Done Checklist Template

```markdown
## Done-Done Checklist

### Level 1: Done ✅

- [x] Work product complete
- [x] Tests pass

### Level 2: Done-Done

- [ ] Documentation updated
- [ ] ADRs updated (if applicable)
- [ ] Version numbers synchronized
- [ ] Session summary created
- [ ] Working docs archived

### Level 3: Done-Done-Done

- [ ] Git commit created
- [ ] Git tag created (if release)
- [ ] Pushed to remote
- [ ] Working files cleaned up
```

### Consequences

**Positive**:

- No ambiguity about completion
- Meta-work not forgotten
- Clean state for next work

**Negative**:

- More steps to "finish"
- Requires discipline

---

## ADR-WF010: Document Naming Conventions

**Status**: MANDATORY

### Context

Consistent naming enables quick identification of document type, age, and purpose.

### Decision

Dual naming convention based on document permanence:

#### Permanent Documents (kebab-case)

- **Pattern**: `description_vX.Y.md` or `description_YYYY-MM-DD.md`
- **Location**: `decided/`, `prompts/`, `reports/`
- **Examples**:
   - `workflow-patterns_v1.0.md`
   - `session-summary_2025-12-05.md`
   - `refactoring-prompt_v2.1.md`

#### Temporary Documents (UPPERCASE)

- **Pattern**: `DESCRIPTION.md` or `DESCRIPTION_YYYY-MM-DD.md`
- **Location**: `ai/` root or `working/`
- **Examples**:
   - `TODO.md`
   - `PROJECT-STATUS.md`
   - `SESSION-NOTES_2025-12-05.md`
   - `CONFUSION_2025-12-05.md`

#### Date Suffix Rules

- **Permanent reports**: MUST include date (`session-summary_2025-12-05.md`)
- **Working session docs**: MUST include date (`SESSION-NOTES_2025-12-05.md`)
- **Ongoing working docs**: SHOULD NOT include date (`TODO.md`, `PROJECT-STATUS.md`)
- **Versioned docs**: Use version, not date (`workflow_v1.0.md`)

### Visual Distinction Benefit

```
At a glance:
├── TODO.md                        ← UPPERCASE = temporary, I manage this
├── PROJECT-STATUS.md              ← UPPERCASE = temporary, current state
├── decided/
│   └── workflow-patterns_v1.0.md  ← kebab-case = permanent, read this
└── working/
    └── SESSION-NOTES_2025-12-05.md ← UPPERCASE+date = temporary session
```

### Consequences

**Positive**:

- Instant identification of document type
- Clear lifecycle expectations
- Easy to find current vs historical

**Negative**:

- Mixed conventions (intentional)
- Requires learning the pattern

---

## ADR-WF011: Confusion Documents

**Status**: RECOMMENDED

### Context

AI often encounters uncertainty during work: ambiguous requirements, conflicting sources, unfamiliar terminology,
missing context. Without a structured way to capture and resolve uncertainty, AI either guesses (risking errors) or
blocks (slowing progress).

### Decision

AI SHOULD create Confusion Documents when confidence drops below 90% on any decision or extraction.

#### When to Create

AI creates a confusion document when:

- Confidence < 90% on extracted data or decision
- Conflicting information in sources
- Ambiguous terminology or requirements
- Missing context needed for decision
- Human input required to proceed

#### File Naming

**Pattern**: `CONFUSION-{TOPIC}_YYYY-MM-DD.md`
**Location**: `ai/working/`

**Examples**:

- `CONFUSION-API-DESIGN_2025-12-05.md`
- `CONFUSION-SCHEMA-MAPPING_2025-12-05.md`
- `CONFUSION-REQUIREMENTS_2025-12-05.md`

#### Document Structure

```markdown
# {TOPIC} - Questions and Uncertainties

**Created**: YYYY-MM-DD
**Status**: OPEN | RESOLVED
**Risk Level**: LOW | MEDIUM | HIGH

## High Confidence Items (>90% - Quick review)

1. ✅ [Item description]
   - **Evidence**: [What supports this]
   - **Confirm**: [Yes/No question for human]

## Medium Confidence Items (50-90% - Need validation)

1. ⚠️ [Item description]
   - **Evidence**: [What supports this]
   - **Uncertainty**: [What's unclear]
   - **Question**: [Specific question for human]

## Low Confidence Items (<50% - Need human input)

1. ❓ [Item description]
   - **Evidence**: [Limited evidence, if any]
   - **Question**: [What AI needs to know]
   - **Options**: [Possible interpretations]

## Translation/Terminology Uncertainties

1. "[Original term]" = "[AI interpretation]"?
   - **Context**: [Where this appears]
   - **Question**: [Clarification needed]

---

## Resolved Items ✅

[Human fills in answers, AI updates status]

1. ✅ [Item] - RESOLVED
   - **Human**: "[Answer provided]"
   - **Action**: [What AI will do with this]
```

### Workflow Integration

```
Session N:
├─ AI: Works on task
├─ AI: Encounters uncertainty
├─ AI: Creates CONFUSION-{TOPIC}_DATE.md
├─ AI: Notifies human (per ADR-WF004)
└─ Session ends (confusion doc preserved)

Session N+1:
├─ AI: Reads CONFUSION-*.md (per ADR-WF003)
├─ Human: Has answered questions in doc
├─ AI: Reads answers, marks RESOLVED
├─ AI: Continues work with resolved context
└─ No re-analysis needed!
```

### Confidence Levels Guide

| Level  | Confidence | AI Action                         | Human Action               |
|--------|------------|-----------------------------------|----------------------------|
| High   | >90%       | Proceed, note for quick review    | Confirm or correct         |
| Medium | 50-90%     | Document uncertainty, may proceed | Validate before next phase |
| Low    | <50%       | MUST NOT proceed                  | Answer before AI continues |

### Implementation

AI MUST:

1. Create confusion doc when confidence < 90% on important decisions
2. Categorize items by confidence level
3. Provide specific, answerable questions
4. Check for resolved items at session start

AI SHOULD:

1. Quote source material for context
2. Offer options/interpretations for human to choose
3. Update document status when resolved

Human SHOULD:

1. Answer questions directly in the document
2. Mark items as resolved
3. Add context AI may not have

### Consequences

**Positive**:

- Uncertainty is explicit, not hidden
- Questions persist across sessions
- Human input is structured and efficient
- AI doesn't guess on important decisions

**Negative**:

- Additional document overhead
- Requires human engagement
- May slow initial progress

---

## ADR-WF012: Session Types

**Status**: RECOMMENDED

### Context

Not all work sessions are alike. Planning sessions differ from building sessions, which differ from validation sessions.
Recognizing session type helps set appropriate expectations and checkpoints.

### Decision

Sessions SHOULD be classified into three types:

#### Type A: Planning Sessions (1-2 hours, ~20% of sessions)

**Purpose**: Design workflows, create strategies, document architecture

**Pattern**:

1. AI researches options
2. AI creates proposal documents
3. Human reviews and decides
4. Document approved approach in `decided/`

**Deliverables**: Workflow docs, architecture decisions, strategy documents

**Checkpoint**: After human approval of approach

#### Type B: Building Sessions (2-4 hours, ~60% of sessions)

**Purpose**: Execute workflows, build features, implement designs

**Pattern**:

1. AI executes planned workflow
2. AI creates confusion docs if uncertain
3. Human validates outputs, answers questions
4. AI incorporates feedback, continues

**Deliverables**: Code, schemas, extracted data, implementation

**Checkpoint**: After each phase or significant deliverable

#### Type C: Validation Sessions (1-2 hours, ~20% of sessions)

**Purpose**: Review, test, validate deliverables

**Pattern**:

1. AI runs validation/tests
2. Human reviews outputs
3. Identify issues together
4. Decide: fix now or defer

**Deliverables**: Validation reports, issue lists, go/no-go decisions

**Checkpoint**: After validation complete

### Session Length Recommendations

| Length           | When to Use                            | Risk Level |
|------------------|----------------------------------------|------------|
| Short (1-2 hrs)  | Planning, validation, incremental work | Any        |
| Medium (2-4 hrs) | Building, one complete phase           | LOW-MEDIUM |
| Long (4+ hrs)    | End-to-end work, milestones only       | LOW only   |

**Why Shorter Sessions Work Better**:

- Lower cognitive load for human validation
- Fresh perspective each session
- Can pause anywhere (especially LOW risk)
- Easier to maintain momentum over time

### Implementation

AI SHOULD:

1. Identify session type at start
2. Set appropriate checkpoints for type
3. Adjust expectations based on type

Human SHOULD:

1. Communicate expected session type/length
2. Be available for sync points appropriate to type

### Consequences

**Positive**:

- Clear expectations for each session
- Appropriate checkpoint frequency
- Better time estimation

**Negative**:

- May feel constraining
- Not all work fits neatly into types

---

## ADR-WF013: Phase Completion Checklist

**Status**: RECOMMENDED

### Context

Phase transitions are critical sync points. Without explicit validation from both AI and human, phases may be marked
complete prematurely.

### Decision

Before marking any phase complete, BOTH AI and human MUST validate.

#### Dual Validation Checklist

```markdown
## Phase Completion: [Phase Name]

### AI Validates ✅

- [ ] All tasks in phase completed
- [ ] Deliverable files created
- [ ] Validation/tests run successfully
- [ ] No HIGH/MEDIUM confidence confusion items open
- [ ] TODO.md updated with completion
- [ ] No blocking issues discovered

### Human Validates ✅

- [ ] Reviewed AI deliverables
- [ ] Answered all confusion document questions
- [ ] Approved quality of work
- [ ] Agreed to proceed to next phase
- [ ] Signed off on phase

### Phase Status

- [ ] ✅ COMPLETE (both AI and human validated)
- [ ] 🔄 IN REVIEW (AI complete, awaiting human)
- [ ] ⏳ IN PROGRESS (work ongoing)
```

### When to Use

| Risk Level | Phase Checklist Required         |
|------------|----------------------------------|
| LOW        | SHOULD use at major milestones   |
| MEDIUM     | MUST use at each phase boundary  |
| HIGH       | MUST use, with explicit sign-off |

### Implementation

AI MUST:

1. Complete AI validation section before requesting human review
2. Not proceed to next phase until human validates
3. Document any exceptions or deferrals

Human MUST:

1. Review deliverables before signing off
2. Answer open questions before approval
3. Explicitly approve phase completion

### Consequences

**Positive**:

- No premature phase transitions
- Clear accountability
- Issues caught early

**Negative**:

- Adds overhead
- Requires human availability

---

## ADR-WF014: Session Metrics

**Status**: RECOMMENDED

### Context

Long-running projects benefit from tracking progress over time. Session metrics help with estimation, momentum, and
project health visibility.

### Decision

For multi-session projects, AI SHOULD track session metrics in `PROJECT-STATUS.md`.

#### Metrics Template

```markdown
## Session Metrics

**Project Start**: YYYY-MM-DD
**Current Session**: N
**Total Sessions**: N
**Total Time**: ~X hours

### Progress by Phase

| Phase | Tasks | Complete | Status         |
|-------|-------|----------|----------------|
| 0     | 3     | 3/3      | ✅ Done         |
| 1     | 4     | 2/4      | 🔄 In Progress |
| 2     | 5     | 0/5      | ⏳ Pending      |

### Session History

| Session | Date       | Duration | Tasks Done | Notes         |
|---------|------------|----------|------------|---------------|
| 1       | 2025-12-01 | 2h       | 3          | Foundation    |
| 2       | 2025-12-03 | 3h       | 2          | Phase 1 start |

### Estimates

- **Current Phase**: ~2 more sessions
- **Overall**: ~60% complete
- **Projected Completion**: ~4 more sessions
```

### When to Track

| Project Length | Track Metrics |
|----------------|---------------|
| Single session | SHOULD NOT    |
| 2-5 sessions   | MAY           |
| 5+ sessions    | SHOULD        |
| Months-long    | MUST          |

### Implementation

AI SHOULD:

1. Update metrics at session end
2. Track actual vs estimated time
3. Note any estimation learnings

Human MAY:

1. Review metrics for project health
2. Adjust estimates based on learnings

### Consequences

**Positive**:

- Visibility into project progress
- Better future estimation
- Motivation from visible progress

**Negative**:

- Overhead to maintain
- Estimates may be wrong

---

## ADR-WF016: Hard Rules Enforcement

**Status**: RECOMMENDED

### Context

AI assistants make recurring mistakes on project-specific rules. Without explicit enforcement, critical rules get
violated repeatedly, causing bugs. The `/clear` command resets context, losing any mid-session reminders.

### Decision

Hard rules SHOULD be enforced through a multi-layer approach with different persistence levels.

#### Rule Tiers

| Tier       | Keyword     | Meaning         | Violation Impact |
|------------|-------------|-----------------|------------------|
| **Tier 1** | MUST NEVER  | Bug if violated | HIGH             |
| **Tier 2** | MUST ALWAYS | Bug if omitted  | HIGH-MEDIUM      |
| **Tier 3** | SHOULD      | Best practice   | LOW              |

#### Layer 1: CLAUDE.md (Survives /clear)

Critical rules summary in CLAUDE.md - always visible, survives `/clear` command.

```markdown
## Hard Rules (NEVER Violate)

**Project-specific rules that cause bugs if violated:**

1. ❌ NEVER [rule description] - [why]
2. ❌ NEVER [rule description] - [why]
3. ✅ ALWAYS [rule description] - [why]

**Full details:** `ai/{context}-hard-rules.md`
```

#### Layer 2: Global Hard Rules (~/.claude/)

User's personal rules across all projects.

**File**: `~/.claude/hard-rules.md`

```markdown
# Global Hard Rules

Rules that apply to ALL my projects.

## Tier 1: MUST NEVER (Bug if Violated)

### GLOBAL-NEVER-1: Commit Secrets

- NEVER commit secrets, API keys, tokens, or credentials
- Why: Security breach, credential rotation required
- Check: Review staged files before commit

### GLOBAL-NEVER-2: Break Without Approval

- NEVER make breaking changes without explicit human approval
- Why: Downstream impact, integration failures
- Check: If changing public API/interface, seek approval first

### GLOBAL-NEVER-3: Guess on Uncertainty

- NEVER proceed with LOW confidence (<50%) without asking
- Why: Compounds errors, wastes time on wrong path
- Check: Create CONFUSION doc, ask human

## Tier 2: MUST ALWAYS (Bug if Omitted)

### GLOBAL-ALWAYS-1: State Assumptions

- ALWAYS state assumptions before proceeding with significant work
- Why: Misaligned assumptions cause rework
- Check: "I'm assuming X, Y, Z - correct?"

### GLOBAL-ALWAYS-2: Verify Before Delete

- ALWAYS verify with human before deleting files or significant code
- Why: Accidental data loss, hard to recover
- Check: "I'm about to delete X - proceed?"

### GLOBAL-ALWAYS-3: Test After Changes

- ALWAYS run tests after code changes (if tests exist)
- Why: Catch regressions immediately
- Check: Run test suite, report results

### GLOBAL-ALWAYS-4: Update TODO on Completion

- ALWAYS update TODO.md/Beads when completing tasks
- Why: Resume protocol depends on accurate state
- Check: Mark task complete before moving on

## Tier 3: SHOULD (Best Practice)

- SHOULD use RFC 2119 keywords in technical docs
- SHOULD create confusion docs when confidence < 90%
- SHOULD batch related changes in single commits
- SHOULD reference file:line when discussing code
```

AI SHOULD check for `~/.claude/hard-rules.md` at session start.

#### Layer 3: Project Hard Rules (Authoritative Detail)

**File**: `ai/{context}-hard-rules.md` (unversioned)

**Location rationale**: Project hard-rules are session context (like TODO.md), not permanent decided patterns. They live
in `ai/` root alongside other working state files.

**Versioning strategy**: Hybrid approach

- Filename: NO version suffix (always `{context}-hard-rules.md`)
- Internal: Version History section tracks changes
- Rationale: Rules evolve but should always be current; history preserved inside

Full documentation with:

- Rule description
- Rationale (why this matters)
- Correct code example
- Wrong code example
- Detection method

#### Layer 4: Code Comments (At Point of Use)

```python
def process_data(row, config):
    """
    CRITICAL RULE: Check type BEFORE checking value!
    See: ai/project-hard-rules_v1.0.md MUST-NEVER-1
    """
    # CRITICAL: Check type FIRST (not value)
    item_type = config["type"]
    ...
```

#### Layer 5: /nudge Command (Mid-Session Refresh)

Use `/nudge` command to re-read hard rules during long sessions or after `/clear`.

### /clear Integration

| What               | Survives /clear? | How to Restore           |
|--------------------|------------------|--------------------------|
| CLAUDE.md rules    | ✅ Yes            | Automatic                |
| Global ~/.claude/  | ✅ Yes            | Automatic (if AI checks) |
| Project hard-rules | ❌ No             | Use `/nudge` command     |
| Session context    | ❌ No             | Use resume protocol      |

### Implementation

AI MUST:

1. Read hard rules summary from CLAUDE.md (always available)
2. Follow Tier 1 (MUST NEVER) rules without exception

AI SHOULD:

1. Check `~/.claude/hard-rules.md` at session start
2. Read project hard-rules when working on related code
3. Reference rule numbers in confusion documents when uncertain

AI MUST (Markdown formatting):

1. Preserve double-space line breaks at end of metadata lines
2. Example: `**Purpose**: Description  ` (two spaces at end for line break)

Human SHOULD:

1. Add critical rules to CLAUDE.md (survives /clear)
2. Maintain global rules in `~/.claude/hard-rules.md`
3. Document project rules in `ai/{context}-hard-rules.md`
4. Use `/nudge` after `/clear` if needed

### Consequences

**Positive**:

- Critical rules always visible (CLAUDE.md)
- Global rules apply everywhere
- Detailed rationale in ADR
- `/nudge` restores context after `/clear`

**Negative**:

- Multiple places to maintain
- Rules can get out of sync

**Mitigation**: CLAUDE.md has summary + link to ADR; ADR is authoritative

---

## ADR-WF017: Documentation Requirements

**Status**: MANDATORY

### Context

Projects need consistent documentation for users, maintainers, and release tracking. Without clear requirements,
documentation is forgotten or inconsistent. Different audiences need different documentation depths.

### Decision

Documentation requirements based on audience and project type:

#### Documentation Hierarchy

**Priority Order** (from most to least critical):

1. **User Documentation** - Enables users to succeed independently
2. **Maintainer Documentation** - Enables extension and troubleshooting
3. **Release Documentation** - Tracks changes for upgraders

#### Template Strategy

**Canonical source**: `templates/` in txo-ai repo
**Project usage**: Copy to `ai/decided/` when starting a project
**ADR references**: Points to `ai/decided/*-example_vX.Y.md` files

```
txo-ai/templates/                    # Canonical templates
├── readme-example_v1.0.md
├── in-depth-readme-example_v1.0.md
└── release-notes-example_v1.0.md

your-project/ai/decided/             # Project copies here
├── readme-example_v1.0.md
├── in-depth-readme-example_v1.0.md
└── release-notes-example_v1.0.md
```

#### README.md (MUST for all projects)

**Target**: "New developer, 15 minutes to success"
**Max Length**: 2 screens (~100 lines)
**Template**: `ai/decided/readme-example_vX.Y.md`

**Required sections**:

- Purpose/Scope (1-2 sentences)
- Prerequisites
- Quick Start (setup + first run)
- Directory Structure
- Configuration Quick Reference
- Common Usage Patterns
- Troubleshooting
- Links to detailed docs

#### in-depth-readme.md (MAY - ask human)

**Target**: "Experienced developer/maintainer who needs to extend or customize"
**Template**: `ai/decided/in-depth-readme-example_vX.Y.md`

**AI SHOULD ask**: "Does this project need in-depth documentation?"

- For complex projects: YES
- For simple scripts: NO

**Required sections** (if created):

- Architecture Philosophy
- Complete Setup Guide
- Advanced Configuration
- Integration Patterns
- Performance & Reliability
- Security Implementation
- Testing and Validation
- Customization Guide
- Troubleshooting Deep Dive

#### release-notes_vX.Y.md (SHOULD for coding projects)

**Target**: Users upgrading to new version
**Location**: `ai/reports/release-notes_vX.Y.md`
**Template**: `ai/decided/release-notes-example_vX.Y.md`

**Header format**:

```markdown
**Release Date**: YYYY-MM-DD
**Previous Version**: vX.Y.Z
**Status**: [Draft | Code Complete | Released]
**Breaking Changes**: [Yes (N) | No]
```

**Required sections**:

- Overview (headline features)
- Breaking Changes (with migration steps)
- New Features
- Improvements
- Migration Guide
- Testing validation

### Documentation Decision Tree

```
Strand complete (done-done-done)?
│
├─ README.md MUST exist
│  └─ AI: "Does this project need in-depth documentation?"
│     ├─ Human says Yes → Create in-depth-readme.md
│     └─ Human says No → Skip
│
├─ Coding project?
│  └─ Yes → release-notes_vX.Y.md SHOULD exist
│
└─ Documentation-only project?
   └─ Skip release notes
```

### Implementation

AI MUST:

1. Verify README.md exists before marking Strand as done-done-done
2. Ask human about in-depth documentation need
3. Use templates from `ai/decided/` for structure

AI SHOULD:

1. Create release-notes for coding projects
2. Keep README under 2 screens
3. Reference in-depth-readme from README (if exists)

Human SHOULD:

1. Copy templates from `templates/` to `ai/decided/` at project start
2. Review and approve documentation before done-done-done
3. Decide if in-depth documentation is needed

### Consequences

**Positive**:

- Consistent documentation across projects
- Clear audience targeting (user vs maintainer)
- Templates reduce effort
- AI knows what to create and when to ask

**Negative**:

- Overhead for simple projects
- Templates need maintenance

**Mitigation**: Scale documentation to complexity; templates make creation fast

---

## ADR-WF018: FLIGHT-PLAN Document

**Status**: MANDATORY

### Context

Projects need an anchor document that captures the project's philosophical identity — what it IS, what load-bearing
choices define it, and what it is NOT. Without this, sessions drift, decisions lack a gauge, and the project's identity
is spread across scattered documents. This is the L0 (Anchor) level in the work hierarchy.

### Decision

Projects MUST create a `FLIGHT-PLAN.md` document at the project root that captures the project's Intent and Anchors.

#### Purpose

FLIGHT-PLAN.md is the **L0 Anchor document** — the project's identity:

- Defines the project's Intent (the gauge — what is this FOR?)
- Lists tested Anchors (load-bearing philosophical positions that survived W-H-S)
- Each Anchor names what the project IS and what it is NOT (counterpoint-tested)

**Note:** FLIGHT-PLAN.md captures IDENTITY, not progress. Progress is tracked in PROJECT-STATUS.md and Beads.
Epics, tech stack, and architecture live in TODO.md, CLAUDE.md, and project docs respectively.

#### Location

- **File:** `FLIGHT-PLAN.md` in project root
- **Case:** UPPERCASE (working document that evolves)
- **Lifecycle:** Transforms to README.md foundation at done-done-done

#### Structure

Two sections: **Intent** and **Anchors**. Standard header/footer per WF002.

Created via `/txo-intent` skill which runs a W-H-S process (loads Shaw Research, walks philosophies
and scenarios with counterpoints, hammers anchors, synthesizes into FLIGHT-PLAN.md). No separate template needed.

**Intent**: The gauge for all TMM epics and W-H-S sessions. One to three sentences.
The `/txo-init` skill validates Intent presence on project setup.

#### Integration with Other Documents

| Document              | Content                                      | Updates        |
|-----------------------|----------------------------------------------|----------------|
| **FLIGHT-PLAN.md**    | Intent, Anchors (L0 identity)                | On identity change |
| **PROJECT-STATUS.md** | Session history, decisions, current position | Every session  |
| **TODO.md**           | Current Epic/Cluster tactical focus          | During work    |
| **Beads**             | Tasks, sub-tasks, dependencies               | Real-time      |

#### Aviation Metaphor

The FLIGHT-PLAN.md name extends the aviation metaphor:

- `/txo-takeoff`: Loads the flight plan (Intent + Anchors) at session start
- Work: Execute the mission within the gauge
- `/txo-land`: Validates work aligns with flight plan

### Implementation

AI MUST:

1. Load FLIGHT-PLAN.md Intent + Anchors at session start (via `/txo-takeoff`)
2. Use Intent as gauge for all session work

AI SHOULD:

1. Reference Anchors when making design decisions
2. Flag when a decision may contradict an Anchor

Human SHOULD:

1. Create FLIGHT-PLAN.md via `/txo-intent` at project start
2. Update via `/txo-intent` when project identity shifts
3. Transform to README.md at project completion

### Consequences

**Positive**:

- Project identity is explicit and tested
- Every session has a gauge (Intent)
- Load-bearing choices are visible and named
- Counterpoints prevent drift ("we chose X, not Y, because Z")

**Negative**:

- Requires W-H-S investment upfront
- Anchors may need revision as project evolves

**Mitigation**: `/txo-intent` can be re-run to update. Anchors are positions, not laws — they evolve through new W-H-S.

---

## Hook Recommendations

**Status**: RECOMMENDED

Hooks can automate workflow reminders. These are recommendations, not requirements.

### SessionStart Hook

**Purpose**: Remind AI of resume protocol

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "prompt",
        "command": "Check for ai/READY-FOR-NEXT-SESSION.md. If exists, summarize current state. Follow resume protocol from ADR-WF003."
      }
    ]
  }
}
```

### SessionEnd Hook

**Purpose**: Remind to create session summary

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "type": "command",
        "command": "echo 'Session ending. Consider: 1) Update TODO.md 2) Create session summary 3) Update READY-FOR-NEXT-SESSION.md'"
      }
    ]
  }
}
```

### Pre-Commit Hook

**Purpose**: Remind about done-done checklist

```json
{
  "hooks": {
    "PreCommit": [
      {
        "type": "command",
        "command": "echo 'Before committing: Check ai/PROJECT-STATUS.md done-done checklist'"
      }
    ]
  }
}
```

---

## Version History

### v1.2 (2026-02-21)

- **ADR-WF000**: Added L0 (Anchor) level — FLIGHT-PLAN.md as project identity document
- **ADR-WF018**: Rewritten — FLIGHT-PLAN.md promoted from RECOMMENDED to MANDATORY, now L0 Anchor (Intent + Anchors), created via `/txo-intent` W-H-S skill, no template needed
- **Layered Architecture**: Added ANCHOR layer above STRATEGIC
- Updated Beads Hierarchy Mapping with Anchor level

### v1.1 (2025-12-18)

- **ADR-WF000**: Added Sub-bead (L4) level, FLIGHT-PLAN.md, Beads hierarchy mapping
- **ADR-WF003**: Added FLIGHT-PLAN.md to Resume Protocol Level 1
- **ADR-WF005**: Added Epic/Task/Sub-task hierarchy, hierarchical commands, loose sync strategy
- **ADR-WF018**: NEW - FLIGHT-PLAN Document for human+AI workflow
- Added flight-plan-template_v1.0.md to templates/
- Updated slash commands (txo-takeoff, txo-land) with FLIGHT-PLAN.md integration

### v1.0.1 (2025-12-05)

- Added ADR format standard reference (Michael Nygard) to Introduction
- Enhanced ADR-WF002: Added version history pattern (filename vs internal versioning)
- Removed ADR-WF015: Decision Log (redundant - decisions in ADRs and session summaries)
- Updated ADR-WF016: Changed hard-rules location from `ai/decided/` to `ai/` root
- Added ADR-WF017: Documentation Requirements (README, in-depth-readme, release-notes)
- Added templates/ directory with documentation examples

### v1.0 (2025-12-05)

- Initial creation
- ADR-WF000: Work Hierarchy Terminology (Strand → Cluster → Bead)
- ADR-WF001: Risk Classification
- ADR-WF002: Document Lifecycle
- ADR-WF003: Resume Protocol
- ADR-WF004: AI-Human Sync Points
- ADR-WF005: Beads Integration
- ADR-WF006: Skills Recommendations
- ADR-WF007: Directory Structure
- ADR-WF008: Pre/Post Coding Workflow
- ADR-WF009: Done Levels
- ADR-WF010: Document Naming Conventions
- ADR-WF011: Confusion Documents
- ADR-WF012: Session Types
- ADR-WF013: Phase Completion Checklist
- ADR-WF014: Session Metrics
- ADR-WF016: Hard Rules Enforcement

---

**Version**: v1.2
**Domain**: AI-Human Workflow
**Purpose**: Tactical and strategic collaboration patterns complementing Beads operational tracking
**Companion**: [Beads](https://github.com/steveyegge/beads) for operational task management (Epic/Task/Sub-task
hierarchy)
