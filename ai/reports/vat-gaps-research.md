# VAT Setup — Gaps & Research (Morre's review points)

**Version**: 1.0
**Created**: 2026-06-15
**Status**: Research for Morre review
**Trigger**: Morre's review of the Tentixo VAT setup (June 15 2026) raised three gaps: (1) odd country VAT rules not auto-handled (table VAT / "tabellmoms", e.g. DK; Swedish voluntary property VAT); (2) a missing XML reporting export format.
**Sources**: [Submit VAT reports](https://learn.microsoft.com/en-us/dynamics365/business-central/finance-how-report-vat) · [Set up VAT](https://learn.microsoft.com/en-us/dynamics365/business-central/finance-setup-vat) · [UK Making Tax Digital](https://learn.microsoft.com/en-us/dynamics365/business-central/localfunctionality/unitedkingdom/making-tax-digital-submit-vat-return) · [Skatteverket — voluntary VAT](https://www.skatteverket.se) · [What is SAF-T (EDICOM)](https://edicomgroup.com/learning-center/what-is-saft)

---

## 1. Missing XML reporting export format

**What Morre means**: a standardised XML format for VAT reporting; an EU format used in SE, UK and others; UK localization has it built in.

**Finding — it's the EC Sales List → VIES XML export.** Business Central has a built-in **EC Sales List** report that produces an XML file with the naming convention `VIES_<Period>_<CompanyVAT>.xml` (the **Export** action). It covers B2B Goods, B2B Services, and B2B Triangulated Goods, driven by the **EU Service** flag in VAT Posting Setup and the **EU 3-Party Trade** flag on documents. It works for **EU countries and the UK** — matching Morre's description.

**The wider reporting picture in BC:**

| Mechanism | What it does | Format | Notes |
|---|---|---|---|
| **EC Sales List** | EU cross-border B2B sales (SE: *periodisk sammanställning*) | **XML** (`VIES_*.xml`) | Built-in, EU + UK. **Likely the gap Morre means.** |
| **VAT Return** | Period VAT declaration (sales + purchases) | Web service / XML or JSON via codeunits | Submission format set by a **Content codeunit** (XML or JSON) per the tax authority |
| **UK Making Tax Digital** | UK VAT return to HMRC | JSON via API | Built into **UK localization** (GovTalk/MTD service connection) |
| **SAF-T** (Standard Audit File for Tax) | Full accounting/tax audit file | XML (OECD standard) | Used in NO/PL/PT/RO/LT etc.; **not** mandated in SE/UK — via partner extension |

**Gap for Tentixo (Swedish environment):**
- The **EC Sales List / VIES XML** export should be enabled and tested — verify the `EU Service` flag is set correctly on the relevant VAT Posting Setup rows (it drives Goods vs Services classification).
- For the **Swedish VAT return** (Skatteverket momsdeklaration) electronic submission, standard BC needs the **VAT Report Setup** configured with the correct report version, and typically a **SE localization / partner extension** for the actual SKV format. Confirm what the SE localization ships vs. what needs a partner add-on.

**Recommendation**: enable + test EC Sales List XML first (built-in, quick win). Separately scope the SE VAT-return submission format (localization vs partner extension) with Morre.

---

## 2. "Tabellmoms" / table VAT and other odd country rules (e.g. DK — can't auto)

**The constraint**: BC's VAT engine supports only **four VAT Calculation Types**:
1. Normal VAT
2. Reverse Charge VAT
3. Full VAT
4. Sales Tax (US-style)

Anything outside `base × percentage` (with reverse-charge / full-VAT variants) **cannot be calculated automatically** by standard BC. Table-based / flat-rate / scheme-specific national VAT (Morre's "tabellmoms", flagged for DK) falls outside these four types, so it requires **manual journal handling or a localization/extension**.

> ⚠️ **Confidence flag**: I could not pin down the exact definition of "tabellmoms" as Morre uses it for DK (web research surfaced Danish reverse-charge rules but not a "table VAT" scheme by that name). The *structural* conclusion holds — BC can't auto-handle non-percentage VAT schemes — but the **specific DK rule should be confirmed with Morre** before we document a workaround.

**What this means for the setup**: the current Tentixo VAT matrix is excellent for percentage-based VAT across the EU country matrix (DOM/EXP/ORG-EU/IND-XX), but genuinely table-based or special national schemes are an inherent BC limitation, not a setup omission. Document them as "manual handling required" rather than trying to force them into VAT Posting Setup.

---

## 3. Swedish voluntary VAT on property (frivillig skattskyldighet för moms på fastighet)

**The rule**: Swedish landlords can **voluntarily** opt to charge VAT on commercial property rent ("frivillig skattskyldighet"), which then lets them deduct input VAT on property acquisition/maintenance. Once opted in, there's a minimum lock-in period, and input-VAT recovery on property costs follows special rules.

**Good news — partially handled already.** The Tentixo VAT setup **already has a dedicated VAT Product Posting Group**:
- **`S-RNT_FULL`** = "Rent voluntary VAT" → posts to **Sales VAT account 2613** (separate from the standard 2611) / Purchase 2642.

So the *output* side (charging VAT on rent and isolating it to its own account) is wired.

**What's likely still missing / manual:**
- **Per-property tracking** of which properties are under voluntary tax liability (BC has no native "property" object — would need dimensions/locations, which conflicts with the "no dimensions" convention, or a fixed-asset/extension approach).
- **Input-VAT recovery rules** on shared/property costs (proportional deduction) — not automated.
- The **lock-in / retroactive adjustment** administration — manual.

**Recommendation**: confirm scope with Morre — the VAT *posting* mechanism exists (`S-RNT_FULL`); the gap is the property-level *administration* (tracking, partial input VAT, lock-in), which is process/extension territory, not VAT Posting Setup.

---

## 4. Table 92 (Customer Posting Group) — blocked

Chris reported uploading a config-package export of **table 92 (Customer Posting Group)** to verify the `DOMESTIC`/`INTERCO` codes — but the file did not land in the repo. **Re-upload needed** to close out the customer-posting-group verification.

---

## Summary / next steps

| Item | Status | Next step |
|---|---|---|
| EC Sales List / VIES XML export | Built-in, likely not enabled | Enable + test; verify `EU Service` flags |
| SE VAT-return e-submission format | Needs scoping | Confirm SE localization vs partner extension with Morre |
| Table VAT / "tabellmoms" (DK) | BC limitation (4 calc types) | Confirm exact DK scheme with Morre; document as manual |
| Swedish voluntary property VAT | Output side wired (`S-RNT_FULL`) | Scope property-level admin (tracking/input VAT/lock-in) |
| Customer Posting Group (table 92) | Upload missing | Re-upload export |

---

*Tentixo AB — Business Central Advisory*
