# Ready for Next Session

**Last Updated**: 2026-07-14
**Risk Level**: LOW
**Git Status**: Clean — all committed & pushed to `origin/main` (`cd23fae`).

---

## ▶ CURRENT — Session 2026-07-13/14 (MB-800 sprint execution)

**Where we left off:** Executed the MB-800 study plan hands-on. Folded **Morre Call 16** (dependency graph: foundation spine, Rim-vs-Crafted, dimensions-as-8-tags, Cost Accounting) into the playbooks + study schedule. Then ran **Sprint 1 — Fixed Assets** (acquisition → depreciation → disposal, solo; Book Value 57k → gain 1k) and **Sprint 2 — Dimensions** (all 6 mechanics solo). Both **🟢**; **Milestone Gate 1 hit ~3.5 weeks early** (was due Aug 7). Wrote hands-on **testing playbooks** (FA v1.4, Dimensions v1.0) and set the per-session-playbook convention. Updated study schedule, gap-analysis v1.3, **FLIGHT-PLAN v1.2**. See `ai/reports/session-summary_2026-07-14.md`.

**Next task:** **Sprint 3 — Journals & payments** (the heaviest remaining 🔴 gap) — payment/cash-receipt journals, apply/undo entries, reversals, **bank reconciliation**. Produce `ai/guides/journals-payments-testing-playbook.md` as we go. *(Plan slots this Aug 10–21, but Chris is ~3.5 wks ahead — can start anytime.)*

**Open threads:** Cost Accounting sketch (non-exam, Formpipe — w/ Morre); FA **LVA variant** + **loss disposal**; Lasernet **lease Exercise 2** (A5, needs Morre) — also resolves the open **1267/1269** CONFUSION doc.

**Key reference docs:** `ai/reports/mb800-study-schedule_v1.1.md` (sprint tracker) · `ai/reports/mb800-gap-analysis.md` · `ai/guides/*-testing-playbook.md` (FA/WIP/Dimensions) · `FLIGHT-PLAN.md` (v1.2).

---

## Where We Left Off (earlier — WIP/billing, June 2026)

Processed Morre session 4 transcript (June 9, 2026). Updated both playbooks (internal + client-facing) with significant corrections:

1. **Billing decision**: Option A confirmed — Subscription Billing for retainers, Project Billing for ad-hoc, two invoices per client. Intent-based separation with legal, MVA, and multi-customer reasoning.
2. **Layered hierarchy**: Number Series moved to side of diagram (dependency for all layers except Posting Groups). Posting Groups now show bidirectional arrow to CoA.
3. **GVH → GVH+W**: Added 34xx WIP as 4th revenue category (activated costs before final invoice).
4. **VAT Prod. Posting Groups**: VAT25 flagged as anti-pattern → use semantic names (SERVICE FULL, GOODS FULL, ELECTRONIC SERVICE, ZERO). BC resolves % via country matrix.
5. **Gen. Bus. Posting Groups**: DOMESTIC/EXPORT split flagged as anti-pattern. Geography belongs on customer card, not in CoA. Intercompany splits are the exception.
6. **General Posting Type**: Added as "the 5th tag" — Sale/Purchase/Settlement alongside the four posting groups.
7. **Fixed-price vs T&M line types**: Items = Billable, Resources = Budget for fixed price. Both Billable and Budget for T&M.
8. **"Correctness based on intent"** not "best practice" — Morre's framing added to working conventions.

## Session 2026-06-15

- Committed playbooks + both billing guides + Tinky billing scenarios + `/docs` uploads + FLIGHT-PLAN; added `.gitignore` rule for `.idea/`.
- Both billing guides done: `subscription-billing-setup.md` (+ full Subscription Option enum) and `project-billing-setup.md` **v1.0** (Step 8 verified against the "Project Create Sales Invoice" dialog).
- Added `ai/guides/config-package-xml-export.md` (Morre's RapidStart XML export method).
- **Started the WIP chapter** (Morre Call 5, June 12): verified real WIP options via MS Learn (5 cost × 6 sales; 5 presets), exported CoA + Job Posting Group + General Posting Setup (`docs/PackageCOA.xml`), and drafted `ai/reports/wip-methods.md` (codebook + booking mapped to real J-EXT accounts). WIP confirmed **fully wired**.
- **"Full Tentixo" decision** — all docs now use the **real Tentixo posting codes** (verified from `docs/PackageVAT1.xml` + `docs/PackageCOA.xml`), not MS-default placeholders. Replaced `CONSULTING1→C-MAIN1`, `SERVICE FULL/VAT25→S-FULL`, `GOODS FULL→G-FULL`, `ELECTRONIC SERVICE→S-ESVC`, `ZERO→S-ZERO/G-ZERO` across both playbooks, both billing guides, and Tinky scenarios. See memories [[feedback-full-tentixo-best-practice]] + [[reference-tentixo-real-posting-codes]].
- **Sandbox audit = both halves clean** ✅: VAT Prod groups already semantic (no rename needed — `VAT25` only lives as the VAT Identifier); Gen. Bus. groups intercompany (no DOMESTIC/EXPORT anti-pattern).

## Session 2026-06-16 (Morre Call 6 — WIP review)

- **WIP codebook → v2.0**: extended to **all 8 Tentixo methods** (5 MS + 3 custom: INVOICED C-P, INVOICED C-TOTAL P, TOTAL C-P), decoded from `docs/PackageWIP_METHODS.xml` (table 1006). Added operational rules (set method at start; run final WIP before close; never change mid-flight; completion≠closing) + item-based cost capture (Items > direct G/L; FIFO; purchase items like hotel).
- **J-EXT confirmed** as external-client default; no domestic job group (group separation needed for consolidation).
- **NEW consolidation research** drafted → `ai/reports/consolidation-research.md`. Proven from CoA: 1712/1713 accounts have Consol Debit/Credit set; 112 intercompany accounts remap to parent (e.g. AR 1565/1566→1564). This is *why* the CoA/posting groups are group-structured.

- **WIP testing playbook built** → `ai/guides/wip-testing-playbook.md` — hands-on sandbox exercise (set method at start → post cost/sales across periods → Calculate WIP → Post WIP to G/L → inspect real J-EXT accounts → reverse → compare methods on separate projects).

## Still open with Morre (WIP)

1. **🐛 J-GRP-OTHR wiring bug** — G/L Expense (Contract) = `3426` (a sales-applied acct); should be `3436`. **Not confirmed in Call 6 — raise again.**
2. **§4 archetype→method mapping** for the 3 new methods — pending Morre sign-off ("check the logic").
3. **Default WIP method** in Projects Setup — not yet decided.
4. **Validate consolidation note** narrative; optionally add a worked elimination example (Lasernet SE↔DK).
5. **🆕 Add `8940 Deferred tax` to the CoA** (Morre) — consolidation needs the P&L deferred-tax account; balance-sheet side (`1370`/`2240`) already exists. See `consolidation-research.md` §5.

## Tracked knowledge channel — IFRS engagement (Lasernet UK)

3rd live engagement (Tentixo `ifrs-16-research` branch; Carla Rogers + Camilla + Morre): IFRS-16 / FRS-102 finance-lease accounting in BC. **Track knowledge only — do NOT act on these tasks.** Docs in `ai/reports/`: `ifrs16-lease-setup-guide-bc`, `ifrs-16-uk-frs102-bc-implementation`, `ifrs-16-leased-assets-research`, `ic-postings-issues-meeting`. Folded into MB-800 plan (`mb800-gap-analysis.md` v1.1): **Fixed Assets 🔴→🟡** (FA classes, depr. books, FA posting groups, Calculate Depreciation, FA G/L journals — seen live via Morre). Converts to 🟢 when Chris runs the sandbox dry-run himself (engagement action A5); **disposal** still untouched. See [[project-ifrs-engagement-channel]].

## Next Task (June 2026 — superseded; see ▶ CURRENT block at top)

1. ~~**Build the WIP testing playbook**~~ **DONE** (`ai/guides/wip-testing-playbook.md`). Hands-on companion to the codebook: simulate a project forward, run Calculate WIP each period, inspect Project WIP Entries + Project Statistics.
2. ~~Sandbox audit~~ **DONE** — both halves clean (see Session notes). No VAT rename needed; Gen. Bus. groups fine.
3. **MB-800**: gap analysis done → `ai/reports/mb800-gap-analysis.md`. Drive targeted sandbox exercises for the 🔴 gaps (journals/payments, inventory txns, fixed assets, security, dimensions, AP/purchasing). Note: Projects/WIP is *not* a dedicated exam domain.

### Small open verifications (need more exports / Morre)
- ~~Consulting tier semantics~~ **DONE (Morre, 2026-06-15)** — `C-MAIN1/2/3` = org's revenue-segmentation choice ("What/Where/How are you selling?"), low-granularity & bank-safe; Staff/Contractor/Education is cost-side (4nnn). Captured in playbook + [[feedback-morre-conventions]] #12.
- ~~Customer Posting Group codes~~ **DONE** — `EXT`/`GRP-*`/`CTRL-*`/`SKV` verified (table 92). Tinky = `EXT`.

### VAT gaps (Morre review, `ai/reports/vat-gaps-research.md`)
- Enable + test **EC Sales List / VIES XML** export (verify `EU Service` flags).
- Scope **SE VAT-return e-submission** format (SE localization vs partner extension).
- Confirm exact **DK "tabellmoms"** scheme with Morre (BC can't auto-calc table VAT).
- **Voluntary property VAT**: output wired (`S-RNT_FULL`); scope property-level admin.

✅ Done since last session: playbook commit, Subscription Billing setup for Tinky (B-SCC00001 / MONTHLY-RET / draft invoice B-SX000004), both billing guides, config-package export guide, WIP codebook draft + account-wiring analysis, MB-800 gap analysis, Gen. Bus. PG review.

## Key Decisions to Remember

- File routing: user uploads → `/docs`, .md → `ai/reports/`, other formats → `ai/docs/`
- Tentixo brand colors in `gfx/TXO-Brand-Guide.md` — always check before styling
- Internal = dark teal cover + "INTERNAL" footer; client = primary teal + "CONFIDENTIAL"
- PDF pipeline: `ai/docs/generate-bp-pdf.py` as reference for branded PDF generation
- **Billing**: Subscription + Project = two invoices, aggregation in Power BI
- **VAT groups**: semantic names, not percentages
- **"Correctness based on intent"**, not "best practice"

## Open Questions (from playbook §12)

- **WIP methods** — 7 types, critical. Morre has research, need to do together.
- ~~Recurring billing~~ **RESOLVED** — Option A confirmed
- Multi-entity / intercompany (Formpipe SE/DK) — partially covered
- BC + Power BI — confirmed as aggregation layer
- Sales Price Lists — deep granularity confirmed, need to explore
- **Dimensions** — Morre says "never use." Need to unpack.
- Revenue recognition timing for physical goods
- Prepaid vs post-pay account handling in carve-outs
- **NEW**: VAT Prod PG rename in sandbox
- **NEW**: Gen. Bus. PG review (anti-pattern check)
- **NEW**: Subscription Package vs Agreement distinction
- **NEW**: MB-800 cert — map updated study guide (post June 30) against playbook, fill gaps. Target Q4 2026. See FLIGHT-PLAN.md M1.

## Formpipe Next Steps

- Decide Finance team and STG BI scope
- Get customer ID mapping table
- ~~Therese fakturaunderlag PDFs / Gurra-Therese time-reporting solution~~ **Dropped (2026-06-15)** — not pursuing for now
