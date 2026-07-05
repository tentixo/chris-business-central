# BC Progress Update — for Morre

**From**: Chris · **Date**: 2026-07-05
**Purpose**: quick read on where I am with Business Central, self-assessed against the MB-800 map, plus next steps and a few things I need from you.

---

## Where I am, in one line

Solid on the **architecture / financials** side (your conventions, posting groups, CoA, VAT), thinner on **daily operations** (journals, payments, inventory). I'm now shifting from reading/listening to **hands-on in the Test environment** — that's the gap that only closes by doing.

---

## Gap analysis at a glance (MB-800 domains)

| Domain (exam weight) | Self-rating | Where it stands |
|---|---|---|
| **Set up BC** (20–25%) | 🟡 Partial | Config packages + number series solid. Gaps: **security/permissions**, assisted setup, approvals. **Dimensions** now partial (see below). |
| **Configure financials** (25–30%) | 🟢 Strongest | Posting groups, CoA, VAT, semantic groups = comfortable. **Fixed Assets** now partial (was a full gap). Still thin: bank/AP journals. |
| **Sales & purchasing** (10–15%) | 🟡 Partial | Sales/customer side OK; **item types + posting setup** reinforced. Vendor/purchasing side is weakest. |
| **Perform BC operations** (30–35%) | 🟡 Partial | Sales invoicing solid. Biggest gaps: **journals & payments** (bank rec, applying entries), **inventory transactions**, FA transactions (now partial). |

---

## What moved recently — and why

The IFRS-16 / intercompany work with Lasernet (Carla, Camilla) has been an unexpectedly strong classroom. Three gaps improved just by working through it:

- **Fixed Assets 🔴 → 🟡** — FA classes, depreciation books, FA posting groups, Calculate Depreciation, FA G/L journals (from watching you build the lease setup).
- **Dimensions 🔴 → 🟡** — default dimensions on items, IC dimension mapping, dimensions flowing with lines, Country-code correction on receipt. (Note: I know your "never use dimensions" stance — the IC work *does* use them, so I've had real exposure.)
- **Item types + General/VAT Posting Setup** — the "five tags" resolving accounts by posting type, reinforced by the IC item-method setup.

The caveat I'm honest about: most of this was **watching you do it**. It only counts as "learned" once I've done it myself — which is the next step.

---

## Next steps

1. **Fixed Assets, hands-on in Test** — a vanilla asset lifecycle (acquire → depreciate → **dispose**), then the real Lasernet lease dry-run (engagement action A5). Converts FA from "seen it" to "done it", and covers disposal (which the lease never teaches). *Exercise sheet is written and ready.*
2. **Journals & payments** — the heaviest exam gap and the most useful operationally (payment/cash-receipt journals, applying entries, bank reconciliation). Next hands-on block after FA.
3. **MB-800** — re-map against the updated study guide (refreshed June 30), fill remaining 🔴s (security, inventory transactions), target the exam **Q4 2026**.

---

## Where I need you

1. **Test environment**: OK for me to create my own FA class + depreciation book in Test, or should I reuse existing ones? (Prefixing mine `CTEST-` either way.)
2. **Lease A5**: when I reach it, let's pair on the **deferral push-back** (mid-lease catch-up) — you flagged that part isn't built yet.
3. **Two WIP loose ends still open from Call 6** whenever convenient: the **J-GRP-OTHR** wiring (G/L Expense = 3426, looks like it should be 3436), and adding **8940 Deferred tax** to the CoA for consolidation.

---

*Learning is captured continuously in the BC repo — happy to walk you through any of it.*
</content>
