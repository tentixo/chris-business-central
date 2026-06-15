# Tiny Minds — Billing Scenario Comparison

**Version**: 1.1
**Status**: Decided — Option A confirmed by Morre (June 9, 2026)
**Created**: 2026-06-09
**Updated**: 2026-06-09
**Scope**: Three approaches to handling mixed billing (retainer + ad-hoc projects) for a single client

---

## Client context

**Customer**: Tiny Minds Lab AB (product/app: TinkyLär, referred to as "Tinky")
**Existing setup**: Customer card, Contact, Item `HM-LITE` (Service type), Resource Chris, Project with task `ITSEC`. First invoice posted (1× HM-LITE @ 18,000 SEK).

**Revenue streams going forward**:

| Stream | Nature | Amount | Cadence |
|--------|--------|--------|---------|
| Monthly retainer | Fixed security posture support | 15,000 SEK/month | Recurring, no defined end |
| Ad-hoc projects | Quoted fixed-price security work | Varies (e.g., 50k–150k) | As needed, scoped per engagement |

**Business rules** (confirmed):
- Retainer is truly fixed — 15k regardless of hours consumed
- Retainer continues running even when ad-hoc projects are active
- One invoice to the client per month (all streams combined)
- Revenue earned in the month invoiced — no deferrals needed

---

## Common setup (applies to all three options)

### Items needed

| Item No. | Description | Type | Gen. Prod. PG | VAT Prod. PG | Unit Price |
|----------|-------------|------|---------------|--------------|------------|
| `HM-LITE` | Heat Map Lite (exists) | Service | C-MAIN1 | S-FULL | 0 (override via price list) |
| `SEC-RETAINER` | Monthly Security Retainer | Service | C-MAIN1 | S-FULL | 0 (override via price list or subscription) |
| `SEC-PROJECT` | Security Project Work | Service | C-MAIN1 | S-FULL | 0 (override via price list) |

All items land on **32xx** (Human/Consulting) accounts through the C-MAIN1 posting group — retainer is human-bound regardless of the flat-fee pricing model (GVH litmus test: remove humans, can we still deliver? No.).

### Posting group flow (same for all options)

```
Customer: Tiny Minds → Cust. Posting Group → Receivables account (1510/1511)
Item: SEC-RETAINER   → Gen. Prod. PG: C-MAIN1 → Revenue account (32xx)
Item: SEC-PROJECT    → Gen. Prod. PG: C-MAIN1 → Revenue account (32xx)
VAT:                 → Bus: DOM × Prod: S-FULL → 25% VAT account (2611)
```

Posting groups are identical across all three options — the difference is **which billing engine generates the invoice lines**, not where the money lands in the ledger.

---

## Option A: Subscription Billing + Project Billing (two invoices)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ SUBSCRIPTION BILLING (retainer)                             │
│                                                             │
│  Subscription Package: "Security Retainer"                  │
│    └── Package Line: SEC-RETAINER, 15k/month, rhythm 1M    │
│                                                             │
│  Customer Subscription Contract: Tiny Minds                 │
│    ├── Contract Type: no deferrals                          │
│    └── Contract Line → Subscription Line (15k, next bill)  │
│                                                             │
│  Billing Template: Monthly, auto-create proposal + document │
│    └── Generates: Sales Invoice (retainer only)             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROJECT BILLING (ad-hoc work)                               │
│                                                             │
│  Project: "Tinky — [Project Name]"                          │
│    └── Task: e.g., SEC-DEPLOY                               │
│         └── Planning Lines: 1× SEC-PROJECT @ quoted price   │
│                                                             │
│  Project Journal → "Create Sales Invoice"                   │
│    └── Generates: Sales Invoice (project only)              │
└─────────────────────────────────────────────────────────────┘
```

### Monthly workflow

**Retainer-only months** (no active project):
1. Billing Template auto-runs → creates billing proposal → creates draft Sales Invoice
2. Review and post. Done. ~1 minute of human effort.

**Months with active project**:
1. Billing Template auto-creates retainer invoice (as above)
2. Separately, post project journal lines and run "Create Sales Invoice" for the project
3. Post both invoices
4. **Client receives two invoices this month**

### Tinky's invoice experience

| Month | Active streams | Invoices received |
|-------|---------------|-------------------|
| Jul 2026 | Retainer only | 1 invoice (15k) |
| Aug 2026 | Retainer only | 1 invoice (15k) |
| Sep 2026 | Retainer + project | 2 invoices (15k + project amount) |
| Oct 2026 | Retainer + project closes | 2 invoices (15k + final project) |
| Nov 2026 | Retainer only | 1 invoice (15k) |

### Reporting / P&L visibility

- **Retainer revenue**: tracked on the Subscription Contract → contract analysis entries, renewal history, price update trail
- **Project revenue**: tracked on the Project → budget vs actual, WIP, margin per task
- **Blended view**: Customer Ledger Entries show all invoices regardless of source. AR aging, customer balance, payment history — all unified at the customer level
- **Clean separation**: project P&L reflects only project work. Retainer revenue lives in its own container. No confusion about whether a project is "done" or not.

### Setup effort

| Step | One-time or recurring |
|------|----------------------|
| Create Item `SEC-RETAINER` | One-time |
| Create Subscription Package + Package Line | One-time |
| Create Customer Subscription Contract | One-time |
| Create Billing Template | One-time (reusable across clients) |
| Monthly retainer invoice | Automated |
| Ad-hoc project setup | Per project |

### Verdict

| | |
|---|---|
| **Morre-alignment** | High — clean separation, architecture-first, posting groups do the work |
| **Automation** | Retainer is fully automated. Project is manual (as it should be). |
| **One invoice?** | No — two invoices when both streams are active |
| **Scalability** | Excellent. Add 10 retainer clients → Billing Template handles them all in one batch run |
| **Learning value** | High — you learn both billing engines on a simple case |
| **Risk** | Low. Worst case: client asks "why two invoices?" and you explain. |

---

## Option B: Subscription Billing + Project Billing with manual merge

### Architecture

Same as Option A, but with one critical difference: the Billing Template does **not** auto-post. Instead, it creates a draft invoice that you manually combine with project lines before posting.

```
┌──────────────────────────────────────────────────────────────────┐
│ MERGE WORKFLOW (monthly)                                         │
│                                                                  │
│  Step 1: Billing Template → Draft Sales Invoice (retainer line)  │
│  Step 2: "Create Sales Invoice" from Project → HOLD, don't post │
│  Step 3: Manually copy project lines onto the draft from Step 1  │
│          (or: create project invoice first, add retainer line)   │
│  Step 4: Post the combined invoice                               │
└──────────────────────────────────────────────────────────────────┘
```

### Monthly workflow

**Retainer-only months**:
1. Billing Template creates draft invoice
2. Review and post. Same as Option A.

**Months with active project**:
1. Billing Template creates draft retainer invoice (don't post yet)
2. Post project journal lines
3. Instead of "Create Sales Invoice" from the project, manually add project lines to the draft retainer invoice
4. Verify totals, post the combined invoice
5. **Client receives one invoice**

### The manual merge step in detail

This is the awkward part. BC's "Create Sales Invoice" from a project creates a *new* Sales Invoice document. It doesn't know about the draft sitting there from the Billing Template. So the merge options are:

1. **Copy lines manually**: Open the draft retainer invoice, manually add a line for the project item, amount, and description. Then mark the project planning lines as invoiced manually. This bypasses the project's own invoicing mechanism — **you lose the automatic link between project ledger entries and the invoice**.

2. **Delete + recreate**: Delete the auto-generated draft, create a blank Sales Invoice manually, add both the retainer line and project line(s). Same problem — project invoicing link is broken.

3. **Use "Get Project Lines"**: Some BC setups allow pulling project lines into an existing Sales Invoice via a "Get Project Lines" function (similar to "Get Shipment Lines"). This preserves the project link. **Need to verify this exists and works alongside subscription billing lines on the same document.**

### Tinky's invoice experience

| Month | Active streams | Invoices received |
|-------|---------------|-------------------|
| Jul 2026 | Retainer only | 1 invoice (15k) |
| Sep 2026 | Retainer + project | 1 invoice (15k + project) |

One invoice every month — the stated preference.

### Reporting / P&L visibility

- If the merge preserves project links ("Get Project Lines"): same as Option A
- If manual line copy: **project reporting is degraded** — the invoice isn't linked back to the project's planning lines, so budget vs actual may not reconcile automatically

### Verdict

| | |
|---|---|
| **Morre-alignment** | Medium — correct architecture underneath, but the merge layer is a manual workaround |
| **Automation** | Retainer draft is automated. Merge step is manual and error-prone. |
| **One invoice?** | Yes |
| **Scalability** | Poor. Every client with both streams needs a manual merge every month. 10 clients = 10 manual merges. |
| **Learning value** | Medium — you learn both engines but also learn a fragile workaround |
| **Risk** | Medium. If "Get Project Lines" works on the draft → workable. If not → broken project audit trail. |

**Key question for Morre**: Does "Get Project Lines" work on a Sales Invoice that was created by the Subscription Billing module? If yes, Option B becomes more viable. If no, the merge breaks the project link and this option is not worth pursuing.

---

## Option C: Everything through Projects (skip Subscription Billing)

### Architecture

No Subscription Billing module. The retainer is a perpetual Project with a recurring monthly task. Ad-hoc work is a separate Project (or separate tasks on a shared project).

```
┌─────────────────────────────────────────────────────────────┐
│ PROJECT: "Tinky — Security Retainer"                        │
│  └── Task: RETAINER                                         │
│       └── Planning Line: SEC-RETAINER, 15k/month            │
│           (Budget line, repeated each month via journal)     │
│                                                             │
│ PROJECT: "Tinky — [Ad-hoc Project Name]"                    │
│  └── Task: SEC-DEPLOY                                       │
│       └── Planning Lines: SEC-PROJECT @ quoted price        │
└─────────────────────────────────────────────────────────────┘

Both projects → "Create Sales Invoice" → one combined invoice
(BC can combine when creating invoices for the same Bill-to Customer)
```

### Monthly workflow

**Retainer-only months**:
1. Open Project Journal for the retainer project
2. Post: 1× SEC-RETAINER @ 15,000 SEK for the current month
3. Run "Create Sales Invoice" from the retainer project
4. Review and post. Done.

**Months with active project**:
1. Post retainer journal line (as above)
2. Post project journal lines for the ad-hoc project
3. Run "Create Sales Invoice" — BC can combine lines from multiple projects for the same Bill-to Customer into one invoice document
4. One invoice with both the retainer line and the project line(s)
5. **Client receives one invoice**

### The retainer "project" — what it looks like

```
Project Card: Tinky — Security Retainer
├── Bill-to: Tiny Minds Lab AB
├── Status: Open (perpetually)
├── WIP Method: N/A or Cost Value (no completion %)
├── Person Responsible: Chris
│
└── Task: RETAINER
     ├── Planning Line Type: Budget
     ├── Item: SEC-RETAINER
     ├── Quantity: 1 per month
     └── Unit Price: 15,000 SEK (from price list)
```

Each month you post a journal line against this task. The project accumulates 12 × 15k = 180k/year in revenue. It never "completes" in the traditional sense — it's a billing container, not a deliverable container.

### Tinky's invoice experience

| Month | Active streams | Invoices received |
|-------|---------------|-------------------|
| Jul 2026 | Retainer only | 1 invoice (15k) |
| Sep 2026 | Retainer + project | 1 invoice (15k + project) |

One invoice every month.

### Reporting / P&L visibility

- **Retainer revenue**: visible on the retainer project, but the project's P&L is unusual — it has revenue and no meaningful "completion." Budget vs actual works (budget 15k/month, actual 15k/month), but WIP and margin analysis are odd for a perpetual project.
- **Project revenue**: clean, same as Options A and B. Ad-hoc projects have proper scope, budget, completion, and margin.
- **Blended view**: Customer Ledger Entries unified as always.
- **Separation risk**: If someone looks at "all projects for Tinky" they see the retainer alongside actual projects. Need discipline to not mix them up in project reporting.

### Handling the perpetual project

The retainer project needs house rules:

1. **Don't run WIP calculations on it** — there's no "% complete" for an ongoing retainer
2. **Don't try to "close" it** — it lives as long as the retainer agreement lives
3. **Review annually** — adjust the monthly amount if the retainer price changes (via price list, not hardcoded on the planning line)
4. **Naming convention**: prefix with "RET-" or similar so retainer projects are visually distinct from scoped projects

### Verdict

| | |
|---|---|
| **Morre-alignment** | Low-Medium — violates "keep recurring outside the project" rule, but posting groups and pricing are correct |
| **Automation** | None — manual journal entry every month for the retainer |
| **One invoice?** | Yes — native, no workaround needed |
| **Scalability** | Medium. Each retainer client needs a monthly journal entry. 10 clients = 10 manual entries. No auto-billing. |
| **Learning value** | Low for Subscription Billing (you skip it entirely). High for Projects (deeper practice). |
| **Risk** | Low technically, medium architecturally. Works fine now; becomes a problem if Tentixo grows retainer business and needs automation. |

---

## Side-by-side comparison

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| | Subscription + Project (two invoices) | Subscription + Project (manual merge) | Projects only |
| **One invoice** | No | Yes | Yes |
| **Retainer automation** | Full | Partial (draft only) | None |
| **Project audit trail** | Clean | At risk (depends on "Get Project Lines") | Clean |
| **Morre's architecture rule** | Follows | Follows (with workaround) | Violates |
| **Monthly effort** | ~1 min (retainer auto, project manual) | ~5-10 min (merge step) | ~3 min (manual journal + invoice) |
| **Scalability to 10 clients** | Excellent (batch billing run) | Poor (10 manual merges) | Medium (10 journal entries) |
| **Learning value** | Both engines | Both engines + workaround | Projects only |
| **Complexity** | Medium (two modules) | High (two modules + merge) | Low (one module) |
| **Risk if setup is wrong** | Two invoices (cosmetic) | Broken project links (functional) | Perpetual project confusion (analytical) |

---

## Questions for Morre

1. **Is two invoices per month acceptable practice?** In your experience, do clients care? If not, Option A is the clear winner.

2. **"Get Project Lines" on a Subscription Billing-generated invoice** — does this work? If yes, Option B becomes viable. If not, Option B is off the table.

3. **Is there a fourth option we're missing?** For example: a Recurring General Journal that posts a direct Sales Invoice line monthly (no Subscription Billing module, no project), combined with project invoicing? Or a blanket Sales Order with recurring invoicing?

4. **For Formpipe** — they have retainers (pre-invoiced, overage-billed) AND T&M projects. Same architectural question at larger scale. Does the answer here set the pattern for Formpipe too?

5. **Price escalation** — when the retainer goes from 15k to 17k next year, Option A handles it via the Subscription Billing Price Update Template. Options B and C need manual price list updates. How much does this matter at Tentixo's scale?

---

## Decision: Option A confirmed (Morre, June 9 2026)

**Option A is correct "from a technical perspective and philosophical with intent."** — Morre

### Morre's additional reasoning (beyond the original analysis)

1. **Legal separation is load-bearing.** Subscription and project billing may have different legal requirements — cancellation terms, liability, contract clauses. If you merge them into one billing container, you lose the one-to-one mapping with legal. The setup propagates into the legal department — this isn't just a technical decision.

2. **Multi-customer projects break the merge.** BC allows projects to span multiple customers (Gen. Bus. Posting Group is set per project journal line). Subscription billing is always single-customer. If someone opens a multi-customer project and you've merged billing, "we had ever" (Morre) — the combined setup breaks silently.

3. **MVA principle applies.** "You cannot remove complexity, you only move it." Merging billing streams moves complexity from BC into manual legal/operational processes. Option A keeps complexity where BC can manage it.

4. **"Correctness based on intent", not "best practice."** Morre rejects the "best practice" framing — many so-called best practices (like DOMESTIC/EXPORT posting groups) are anti-patterns. Evaluate by intent: subscription = fixed, predictable, one customer. Project = messy, evolving, potentially multi-customer. Different intent → different containers.

5. **Aggregation belongs in Power BI.** Unified customer-level revenue reporting happens in the BI layer, not the invoice layer. The Customer card (org ID) is the join key across subscription and project revenue.

6. **Two invoices is more common than one.** Morre notes that the more common client request is actually *multiple* invoices to the same org — different departments want separate invoices with different reference codes/cost centers. Two invoices is the normal case, not an exception.

7. **Fourth option for edge cases: Python API scripts.** For genuinely complex scenarios, Morre's toolbox includes generating invoices via the BC API with Python scripts. This is the escape hatch, not the default.

### Next steps

- Set up Subscription Billing for Tinky in Tentixo sandbox (hands-on)
- Explore Subscription Package vs Subscription Agreement distinction (Morre also unsure — needs hands-on)
- Use this pattern as the template for Formpipe retainer billing

---

*Version History*

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-09 | Initial three-scenario comparison for Morre review |
| 1.1 | 2026-06-09 | Option A confirmed by Morre. Added legal separation, MVA, multi-customer, and aggregation-layer reasoning |
