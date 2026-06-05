# MVA: Most Viable Architecture

## Elevator Pitch (3 Min Read, All Audiences)

**Version**: 2.1
**Created**: 2025-12-14
**Updated**: 2026-02-22
**Purpose**: Foundational philosophy prompt. MVA is the WHY behind TMM and W-H-S.
**Load-when**: Session start (if not already loaded), /txo-init, when discussing architecture decisions or calcification.
**Audience**: Universal (Boss, Lead, Worker, User, Student — Human and AI)

---

## The Unescapable Natural Laws

Three natural laws govern complex systems — software, cloud architectures, buildings, business processes, documentation — anything that
grows:

**a. Tesler's Law** (Conservation of Complexity)
Complexity cannot be removed — it can only be moved. Poorly designed systems push complexity onto users.

**b. Future Complexity** (Inevitable Emergence)
Growing systems will encounter complexity. It's hidden now, but growth makes it visible.

**c. Architectural Calcification** (Exponential Change Cost)
Early decisions calcify as systems grow. Some decisions become load-bearing — other structures depend on them. Load-bearing
decisions that aren't caught in time calcify: they can no longer be changed at all. The cost of change isn't linear — it's
exponential with time.

**Most Viable Architecture (MVA)**: Drags the complexity into the now and absorbs it when it's cheap, transforming it
into lasting flexibility and freedom.

MVA is a countermovement to MVP (Minimum Viable Product) — future success is not a quick fix. MVA saves money and time
by addressing the unescapable natural laws.

---

## Load-Bearing vs. Decorative: Not All Decisions Are Equal

In any complex system, decisions fall into two categories:

### Load-Bearing Decisions (Foundational)

Other structures depend on these. Change them and everything above must be excavated:

- Data models (how you identify and relate things)
- Authentication architecture (how identity works)
- API contracts (how systems communicate)
- Multi-cultural (m10e) support (internationalization foundations)
- Security model (how you protect)

**Examples across domains**:

- **Software**: UUIDs vs auto-increment IDs (distributed systems)
- **AWS**: VPC design, IAM patterns, data residency strategy
- **Buildings**: Foundation depth, load-bearing wall placement
- **Business**: Legal structure, governance model

### Decorative Decisions (Changeable)

Nothing depends on these structurally. Change them when better options appear:

- UI frameworks (React, Vue, Angular)
- Color schemes and styling
- Logging and monitoring tools
- Instance types and scaling parameters
- Build tools and developer workflows

### The Danger: Deciding Too Early

The danger isn't making load-bearing decisions. The danger is making them before you understand what you're building. A
decision made in the right direction becomes your foundation. The same decision made in the wrong direction becomes your
prison.

And you often don't know which decisions are load-bearing until you've looked. What seems decorative today may turn out
to carry weight. What seems foundational may turn out to be changeable. The distinction isn't obvious — it requires
research with intent.

### From Load-Bearing to Calcified

A load-bearing decision caught early can still be changed — it's expensive, but possible. Leave it too long and layers
build on top: code, infrastructure, processes, habits. The decision calcifies. Now it can't be changed without
destroying and rebuilding.

MVA's argument: find your load-bearing decisions and get them right while they're still malleable. Before they calcify.

---

## Finding What's Load-Bearing: Walk Before You Decide

You can't identify load-bearing decisions from a conference room. You need to explore — widely and deeply — before
committing.

**Walk wide**: Look at other domains. The pattern you're looking for might already exist in buildings, biology, business,
or another industry. Borrowing proven patterns from other fields is cheaper than inventing from scratch.

**Walk long**: Don't rush through known territory. Deep exploration reveals hidden dependencies — the connections between
decisions that make them load-bearing. What seems independent often isn't.

**Walk, then Hammer, then Walk again**: When you find something that seems important, hammer it. Try to break it from
every angle. If it holds, it's an anchor — build on it. If it breaks, you learned something valuable before it became
expensive. Then walk again. The hammering reveals new territory. (This process is formalized as W-H-S — Walk-Hammer-Synthesis — in our workflow.)

**Write down what you found (Synthesis)**: After walking and hammering, write down what you found. This is a Synthesis —
not a decision. You're locking what you understand, not what you've chosen. Architecture is a graph problem. One walk
doesn't cover it. Multiple syntheses — from different angles, different domains, different concerns — may be needed
before you're ready to decide.

**Then decide, with eyes open**: When your syntheses converge — when the load-bearing decisions are visible and have
survived hammering — then commit. Not before.

This is research with intent: know what you're building toward, walk until you have strong anchors, hammer them, write
down what holds, and decide when the picture is clear. The work happens on whiteboards and in documents, where changes
are cheap.

---

## The Tesler Transformation: Absorbing Complexity

**Tesler's Law**: Complexity cannot be removed, only moved.

**The MVP Trap**:

```
Simple architecture → Complex user experience
Users navigate the chaos → System can't grow
```

**The MVA Approach**:

```
Architects absorb complexity → Transform it into structure
Solid architecture → Simple user experience
Users get freedom → System grows without breaking
```

**MVA's Promise**: Architects absorb complexity so users get a foundation that:

- Grows with the organization and the system
- Is flexible enough to "just add, almost never rebuild"

---

## It's Cheaper to Delete Whiteboard Lines

> "Get the Right People in the Room and use the whiteboard — but also sometimes the right person is AI" – Morre

**Phase 1**: Build your case to see and discuss (whiteboard, Markdown, diagrams, vision)

- Changes cost marker lines, not years of money
- Mistakes cost documents, not production downtime
- Complexity is visible and malleable

**Phase 2**: Put foundations under them (MVA architecture)

- Choose load-bearing decisions with eyes open
- Build extension points, not limitations
- Create structure that absorbs future complexity

**Phase 3**: Just add, almost never rebuild

- Decorative decisions remain free
- Growth doesn't require destruction
- Evolution instead of revolution

---

## Universal Application: Beyond Software

MVA applies wherever complexity exists:

**Software Systems**:

- Load-bearing: Data models, auth, API versioning
- Decorative: UI frameworks, build tools, styling
- Outcome: Systems that scale without rewrites

**Cloud Architecture**:

- Load-bearing: VPC design, IAM patterns, networking
- Decorative: Instance types, monitoring dashboards, tagging
- Outcome: Infrastructure that grows without redesign

**Building Design**:

- Load-bearing: Foundation, structural walls, utilities routing
- Decorative: Paint, furniture, fixtures
- Outcome: Buildings that adapt to new uses

**Business Processes**:

- Load-bearing: Legal structure, governance, financial model
- Decorative: Meeting schedules, office layout, tools
- Outcome: Organizations that scale without restructuring

**Documentation & Process**:

- Load-bearing: Naming conventions (tree-structured: important→less-important, top-down in relationships), format choices (images calcify slower than text — a diagram needs less energy to change than 100 lines of prose)
- Decorative: Specific authoring tools, styling, layout
- Outcome: Documentation that grows without contradictions — and stays understandable

**The Pattern**: In every domain, identify what calcifies, get it right when it's cheap, and everything else evolves
freely.

---

## Start Now: Three Questions

**Question 1**: Which of your current decisions are load-bearing?
*(What would force a rebuild if you changed it?)*

**Question 2**: Have you walked wide and long enough to know the difference?
*(If you haven't challenged your assumptions, you don't know yet)*

**Question 3**: Is the complexity in your architecture (absorbed, structured) or in your users' experience (chaotic,
limiting)?
*(If users struggle, complexity landed on the wrong side)*

---

## The MVA Principle

> **"Absorb complexity when it's cheap, transform it into lasting flexibility and freedom."**

---

**Next Steps**:

- **Understand the philosophy**: [MVA Core Philosophy](https://github.com/tentixo/mva) (external, 20 min read)
- **See it in practice**: Naming convention in `ai/prompts/TMM/tmm-0-foundation_v0.8.md` §5 — a load-bearing decision applied to file naming
- **Start applying it**: Use W-H-S to find your load-bearing decisions before committing

---

## Version History

**v2.1** (2026-02-22):

- Promoted to prompt: moved from `ai/docs/` to `ai/prompts/` (foundational for TMM and W-H-S)
- Added: Prompt metadata header (Purpose, Load-when)
- Added: Documentation & Process as 5th domain in Universal Application (naming conventions as calcification-fast, images vs text calcification speed)
- Added: One bridge sentence connecting Walk/Hammer/Synthesis to W-H-S (line ~100)
- Updated: Audience includes User and Student (5 types, aligned with Shaw Audience)
- Updated: Next Steps references local project docs alongside external MVA repo
- Removed: `-0-` from filename (standalone document, not part of numbered sequence)

**v2.0** (2026-02-19):

- Added: "Finding What's Load-Bearing" section (walk wide, walk long, challenge before locking)
- Added: Load-bearing → calcified progression (two states, not one)
- Added: "The Danger: Deciding Too Early" — premature decisions as the real risk
- Updated: Three Questions (added "have you walked wide and long enough?")
- Updated: Audience includes AI
- Removed: Economics section (ungrounded numbers)
- Removed: "This is the Way" (decorative)
- Tightened throughout

**v1.1** (2026-01-13):

- Minor updates

**v1.0** (2025-12-14):

- Initial elevator pitch
- Three natural laws, load-bearing vs decorative, Tesler Transformation

---

*MVA: Because successful systems live longer than you think they will.*