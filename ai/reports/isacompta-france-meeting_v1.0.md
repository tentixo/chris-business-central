# IsaCompta / France Double-Bookkeeping — Meeting Summary

**Date**: 2026-06-23 (summary) · **Meeting**: 2026-06-16, 11:31 (58 min)
**Source**: `docs/IsaCompta usage.docx` (Teams recording transcript)
**Participants**: Camilla Höög, Lars Mårelius ("Morre"), Chris Mansson, **Veronique Moncere (France entity accountant)**, Jevgēnijs Jemeljanovs ("Jeff" — dev)
**Purpose**: Understand *why* France still runs two accounting systems in parallel (IsaCompta + Business Central) and identify what to fix to retire the double-entry.

---

## ⚑ The situation in one paragraph

France keeps **double books**: **IsaCompta** (the French auditor's accounting software, used to file the **FEC** report to the French tax administration) **and** Business Central. Veronique records into both, compares balances monthly/at year-end, and 2025 has now been closed in BC. She has **not** imported BC data into IsaCompta directly — she only *compares* — because the auditor's import would **replace** existing data and the two can't reconcile cleanly. Account mapping (FR ↔ BC) is essentially done; the gaps are **dimensions/granularity** and a handful of accounts where **partner margin** and **deferred income/cost** are handled differently between the two systems.

---

## 1. Root problems identified

| # | Problem | Detail |
|---|---|---|
| P1 | **Partner margin handled wrong upstream** | BC mixes partner margin with costs on shared accounts. French law: partner margin is a **reduction of sales** (a minus on sales), **not a cost**. Morre: likely a **group/mother-company setup issue** (suspected since ~2018) — fixing it downstream in the FR mapping is patching the wrong end. Carla hit the same issue. |
| P2 | **Deferred income/cost differs between systems** | The biggest reconciliation gap. Same sales/charges/products in both, but the **year-end profit differs** — traced to deferred (recognized-in-advance) accounts. Veronique reconciles via an **error-prone Excel +/- file** each month. |
| P3 | **IsaCompta can't compare an imported period** | The auditor's tool would *replace* historical values on import, so they can't compare BC vs IsaCompta for the same period (system limitation, not human — auditors "are not geeks"). Workaround: import from a single start date without erasing the past. |
| P4 | **FEC export not finalized** | BC→FR export exists in principle (same engine as the FEC report — convert BC account no. → French account no.), but the import/comparison friction (P3) means Veronique never adopted it. |

---

## 2. Action register

| # | Action | Owner | Notes |
|---|---|---|---|
| A1 | **Fix partner-margin handling in BC** — find the legally-correct IFRS/France treatment, then tag/separate it (own account or shared-account tag), then re-check the FR mapping difference | **Morre + Chris** | Multi-step; **ties into the IFRS-16 work**. Step 1 = correct setup upstream; Step 2 = map to FR; Step 3 = measure residual difference |
| A2 | **Build a deferred income/cost report** (Power BI) off the **deferral tags** — each deferral links to its invoice; group by invoice type so the auditor can see what sits in the deferred accounts | **Chris / Morre** | ~1 week. Replaces Veronique's manual Excel; Morre has the same auditor question on his own books |
| A3 | **Finalize FEC-style export** BC→French account numbers | **Jeff** (build) · **Veronique** (mapping) | Accounts mapped; **dimensions + finer granularity still open** |
| A4 | **Confirm France VAT rule — debits vs payments** (realized vs unrealized VAT) | Chris / Veronique | Gate for e-invoicing; links to the existing FR VAT realized/unrealized thread |
| A5 | **Scope EU XML VAT / e-invoicing reporting** so France reports directly (no manual entry) | **Chris** ("you got this") | Drivers: **e-invoicing mandatory ~Sept 2027** + **10-day intra-EU transaction reporting**. Morre: BC VAT granularity likely already supports it (standard EC Sales List, or build via Gemini if MS isn't ready) |
| A6 | **Reporting-basis (Rillion) note** — set the report up so it's automatic for Veronique; flag that the issue/received-basis change isn't visible directly in the numbers | Morre | "New flow" — report can be done in ~2 weeks given the pristine prep |
| A7 | **More day-to-day support for Veronique** — work problems *together* rather than her solving alone | Jeff (raised) / team | — |

---

## 3. Open question (unresolved)

> **Veronique:** *"Are we sure we'll still be on Business Central in a year?"* — wary of investing heavy work after ~2 years of software churn. **Not answered in the meeting.** Worth surfacing before committing A1–A5 effort.

---

## 4. Relevance to the MB-800 plan / our learning

- **Deferrals** (A2), **VAT / EC Sales List / e-invoicing XML** (A4/A5), and **financial reporting / account mapping** (A3) all map to MB-800 *Configure financials* + *Perform operations*. Track alongside [`vat-gaps-research.md`](vat-gaps-research.md) and the IFRS engagement channel ([`mb800-gap-analysis.md`](mb800-gap-analysis.md) §Knowledge channel).
- **Partner margin** (A1) is an IFRS/group-setup topic Morre explicitly links to the IFRS-16 work — keep it with [`ifrs-16-uk-frs102-bc-implementation_v1.0.md`](ifrs-16-uk-frs102-bc-implementation_v1.0.md).

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-23 | Initial — summary of the 2026-06-16 IsaCompta/France meeting (Camilla, Morre, Chris, Veronique, Jeff). Double-bookkeeping situation, 4 root problems (partner margin, deferred income/cost, IsaCompta import limitation, FEC export), 7-item action register, unresolved "still on BC in a year?" question, MB-800 relevance. |
