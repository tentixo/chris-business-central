# Consolidation in Business Central — and why Tentixo's CoA is built for it

**Version**: 1.0 (draft for Morre review)
**Created**: 2026-06-16
**Status**: Research — fulfils Morre's assignment (Call 6, June 15): explain BC consolidation basics, show how Tentixo's chart of accounts is designed for it, and tie it back to the job/WIP structure.
**Sources**: [MS Learn — Consolidate data from multiple companies](https://learn.microsoft.com/en-us/dynamics365/business-central/finance-consolidated-company-reporting); Tentixo `docs/PackageCOA.xml`, `docs/PackageCUST_POST_GROUPS.xml`

---

## 1. What consolidation is

Many groups run several legal entities (subsidiaries). **Consolidation** combines the general-ledger entries of two or more companies into a single **consolidated company** for group-level reporting.

- Each source company is a **business unit**.
- The **consolidated company** is just a **container** — it holds the combined figures and has *no live business data of its own*.
- Business units can have **different charts of accounts, fiscal years, and currencies**; you can consolidate the full amount or a percentage (for partly-owned entities).

---

## 2. How BC actually does it

1. **Account mapping — the core mechanism.** Every G/L account has a **`Consol. Debit Acc.`** and **`Consol. Credit Acc.`** field. When you run consolidation, each subsidiary entry is carried into the consolidated company *on the account named in those fields*. This is how different/granular subsidiary accounts roll up to a single group account.
2. **Currency.** If a business unit reports in a different currency, you set up **consolidation exchange rates** (can differ per G/L account).
3. **Run.** From the **Business Units** page in the consolidated company → **Test Database/File** first (it checks for missing accounts/dimension codes) → then **Consolidate** (assisted setup). Data can come from the same environment, another BC environment, an exported **XML file** (`Export Consolidation` batch job), or via the free **API**.
4. **Eliminations (manual).** Intercompany transactions are recorded in *both* companies, so they'd double-count. You remove them with general-journal **elimination** entries, checked via the **G/L Consolidation Eliminations** report (16) before posting.
5. **Reports.** Consolidated Trial Balance (17), Consolidated Trial Balance (4) (18, four-column: local / converted / eliminations / total), Consolidated Trial Balance Excel (4410), Intercompany Transactions (512).

> **Consolidation vs. Intercompany (IC):** IC automates *posting* transactions between entities (sales/purchase/journals across companies); consolidation *combines and reports*. They complement each other — IC keeps the two sides in sync; consolidation rolls them up and eliminates them.

---

## 3. Why Tentixo's chart of accounts is built this way

Morre's point — *"consolidation is based on the chart of accounts; you must separate intercompany or the automatic consolidation breaks"* — is provable directly from the export:

**Evidence from `docs/PackageCOA.xml` (1,713 accounts):**
- **1,712 accounts have `Consol. Debit/Credit Acc.` set** — the CoA is *fully wired* for consolidation, not an afterthought.
- **112 accounts deliberately remap** (their Consol account ≠ their own number) — and these are exactly the **group/intercompany accounts**, collapsing to a single parent account in the consolidated company:

| Subsidiary-level account | Consolidates to |
|---|---|
| 1565 Accounts receivable, **GRP-DAUG** | → **1564** |
| 1566 Accounts receivable, **GRP-OTHR** | → **1564** |
| 1665 Current receivables from subsidiaries, GRP | → 1664 |
| 1755 Accrued main income, GRP-DAUG | → 1754 |
| 2365 Long-term liabilities to subsidiaries, GRP | → 2364 |

So the **group-structured posting groups** we mapped earlier are not decoration — they're the machinery of consolidation:
- **Gen. Bus. / Customer / Job Posting Groups** all split into `EXT` + `GRP-MOTH/DAUG/OTHR` + `CTRL-ASSO/JV/OTHR`.
- That split routes intercompany revenue, receivables, and project cost/sales onto **distinct accounts** that can be (a) tracked separately, (b) collapsed via Consol mapping, and (c) **eliminated** at group level.

**Why "domestic" would be wrong** (Morre): geography is *not* a basis for posting groups — "you might sell to a German who runs a project in Sweden; is that domestic?" Geography lives on the **customer card**. The posting-group split is by **legal-entity relationship** (external vs group vs controlled), because *that* is what consolidation and elimination need.

**The "miscellaneous" balance**: groups like `C-MISC` / `S-MISC` / `G-MISC` exist so you can split every cost to the right consolidation bucket **without** exploding the CoA into unmanageable granularity. Split enough to consolidate; not so much that the bank-facing CoA leaks detail (see [[feedback-morre-conventions]] #12).

---

## 4. Tie-back to jobs / WIP

This is the answer to *"can you now understand what we're doing in jobs?"*:

- A project for **Lasernet Sweden** vs a project **between Lasernet SE and Lasernet DK** must post to **different job posting groups** (`J-EXT` vs `J-GRP-*`/`J-CTRL-*`). If they shared one group, the intercompany project's cost/sales couldn't be separated — and automatic consolidation + elimination would be corrupted.
- The WIP clearing accounts already carry the same suffixes (e.g. Recognized Project Sales `3411` EXT vs `3414` GRP-MOTH …), so even **in-progress** project value consolidates and eliminates correctly, not just final invoices.
- This is why `J-EXT` is the **external** default (confirmed Call 6) and there is deliberately **no "domestic" job group**.

---

## 5. Deferred tax — a consolidation-only adjustment *(Morre, June 16)*

Deferred tax (*uppskjuten skatt*) barely appears in single-entity Swedish books but shows up the moment you consolidate. Two sources:

1. **Untaxed reserves split.** In standalone Swedish accounts, *obeskattade reserver* (periodiseringsfonder, ackumulerade överavskrivningar) sit as a single untaxed amount. In the **consolidated** accounts this is not allowed — each reserve must be split into **equity (~79.4%)** and a **deferred tax liability (~20.6%**, the SE corporate rate). The annual movement of the tax portion hits the P&L deferred-tax line.
2. **Temporary differences from consolidation entries** — eliminating internal profit (inventory/assets) or fair-value/PPA adjustments on acquisition create deferred tax assets/liabilities, again with a P&L effect.

**CoA gap (verified against `docs/PackageCOA.xml`):** the **balance-sheet** side exists —
- `1370` Deferred tax asset
- `2240` Provisions for deferred taxes (liability)

— but the **P&L counterpart is missing**: `89xx` has `8910/8920/8930/8980` and **no `8940`**. So there's nowhere to post the deferred-tax *expense/income* that consolidation generates.

➡️ **Action: add `8940 Uppskjuten skatt` (Deferred tax)** to the CoA, per BAS 2022 ([Kontoplan 2022](https://www.bas.se/wp-content/uploads/2022/01/Kontoplan-2022.pdf)). Balance-sheet accounts (`1370`/`2240`) are already in place.

---

## 6. Open items / next steps

- [ ] **Add `8940 Deferred tax`** to the CoA (P&L side missing; `1370`/`2240` already present).
- [ ] **Confirm the narrative with Morre** — especially the consolidation-of-intercompany-jobs framing.
- [ ] Optional: a worked **elimination example** (e.g. Lasernet SE invoices Lasernet DK) showing the double-count and the elimination journal.
- [ ] Decide whether Tentixo needs a **consolidated company** set up now, or this is reference for client engagements (e.g. Formpipe SE/DK).
- [ ] Relationship to **Intercompany (IC) automation** — scope separately if clients need auto-posting between entities.

---

*Tentixo AB — Business Central Advisory*
