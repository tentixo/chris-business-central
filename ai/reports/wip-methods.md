# WIP Methods — Codebook & Booking Reference

**Version**: 1.0 (draft for Morre review)
**Created**: 2026-06-15
**Status**: Analysis — fulfils Morre's WIP assignment (Call 5, June 12 2026)
**Scope**: Business Central project (job) Work-In-Process methods — what they are, which to use when, and how they book against Tentixo's actual chart of accounts
**Sources**: [MS Learn — WIP methods](https://learn.microsoft.com/en-us/dynamics365/business-central/projects-understanding-wip); Tentixo CoA + Job Posting Group export (`docs/PackageCOA.xml`)

---

## 1. Why WIP exists

A project incurs **costs over time** but is **invoiced at intervals** (e.g. 50% up front / 50% at the end, or paid once but delivered over months). Between invoices, the financial statements are wrong unless you estimate the in-progress value. **WIP** is the routine that values unfinished project work in the general ledger.

The core question WIP answers: **when do you recognize cost, and when do you recognize sales?** ("Have we reached a level we'll actually get paid for?")

---

## 2. The mechanism — two dropdowns

A WIP Method (`Alt+Q` → **Project WIP Methods**) is just two fields:

- **Recognized Costs** — 5 options
- **Recognized Sales** — 6 options

| Recognized Costs (5) | Recognized Sales (6) |
|---|---|
| At Completion | At Completion |
| Cost of Sales | Contract (Invoiced Price) |
| Cost Value | Usage (Total Cost) |
| Contract (Invoiced Cost) | Usage (Total Price) |
| Usage (Total Cost) | Percentage of Completion |
| | Sales Value |

That's a theoretical **5 × 6 = 30** combinations. **Most are nonsensical or illegal.** BC ships **5 sensible presets** — and per Morre's instinct, those 5 (maybe a couple more) are all you need. You don't build 30 codes.

> **Reconciliation note**: the playbook's "7 types" and Morre's "5×5=25" were both approximations. Truth: 5 cost × 6 sales options; 5 predefined methods.

---

## 3. The 5 predefined methods — and when to use each

| Method | Recognized Costs | Recognized Sales | Recognizes... | Use when |
|---|---|---|---|---|
| **Completed Contract** | At Completion | At Completion | Nothing until project is done | High uncertainty in cost/revenue estimates; short projects that finish in one period; maximum conservatism |
| **Cost Value** | Cost Value | Contract (Invoiced Price) | Cost held as WIP asset until invoiced; sales only when invoiced | You want costs capitalised as WIP but revenue strictly tied to invoicing |
| **Cost of Sales** | Cost of Sales | Contract (Invoiced Price) | Cost matched to the invoiced %; sales only when invoiced | Conservative; revenue follows invoicing, cost matched to it |
| **Sales Value** | Usage (Total Cost) | Sales Value | Costs as incurred; **sales (incl. margin) accrued proportional to costs** | Fixed-price with a **reliable budget**; you want margin recognised as work progresses ← *Tinky uses this* |
| **Percentage of Completion** | Usage (Total Cost) | Percentage of Completion | Costs as incurred; **sales by completion %** (cost-to-budget) | Long fixed-price engagements with reliable cost budgets (classic long-term contract accounting) |

### The two big "families"
- **Recognize as you go** (Sales Value, Percentage of Completion): cost recognised when reported (`Usage (Total Cost)`), revenue accrued before invoicing. Needs a trustworthy **budget** — these formulas divide by Budget (Total Cost/Price).
- **Recognize at invoice / completion** (Cost Value, Cost of Sales, Completed Contract): revenue waits for the invoice (or project completion). Safer when estimates are shaky.

---

## 4. Tentixo codebook — project type → recommended method

| Project archetype | Recommended WIP method | Rationale |
|---|---|---|
| **Short fixed-price, invoiced once** (e.g. Tinky Heat Map, 18k) | **Sales Value** *(or Completed Contract)* | Tinky's current setting. Single short engagement — either works; Sales Value keeps it consistent with longer fixed-price work |
| **Long fixed-price, reliable budget** | **Percentage of Completion** | Recognises revenue by completion % over the project life |
| **Fixed-price, shaky/uncertain estimates** | **Completed Contract** | Don't recognise anything until delivered — avoids restating |
| **T&M / cost-reimbursable** | **Sales Value** | Margin tracks reported effort against budget |
| **Pass-through cost, bill-when-invoiced** | **Cost Value** or **Cost of Sales** | Revenue strictly tied to invoicing |

> **Prerequisite for the "recognize as you go" methods**: the project must have **Budget (Total Cost)** and **Billable (Total Price)** filled in correctly, or the formulas produce garbage. No budget → use Completed Contract.

---

## 5. How it books — mapped to Tentixo's actual accounts (J-EXT)

These are the **real account numbers** wired into the **J-EXT** Job Posting Group (external client projects — the default for clients like Tinky). Other groups (GRP-*, CTRL-*) use the same balance-sheet WIP accounts but suffix-variant P&L clearing accounts.

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

### Worked example — Sales Value (Tinky's method)
As work is reported and WIP is calculated:

**Cost recognition** (`Usage (Total Cost)` = Actual cost):
```
Dr 4411 Recognized Costs Projects, EXT      (cost hits P&L)
   Cr 1472 WIP, costs estimated
Dr 1472 WIP, costs estimated
   Cr 4421 Applied Jobs Costs Projects, EXT  (clears the applied cost)
```

**Sales recognition** (`Sales Value` = Actual price × Billable/Budget):
```
Dr 1478 WIP, invoiced
   Cr 3411 Recognized Project Sales, EXT     (revenue hits P&L)
Dr 3421 Applied Project Sales, EXT
   Cr 1478 WIP, invoiced
Dr 1477 WIP, accrued sales
   Cr 3490 Adjustment Project Sales          (accrues the not-yet-invoiced portion)
```

**On project completion**, Calculate WIP reverses the WIP entries and posts the final position:
```
Dr 3421 Applied Project Sales, EXT
   Cr 3411 Recognized Project Sales, EXT     (Amount = Invoiced Total Price)
```

This is exactly Morre's mental model: **Applied → Recognized → (Adjustment) → Invoice.**

---

## 6. The deeper principle — *when did the event happen?*

WIP is one face of a bigger accrual question (Morre + Masha, Call 5): **which period does a cost/revenue belong to?**

- A business trip booked & paid in advance, but flown next month — actualise on booking, on the flight, or on the card settlement?
- Projects add a **second layer**: you're paid a fixed price, but a trip *on* the project has its own timing.

**Rule of thumb**: post to the period the **economic event** occurred (work done / service consumed), not when cash moved. WIP and accruals are the tools that move value into the right month. (See playbook §5 bookkeeping fundamentals.)

---

## 7. Findings from the CoA / Job Posting Group export

1. ✅ **WIP is fully wired.** All 7 Job Posting Groups have every WIP account populated — WIP calc will post without account errors.
2. ⚠️ **No generic/domestic Job Posting Group** — all 7 are group/intercompany variants (EXT, GRP-MOTH/DAUG/OTHR, CTRL-ASSO/JV/OTHR). **J-EXT** is the de-facto default for external clients. *Confirm with Morre this is intended.*
3. 🐛 **Likely wiring bug — J-GRP-OTHR**: its *G/L Expense (Contract)* account is **3426** ("Applied Project Sales, GRP-OTHR" — a sales account) where every other group points at a `34**3**x` expense account; it should almost certainly be **3436** ("G/L Expenses Projects, GRP-OTHR"). Flag to Morre.

---

## 8. Open items / next steps

- [ ] **Confirm J-EXT** as the default Job Posting Group for external client projects (Morre).
- [ ] **Fix J-GRP-OTHR** G/L Expense (Contract): 3426 → 3436 (Morre).
- [ ] **Build the testing playbook** — simulate a project moving forward (book cost + revenue, run Calculate WIP each period, inspect Project WIP Entries & Project Statistics). This becomes a hands-on `ai/guides/` companion to this codebook.
- [ ] **Validate which of the 5 methods Tentixo actually wants to offer** as a standard menu (likely Sales Value + Percentage of Completion + Completed Contract; Cost Value/Cost of Sales as edge cases).
- [ ] Decide the **default WIP method** in Projects Setup.

---

*Tentixo AB — Business Central Advisory*