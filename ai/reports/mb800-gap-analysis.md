# MB-800 — Gap Analysis vs. Captured Knowledge

**Version**: 1.0
**Created**: 2026-06-15
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
2. **Dimensions is a whole exam sub-area — but Morre says "never use."** Real tension: for the exam you must *know* dimensions cold (setup, global/shortcut, defaults, blocking, priorities) even though Tentixo's convention avoids them. Treat dimensions as **exam-only study**.

---

## Domain 1 — Set up Business Central (20–25%)

| Sub-area | Status | Notes |
|---|---|---|
| Create & configure a company (assisted setup, config worksheet, **config package**, opening balances, data migration) | 🟡 | Config packages 🟢 (`config-package-xml-export.md`); assisted setup / opening balances / migration = gaps |
| Manage security (profiles, permission sets, security filters, security groups, auditing) | 🔴 | Not covered |
| Set up core functionality (reports/layouts, job queues, **number series**, Copilot/agents) | 🟡 | Number series 🟢 (subscription setup); reports/job queues/Copilot = gaps |
| **Set up dimensions** (values, global/shortcut, defaults, blocking combos, priorities) | 🔴 | Gap + Morre tension (see headline) |
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
| Fixed assets (depreciation books, FA classes, depreciation methods) | 🔴 | Not covered |

## Domain 3 — Configure sales and purchasing (10–15%)

| Sub-area | Status | Notes |
|---|---|---|
| Inventory setup (item settings, categories, attributes, UoM, variants, locations, item ledger relationships, **costing methods**, SKUs) | 🟡 | Item/service setup touched; costing methods / inventory / variants / SKUs = gaps |
| Master data for sales & purchasing (customer & vendor core settings) | 🟡 | Customer side ok; vendor side gap |
| Pricing & discounts (vendor purchase prices, purchase discounts, **customer sales prices**, sales discounts) | 🟡 | Sales price lists discussed; discounts & purchase pricing = study |

## Domain 4 — Perform BC operations (30–35%) — *biggest weight, increased*

| Sub-area | Status | Notes |
|---|---|---|
| Basic tasks (pages, filters, find/inspect, **Edit in Excel**, **data analysis mode**, personalize) | 🟡 | Navigation ok; Edit-in-Excel / analysis mode = practice |
| Process purchases (quotes, PO, receive, over-receive, reverse, posted invoice, recurring lines, blanket, deferrals) | 🔴 | Purchasing flow not covered |
| Process sales (quotes, convert quote, availability, ship, reverse, **sales invoice**, recurring lines, blanket, deferrals) | 🟡 | Sales invoice 🟢; quotes/shipping/blanket/deferrals = study |
| Process financial documents (invoices, credit memos, combine shipments, correct posted, prepayment) | 🟡 | Invoicing covered; credit memos / prepayment / corrections = study |
| Process journals & payments (payment & cash-receipt journals, payment reg, apply/undo entries, reverse, **bank reconciliation**, recurring, GL allocations, currency adjust, **dimension correction**, revalue) | 🔴 | Large gap — high exam value |
| Process fixed asset transactions (acquisition, depreciation, disposal) | 🔴 | Not covered |
| **Process inventory transactions** (receipts, shipments, transfers, adjust cost, count, reclassify) — *NEW topic* | 🔴 | New in June 30 outline; not covered |

---

## Priority study list (by exam weight × current gap)

1. **Process journals & payments** (D4) — heavy weight, big gap (bank rec, apply entries, payment journals, dimension correction)
2. **Process inventory transactions** (D4) — new topic, full gap
3. **Fixed assets** (D2 setup + D4 transactions) — full gap, appears twice
4. **Security & permissions** (D1) — full gap
5. **Dimensions** (D1) — full gap + study despite Morre's "never use"
6. **Purchasing / AP** (D2 + D3 + D4) — vendor side consistently weak
7. Round out **inventory setup & costing methods** (D3)

**Leverage existing strength**: posting groups, CoA, customer setup, sales invoicing (D2 mostly, parts of D3/D4) — light revision only.

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
