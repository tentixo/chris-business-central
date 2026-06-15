# Ready for Next Session

**Last Updated**: 2026-06-15
**Risk Level**: LOW
**Git Status**: Playbook + billing docs committed. Uncommitted: FLIGHT-PLAN.md, this file, /docs uploads.

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

- Committed playbooks + both billing guides + Tinky billing scenarios.
- Deleted the 21 `Screenshot 2026-06-*` process screenshots (superseded by the subscription guide; never entered git history — contained client PII). Kept the named ERD/posting reference diagrams.
- Added full **Subscription Option** enum to `subscription-billing-setup.md`.
- Wrote `ai/guides/project-billing-setup.md` (v0.9 **draft**) — 8-step project billing flow, counterpart to the subscription guide.

## Next Task

1. **Sandbox audit**: Rename VAT Prod. Posting Groups from VAT25 etc. to semantic names. Review Gen. Bus. Posting Groups.
2. **Research WIP methods** with Morre — 7 types, choosing wrong one is catastrophic.
3. **Optional**: commit/clean remaining `/docs` uploads (call transcripts, xlsx, NO_SERIES config package) and FLIGHT-PLAN.md.

✅ Done since last session: playbook commit, Subscription Billing setup for Tinky (B-SCC00001 / MONTHLY-RET / draft invoice B-SX000004), Project Billing guide **v1.0** (Step 8 verified against the "Project Create Sales Invoice" sandbox dialog).

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

- Follow-up with Therese for sample fakturaunderlag PDFs
- Excavate the Gurra-Therese BC time-reporting solution
- Decide Finance team and STG BI scope
- Get customer ID mapping table
