# Ready for Next Session

**Last Updated**: 2026-06-15
**Risk Level**: LOW
**Git Status**: Clean — all session work committed (15 commits). See `ai/reports/session-summary_2026-06-15.md`.

---

## Where We Left Off

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

## Raise with Morre next session (WIP)

1. **Confirm J-EXT** as the default Job Posting Group for external client projects — there is **no generic/domestic** job posting group; all 7 are group/intercompany variants (EXT, GRP-*, CTRL-*).
2. **🐛 Fix J-GRP-OTHR wiring bug**: its *G/L Expense (Contract)* account is **3426** (a sales-applied account) but should be **3436** ("G/L Expenses Projects, GRP-OTHR") to match every other group's pattern.
3. **Validate the codebook** (`ai/reports/wip-methods.md`) — the archetype→method recommendations in §4 are my reasoning, not yet Morre's rulings.
4. **Decide the default WIP method** in Projects Setup, and which methods to offer as the standard menu.

## Next Task

1. **Build the WIP testing playbook** — hands-on companion to the codebook: simulate a project forward, run Calculate WIP each period, inspect Project WIP Entries + Project Statistics. Lands in `ai/guides/`.
2. ~~Sandbox audit~~ **DONE** — both halves clean (see Session notes). No VAT rename needed; Gen. Bus. groups fine.
3. **MB-800**: gap analysis done → `ai/reports/mb800-gap-analysis.md`. Drive targeted sandbox exercises for the 🔴 gaps (journals/payments, inventory txns, fixed assets, security, dimensions, AP/purchasing). Note: Projects/WIP is *not* a dedicated exam domain.

### Small open verifications (need more exports / Morre)
- **Consulting tier semantics** — what distinguishes `C-MAIN1` / `C-MAIN2` / `C-MAIN3`? (ask Morre)
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
