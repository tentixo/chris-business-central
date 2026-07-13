# MB-800 Study Schedule — Progress Tracker

**Version**: 1.0 · **Created**: 2026-07-06
**Owner**: Chris Mansson · **Reviewer**: Lars Mårelius (Morre)
**Companion**: `ai/reports/mb800-gap-analysis.md` (the domain-by-domain gap map this schedule works from).

---

## The plan on one line

Sit **MB-800 in the week of 2 November 2026**, reached through **8 fortnightly sprints + a final revision week** at **10–15 h/week**, learning by **blending live client work with targeted sandbox study** — closing the 🔴/🟡 gaps first, strong areas revised last, two full mock exams before the seat.

| Parameter | Value |
|---|---|
| **Target exam** | Week of **Mon 2 Nov 2026** (early Q4, per FLIGHT-PLAN M1) |
| **Capacity** | 10–15 h/week (~20–30 h per sprint) |
| **Method** | Blend — client engagement as classroom + dedicated study for gaps no client touches |
| **Cadence** | 2-week sprints; each ends with a **checkpoint Morre signs off** |
| **Pass mark** | 700/1000 · ~60 questions · 100 min · ~$165 |

> **Runway note:** ~17 weeks × 10–15 h ≈ 170–250 h — still ample for MB-800 (most prep in 40–80 h). Pulling the date to early November removes **buffer**, not coverage: the D1 admin topics are merged into one sprint and the final revision is a single week. If client load spikes, the slip path is mid-November (still Q4) — see the flex note. If mocks are strong by early October, the seat can be pulled forward.

---

## How Morre tracks it

Each sprint has a **Checkpoint deliverable** (something concrete to show — a posted sandbox flow, a mock score) and a **target rating** (moving a domain toward 🟢). Chris updates the **Status** column; Morre reviews it at the fortnightly checkpoint and signs off or adjusts.

**Status key**: ☐ not started · ◐ in progress · ✅ done (self-rating in brackets, e.g. ✅🟢)

---

## The sprints

| # | Dates (2026) | Focus (MB-800 domain) | Standard-first study | Hands-on / client tie-in (blend) | Checkpoint deliverable → target | Status |
|---|---|---|---|---|---|---|
| **1** | Jul 6–17 | **Fixed Assets** (D2 setup + D4 txns) | MS Learn FA module | Run `fixed-assets-testing-playbook` end-to-end (3 acquisition routes, depreciation, disposal, LVA). **Client:** Lasernet lease dry-run (A5) | Show FA lifecycle in sandbox; resolve 1267/1269 → **FA 🟡→🟢** | ☐ |
| **2** | Jul 20–31 | **Dimensions** (D1) | Global vs shortcut, defaults, blocking combos, priorities | Create dimension + values; default on FA; blocked combination; dimension correction. **Client:** IC item-method dimensions | Demo a blocked combo + a correction → **Dimensions 🟡→🟢** | ☐ |
| **3** | Aug 3–14 | **Journals & payments** (D4 — heaviest gap) | Gen/payment/cash-receipt journals, applying entries, bank rec, reversals | Payment journal → apply to invoice; cash receipt → apply; undo/reverse; **bank reconciliation**. **Client:** Masha monthly cycle (§11) | Show a posted bank rec + applied entries → **🔴→🟢** | ☐ |
| **4** | Aug 17–28 | **Purchasing & AP** (D2/D3/D4) | Vendor setup, PO cycle, purchase pricing/discounts | Vendor → PO → receive → invoice → pay; blanket order; purchase price. **Client:** lessor invoice scan, IC receipts | Full P2P cycle posted → **🔴/🟡→🟢** | ☐ |
| **5** | Aug 31–Sep 11 | **Inventory** setup + transactions (D3 + D4 *new topic*) | Item types, costing methods (FIFO/avg/std), locations | Item journal (adj); transfer order; physical count; adjust cost. **Client:** IC item types, WIP cost capture | Item lifecycle + a transfer + a count → **🔴→🟡/🟢** | ☐ |
| **6** | Sep 14–25 | **Set up BC + Security** (D1 — *merged*) | Assisted setup, config package, opening balances, data migration, number series, job queues; permission sets, security groups/filters, approvals | Import a config package (existing guide); number series; a job queue; create + assign a permission set; a purchase approval workflow | Config package imported + permission set/approval demoed → **🟡/🔴→🟢** | ☐ |
| **7** | Sep 28–Oct 9 | **Consolidate D2 + sales/AR** + **MOCK #1** | Financial reporting / account schedules, deferrals, prepayment, credit memos | Build an account schedule; deferral + prepayment + credit memo. **First full practice exam** | **Mock score #1** shared; weak-domain list → all domains ≥🟡 | ☐ |
| **8** | Oct 12–23 | **Re-study mock gaps** + basic ops (D4) + **MOCK #2** | Whatever mock #1 exposed; pages/filters, Edit in Excel, data analysis mode | Re-drill weak areas; practice analysis mode. **Mock #2** end of sprint | **Mock #2 ≥ 80%**; heat-map all 🟢/🟡 | ☐ |
| **9** | Oct 26–30 *(1 wk)* | **Final revision + readiness** | Light revision only — no new material | 2–3 timed full mocks; review misses. **Book the exam** | Consistent mock ≥ pass; **Morre readiness sign-off** | ☐ |
| 🎯 | **Nov 2–6** | **SIT MB-800** | — | — | **Pass (≥700)** | ☐ |

---

## Milestone gates (Morre sign-off points)

1. **End Sprint 2 (Jul 31)** — Fixed Assets + Dimensions green (the two 🟡s closest to done).
2. **End Sprint 5 (Sep 11)** — the heavy D4 operational gaps closed (journals/payments, purchasing, inventory).
3. **End Sprint 6 (Sep 25)** — D1 setup + security closed → **every domain at least 🟡**.
4. **End Sprint 7 (Oct 9)** — **Mock #1** taken; honest baseline score.
5. **End Sprint 9 (Oct 30)** — readiness sign-off; exam booked.
6. **Exam week (Nov 2–6)** — sit it.

---

## Coverage check — every domain is scheduled

| MB-800 domain | Weight | Sprints |
|---|---|---|
| Set up Business Central | 20–25% | 2 (dimensions), 6 (company/config + security) |
| Configure financials | 25–30% | 1 (FA), 3 (journals), 7 (reporting/deferrals) — *plus existing strengths (posting groups, CoA, VAT) revised in 7* |
| Sales & purchasing | 10–15% | 4 (purchasing), 5 (inventory), 7 (sales/AR) |
| Perform BC operations | 30–35% | 3, 4, 5 (the big operational block), 8 (basic tasks) |

---

## Mock-exam plan

- **Mock #1** — end Sprint 7 (Oct 9): honest baseline; drives Sprint 8's re-study.
- **Mock #2** — end Sprint 8 (Oct 23): target ≥ 80%.
- **Mocks #3–5** — Sprint 9 (Oct 26–30): timed, full-length; sit the real exam only once consistently clearing the pass mark.
- Use the **official Microsoft practice assessment** (free) as the anchor; supplement if useful.

---

## If it slips (thin buffer — watch it)

- With early-Nov there's little slack: the merged Sprint 6 and the single final week are the pressure points.
- If **one** milestone gate slips, absorb it by trimming Sprint 9 revision.
- If **two** gates slip, re-plan with Morre toward **mid/late November 2026** (still Q4) rather than compressing the mock cycle.
- Green early? Pull the seat into **late October**.

---

*Tracks against `mb800-gap-analysis.md`. Hands-on exercises live in `ai/guides/`. Tentixo AB — Business Central Advisory.*
</content>
