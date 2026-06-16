# WIP Methods — Codebook & Booking Reference

**Version**: 2.0
**Created**: 2026-06-15 · **Updated**: 2026-06-16 (Morre review, Call 6 — extended to all 8 Tentixo methods)
**Status**: Codebook for Tentixo's 8 WIP methods; archetype recommendations (§4) still pending final Morre sign-off
**Scope**: Business Central project (job) Work-In-Process methods — what they are, which to use when, how they book against Tentixo's chart of accounts, and the operational rules for running WIP safely
**Sources**: [MS Learn — WIP methods](https://learn.microsoft.com/en-us/dynamics365/business-central/projects-understanding-wip); Tentixo exports `docs/PackageWIP_METHODS.xml` (table 1006), `docs/PackageCOA.xml`; Morre Calls 5 (June 12) & 6 (June 15)

---

## 1. Why WIP exists

A project incurs **costs over time** but is **invoiced at intervals** (e.g. 50% up front / 50% at the end). Between invoices the financial statements are wrong unless you estimate the in-progress value. **WIP** values unfinished project work in the general ledger.

**Morre's key insight**: without WIP, the *calculated* costs on resources (e.g. a consultant's salary cost rate) are only visible inside the project's lower panel — the margin lives off the books. **Running WIP makes those calculated costs *real and visible in the chart of accounts.*** That's the whole point.

The core question WIP answers: **when do you recognize cost, and when do you recognize sales?**

---

## 2. The mechanism — two dropdowns

A WIP Method (`Alt+Q` → **Project WIP Methods**, table **1006**) is two fields:

| Recognized Costs (5 options) | Recognized Sales (6 options) |
|---|---|
| At Completion | At Completion |
| Cost of Sales | Contract (Invoiced Price) |
| Cost Value | Usage (Total Cost) |
| Contract (Invoiced Cost) | Usage (Total Price) |
| Usage (Total Cost) | Percentage of Completion |
| | Sales Value |

Theoretical space = **5 × 6 = 30** combinations (Morre estimated 25; the extra row is the 6th sales option). Most are **invalid ("illegal") variants** — you don't build 30 codes. BC ships **5 system-defined presets**; **Tentixo added 3 more** (researched, "done for a reason") for a **total of 8**.

---

## 3. The 8 Tentixo WIP methods

Decoded from `docs/PackageWIP_METHODS.xml`. ⭐ = the 3 Tentixo additions.

| Code | Recognized Costs | Recognized Sales | What it recognizes |
|---|---|---|---|
| **COMPLETED CONTRACT** | At Completion | At Completion | Nothing until the project completes |
| **COST OF SALES** | Cost of Sales | Contract (Invoiced Price) | Cost matched to invoiced %; sales only when invoiced |
| **COST VALUE** | Cost Value | Contract (Invoiced Price) | Cost held as WIP asset; sales only when invoiced |
| **POC** (Percentage of Completion) | Usage (Total Cost) | Percentage of Completion | Cost as incurred; sales by completion % (cost/budget) |
| **SALES VALUE** | Usage (Total Cost) | Sales Value | Cost as incurred; sales (incl. margin) accrued proportional to cost |
| ⭐ **INVOICED C-P** (Invoiced Costs & Invoiced Price) | Contract (Invoiced Cost) | Contract (Invoiced Price) | **Both** cost and sales recognized **only when invoiced** — fully invoice-driven |
| ⭐ **INVOICED C-TOTAL P** (Invoiced Costs & Total Price) | Contract (Invoiced Cost) | Usage (Total Price) | Cost only when invoiced; sales at total (actual) price |
| ⭐ **TOTAL C-P** (Total Costs & Total Price) | Usage (Total Cost) | Usage (Total Price) | Both at actuals — cost as incurred, sales at total actual price |

### The two big families
- **Recognize as you go** (SALES VALUE, POC, TOTAL C-P): cost recognized when reported (`Usage (Total Cost)`); revenue accrued before invoicing. **Needs a trustworthy budget** — the formulas divide by Budget (Total Cost/Price).
- **Recognize at invoice / completion** (COST VALUE, COST OF SALES, INVOICED C-P, INVOICED C-TOTAL P, COMPLETED CONTRACT): revenue (and sometimes cost) waits for the invoice or completion. Safer when estimates are shaky.

### What Morre's 3 additions unlock
The 5 MS presets never use **Contract (Invoiced Cost)** on the cost side, nor **Usage (Total Price)** on the sales side. Tentixo's 3 additions cover those:
- **INVOICED C-P** — strict invoice-matched on *both* sides. Use when nothing should hit the P&L until billed, but you still want WIP to park cost/revenue in the interim.
- **INVOICED C-TOTAL P** — asymmetric: hold cost until invoiced, but accrue sales at actual total price.
- **TOTAL C-P** — recognize everything at actual values as it happens (no budget-ratio smoothing like SALES VALUE/POC).

> ⚠️ **Archetype mapping (§4) is my interpretation** of these three — Morre asked to "check the logic." Treat §4 as a proposal pending his sign-off.

---

## 4. Codebook — project archetype → method *(proposal, pending Morre)*

| Project archetype | Recommended method | Rationale |
|---|---|---|
| Short fixed-price, invoiced once (e.g. Tinky Heat Map) | **SALES VALUE** *(or COMPLETED CONTRACT)* | Tinky's current setting; consistent with longer fixed-price work |
| Long fixed-price, reliable budget | **POC** | Revenue by completion % over the project life |
| Fixed-price, uncertain estimates | **COMPLETED CONTRACT** | Nothing recognized until delivered — avoids restating |
| T&M / cost-reimbursable, reliable budget | **SALES VALUE** | Margin tracks reported effort vs budget |
| T&M, recognize at actuals (no budget smoothing) | ⭐ **TOTAL C-P** | Cost + sales at actual totals as incurred |
| Strict invoice-driven (milestone/pass-through), P&L only at billing | ⭐ **INVOICED C-P** | Both sides recognized only when invoiced |
| Hold cost to invoice but accrue full sales | ⭐ **INVOICED C-TOTAL P** | Asymmetric cost/sales timing |
| Revenue strictly tied to invoicing, cost capitalised | **COST VALUE** / **COST OF SALES** | Conservative revenue |

> **Prerequisite for "recognize as you go" methods**: the project must have **Budget (Total Cost)** and **Billable (Total Price)** entered, or the formulas produce garbage. No budget → use COMPLETED CONTRACT or an invoice-driven method.

---

## 5. How it books — Tentixo accounts (J-EXT) — *Morre-approved as "simplified, makes sense"*

`J-EXT` is the **confirmed default** for external client projects (see §7). Other groups (`GRP-*`, `CTRL-*`) share the balance-sheet WIP accounts but use suffix-variant P&L clearing accounts.

| Role | Account | Name |
|---|---|---|
| WIP Costs (asset) | 1472 | WIP, costs estimated |
| WIP Accrued Costs (asset) | 1471 | WIP, costs incurred |
| WIP Accrued Sales (asset) | 1477 | WIP, accrued sales |
| WIP Invoiced Sales | 1478 | WIP, invoiced |
| Recognized Costs (P&L) | 4411 | Recognized Costs Projects, EXT |
| Recognized Sales (P&L) | 3411 | Recognized Project Sales, EXT |
| Job Costs Applied | 4421 | Applied Jobs Costs Projects, EXT |
| Item / Resource / G/L Costs Applied | 4431 / 4441 / 4451 | Applied …Costs Projects, EXT |
| G/L Expense (Contract) | 3431 | G/L Expenses Projects, EXT |
| Job Sales Applied | 3421 | Applied Project Sales, EXT |
| Cost Adjustment | 4490 | Jobs Cost Adjustment |
| Sales Adjustment | 3490 | Adjustment Project Sales |

**The move that confuses users** (Morre's warning): a *direct* sale of consulting posts revenue straight to **3211 / 3221 / 3231** (C-MAIN1/2/3). But once a project uses WIP, **WIP moves it**: recognized sales go to **3411**, cost parks on **44xx**, and on the final run / invoice it lands on **3421**. Each WIP run does ~40 postings and counter-postings back and forth. So a user may look for "Chris" on 3221 and not find him — *he's been moved by WIP*. **Users must understand this flow** or they'll think entries were deleted.

### Worked example — SALES VALUE
```
Cost (Usage Total Cost):
  Dr 4411 Recognized Costs Projects, EXT   Cr 1472 WIP, costs estimated
  Dr 1472 WIP, costs estimated             Cr 4421 Applied Jobs Costs Projects, EXT
Sales (Sales Value = Actual price × Billable/Budget):
  Dr 1478 WIP, invoiced                    Cr 3411 Recognized Project Sales, EXT
  Dr 3421 Applied Project Sales, EXT       Cr 1478 WIP, invoiced
  Dr 1477 WIP, accrued sales               Cr 3490 Adjustment Project Sales
```
The applied → recognized loop **adjusts repeatedly** until the invoice or project close. Morre's model: **Applied → Recognized → (Adjust, looping) → Invoice.**

---

## 6. ⚠️ Operational rules — non-negotiable (Morre, Call 6)

Changing WIP after it has run is **"absolutely devastating."** Follow these:

1. **Set the correct WIP method at project START.** Changing the method after WIP has run makes BC try to *reverse postings on accounts it never posted to* — it doesn't cleanly undo the old method first. Corrupts the ledger.
2. **Always run WIP every month**, and **run a final WIP immediately before closing the project.** If you close with WIP still calculated, lingering WIP entries are stranded and **cannot be backtracked**.
3. **Completion ≠ closing.** *Completion* = you've run the final WIP and the position is correct. *Closing* = just a button afterwards. Order: final WIP → then close.
4. **Trust BC in between.** It does dozens of back-and-forth postings each run; this is correct behaviour, not errors. Don't "fix" it manually.

---

## 7. Cost capture — use Items, not direct G/L (Morre, Call 6)

How you capture project cost determines whether WIP is *correct*:

- **Prefer Items over booking on a G/L account directly.** Booking cost straight to a G/L account in the project journal **hides granularity from the project** — you lose the real per-purchase cost.
- **Items track true cost via FIFO + scanned purchase invoices.** Map your item to the vendor's purchase item; the exact purchase cost is logged, so WIP for items is accurate. (Resource costs, by contrast, are *calculated/planned* rates — like manufacturing average cost, they're dangerous if not kept updated, e.g. after a salary raise.)
- **Use "purchase items"** — things you buy but never sell (e.g. **hotel / accommodation**). Tentixo already has such groups. Setup cost: you must create a **Gen. Prod. Posting Group** so the item lands on the right account — a one-time fiddle that pays off in cost accuracy.

---

## 8. The deeper principle — *when did the event happen?*

WIP is one face of the accrual question: **which period does a cost/revenue belong to?** A trip booked & paid in February but flown in June — recognize on booking, card settlement, or travel? If it's *on a project*, **WIP moves it to the right period automatically** once it's tagged correctly — you don't have to manage it manually (the alternative on direct invoices is deferrals). Post to the period the **economic event** occurred.

---

## 9. Status & outstanding issues

| Item | Status |
|---|---|
| All 8 methods documented | ✅ this version |
| **J-EXT as external-client default** | ✅ **Confirmed by Morre** — no domestic job group (geography is on the customer card; group separation is needed for intercompany consolidation, e.g. Lasernet SE × DK) |
| Booking mapped to real accounts (J-EXT) | ✅ Morre approved ("simplified, makes sense") |
| Operational rules + item-costing | ✅ captured (§6, §7) |
| 🐛 **J-GRP-OTHR** G/L Expense (Contract) 3426 → 3436 | ⏳ **Still open** — not explicitly confirmed in Call 6; raise again |
| §4 archetype → method mapping for the 3 new methods | ⏳ **Pending Morre sign-off** ("check the logic") |
| Default WIP method in Projects Setup | ⏳ Not yet decided |
| **NEW — Consolidation research** (Morre assigned) | ⏳ Explain BC consolidation basics + why the group-based CoA/job posting enables automatic consolidation. Separate research note. |
| Build the hands-on **WIP testing playbook** | ✅ Done → `ai/guides/wip-testing-playbook.md` |

---

*Tentixo AB — Business Central Advisory*
