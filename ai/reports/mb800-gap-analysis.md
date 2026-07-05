# MB-800 — Gap Analysis vs. Captured Knowledge

**Version**: 1.2
**Created**: 2026-06-15
**Updated**: 2026-06-23 (v1.1) — folded in the IFRS engagement (Lasernet UK); Fixed Assets 🔴→🟡
**Updated**: 2026-07-05 (v1.2) — folded in new IC-item-method + IAS 38 docs; **Dimensions 🔴→🟡**; item-types + posting-setup reinforced
**Milestone**: FLIGHT-PLAN M1 — MB-800 Functional Consultant Associate, target Q4 2026
**Exam**: ~60 questions, 100 min, pass 700/1000, ~$165
**Source**: [MB-800 study guide (skills as of June 30, 2026)](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/mb-800)

---

## How to read this

Each exam sub-area is rated against what we've captured so far (playbook, billing guides, WIP codebook, hands-on Tinky work):

- 🟢 **Strong** — covered hands-on + documented
- 🟡 **Partial** — touched, but gaps remain
- 🔴 **Gap** — not yet covered

---

## Two headline insights

1. **Projects / Jobs / WIP is NOT a dedicated MB-800 domain.** Our deep WIP work is **client-driven (Tinky/Formpipe), not exam-driven**. Don't over-index WIP for the cert.
2. **Dimensions is a whole exam sub-area — Morre says "never use," but the IC engagement now uses them.** Nuance update: the IFRS/IC work *does* use dimensions (default dimensions on items, Country/Function/Product/Revenue dimensions carried on IC lines, dimension correction on receipt) — so it's **no longer purely exam-only**. You now have hands-on exposure to **defaults + how dimensions flow with document lines + correction**; the *exam-specific* mechanics still to study are **global vs shortcut, blocking combinations, and priorities**.

## Knowledge channel — IFRS engagement (Lasernet UK, `ifrs-16-research` branch)

A **third live engagement** now feeds the plan: Chris is working on Tentixo's IFRS-16 / FRS-102 lease-accounting project (separate repo; Carla Rogers + Camilla Höög + Morre). Not driven by us, but the **hands-on exposure maps straight onto top-priority exam gaps** — above all **Fixed Assets** (was gap #3, appeared twice), and now **Dimensions** and **item types / posting setup** via the IC posting work. Tracked docs:
- **Fixed Assets / lease**: `ifrs16-lease-setup-guide-bc_v1.0.md`, `ifrs-16-uk-frs102-bc-implementation_v1.0.md`, `ifrs-16-leased-assets-research_v1.0.md`
- **Intercompany / items / dimensions**: `ic-posting-item-method-setup-guide_v2.0.md`, `ic-items-lease-valuation-research_v1.0.md`, `ic-postings-issues-meeting_v1.0.md`
- **Intangibles**: `capitalization-development-costs-ias38_v1.0.md` (IAS 38 — amortization = same mechanic as FA depreciation)

> **Caveat (Anchor 2):** much of this was **built live by Morre** while Chris observed/documented. It converts from 🟡→🟢 once Chris runs the **sandbox dry-run himself** (the engagement's own action A5). Track the difference between "seen Morre do it" and "done it."

---

## Domain 1 — Set up Business Central (20–25%)

| Sub-area | Status | Notes |
|---|---|---|
| Create & configure a company (assisted setup, config worksheet, **config package**, opening balances, data migration) | 🟡 | Config packages 🟢 (`config-package-xml-export.md`); assisted setup / opening balances / migration = gaps |
| Manage security (profiles, permission sets, security filters, security groups, auditing) | 🔴 | Not covered |
| Set up core functionality (reports/layouts, job queues, **number series**, Copilot/agents) | 🟡 | Number series 🟢 (subscription setup); reports/job queues/Copilot = gaps |
| **Set up dimensions** (values, global/shortcut, defaults, blocking combos, priorities) | 🟡 | **Promoted from 🔴 via IC engagement**: default dimensions on items, IC Dimensions mapping, dimensions flowing with lines, Country-dimension correction on receipt — all touched. **Still study-only**: global vs shortcut, blocking combos, priorities |
| Approvals via workflows | 🔴 | Not covered |

## Domain 2 — Configure financials (30–35%) — *our strongest*

| Sub-area | Status | Notes |
|---|---|---|
| Financial mgmt setup (GL setup, accounting periods, payment terms, **deferrals**, currencies, payment methods) | 🟡 | Payment terms + deferrals touched in billing; periods/currencies/payment methods = gaps |
| Manage CoA (GL accounts, account categories/subcategories, financial reporting, GL allocations) | 🟡 | Deep CoA exposure now (1,713-account export); categories/financial-reporting/allocations = study |
| **Set up posting groups** (specific, general, general posting setup, inventory posting setup, multiple posting groups) | 🟢 | Core competency — playbook §3–4, GVH+W, semantic VAT groups |
| Journals & bank accounts (templates+number series, batches, recurring journals) | 🟡 | Project/journal batches covered; bank accounts/recurring = gaps |
| Accounts payable (vendor accounts, P&P setup, payment journals, vendor ledger relationships) | 🔴 | Purchasing/vendor side weak |
| Accounts receivable (customer accounts, S&R setup, cash receipt journals, payment registration, customer ledger relationships) | 🟡 | Customer setup 🟢; cash receipts / payment registration / ledger-entry relationships = study |
| Fixed assets (depreciation books, FA classes, depreciation methods) | 🟡 | **Promoted from 🔴 via IFRS engagement**: FA class/subclass (`RIGHT-OF-USE`), G/L-integrated depreciation book (`LEASED-FA`), straight-line, **FA posting group** + **FA Posting Type Setup** (Custom 1/2, `Part of Book Value` OFF) all seen live (Morre's build). → 🟢 after Chris's own sandbox run |

## Domain 3 — Configure sales and purchasing (10–15%)

| Sub-area | Status | Notes |
|---|---|---|
| Inventory setup (item settings, categories, attributes, UoM, variants, locations, item ledger relationships, **costing methods**, SKUs) | 🟡 | **Reinforced via IC engagement**: item **types** (Inventory / Non-Inventory / Service) and *when each posts to inventory G/L*, purchase/expense items, internal/clearing items, **Charge (Item)** line type, Item References, Gen. Prod. groups on items. Still gaps: costing methods, variants, locations, SKUs |
| Master data for sales & purchasing (customer & vendor core settings) | 🟡 | Customer side ok; vendor side gap |
| Pricing & discounts (vendor purchase prices, purchase discounts, **customer sales prices**, sales discounts) | 🟡 | Sales price lists discussed; discounts & purchase pricing = study |

## Domain 4 — Perform BC operations (30–35%) — *biggest weight, increased*

| Sub-area | Status | Notes |
|---|---|---|
| Basic tasks (pages, filters, find/inspect, **Edit in Excel**, **data analysis mode**, personalize) | 🟡 | Navigation ok; Edit-in-Excel / analysis mode = practice |
| Process purchases (quotes, PO, receive, over-receive, reverse, posted invoice, recurring lines, blanket, deferrals) | 🔴 | Purchasing flow not covered |
| Process sales (quotes, convert quote, availability, ship, reverse, **sales invoice**, recurring lines, blanket, deferrals) | 🟡 | Sales invoice 🟢; quotes/shipping/blanket/deferrals = study |
| Process financial documents (invoices, credit memos, combine shipments, correct posted, prepayment) | 🟡 | Invoicing covered; credit memos / prepayment / corrections = study |
| Process journals & payments (payment & cash-receipt journals, payment reg, apply/undo entries, reverse, **bank reconciliation**, recurring, GL allocations, currency adjust, **dimension correction**, revalue) | 🔴 | Large gap — high exam value. *Minor touch*: dimension correction seen (Country fix on IC receipt). Core gaps remain: bank rec, apply/undo, payment journals |
| Process fixed asset transactions (acquisition, depreciation, disposal) | 🟡 | **Promoted from 🔴 via IFRS engagement**: acquisition (FA G/L journal, Bal. Acct = liability), **Calculate Depreciation** run, FA G/L journals (Custom 1/2 split). **Disposal still untouched** → keep on study list |
| **Process inventory transactions** (receipts, shipments, transfers, adjust cost, count, reclassify) — *NEW topic* | 🔴 | New in June 30 outline; not covered |

---

## Priority study list (by exam weight × current gap)

1. **Process journals & payments** (D4) — heavy weight, big gap (bank rec, apply entries, payment journals)
2. **Process inventory transactions** (D4) — new topic, full gap
3. **Security & permissions** (D1) — full gap
4. **Purchasing / AP** (D2 + D3 + D4) — vendor side consistently weak
5. Round out **inventory setup & costing methods** (D3) — item types now covered; costing/variants/locations/SKUs remain
6. **Dimensions** (D1) — **demoted from #4 → 🟡** via IC engagement. Remaining study-only: global vs shortcut, blocking combos, priorities.
7. ~~**Fixed assets**~~ **demoted → 🟡** via IFRS engagement. Remaining: **FA disposal** (untouched), and Chris running setup+depreciation himself in sandbox to lock 🟢.

**Leverage existing strength**: posting groups, CoA, customer setup, sales invoicing (D2 mostly, parts of D3/D4) — light revision only. **Newly leverageable** (IFRS/IC engagement): Fixed Assets setup + acquisition/depreciation, deferrals technique, **item types + General/VAT Posting Setup account resolution** (the "five tags"), **dimension defaults + flow-through** — revise toward exam framing rather than learn cold.

---

## Change-log notes (vs. pre-June-30 exam)

- **Set up Business Central**: % decreased; "Set up core functionality" had a *major* change; "Describe BC integrations" **removed**.
- **Perform BC operations**: % increased; "Perform basic tasks" *major* change; "Process journals and payments" *major* change; **"Process inventory transactions" is new**.
- **Configure financials**: no % change, minor edits only — our strong domain stayed stable.

---

## Approach (per FLIGHT-PLAN Anchor 3)

Keep learning primarily via client work + Morre. Use this gap list to drive **targeted sandbox exercises** for the 🔴 areas (same pattern as the Tinky/billing setups). Re-check this guide for any late changes, then sit the exam Q4 2026.

---

*Tentixo AB — Business Central Advisory*
