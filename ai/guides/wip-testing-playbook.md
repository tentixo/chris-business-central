# WIP Testing Playbook — drive a project and watch WIP behave

**Version**: 1.0
**Created**: 2026-06-16
**Author**: Tentixo AB
**Scope**: A hands-on sandbox exercise — set up a throwaway project, post cost + sales across periods, run Calculate WIP / Post WIP to G/L, and inspect exactly where the money moves. Companion to the codebook `ai/reports/wip-methods.md`.
**Audience**: BC functional user learning WIP (do this in a **sandbox**, not production)
**Sources**: [MS Learn — Calculating WIP walkthrough](https://learn.microsoft.com/en-us/dynamics365/business-central/walkthrough-calculating-work-in-process-for-a-job); Morre Calls 5–6

---

## What you'll learn

By running this once you'll *see*, in real accounts:
- How WIP **parks** project value on the balance sheet between invoices and **recognizes** it in the P&L.
- How WIP **moves** postings (the ~40 back-and-forth entries Morre warned about) — e.g. consulting revenue off `3211` onto `3411`/`3421`.
- The two-step rhythm: **Calculate WIP** (review) → **Post WIP to G/L** (commit).
- Why you **set the method at the start** and **run a final WIP before closing**.

> ⚠️ **Golden rules before you start** (from codebook §6):
> 1. Set the **WIP Method at project start** — never change it after WIP has run (BC will try to reverse postings on accounts it never touched).
> 2. Run WIP **every period**, and a **final WIP before closing**. Closing with un-run WIP strands entries you can't backtrack.
> 3. **Completion ≠ closing** — final WIP first, *then* close.
> To compare methods, use a **separate test project per method** — don't switch methods on one project.

---

## 0. Prerequisites (one-time)

- A sandbox you can post in, with the Tentixo CoA/posting groups.
- A **test customer** (don't use a real client — e.g. create `ZZ-WIPTEST`, Customer Posting Group `EXT`).
- Confirm the **J-EXT Job Posting Group** has its WIP accounts wired (it does — see codebook §5).

---

## 1. Create the test project

`Alt+Q` → **Projects** → **+ New**

| Field | Value | Notes |
|---|---|---|
| Description | `WIP TEST - Sales Value` | name it after the method you're testing |
| Bill-to Customer No. | `ZZ-WIPTEST` | the test customer |
| **Job/Project Posting Group** | **`J-EXT`** | external default |
| Status | `Open` | |

**Set the WIP method NOW** — on the **Posting** FastTab:
| Field | Value |
|---|---|
| **WIP Method** | `SALES VALUE` (for the first run; later repeat with others) |
| **WIP Posting Method** | `Per Project` (simplest) or `Per Project Ledger Entry` |

### Add a task and mark it for WIP
Choose **Project Task Lines**:
- Add one **Posting**-type task, e.g. `1000` "Test work".
- In the **WIP-Total** column, set the group boundary: a `Total` line defines the range; `Excluded` drops a posting task from WIP. For a single task you can leave the posting line blank and rely on the project-level calc. (Use `Excluded` later to prove a task drops out of the WIP figure.)

### Give it a budget (required for "recognize as you go")
SALES VALUE / POC / TOTAL C-P divide by budget — without it the formula produces garbage. On the planning lines set **Budget**: e.g. Budget (Total Cost) 10,000 and Billable (Total Price) 18,000 so there's a margin to watch.

---

## 2. Period 1 — post some cost (no invoice yet)

`Alt+Q` → **Project Journals** (DEFAULT batch).

Post a cost line — prefer an **Item** or **Resource** (see codebook §7 on why Items give true cost):
```
Type=Resource, No.=CHRIS, Project Task=1000, Qty=10 hrs, Line Type=Budget/Billable as per model
```
Post with **F9**. (This is *usage* — actual cost is now on the project, but nothing is in the P&L as project revenue/cost yet.)

### Calculate WIP
Project Card → **WIP** action → **Calculate WIP** → on **Project Calculate WIP**:
| Field | Value |
|---|---|
| No. | your test project |
| Posting Date | end of period 1 (later than the work date) |
| Document No. | `1` (for traceability) |

**OK**. Expect a warnings message — that's normal.

### Review BEFORE posting
- Project Card → **WIP and Recognition** FastTab → look at the **To Post** column (e.g. `Recog. Costs Amount`, `Recog. Sales Amount`). Nothing has hit the G/L yet.
- Project Card → **WIP Entries** → see the calculated entry (one per calculation run).
- `Alt+Q` → **Project WIP Cockpit** → **Show Warnings** to read any warnings.

### Post WIP to G/L
Project Card → **WIP** → **Post WIP to G/L** → set **Document No.** → **OK**.

### Verify where it landed (the payoff)
- Project Card → **WIP and Recognition** → the **Posted** column is now filled (`Recog. Costs G/L Amount` etc.).
- Project Card → **WIP G/L Entries** → see the G/L postings.
- Cross-check the **actual accounts** (codebook §5, J-EXT):
  - cost parked on **1472 / 1471** (WIP asset), recognized cost on **4411**;
  - accrued sales on **1477**, recognized sales on **3411**.

You've now made the calculated cost **real and visible in the CoA** — Morre's whole point.

---

## 3. Period 2 — add cost + an invoice, watch the "move"

1. Post more usage in the **Project Journal** (another few hours / an item).
2. Create a **project invoice** (see `project-billing-setup.md` §8) and post it.
3. **Calculate WIP** again (Posting Date = end of period 2, Document No. `2`) → review → **Post WIP to G/L**.

**What to observe**: the invoice posted revenue directly (e.g. `3211`/`3421`), but WIP **moves** it — you'll see counter-postings shuffling between `3411` (recognized), `3421` (applied), `1477`/`1478` (WIP), `3490` (adjustment). This is the **applied → recognized → adjust loop**. A user looking for the revenue on `3211` won't find it — *WIP moved it*. That's correct.

---

## 4. Completion — final WIP, then close

1. Post any final usage and the final invoice.
2. **Calculate WIP** one last time → review → **Post WIP to G/L**. At completion, WIP **reverses the parked WIP** and lands everything on the final P&L accounts (`Dr 3421 → Cr 3411` for the invoiced total).
3. Check **WIP and Recognition** shows no remaining WIP (balance-sheet WIP accounts net to zero for the project).
4. **Only now** set the project **Status = Completed** and close.

> If you close *before* the final WIP, the parked WIP lingers and can't be backtracked — that's the trap.

---

## 5. Reversing a WIP posting (if you got it wrong)

Project Card → **WIP** → **Post WIP to G/L** → set **Reversal Document No.** and **Reversal Posting Date** (= the original WIP posting date) → tick **Reverse Only** → **OK**. Then check **WIP G/L Entries** show **Reversed**, fix the inputs (e.g. WIP-Total on tasks, dates), recalculate, and post again.

---

## 6. Compare methods (the learning loop)

Repeat §1–4 on **fresh test projects**, one per method, same budget/usage, and diff the **WIP and Recognition** figures:

| Test project | WIP Method | What to notice |
|---|---|---|
| WIP TEST - Sales Value | `SALES VALUE` | sales accrued proportional to cost (margin shows early) |
| WIP TEST - POC | `POC` | sales by completion % (cost/budget) |
| WIP TEST - Completed | `COMPLETED CONTRACT` | nothing recognized until completion |
| WIP TEST - Cost Value | `COST VALUE` | cost capitalised; sales only when invoiced |
| WIP TEST - Total C-P | `TOTAL C-P` ⭐ | both at actual totals — no budget smoothing |
| WIP TEST - Invoiced C-P | `INVOICED C-P` ⭐ | nothing recognized until invoiced (both sides) |

(See codebook §3 for all 8.) **Never** change the method on an existing project to compare — always a new project.

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| WIP calc empty / zero recognized sales | No budget (Total Cost/Price) on planning lines | Add budget — required for SALES VALUE / POC / TOTAL C-P |
| Warnings after Calculate WIP | Normal — review them | **Project WIP Cockpit** → Show Warnings |
| Revenue "disappeared" from 3211/3221 | WIP moved it to 3411/3421 | Expected — read the WIP G/L Entries; it's the move, not a deletion |
| Posted WIP looks wrong | Wrong WIP-Total / dates / method | **Reverse Only** (§5), correct, recalc, repost |
| Method change wreaked havoc | Method changed after WIP ran | Don't — start a new project (golden rule #1) |
| WIP lingering after close | Closed before final WIP run | Can't backtrack — always final-WIP before closing |

---

## 8. Cleanup

These are throwaway test projects in a sandbox. Once you've learned the behaviour, leave them (sandbox) or remove per your sandbox-hygiene practice. **Never** run this loop on a live client project except as the real monthly WIP process.

---

*Tentixo AB — Business Central Advisory*
