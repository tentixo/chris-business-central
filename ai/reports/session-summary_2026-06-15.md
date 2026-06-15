# Session Summary — 2026-06-15

**Risk Level**: LOW
**Commits**: 15 (`3bc1222` → `fe9d81e`)
**Focus**: Billing guides finalised; WIP chapter opened; "full Tentixo" doc reconciliation against real config exports; VAT gap research.

---

## Accomplishments

### Billing
- Committed both playbooks + Tinky billing scenarios; added `.gitignore` for `.idea/`.
- `subscription-billing-setup.md` — added the full **Subscription Option** enum.
- `project-billing-setup.md` — created and finalised to **v1.0** (Step 8 verified against the live "Project Create Sales Invoice" dialog).
- `config-package-xml-export.md` — reusable guide for Morre's RapidStart XML export method.

### WIP chapter (Morre Call 5)
- Verified real WIP options via MS Learn (5 Recognized Costs × 6 Recognized Sales; 5 presets) — corrected the "7 types / 5×5" confusion.
- Exported CoA + Job Posting Group + General Posting Setup (`docs/PackageCOA.xml`).
- Drafted `ai/reports/wip-methods.md` — codebook (archetype→method) + booking mapped to **real J-EXT accounts**. WIP confirmed **fully wired**.
- Found likely bug: **J-GRP-OTHR** G/L Expense (Contract) = 3426, should be 3436.

### "Full Tentixo" reconciliation
- Decision: all docs use **real Tentixo codes**, not MS-default placeholders (Tentixo's sophisticated setup + Morre's automation = the differentiator).
- Verified codes from `docs/PackageVAT.xml`, `docs/PackageCOA.xml`, `docs/PackageCUST_POST_GROUPS.xml` and propagated across both playbooks, both billing guides, Tinky scenarios.
- Mapping: `CONSULTING1→C-MAIN1`, `SERVICE FULL/VAT25→S-FULL`, `GOODS FULL→G-FULL`, `ELECTRONIC SERVICE→S-ESVC`, `ZERO→S-ZERO/G-ZERO`; Customer Posting Group `DOMESTIC/INTERCO → EXT/GRP-*/CTRL-*/SKV`.
- **Sandbox audit closed — both halves clean**: VAT groups already semantic; Gen. Bus. groups intercompany (no geo anti-pattern).

### MB-800
- `ai/reports/mb800-gap-analysis.md` — domain coverage vs the June 30 skills outline + prioritised study list. Key: Projects/WIP not a dedicated exam domain; Dimensions is exam-only.

### VAT gap research (Morre review)
- `ai/reports/vat-gaps-research.md` — EC Sales List/VIES XML as the missing reporting format; table VAT ("tabellmoms" DK) is a BC limitation; voluntary property VAT output wired via `S-RNT_FULL`.

---

## Key decisions
- **Go full Tentixo** — real codes/structure as the Best Practice standard ([[feedback-full-tentixo-best-practice]]).
- Billing **Option A** (two invoices) carried through; J-EXT = external-client default.
- Dropped Formpipe Therese/Gurra thread; parked Playbook §12.

## Memories written
- `feedback-full-tentixo-best-practice`, `reference-tentixo-real-posting-codes` (both in MEMORY.md).

## Files created
`ai/guides/`: project-billing-setup.md, config-package-xml-export.md ·
`ai/reports/`: wip-methods.md, mb800-gap-analysis.md, vat-gaps-research.md, this summary ·
`docs/`: PackageCOA.xml, PackageVAT.xml, PackageCUST_POST_GROUPS.xml (+ Call 5 transcript)

---

## Next session priorities
1. **WIP — Morre review**: validate codebook; confirm J-EXT default; fix J-GRP-OTHR (3426→3436); decide default WIP method.
2. **Build the WIP testing playbook** (hands-on companion to the codebook).
3. **VAT follow-ups**: enable/test EC Sales List XML; scope SE VAT-return submission; confirm DK tabellmoms; scope property-VAT admin.
4. **MB-800**: targeted sandbox exercises for 🔴 gaps (journals/payments, inventory, fixed assets, security, dimensions, AP).
5. **Ask Morre**: what distinguishes C-MAIN1/2/3.

## FLIGHT-PLAN progress
- **M1 (MB-800, Q4 2026)**: gap analysis complete — structural prep done; targeted study exercises are the next concrete step.
