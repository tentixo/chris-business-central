# MB-800 Study Schedule — Progress Tracker

**Version**: 1.1 · **Created**: 2026-07-06 · **Updated**: 2026-07-13
**Owner**: Chris Mansson · **Reviewer**: Lars Mårelius (Morre)
**Companions**: `ai/reports/mb800-gap-analysis.md` (the domain-by-domain gap map) · `docs/FGGE-Machinery_v4.png` (Morre's dependency-graph diagram, Call 16).

---

## What changed in v1.1 (Morre Call 16 — 10 Jul 2026)

Morre reviewed the sprint structure and **endorsed it** — *"the sprints are proved, I think they're gonna work that way."* The v1.1 edits fold in his teaching from that call plus one steer on **how** to study:

1. **Start this week.** Sprint 1 re-anchored to **Mon 13 Jul**; the 9-sprint cadence now lands the seat in the **week of 9 Nov 2026** (still early-to-mid Q4, per FLIGHT-PLAN M1).
2. **The foundation spine goes first** (new section below). Number series → CoA settings + posting groups/setup → journals-vs-documents → VAT settlement. Every exam topic (FA, dimensions, journals, purchasing, inventory) is an *application* of these — Morre's core message.
3. **The Morre method** — don't learn layer-by-layer in the abstract. For each topic: open its posting groups/setup → post one transaction → **inspect where it lands in the VAT ledger + General Ledger** → glue a map.
4. **Dimensions friction resolved** — *"Dimension is not a module — it's 8 fields where you put tags on transactions."* Simple to use (learn the vanilla mechanics for the exam); the reason to *minimise* them is calcification. No exam-vs-Morre conflict.
5. **Cost Accounting added** — a separate ledger, the architectural alternative to dimensions. **Not in the MB-800 basic exam**, but Morre wants it *"because we most likely will use it for Formpipe."* Added as a labelled, non-exam adjunct.
6. **Financials enriched** — account categories & financial reporting (the nightly aggregation), VAT statement & settlement (incl. the MOSS/one-account quirk), and year-end close (moving the P&L result to the balance sheet).

---

## The plan on one line

Sit **MB-800 in the week of 9 November 2026**, reached through **8 fortnightly sprints + a final revision week** at **10–15 h/week**, learning by **blending live client work with targeted sandbox study on the foundation spine** — closing the 🔴/🟡 gaps first, strong areas revised last, two full mock exams before the seat.

| Parameter | Value |
|---|---|
| **Target exam** | Week of **Mon 9 Nov 2026** (early-mid Q4, per FLIGHT-PLAN M1) |
| **Started** | **Week of Mon 13 Jul 2026** — Sprint 1 live |
| **Capacity** | 10–15 h/week (~20–30 h per sprint) |
| **Method** | Blend — client engagement as classroom + dedicated study for gaps no client touches; **the Morre method** (trace every posting into the ledgers) applied throughout |
| **Cadence** | 2-week sprints; each ends with a **checkpoint Morre signs off** |
| **Pass mark** | 700/1000 · ~60 questions · 100 min · ~$165 |

> **Runway note:** ~17 weeks × 10–15 h ≈ 170–250 h — ample for MB-800 (most prep in 40–80 h). Starting a week later than the v1.0 draft moves the seat one week to ~9 Nov and removes **buffer**, not coverage: the D1 admin topics stay merged in one sprint and the final revision is a single week. Slip path is mid/late November (still Q4). If mocks are strong by mid-October, pull the seat into early November.

---

## The foundation spine — master this first (Morre's dependency graph)

Morre's central message on Call 16: the topics on the exam are not separate subjects to memorise — they are all the **same machinery** applied in different places. Get the spine solid and *"you understand everything in payment journal, purchasing, fixed assets and everything."* Study the spine, then treat each exam domain as an application of it.

**The layers, in dependency order (solve top-down):**

- **Layer 0 — Number series (the technical layer).** Every document/transaction needs a unique number, unique *across the group* (prefix `A`/`B`/`Z` + dash + locally-unique number). No number series → no posting. Know **manual vs automatic** numbers: bank accounts, employees and resources are *named, not numbered* (manual). A resource and its employee can share the same ID (linked). The **employee register** is for anyone owed a *post-tax* payment — including a sub-consultant reimbursed for a client dinner (it's **debt on the balance sheet**), so separate posting groups keep *staff* debt distinct from *sub-consultant* debt.
- **Layer 1 — Chart of Accounts + Posting Groups + Posting Setup (the magic).** Have a *sense* of every CoA setting (AI fills the detail). The load-bearing one: **Direct Posting** — turn it **off** on ledger-linked accounts so they can only be moved *through documents* (invoices/credit memos), blocking "fat-finger" manual edits that desync the sub-ledgers. **Posting groups are pointers to where to post**; the **General Posting Setup** and **VAT Posting Setup** are the combination matrices they resolve against.
- **The posting mechanism — only two ways in.** You post either by a **journal** or by a **document.** (Auto-revaluations are just automatic journal postings.) Everything else is a special case of these two.
- **VAT statement & settlement.** The **VAT statement** validates the report; the **settlement** moves the VAT-ledger sums into the settlement accounts (SE: output `2610` / input `2640` → **`2650`** = what you send the Swedish tax office; EU items settle to **`2690`**). Know *when* VAT posts to the VAT ledger and when it doesn't. **MOSS quirk:** a non-VAT-registered buyer is treated as an individual — cross-border B2C VAT (e.g. a French sale) is owed to *that* country's tax office and parked in a **single clump-sum MOSS account** for all non-SE countries; the per-country granularity lives in the VAT ledger (there's no MOSS VAT report yet).
- **Account Categories & Financial Reporting (the aggregation machinery).** Two levels (category → subcategory). BC sums the granular child accounts into categories **every night** so you get a daily income statement / cash flow. Set up **manually per company** — *cannot* be done via config package. Use **"view uncategorised accounts"** as a completeness check (any 4-digit account still showing = missed). Reports show totals only; **drilling into granular child accounts needs Power BI** (the VAT statement preview has partial drill-down).
- **Year-end close.** Move the P&L result to the balance sheet: summarise revenue and cost, then book a "cost called profit" so the income statement zeroes and equity grows.

### RIM data vs Crafted data (the golden rule — the red "No!" arrow)

- **RIM data** = how you *legally* punch things into BC: how to book a receipt/invoice, the actual monthly FA depreciation, the warehouse valuation. The raw, legally-correct bookkeeping.
- **Crafted data** = anything a human *decides*: account categories, aggregation & normalisation rules, posting-setup settings — all analysis.
- **The rule:** crafted decisions must **never** create a dependency on the RIM-data people. Things you change often must not touch RIM data. RIM people punch data in as fast as possible; crafting/analysis happens in a separate layer. (This is *why* dimensions are risky — see Sprint 2.)

### The Morre method — how to study each topic

Don't learn the layers abstractly. For each new area (FA, inventory, purchasing, payments): **open its posting groups + posting setup → post one transaction → inspect where it landed in the VAT ledger + General Ledger → glue together a map.** Repeat until the map is complete. The spine above is what makes every topic legible.

> **Diagram:** `docs/FGGE-Machinery_v4.png` (Morre's "Financial Governance & Compliance / Government Engine", v4) — three panels: (1) governance levels ORG → Group → External with the *Shield/Reserve/Sword* intents (Compliance/Buffer/Revenue); (2) **The Aggregation Machinery** (entity APIs → Aggregation → Normalize → Consolidation "Done-2 magic" → View & Dig → Analyze & Report, with rules created and stored separately); (3) **The Loop** (Rim + Crafted → Combine → Analyze & Decide → new decisions, with the red **"No!"** = crafted must never write back into Rim).

---

## How Morre tracks it

Each sprint has a **Checkpoint deliverable** (something concrete — a posted sandbox flow traced through the ledgers, a mock score) and a **target rating** (moving a domain toward 🟢). Chris updates the **Status** column; Morre reviews it at the fortnightly checkpoint and signs off or adjusts.

**Status key**: ☐ not started · ◐ in progress · ✅ done (self-rating in brackets, e.g. ✅🟢)

---

## The sprints

| # | Dates (2026) | Focus (MB-800 domain) | Standard-first study | Hands-on / client tie-in (blend) | Checkpoint deliverable → target | Status |
|---|---|---|---|---|---|---|
| **1** | **Jul 13–24** | **Foundation spine + Fixed Assets** (D2 setup + D4 txns) | The spine (number series, CoA settings incl. **Direct Posting**, posting groups/setup, journals-vs-documents) + MS Learn FA module | Apply the **Morre method** to FA: run `fixed-assets-testing-playbook` end-to-end (3 acquisition routes, depreciation, disposal, LVA) and **trace each posting into the FA ledger + G/L**. **Client:** Lasernet lease dry-run (A5) | FA lifecycle in sandbox + can trace a posting through the ledgers; resolve 1267/1269 → **FA 🟡→🟢** | ◐ *(started wk 13 Jul)* |
| **2** | Jul 27–Aug 7 | **Dimensions** (D1) *+ Cost Accounting adjunct* | Dimensions as **8 tag fields** — types, values, defaults, blocking combos, priorities — *plus* the calcification / RIM-vs-crafted rationale for minimising them. **Adjunct (non-exam, Formpipe):** Cost Accounting = a separate ledger, the alternative to dimensions | Create dimension + values; default on FA; blocked combination; dimension correction. Sketch a cost-accounting setup. **Client:** IC item-method dimensions; Formpipe cost-allocation | Demo a blocked combo + a correction; explain the **dimensions-vs-cost-accounting** trade-off → **Dimensions 🟡→🟢** | ☐ |
| **3** | Aug 10–21 | **Journals & payments** (D4 — heaviest gap) | Gen/payment/cash-receipt journals, applying entries, bank rec, reversals | Payment journal → apply to invoice; cash receipt → apply; undo/reverse; **bank reconciliation** — trace each into the G/L. **Client:** Masha monthly cycle (§11) | Show a posted bank rec + applied entries → **🔴→🟢** | ☐ |
| **4** | Aug 24–Sep 4 | **Purchasing & AP** (D2/D3/D4) | Vendor setup, PO cycle, purchase pricing/discounts | Vendor → PO → receive → invoice → pay; blanket order; purchase price. **Client:** lessor invoice scan, IC receipts | Full P2P cycle posted + traced → **🔴/🟡→🟢** | ☐ |
| **5** | Sep 7–18 | **Inventory** setup + transactions (D3 + D4 *new topic*) | Item types, costing methods (FIFO/avg/std), locations | Check the **inventory posting groups/setup → see where postings end up** (Morre's exact drill); item journal (adj); transfer order; physical count; adjust cost. **Client:** IC item types, WIP cost capture | Item lifecycle + a transfer + a count, traced to the G/L → **🔴→🟡/🟢** | ☐ |
| **6** | Sep 21–Oct 2 | **Set up BC + Security** (D1 — *merged*) | Assisted setup, config package, opening balances, data migration, **number series (manual vs automatic)**, job queues; permission sets, security groups/filters, approvals | Import a config package (existing guide); set up a number series + a manual-number register (bank/employee); a job queue; create + assign a permission set; a purchase approval workflow | Config package imported + number series + permission set/approval demoed → **🟡/🔴→🟢** | ☐ |
| **7** | Oct 5–16 | **Financials deep (D2)** + sales/AR + **MOCK #1** | **Account categories & financial reporting** (nightly aggregation), **VAT statement & settlement** (+ MOSS one-account quirk), **year-end close** (P&L→balance sheet); account schedules, deferrals, prepayment, credit memos | Set up an account category + view uncategorised; run a VAT settlement; build an account schedule; deferral + prepayment + credit memo. **First full practice exam** | **Mock score #1** shared; VAT settlement + account categories demoed; weak-domain list → all domains ≥🟡 | ☐ |
| **8** | Oct 19–30 | **Re-study mock gaps** + basic ops (D4) + **MOCK #2** | Whatever mock #1 exposed; pages/filters, Edit in Excel, data analysis mode | Re-drill weak areas; practice analysis mode. **Mock #2** end of sprint | **Mock #2 ≥ 80%**; heat-map all 🟢/🟡 | ☐ |
| **9** | Nov 2–6 *(1 wk)* | **Final revision + readiness** | Light revision only — no new material | 2–3 timed full mocks; review misses. **Book the exam** | Consistent mock ≥ pass; **Morre readiness sign-off** | ☐ |
| 🎯 | **Nov 9–13** | **SIT MB-800** | — | — | **Pass (≥700)** | ☐ |

---

## Milestone gates (Morre sign-off points)

1. **End Sprint 2 (Aug 7)** — Fixed Assets + Dimensions green (the two 🟡s closest to done); cost-accounting trade-off understood.
2. **End Sprint 5 (Sep 18)** — the heavy D4 operational gaps closed (journals/payments, purchasing, inventory).
3. **End Sprint 6 (Oct 2)** — D1 setup + security closed → **every domain at least 🟡**.
4. **End Sprint 7 (Oct 16)** — **Mock #1** taken; honest baseline score.
5. **End Sprint 9 (Nov 6)** — readiness sign-off; exam booked.
6. **Exam week (Nov 9–13)** — sit it.

---

## Coverage check — every domain is scheduled

| MB-800 domain | Weight | Sprints |
|---|---|---|
| Set up Business Central | 20–25% | 2 (dimensions), 6 (company/config + number series + security) |
| Configure financials | 25–30% | 1 (spine + FA), 3 (journals), 7 (account categories, VAT settlement, year-end, deferrals) — *plus existing strengths (posting groups, CoA, VAT) that are the spine itself, revised in 7* |
| Sales & purchasing | 10–15% | 4 (purchasing), 5 (inventory), 7 (sales/AR) |
| Perform BC operations | 30–35% | 3, 4, 5 (the big operational block), 7 (VAT settlement/year-end), 8 (basic tasks) |

> **Cost Accounting** is deliberately *not* mapped to an exam domain — it isn't in the MB-800 basic. It rides as a labelled adjunct in Sprint 2 (paired with dimensions, since they *"stand against each other"*) because Morre expects to use it for **Formpipe**. Study for capability, not for the exam.

---

## Mock-exam plan

- **Mock #1** — end Sprint 7 (Oct 16): honest baseline; drives Sprint 8's re-study.
- **Mock #2** — end Sprint 8 (Oct 30): target ≥ 80%.
- **Mocks #3–5** — Sprint 9 (Nov 2–6): timed, full-length; sit the real exam only once consistently clearing the pass mark.
- Use the **official Microsoft practice assessment** (free) as the anchor; supplement if useful.

---

## If it slips (thin buffer — watch it)

- With early-mid-Nov there's little slack: the merged Sprint 6 and the single final week are the pressure points.
- If **one** milestone gate slips, absorb it by trimming Sprint 9 revision.
- If **two** gates slip, re-plan with Morre toward **late November 2026** (still Q4) rather than compressing the mock cycle.
- Green early? Pull the seat into **early November**.

---

*Tracks against `mb800-gap-analysis.md`. Hands-on exercises live in `ai/guides/`. Dependency-graph teaching from Morre Call 16 (10 Jul 2026); diagram `docs/FGGE-Machinery_v4.png`. Tentixo AB — Business Central Advisory.*
