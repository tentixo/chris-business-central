# Project Billing — Setup Guide

**Version**: 1.0
**Created**: 2026-06-15
**Updated**: 2026-06-15 (Step 8 verified against sandbox dialog)
**Author**: Tentixo AB
**Scope**: End-to-end setup of project (job) billing in Business Central for ad-hoc, quoted engagements
**Audience**: BC functional user or administrator

---

## What this guide covers

Setting up BC's Project Billing module to invoice a one-off, quoted engagement (e.g., a fixed-price Heat Map, a workshop series, or T&M consulting). By the end, you'll have:

- A customer, contact, item, and resource configured for project work
- A project with at least one task
- Posted project journal lines (the work/deliverable)
- A draft sales invoice generated from the project, ready to post

**When to use this vs. Subscription Billing**: Project Billing is for **variable, evolving, quoted work** — new project per engagement. For **fixed recurring revenue** (retainers, managed services), use `subscription-billing-setup.md` instead. When both apply to one customer, they produce two separate invoices by design — see the Architecture note.

**Prerequisites**: posting groups configured; if the customer is new, follow Steps 1–2, otherwise skip to Step 6.

---

## The 8-step flow

Order matters because of layer dependencies — each step builds on the one before.

```
1. Customer → 2. Contact → 3. Item → 4. Resource → 5. Employee
   → 6. Project → 7. Project Journal → 8. Create Invoice
```

---

## Step 1 — Create the Customer

**Open**: `Alt+Q` → "Customers" → + New

| Field | Value (domestic SE B2B) | Notes |
|---|---|---|
| Gen. Bus. Posting Group | `EXT` | |
| VAT Bus. Posting Group | `EXT` | |
| Customer Posting Group | `DOMESTIC` | |
| Country/Region Code | `SE` | |
| Registration No. | org.nr (e.g. `5566778899`) | On General FastTab (newer BC) or Invoicing FastTab (older) — **not** the same field as VAT Registration No. |
| VAT Registration No. | `SE` + org.nr + `01` | Validate to auto-populate name/address |
| Payment Terms | `30D` | |

---

## Step 2 — Add Contacts

Creating a Customer auto-creates a company-type **Contact** card. Open it and **add person contacts** (decision-maker, billing/AP, technical lead).

Watch for duplicate contacts if the same company is both customer and vendor — merge via Contact → Actions → Merge.

---

## Step 3 — Create the Item (Service-type)

The item is the invoiceable deliverable (e.g., the fixed-price Heat Map).

**Open**: `Alt+Q` → "Items" → + New

| Field | Value | Notes |
|---|---|---|
| Type | **Service** | Service type is for project billing items (contrast: subscription items must be Non-Inventory) |
| Base Unit of Measure | `EA` | International standard; PCS maps to EA internally |
| Gen. Prod. Posting Group | `C-MAIN1` | Consulting — human-bound delivery → controls revenue account (3211) |
| VAT Prod. Posting Group | `S-FULL` | Services, full VAT. Semantic name, **not** `VAT25` (percentage-based names are an anti-pattern) |
| Inventory Posting Group | blank | Service item, no stock |
| Unit Price | `0` or a reference/catalogue price | Real prices come from price lists or the journal override — don't lock pricing into the item |

---

## Step 4 — Create the Resource (the "we sell you" side)

The resource is the consultant's billable capacity.

**Open**: `Alt+Q` → "Resources" → + New

| Field | Value | Notes |
|---|---|---|
| Type | **Person** | |
| Base Unit of Measure | `HOUR` | |
| Unit Cost | `560` | Internal cost rate |
| Unit Price | `1400` | Default sell rate — override per client/project |
| Gen. Prod. Posting Group | `C-MAIN1` | Consulting (revenue 3211) |
| VAT Prod. Posting Group | `S-FULL` | Services, full VAT — semantic, not percentage-based |

**Trap**: Unit Cost and Unit Price sit next to each other. Don't change Unit Cost when you mean Unit Price.

---

## Step 5 — Link the Employee (the "you work for us" side)

Create the parallel **Employee** record and link it to the Resource via the Resource card's `Employee No.` field. Payroll-side setup is a separate workstream — for billing, the link is what matters.

---

## Step 6 — Create the Project

**Open**: `Alt+Q` → "Projects" → + New

| Field | Value | Notes |
|---|---|---|
| Bill-to Customer No. | the customer | |
| Project Posting Group | a consulting-aligned group with WIP account configured | |
| Status | `Open` | |
| Person Responsible | the lead consultant | Pulled from Contacts |
| WIP Method | **must match project type** | e.g., Sales Value for fixed-price |

**Project Tasks**: start with **one** posting-type task (e.g., `1000 Heat Map`, or `ITSEC`). Add sub-tasks only when the engagement splits (pre-study / execution / post). Don't pre-optimise.

> ⚠️ **WIP Method is load-bearing.** If a T&M project has WIP method set to "Fixed Price" (or vice versa), WIP postings hit the wrong chart-of-accounts entries. Confirm WIP Method on the project card *before* any WIP calculation.

---

## Step 7 — Post the Project Journal

This captures the work — the deliverable (revenue) and the effort (cost).

**Open**: `Alt+Q` → "Project Journals"

**Batch hygiene**: check which batch you're in (top of the page). Use the `DEFAULT` batch for manual work. **Never** post manually to the API batch (it has its own number series for automation).

### Fixed-price vs T&M — the line-type split

| Billing model | Item lines | Resource lines |
|---|---|---|
| **Fixed price** | **Billable** (the invoiceable deliverable, e.g., HM-LITE @ 18k) | **Budget** (effort tracking only — hours don't appear on the invoice) |
| **T&M** | Usually not needed | **Both Billable and Budget** (hours are both cost unit and billing unit) |

**Example — fixed-price Heat Map:**

```
Line 1 (revenue capture):
  Type=Item, No.=HM-LITE, Project Task=1000, Qty=1,
  Unit Price=18000 (override), Line Type=Billable

Line 2 (cost capture):
  Type=Resource, No.=CHRIS, Project Task=1000, Qty=16,
  Line Type=Budget
```

For T&M: Resource lines are `Both Billable and Budget`; no separate Item line needed.

**Date shortcuts**: type `T` + Tab for today; for prior months type the short date (e.g., `0430` for April 30 — post hours to the month the work happened).

**Currency**: edit `Unit Price`, not `Unit Price (LCY)` (the LCY field auto-calculates; for SEK projects they're identical).

**Late hours**: post old hours to the correct past month. BC's invoicing picks up anything uninvoiced regardless of date, so they're captured on the next run.

**Post the journal** with **F9**.

---

## Step 8 — Create the Project Invoice

**Two ways to create the invoice:**

1. **Global**: `Alt+Q` → "Project Create Sales Invoice" → OK. Takes **all** uninvoiced billable lines, scoped by the filter below.
2. **Per task line**: from the project task → Manage → Line → Documents → Create Sales Invoice. Invoices just that task — useful to bill pre-study separately from execution.

The **Project Create Sales Invoice** dialog has two sections:

**Options**

| Field | Value | Notes |
|---|---|---|
| Posting Date | invoice date (e.g., `2026-06-15`) | |
| Document Date | invoice date | |
| Create Invoice per | **Project** | One invoice per project. Other option: **Project Task** (separate invoice per task) |

**Filter: Project Task**

| Field | Value | Notes |
|---|---|---|
| Project No. | the project | Scopes the run to one project; leave blank to bill all projects |
| Project Task No. | a task | Optional — narrow to a single task |

Click **OK** (or **Schedule…** to queue it). BC generates a draft Sales Invoice linked to the project.

### Review and post

Open the draft (`Alt+Q` → "Sales Invoices" → latest draft).

- **Project-linked lines are locked** — you can't change quantity or price on them. You *can* add extra lines (comments, one-off charges), but those additions are **not** tracked back to the project.
- **Work Description** (under "Show more" on the header): text printed above the line items — use for engagement/period descriptions.
- Review header / lines / **Statistics (F7)** — check VAT and posting groups resolve correctly.

When satisfied, **Post** (or **Post & Send** to email the customer).

After posting, the project ledger marks those lines as **invoiced** (a dot/boolean). **BC will never invoice the same line twice** — the core safety net. Open **Project Statistics** for budget vs actual, billable vs non-billable, cost vs revenue, and margin.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| WIP postings hit wrong accounts | WIP Method doesn't match project type | Set correct WIP Method on the project card (Step 6) before WIP calc |
| Hours don't appear on the invoice (fixed price) | Resource lines set to Billable instead of Budget | For fixed price, Resource lines = Budget; the Item line is the billable deliverable |
| Can't edit qty/price on the draft invoice | Lines are project-linked (locked by design) | Adjust in the project journal and recreate, or add a separate (untracked) line |
| Line invoiced unexpectedly / not at all | Line Type wrong (Billable vs Budget) | Budget lines never invoice; Billable lines do — check Step 7 |

---

## Architecture note

Project Billing is for **variable, project-based work** — quoted engagements, T&M, evolving scope. For **fixed recurring revenue**, use Subscription Billing instead. They are separate billing engines by design:

- **Different intent**: projects evolve; subscriptions are predictable.
- **Different legal terms**: project and subscription contracts typically differ (cancellation, liability, scope clauses).
- **Separate invoices**: when both are active for one customer, they generate separate invoices — this is correct, not a limitation. Projects can also span multiple customers (Gen. Bus. Posting Group per line); subscriptions are always one customer.

Revenue from both streams is aggregated per customer in **Power BI** for unified reporting — the aggregation layer is Power BI, not the invoice. See `ai/reports/tinky-billing-scenarios.md` for the full three-scenario analysis behind this decision.

---

*Tentixo AB — Business Central Advisory*