# Business Central Learning — Flight Plan

**Version:** 1.2
**Updated:** 2026-07-14
**Created:** 2026-06-02
**Domain:** Business Central operational competence (Tentixo)

---

## Root Intent

### Intent

Get good enough at Business Central to independently work with clients and solve their problems. Not mirror Morre's full 360 depth — own the client-facing lane: configuration, troubleshooting, guiding users, understanding why things work so you can explain and decide confidently. Independence is progressive — each solved problem becomes a pattern you can apply next time.

### Anchors

**The Floor — what you stand on**

**Anchor 1: Morre's conventions as measuring stick.**
Morre's BC conventions (layered hierarchy, posting group logic, transaction-based thinking, GVH framework) are the foundation — not just a starting point, but the lens through which every client setup is evaluated. Not up for reinvention.
*Opposite rejected: developing your own BC methodology or adopting client conventions as primary.*

**Anchor 2: Experience boundary, not role boundary.**
Done it before = go. New territory = Morre first. Coding and heavy backend stay with Morre. This isn't a philosophical position about roles — it's sequencing. Get the client-facing side solid first; coding is a later chapter, if at all, and with Claude's help.
*Opposite rejected: full-stack BC consulting, or rigid role-based division.*

---

**The Method — how you get there**

**Anchor 3: Learning by doing, clients as classroom — certification as consolidation.**
Real client context (Lasernet, Formpipe) drives the learning. Sandbox tasks and exercises build the muscle. Theory fills in around practice, not the other way around. Try first, Morre as backstop when stuck. The MB-800 certification is a consolidation milestone — it validates accumulated hands-on knowledge and fills structural gaps, not a starting point.
*Opposite rejected: certification-first, theory-before-practice.*

**Anchor 4: Three channels, one workbench — capture is non-negotiable.**
Knowledge comes from three sources: tasks Morre sets (sandbox exercises), BC sessions with Morre (guided teaching), and Masha's accounting tours (practical operations, recorded). All converge in this repo. If a learning event doesn't flow through the workbench, the value is lost. This is the MVA principle applied to learning — capture when cheap or pay later.
*Opposite rejected: learning by immersion alone without structured capture.*

**Anchor 5: Structured playbook, not a dump.**
The playbook is an operational reference, not chronological notes. Structure is load-bearing — a dump wouldn't survive growth. Watch flag: if findability degrades as the playbook grows, restructure early.
*Opposite rejected: personal notes log, unstructured journal.*

---

**The Goal — where you're heading**

**Anchor 6: Progressive independence through accumulated patterns.**
Independence isn't a switch — it's a growing library of "I've seen this before." Each problem Morre walks you through becomes a pattern you can apply next time it appears with another client. The goal is a repertoire large enough to handle client conversations and support tickets, with clear judgment about when to escalate.
*Opposite rejected: binary independence ("ready" vs "not ready"), or rigid escalation tiers.*

**Anchor 7: Fluid triage — judgment, not a rulebook.**
Assess a problem, know if it's within your repertoire or not, act or escalate accordingly. The boundary is fluid and grows with experience. No formal tier system — organic and honest.
*Opposite rejected: scripted L1/L2 escalation matrix.*

---

## Milestones

### M1: MB-800 — Dynamics 365 Business Central Functional Consultant Associate

**Target**: Q4 2026 — now scheduled for the **week of 9 Nov 2026**
**Exam**: MB-800, ~60 questions, 100 min, pass at 700/1000, ~$165 USD
**Status**: **Active — executing the sprint schedule, ahead of plan** (see Progress below)

**Why this cert, why now**: The MB-800 validates exactly the client-facing functional consultant role Chris is building (Anchor 2). It covers configuration, financials, sales/purchasing, and daily operations — the same territory Morre is teaching. Having the credential adds credibility with clients like Formpipe. It is *not* the developer cert (AL coding), which stays out of scope per Anchor 2.

**How it fits Anchor 3**: Chris already has months of hands-on client work (Tinky, Formpipe) and Morre's architectural framework internalized. The cert consolidates that experience and systematically fills gaps that might not arise organically through current engagements.

**Exam domains and readiness** (baseline, June 2026):

| Domain | Weight | Current level | Gap areas |
|---|---|---|---|
| Set up Business Central | 20–25% | Partial | Data migration packages, security roles/permissions, company creation |
| Configure financials | 25–30% | Strong | Posting groups, CoA, journals, VAT — all covered by Morre sessions |
| Configure sales and purchasing | 10–15% | Partial | Purchase orders, vendor setup, purchase pricing |
| Perform BC operations | 30–35% | Partial | Year-end close, financial reporting, inventory operations |

**Progress (as of 2026-07-14) — ahead of schedule:**
- **Gap analysis + sprint schedule built** — `ai/reports/mb800-gap-analysis.md` (v1.3) and `ai/reports/mb800-study-schedule_v1.1.md`: 8 fortnightly sprints + a revision week, exam targeted for the **week of 9 Nov 2026**.
- **Sprint 1 — Fixed Assets: ✅🟢** — full acquisition → depreciation → disposal lifecycle run **solo** in the sandbox (13–14 Jul), debugging every BC quirk unaided.
- **Sprint 2 — Dimensions: ✅🟢** — all six mechanics (create, default, global-vs-shortcut, blocking, correction, priorities) run **solo** in the same session.
- **Milestone Gate 1 (FA + Dimensions green) hit ~3.5 weeks early** (was due 7 Aug) — the "seen it → done it" jump (Anchor 6) landing faster than planned.
- Each hands-on session now yields a reusable **testing playbook** in `ai/guides/` (FA, WIP, Dimensions) — a self-built revision library (Anchors 4 & 5 in action).

**Approach** (now executing, not just planning):
1. Continue primary learning via client work and Morre sessions (Anchor 3) — ongoing
2. ~~Map updated MB-800 study guide against playbook, identify gaps~~ **✅ done** → gap analysis + schedule built
3. Fill gaps with targeted sandbox exercises (same pattern as Tinky/Formpipe) — **in progress**; next: Sprint 3, Journals & payments (heaviest remaining 🔴 gap)
4. Two full mock exams, then take the exam (week of 9 Nov 2026)

**Renewal**: Annual free online assessment — not a significant maintenance burden.

---

## Version History

**Version 1.0** (2026-06-02):
- Initial FLIGHT-PLAN created via W-H-S with Chris
- 7 anchors across 3 clusters: Floor (2), Method (3), Goal (2)
- All anchors survived Hammer at ~82% average confidence

**Version 1.1** (2026-06-10):
- Added Milestones section with MB-800 certification target (Q4 2026)
- Updated Anchor 3 to include certification as a consolidation step, not a starting point

**Version 1.2** (2026-07-14):
- M1 status: Planning → **Active**; exam pinned to the week of 9 Nov 2026
- Added a **Progress** block: Sprints 1 (Fixed Assets) & 2 (Dimensions) complete solo, **Milestone Gate 1 hit ~3.5 weeks early**; per-session testing playbooks now produced in `ai/guides/`
- Relabelled the June readiness table as the baseline; updated the Approach to reflect execution (gap analysis + schedule done; Sprint 3 next)
