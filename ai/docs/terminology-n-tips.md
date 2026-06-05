# TXO AI Framework - Terminology Reference

**Version:** 2.0
**Updated:** 2026-01-13

Complete reference for all terminology used in the TXO AI Framework.

---

## Four Box Model

The organizational structure for TMM (The META Machinery) documentation.

| Box              | Purpose                 | Contains                                        | Documents                  |
|------------------|-------------------------|-------------------------------------------------|----------------------------|
| **Foundation**   | What everything sits on | Tech stack, patterns, objectives                | `system-foundation.md`     |
| **Process**      | How we work             | TMM docs, dev-order, session management         | `tmm-*.md`, `dev-order.md` |
| **Design Graph** | What we build           | Nodes (entities), edges (contracts), data model | `node-*.md`, `edge-*.md`   |
| **External**     | What we depend on       | External services, APIs, integrations           | `external-*.md`            |

**Visual:**

```
┌─────────────┐ ┌───────────────────┐ ┌─────────────┐
│   PROCESS   │ │   DESIGN GRAPH    │ │  EXTERNAL   │
└─────────────┘ └───────────────────┘ └─────────────┘
                        │
════════════════════════╪════════════════════════════
                        ▼
              ┌───────────────────────┐
              │      FOUNDATION       │
              └───────────────────────┘
```

---

## Three Layers (Context / Constraints / Behavior)

How TMM documents capture information:

| Layer           | Questions       | Keywords                                | Enforcement                    |
|-----------------|-----------------|-----------------------------------------|--------------------------------|
| **Context**     | WHY + WHERE     | Why does this exist? What's the domain? | Understanding, not enforcement |
| **Constraints** | WHAT + WHAT-NOT | What are boundaries? What's forbidden?  | Hard (MUST) or Soft (SHOULD)   |
| **Behavior**    | HOW + HOW-NOT   | What should happen? What must not?      | Guidance, AI chooses           |

**Mapping to RFC-style:**

| Layer              | RFC Keywords       | Violation Impact |
|--------------------|--------------------|------------------|
| Context            | —                  | —                |
| Constraints (Hard) | MUST, MUST NOT     | Failure          |
| Constraints (Soft) | SHOULD, SHOULD NOT | Suboptimal       |
| Behavior           | MAY                | AI discretion    |

---

## META Levels

Abstraction levels for AI-human collaboration:

| Level         | You Are...                      | AI Should...               | Example                |
|---------------|---------------------------------|----------------------------|------------------------|
| **META-META** | Designing the process itself    | Stay abstract, no examples | Improving TMM docs     |
| **META**      | Filling Four Boxes, documenting | Document, don't implement  | Running TMM stages     |
| **EXECUTE**   | Building from completed specs   | Write code, implement      | Coding from design doc |

**Switching Rule:** AI MUST ask before switching levels.

**Signals:**

```
META → EXECUTE: "Spec complete. Switch to EXECUTE to implement? (approved?)"
EXECUTE → META: "Implementation done. Return to META for review? (approved?)"
```

---

## System Objectives (P0 / P1 / P2)

Prioritized objectives for system design:

| Priority | Category       | Objectives                                | Rule               |
|----------|----------------|-------------------------------------------|--------------------|
| **P0**   | Non-Negotiable | Correctness, Security                     | Always beats P1/P2 |
| **P1**   | Primary        | Reliability, Maintainability, Testability | Optimize for       |
| **P2**   | Secondary      | Performance, Simplicity, Evolvability     | Nice to have       |

**Conflict Resolution:**

- P0 always wins
- Within same priority: context decides (document in ADR)
- When in doubt: prefer maintainability over performance
- When in doubt: prefer simplicity over features

---

## Risk Levels

Classification for workflow decisions:

| Level      | Example                          | Documentation   | Human Sync            |
|------------|----------------------------------|-----------------|-----------------------|
| **LOW**    | Typo fixes, config tweaks        | Minimal         | MAY skip approvals    |
| **MEDIUM** | Features, refactoring            | Comprehensive   | SHOULD at milestones  |
| **HIGH**   | Architecture changes, migrations | Detailed + ADRs | MUST before each step |

---

## Done Levels

Three-tier completion tracking:

| Level              | Meaning     | Tracked In          | Includes                                         |
|--------------------|-------------|---------------------|--------------------------------------------------|
| **Done**           | Code works  | `TODO.md`           | Tests pass, feature implemented                  |
| **Done-Done**      | Docs synced | `PROJECT-STATUS.md` | ADRs written, versions synced, cross-refs valid  |
| **Done-Done-Done** | Published   | Git history         | Committed, tagged, pushed, working docs archived |

---

## Audiences

Target readers for documentation (Shaw Framework):

| Audience   | Focus | Compression | Reading Time | Principle         |
|------------|-------|-------------|--------------|-------------------|
| **Boss**   | WHY   | 10:1        | 5 min        | Decision-Enabling |
| **Lead**   | WHAT  | 3:1         | 15 min       | Planning-Enabling |
| **Worker** | HOW   | 1:1         | 30 min       | 4am Principle     |

**4am Principle:** Worker docs must be clear enough that someone woken at 4am can follow the steps half-asleep.

---

## Document Types (Audience Structure)

| Type       | Purpose                              | Naming                    | Example                   |
|------------|--------------------------------------|---------------------------|---------------------------|
| **WHERE**  | Common destination for all audiences | `WHERE-{context}.md`      | `WHERE-authentication.md` |
| **PRIME**  | Principal doc for specific audience  | `{AUDIENCE}-{context}.md` | `BOSS-authentication.md`  |
| **LINKED** | Deep-dive on one aspect              | `focus-{context}.md`      | `focus-jwt-validation.md` |
| **REF**    | External reference                   | Any name                  | `rfc7519-jwt.md`          |

---

## ADR Domains

Naming convention: `adr-{domain}-{topic}_v{version}.md`

| Domain         | Purpose                    | Examples                                                      |
|----------------|----------------------------|---------------------------------------------------------------|
| **foundation** | Technology/framework rules | `adr-foundation-java_v1.3.md`, `adr-foundation-vertx_v1.2.md` |
| **process**    | Workflow/methodology       | `adr-process-ai-workflow_v1.1.md`, `adr-process-shaw-*`       |

---

## MVA Natural Laws

Most Viable Architecture principles:

| Law                             | Statement                                | Implication                                            |
|---------------------------------|------------------------------------------|--------------------------------------------------------|
| **Tesler's Law**                | Complexity can't be removed, only moved  | Absorb complexity in architecture, not user experience |
| **Future Complexity**           | Growing systems reveal hidden complexity | Plan for what you can't see yet                        |
| **Architectural Calcification** | Early decisions become irreversible      | Get load-bearing decisions right early                 |

---

## Load-Bearing vs Decorative

| Type             | Can Change?          | Examples                                      | When to Decide   |
|------------------|----------------------|-----------------------------------------------|------------------|
| **Load-Bearing** | No (without rebuild) | Data models, auth architecture, API contracts | Early, carefully |
| **Decorative**   | Yes (anytime)        | UI frameworks, build tools, styling           | When convenient  |

---

## TMM Stages

The META Machinery process:

| Stage | Name       | Primary Box  | Key Action                    |
|-------|------------|--------------|-------------------------------|
| 0     | FOUNDATION | Foundation   | System-level context          |
| 1     | DUMP       | Design Graph | Extract everything from human |
| 2     | CATEGORIZE | All boxes    | Sort into boxes               |
| 3     | SCOPE      | Design Graph | Define boundaries             |
| 4     | DECISIONS  | Foundation   | Document ADRs                 |
| 5     | TESTS      | Design Graph | Test cases + smoke tests      |
| 6     | SKILLS     | Process      | Dev-order + features          |
| 7     | VALIDATE   | All boxes    | Completeness check → EXECUTE  |

---

## Shaw Flows

Documentation quality workflows:

| Flow           | Input         | Process                   | Output                 |
|----------------|---------------|---------------------------|------------------------|
| **Research**   | Unknown topic | Walk → Hammer → Synthesis | Large source doc       |
| **Adaptation** | Lengthy doc   | Analyze → Transform       | Audience-specific docs |

**Research Phases:**

- **Walk:** Explore, find anchors, define scope
- **Hammer:** Test principles, resolve contradictions, build mental models
- **Synthesis:** Create comprehensive research document

---

## Enforcement Levels

How rules escalate from suggestion to requirement:

```
Design doc  →  ADR  →  Hard-rules
"how we do it"  "decided"  "must follow"
"suggestion"    "why"      "never violate"
```

| Level      | Where                | Content                | Loaded                  |
|------------|----------------------|------------------------|-------------------------|
| Design     | `{entity}-design.md` | Suggestions, patterns  | On demand               |
| ADR        | `adr-*.md`           | Decisions with context | When exploring decision |
| Hard-rules | `hard-rules-*.md`    | MUST/MUST NOT only     | Via `/nudge`            |

---

## Work Hierarchy

| Level | Term         | Scope                   | Tracked In                         | Beads         |
|-------|--------------|-------------------------|------------------------------------|---------------|
| L1    | **Strand**   | Full project/initiative | FLIGHT-PLAN.md + PROJECT-STATUS.md | —             |
| L2    | **Cluster**  | Phase/milestone         | TODO.md + Beads Epic               | `bd-xxxx`     |
| L3    | **Bead**     | Individual task         | Beads Task                         | `bd-xxxx.N`   |
| L4    | **Sub-bead** | Complex breakdown       | Beads Sub-task                     | `bd-xxxx.N.M` |

---

## Slash Commands

| Command        | Purpose                     | When to Use                   |
|----------------|-----------------------------|-------------------------------|
| `/txo-takeoff` | Start session, load context | Every session start           |
| `/txo-land`    | End session, commit, sync   | Every session end             |
| `/nudge`       | Reload hard-rules           | After `/clear`, context drift |
| `/nag`         | Completeness check          | During TMM, before finalizing |
| `/retro`       | Session retrospective       | After wobbly sessions         |
| `/pause-tmm`   | Pause TMM session           | Mid-TMM session break         |
| `/resume-tmm`  | Resume TMM session          | Continuing TMM work           |

---

## Beads Hierarchy

| Level    | Type          | Pattern      | Parent Required |
|----------|---------------|--------------|-----------------|
| Epic     | `--type=epic` | `bd-xxx`     | No              |
| Task     | `--type=task` | `bd-xxx.N`   | `--parent=EPIC` |
| Sub-task | `--type=task` | `bd-xxx.N.M` | `--parent=TASK` |

**Closure Rule:** Close children before parents.

---

## Document Locations

| Location           | Purpose                 | Examples                                                                               |
|--------------------|-------------------------|----------------------------------------------------------------------------------------|
| Project root       | Mission, AI guidance    | `FLIGHT-PLAN.md`, `CLAUDE.md`                                                          |
| `ai/`              | Session state           | `TODO.md`, `PROJECT-STATUS.md`, `hard-rules-{context}.md`, `READY-FOR-NEXT-SESSION.md` |
| `ai/decided/`      | Finalized decisions     | `adr-{domain}-{context}.md`                                                            |
| `ai/docs/`         | External documents      | MVA principle, PDF from vendors                                                        |
| `ai/project-docs/` | TMM outputs             | Four Boxes documents                                                                   |
| `ai/prompts/`      | AI prompts              | `TMM/tmm-*.md`                                                                         |
| `ai/reports/`      | Session records         | `retro_YYYY-MM-DD.md`                                                                  |
| `ai/skills/`       | Project specific skills | `create-vertx-message-bus-json.md`                                                     |
| `ai/templates/`    | Templates for AI        | `readne-example.md`                                                                    |
| `ai/working/`      | Scratch work for AI     | `CONFUSION-{context}.md`, `tmm-four-boxes-progress.md`                                 |

---

## Values: null vs n/a

| Value    | Meaning                        | Action                       |
|----------|--------------------------------|------------------------------|
| **null** | Section not filled, incomplete | Run `/nag`, fill the section |
| **n/a**  | Explicitly nothing applies     | Valid, no action needed      |

---

## Communication Shortcuts

| Pattern                   | Example                                                                                | When                 |
|---------------------------|----------------------------------------------------------------------------------------|----------------------|
| Semicolon answers         | "1. Yes; 2. No; 3. TBD"                                                                | Multiple questions   |
| Explicit Yes/No           | "Yes" not "That could work"                                                            | Binary decisions     |
| Risk declaration          | "HIGH risk because..."                                                                 | Before major changes |
| Level declaration         | "We're at META"                                                                        | Prevent drift        |
| Diversion alert           | "You're implementing, we're at META", "We are reseaching WHY not HOW"                  | AI drift detected    |
| Bias check                | "You feel too detailed. Do you have any implicit bias or anchoring?"                   | AI narrow-minded     |
| Dig deeper                | "Analyze why an address is needed from first principles: send package, visit..."       | META and Research    |
| Socratic method           | "Are you sure that is according to...", "Is that really..." instead of pointing it out | AI missed things     |
| Validate understanding    | "What are your CONFUSION levels regarding our discussion?"                             | Expose CONFUSION     |
| Upgrade understanding     | "Tree vs. Graph: You can only sort a bookshelf one way: color, size..."                | Complex research     |
| Idea not fully in context | "SIDE QUEST: Create a bead for XXX to dig into YYY..."                                 | Avoid poisioning     |
| Vague vs. Anchor terms    | "We have an entity" (low context) vs. "Use MVA to..." (specified context)              | Avoid poisioning     |
| AI miss tools available   | "Can we split the big PDF into single-pages using Python?"                             | AI has problem       |

---

## Test Categories (NASA-style)

| Category        | Tests For                     | Example                      |
|-----------------|-------------------------------|------------------------------|
| **Nominal**     | Expected behavior             | Happy path works             |
| **Off-Nominal** | Failure & recovery            | Error handling               |
| **Boundary**    | Limits & edge cases           | Max/min values               |
| **Stress**      | Load & resource constraints   | High volume                  |
| **Robustness**  | Graceful degradation          | Partial failures             |
| **Safe State**  | Safety-critical               | Critical failure recovery    |
| **Chaos**       | Intentional failure injection | Kill component mid-operation |

---

## Mermaid Color Palette

Standard colors for diagrams:

| Color    | Hex       | Use For                         |
|----------|-----------|---------------------------------|
| Blue     | `#0D5ED7` | Service nodes, primary entities |
| Green    | `#237046` | Data, success states            |
| Dark Red | `#870000` | Foundation, schemas, critical   |
| Indigo   | `#4B0082` | Edges, contracts, decisions     |
| Orange   | `#A34700` | Data Model, warnings            |
| Slate    | `#2F4F4F` | Containers, grouping            |
| Teal     | `#006C6C` | Process, workflow               |
| Olive    | `#556B2F` | Design Graph container          |
| Magenta  | `#8B008B` | External services               |
| Gray     | `#696969` | Background, neutral             |

---

**See also:**

- [README.md](../../README.md) - Framework overview
- [TMM Guide](../../docs/tmm-readme.md) - In-depth TMM documentation
- [MVA Philosophy](mva-0-elevator-pitch_v1.1.md) - Architecture principles
