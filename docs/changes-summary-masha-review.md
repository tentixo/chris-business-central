# Changes Summary — Masha BC Sessions

**Compared**: `masha-bc-sessions.md` (base) vs `masha-bc-sessions-comments.md` (reviewed)
**Date**: 2026-06-08

`masha-bc-sessions-comments.md` is the base document with Masha's inline review comments and a handful of factual edits. Below is everything that differs, grouped as **factual corrections/additions** (should be merged into the base) and **open comments/questions** (decisions needed before merging).

---

## Factual corrections & additions (merge into base)

| # | Section | Change |
|---|---------|--------|
| 1 | 2. GL entries — receipts | **New rule on posting groups**: Five posting groups on every transaction is valid per §4.3 of the playbook. **Exception**: bank-account-to-bank-account transactions (e.g. Danske→Employee, Danske→SKV, loans to/from companies). |
| 2 | 2. GL entries — receipts | **New bullet — Total amount**: Bank statement is the source of truth, especially important for receipts in non-SEK. |
| 3 | 10. Purchase invoices (Manual) | **Corrected scope**: Manual method is *rarely* used at Tentixo, but Masha uses it for all other companies (Swaxy, Idonex, etc.). *(Base said "Used for most vendors at Tentixo" — this is reversed.)* |
| 4 | 12. Foreign currency | **Account numbers specified**: Exchange gains = **3960** (was "7xxx"), Exchange losses = **7960** (was "7xxx"). |
| 5 | 12. Foreign currency (workaround) | **Added warning**: When creating the manual G/L entry for exchange gains, remove the currency so the correction is made in SEK. |

---

## Open comments & questions (decide before merging)

| # | Section | Comment |
|---|---------|---------|
| A | 9. Sales invoices | On "Lines can be G/L Accounts": Masha can't recall ever using G/L Accounts on Sales invoices — technically possible but unsure if reasonable. *Verify / qualify the claim.* |
| B | 10. Purchase invoices (Tungsten, verify step) | The verify-extracted-data step may be automatable — could skip manual validation in Tungsten and validate only in Incoming Documents. *Workflow improvement to confirm.* |
| C | 12. Foreign currency (heading) | This whole section belongs under **Payment reconciliation**. *Restructure suggestion.* |
| D | 12. Recurring FX expenses | These are receipts, but payment reconciliation (with FX corrections) is done for invoices only. Suggests moving this note to the receipts section. *Restructure suggestion.* |
| E | Flags — physical receipt stamping | Unsure if recommendable: there's a legal requirement for a paper trail when digital storage isn't possible, so it may be necessary rather than a shortcut. |
| F | Flags — skipping Quotes/Orders | Whether this is recommendable for clients depends on each client's sales process. |
| G | Flags — quarterly bank reconciliation | Not really technically possible — XML files are monthly, so reconciliation is effectively monthly. *(Possibly remove from "shortcuts" list.)* |
| H | Best practices — journal batch presets | Tax account can be added to the preset too. |
| I | Best practices — Tungsten Automation | Morre says BC now has **native** invoice-scanning support — a new function, not yet configured at Tentixo. *May supersede Tungsten.* |

---

## Notes

- No content was deleted between the two files; all changes are additions, one correction (#3), and the FX account numbers (#4).
- Items #1–#5 are ready to fold into `masha-bc-sessions.md` (would bump it to v1.1).
- Items A–I need Masha/Morre input or a restructuring decision before they're resolved.
