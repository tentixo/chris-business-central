# IFRS 16 Leased Assets — Research Note

**Branch**: `ifrs-16-research`
**Date**: 2026-06-18
**Source**: Call with Lars Mårelius (Morre), 2026-06-18 — `docs/Call with Lars Mårelius (8).docx`
**Companion to**: [`ifrs-posting-layer-rfc_v1.0.md`](ifrs-posting-layer-rfc_v1.0.md) §6 (IFRS 16 Worked Lens). That RFC answers *which layer books the lease*; this note answers *how to measure and post it*.
**Ground rule from Morre**: *"Figure out how you should handle it first, before you go into how Business Central can do the setup."* This note leads with principle (§1–§7); BC mechanics come last (§8).

---

## 0. The six questions from the call

| # | Morre's question (paraphrased) | Short answer | §  |
|---|---|---|---|
| 1 | A leased asset's value is never on an invoice — *what is it worth?* | **PV of the lease payments**, not market/fair value. You compute it; nobody has to "tell you the market value." | §3 |
| 2 | Trust the leasing vendor's depreciation, or is there a rule (e.g. 10 years)? | Depreciate over the **shorter of lease term and useful life**. The vendor's invoice is irrelevant to depreciation. | §4 |
| 3 | The monthly invoice = depreciation + interest. How do you book that? | The cash split is **principal + interest**, *not* depreciation + interest. Depreciation is a **separate, independently-computed** charge. | §5 |
| 4 | Vendor says 10,000/mo, IFRS says 8,000 — you "have more value than allowed." | That gap is a **book-vs-tax temporary difference → deferred tax** (IAS 12). It is expected, not an error. | §6 |
| 5 | Should the leased-asset depreciation book be integrated or non-integrated? | Depends on the **layer** (§2). In the Swedish legal entity under RFR 2 it is **rent expense — no capitalization at all**. The ROU asset is a **group-level** item. | §2, §8 |
| 6 | IC leases — "subsidize the daughter, say it's 10,000." | Must be **arm's length** (transfer pricing); the IC lease is **eliminated at the group** (RFC §6). You cannot set the rent freely. | §7 |

---

## 1. Why this felt confusing on the call

Two mental models got crossed:

1. **"The invoice is the value, and the invoice is depreciation."** Under IFRS 16 neither is true. The asset's value is the *present value of all future payments* (computed once, at commencement); and the monthly invoice is a *financing payment* (principal + interest), while depreciation is a *third, separate* number.
2. **"There is one right answer for leased assets."** There are **three different correct answers** depending on which set of books you are in — Swedish tax, the Swedish legal entity, and the IFRS consolidation. The leasing fee that is "just a cost" in one is a capitalized asset in another. That is the whole knot, and §2 unties it.
3. **"A lease is just a rent."** No — *be cautious* (Morre, 2026-06-22). There's an **ownership spectrum**: **buy** (full ownership) → **loan-financed purchase** (own, but not free-and-clear until repaid) → **lease** (you carry the asset's risks/rewards — "you kind of own it", fully responsible for it) → **rent** (no ownership; the rental company stays responsible). **IFRS 16 / FRS 102 capitalize the lease** precisely because it sits on the *owning* side of that line — which is why it goes on-balance-sheet, not expensed as rent.

---

## 2. First principle — three layers, three treatments

This is the resolving insight. A finance lease (e.g. a leased car or office) is accounted for **differently in three places**, and BC's "integrated vs non-integrated" puzzle is downstream of *which layer you are posting in*.

| Layer | Standard | Lease treatment | Balance sheet | P&L |
|---|---|---|---|---|
| **Swedish tax** | IL (Inkomstskattelagen) | **Rental.** Lessor owns & depreciates; lessee deducts the **whole fee**. | No asset, no liability on lessee. | Full leasing fee deductible. |
| **Legal entity — SE** (Done1, statutory books in BC) | **RFR 2 / K3** | **MAY treat all leases as operating = rent** (permitted simplification) — *but* per the project decision (D1, below) they capitalize at Done1 anyway. | Off-balance-sheet note if exemption taken; else ROU + liability. | Rent expense, or depreciation + interest if capitalized. |
| **Legal entity — UK** (Done1) | **FRS 102 (2026)** | **MUST capitalize** — on-balance-sheet lessee model (periods from **1 Jan 2026**), aligned with IFRS 16 (OBR discount rate). | ROU asset + lease liability. | Depreciation + interest (front-loaded). |
| **Group / consolidation** (Done2, FGGE) | **Full IFRS 16** | Capitalized; only genuine **group-level** adjustments + IC lease elimination remain here. | ROU/liability already up from Done1. | — |

**Consequence for the project — DECISION D1 (load-bearing): capitalize at the legal entity (Done1).**

> The 2026-06-17 meeting (→ [`ifrs-16-uk-frs102-bc-implementation`](ifrs-16-uk-frs102-bc-implementation_v1.0.md)) **resolved the earlier fork**: lease capitalization is done **in the legal entity (Done1), not at group level**. For the **UK** this is now *mandatory* (FRS 102 from 1 Jan 2026); for **SE** the RFR 2 exemption still exists but the group chooses to capitalize at Done1 anyway, for a uniform model and to let BC's vanilla consolidation reconcile automatically. Done2 keeps only genuine group-level adjustments + IC lease elimination ([RFC §6](ifrs-posting-layer-rfc_v1.0.md)).

This answers Q5: the leased asset **is** a fixed-asset card in the entity (new `RIGHT-OF-USE` subclass), with the ROU/liability/interest/depreciation posted there — *integrated* with the entity G/L. The "nothing to integrate at entity level" reading below applies only to the *un-elected* RFR 2 rent treatment, which the project has chosen **not** to use.

~~**The fork to confirm with Lars**~~ **RESOLVED (D1):** capitalize in the legal entity. UK mandatory under FRS 102; SE by group policy. See the implementation report for the BC setup (subclass, two-line interest split, mid-lease deferral adoption, rollout).

---

## 3. Q1 — What is a leased asset "worth"? (initial measurement)

You do **not** need anyone to tell you the market value. IFRS 16 measures the asset from the *payments*, in two steps:

**Step 1 — Lease liability = present value of the lease payments** not yet paid at commencement, discounted at:
- the **interest rate implicit in the lease** if readily determinable (rare — the lessor rarely tells you), else
- the lessee's **incremental borrowing rate (IBR)** — what *you* would pay to borrow, over a similar term, with similar security, to buy a similar asset. This is a **policy input** to set group-wide.

Payments included: fixed payments (less incentives), index/rate-based variable payments, residual-value guarantees, a purchase-option price if reasonably certain, and termination penalties if the term reflects ending early.

**Step 2 — ROU asset =** lease liability **+** payments made at/before commencement **+** initial direct costs **+** estimated dismantling/restoration **−** lease incentives received.

> **Answer to "what is it worth?":** the ROU asset ≈ the PV of what you will pay. For an office at 10,000/month over a known term, the value is the discounted sum of those payments — a number you *calculate*, not a valuation someone supplies. (The transfer-pricing/market-value worry only re-enters for **intercompany** leases — §7 — where the *payment itself* must be arm's length.)

### Worked example — leased car, 10,000/month, 36-month term, IBR 6%/yr (0.5%/mo)

| Item | Value |
|---|---|
| Lease liability at commencement = PV of 36 × 10,000 @ 0.5%/mo | **≈ 328,700** |
| ROU asset (no IDC/incentives) | **≈ 328,700** |
| Depreciation/month (straight-line, 36 mo) | 328,700 / 36 ≈ **9,131** |
| Month-1 interest (328,700 × 0.5%) | **1,644** |
| Month-1 principal (10,000 − 1,644) | **8,356** |
| Liability after month 1 | ≈ 320,344 |
| **Month-1 total P&L** = dep 9,131 + interest 1,644 | **10,775** (vs cash 10,000 — front-loaded) |

Note the three distinct numbers that the call conflated: **invoice 10,000 ≠ depreciation 9,131 ≠ principal 8,356.**

---

## 4. Q2 — Depreciation period: trust the vendor, or a rule?

**Neither the vendor's invoice nor a flat "10 years."** IAS 16 (applied via IFRS 16) depreciates the ROU asset on a systematic basis — normally **straight-line** — over the **shorter of the lease term and the asset's useful life**:

- **If the lease transfers ownership / has a purchase option reasonably certain to be exercised** → depreciate over the **asset's useful life** (you'll keep it).
- **Otherwise** → depreciate over the **lease term** (you give it back).

So Lars's instinct that buildings and cars differ is right, but the driver is **lease term vs useful life**, not the vendor's amortization schedule:
- **Leased office / building** → typically the lease term (e.g. 10 years) — usually shorter than the building's useful life.
- **Leased car** → typically the lease term (e.g. 3–5 years).

This is why the **subclass tag** (leased car vs leased office) is the right BC modelling choice (Lars reached this in the call): same posting account, different *depreciation profile per card*.

---

## 5. Q3 — The monthly invoice split

The leasing invoice is **not** "depreciation + interest." Under IFRS 16 there are **two independent mechanisms**:

1. **The cash payment** reduces the **lease liability** and is split into:
   - **Interest** = opening liability × periodic rate (the *unwind*; front-loaded, falls over time), and
   - **Principal** = the remainder (rises over time).
2. **Depreciation** of the ROU asset is computed **separately** (§4), usually straight-line, and is **unrelated to the cash amount**.

Total monthly P&L = **depreciation + interest** (front-loaded overall, vs. the flat rent of the old operating-lease method). Monthly journal at the **group/IFRS layer**:

```
Dr  Lease interest expense        (unwind of liability)      e.g. 1,644
Dr  Lease liability  (principal)  (plug to the cash paid)    e.g. 8,356
    Cr  Bank / AP                 (the invoice)                  10,000

Dr  Depreciation — ROU asset                                   9,131
    Cr  Accumulated depreciation — ROU                          9,131
```

> **This is exactly the gotcha Lars hit** ("the invoice is depreciation + interest… but that's not the value of the car"). Correct — the invoice never carries the asset value; the value was set once (§3), and the invoice is a *financing repayment*, not depreciation.

---

## 6. Q4 — "Vendor says 10,000, IFRS says 8,000" → deferred tax

This delta is **expected and correct**, not a mismatch to fix:

- **Tax (Sweden):** deducts the **whole leasing fee** each period (lease = rental for tax).
- **IFRS/book:** deducts **depreciation + interest**, on a different time profile.

The cumulative difference between the book carrying amounts (ROU asset vs lease liability) and their **nil tax base** is a **temporary difference → deferred tax** under **IAS 12**. The 2023 IAS 12 amendment (*Deferred Tax related to Assets and Liabilities arising from a Single Transaction*, effective from 2023) **removed the initial-recognition exemption for leases**, so you now **recognize deferred tax on the ROU asset and lease liability** (broadly offsetting on day 1, then diverging as the two unwind on different curves).

> **One-line rule:** the book-vs-tax gap is *supposed* to exist; you carry it as **deferred tax** at the layer that capitalizes (the group, if the entity uses the RFR 2 exemption), not as a posting error to be reconciled away.

---

## 7. Exemptions and intercompany

### 7.1 Recognition exemptions (the "LVA" tie-in)
IFRS 16 lets you **not** capitalize, expensing straight-line instead, for:
- **Short-term leases** — term ≤ 12 months (no purchase option), elected by class of asset; and
- **Low-value leases** — assessed on the asset *when new* (IASB's basis for conclusions reasons around **~USD 5,000**), e.g. laptops, phones, small office furniture — elected lease-by-lease.

This **maps onto the existing LVA (low-value asset) depreciation book** Lars described: the same "write it off, don't track depreciation, but keep it for insurance" logic. Leased low-value/short-term items ride the **non-integrated LVA-style treatment**; only material long leases (cars, offices) go through the full ROU machinery.

### 7.2 Intercompany leases — answer to "subsidize the daughter, say it's 10,000"
You **cannot** set the rent freely:
- **Transfer pricing (arm's length):** an IC lease (parent leases an office to a daughter) must be priced at **market rent**. Setting it artificially (10,000 to subsidize) is a tax-authority red flag and distorts both entities' results. *This* is the one place Lars's "someone needs to tell you the market value" worry is real — for **IC** rent-setting, not for measuring an external lease.
- **Group elimination:** the IC lease nets out in consolidation — lessee ROU + liability against lessor receivable + asset, and IC rent income vs expense — per [RFC §6](ifrs-posting-layer-rfc_v1.0.md) and the IC elimination chain. At the group the asset is simply *owned*.

---

## 8. THEN — Business Central mechanics (second, per Morre's rule)

Mapped onto what Lars demonstrated (depreciation books, subclasses, FA posting groups, integrated vs non-integrated journals):

| Concept | BC mechanism | Setting |
|---|---|---|
| **Tag the asset type** | FA Class (tangible) + **Subclass** (`LEASED-CAR`, `LEASED-OFFICE`) | Subclass is *only a tag*; it differentiates car vs office for reporting & depreciation profile. |
| **Route to accounts** | **FA Posting Group** (`LEASED`) | One posting group "Leased assets"; cars & offices share it (same accounts), separated by subclass tag — Lars's conclusion. |
| **Hold the IFRS view** | A dedicated **depreciation book** `LEASED` / `IFRS` | See integration decision below. |
| **Low-value / short-term** | Existing **LVA book**, **non-integrated** | Write-off-at-once; insurance tracking only. §7.1. |
| **Post depreciation** | `Calculate Depreciation` → journal → post | FA **Journal** for non-integrated; FA **G/L Journal** for integrated. (The two look-alike journals are the classic BC gotcha Lars flagged.) |

**Integration decision — RESOLVED by D1 (capitalize at the legal entity):**

The lease is a **fixed asset in the legal entity** via a new `RIGHT-OF-USE` subclass, **integrated** with the entity G/L — ROU/liability/interest/depreciation all post at Done1. (The earlier "non-integrated parallel book" option is moot now that the entity capitalizes outright.) The book-vs-tax gap is carried as **deferred tax** (§6). Full BC setup, the two-line interest split, and the mid-lease deferral adoption are in → [`ifrs-16-uk-frs102-bc-implementation`](ifrs-16-uk-frs102-bc-implementation_v1.0.md) §3–§4.

> **The BC "integrated vs non-integrated" question is settled: integrated, at the legal entity.**

---

## 9. Open items to confirm with Lars

1. ~~**The fork (blocks everything)**~~ **RESOLVED (D1, 2026-06-17):** capitalize at the **legal entity** — UK mandatory under FRS 102 (2026), SE by group policy. → [`ifrs-16-uk-frs102-bc-implementation`](ifrs-16-uk-frs102-bc-implementation_v1.0.md).
2. **Discount-rate policy:** set a group-wide methodology — **IBR** under IFRS 16, **OBR** (obtainable borrowing rate) for UK entities under FRS 102 — needed before any ROU can be measured (§3).
3. **Materiality / portfolio:** which leases are material enough for full ROU vs. which ride short-term/low-value exemptions (§7.1) — define the cut-off (ties to the LVA book threshold; FRS 102 low-value is more permissive).
4. **Financial-assets book (carried over from the call):** Lars's separate open question — whether financial assets need a 4th depreciation book or are booked directly in the CoA — is **out of scope** here (not a lease question); track separately.
5. **Where the capitalization is *operationally produced*:** now Done1 (legal entity, BC fixed-asset register) per D1, *not* a Done2 top-side. Confirm the two-line interest split + auto-depreciation in test (impl. report §3, action A5).

---

## 10. One-paragraph answer for Morre

A leased car/office is worth the **present value of the payments you'll make** (discounted at your incremental borrowing rate) — you compute it, nobody quotes you a market value. You depreciate that value straight-line over the **shorter of the lease term and useful life** (office ~10 yrs, car ~3–5), *ignoring* the vendor's invoice schedule. The monthly invoice is **principal + interest**, not depreciation — depreciation is a separate charge — so total IFRS cost is depreciation + interest and runs **higher early, lower late** than the old flat rent. The gap between that and the tax view (Sweden deducts the **whole fee**) is **deferred tax**, expected by design. And crucially: in a **Swedish legal entity under RFR 2 you don't capitalize at all — the lease is just rent** — so the ROU asset, the depreciation book, and the "integrated vs not" question all belong to the **group/consolidation layer**, not the legal entity's BC company. Settle that layer choice first; the BC setup falls out of it. Intercompany leases are the one exception where market value matters directly — they must be **arm's length** and are **eliminated at the group**.

---

## Sources

- [IFRS 16 *Leases* — IFRS Foundation (standard PDF)](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2024/issued/part-a/ifrs-16-leases.pdf?bypass=on)
- [IFRS 16 — Recognition and Measurement (IFRS Community)](https://ifrscommunity.com/knowledge-base/ifrs-16-recognition-and-measurement-of-leases/)
- [IFRS 16 Leases: Summary, Examples, Entries (FinQuery)](https://finquery.com/blog/ifrs-16-leases-summary-examples-entries-disclosures/)
- [Insights into IFRS 16 — Lease term (Grant Thornton)](https://www.grantthornton.global/globalassets/1.-member-firms/global/insights/article-pdfs/ifrs/insights-into-ifrs-16-lease-term-july-2020.pdf)
- [Special tax rules for financial leasing — Sweden (PwC Tax Matters)](https://blogg.pwc.se/taxmatters-en/special-tax-rules-for-financial-leasing)
- [Recognising deferred tax on leases — IAS 12 amendment (KPMG)](https://kpmg.com/xx/en/our-insights/ifrg/2024/deferred-tax-recognition-lease-assets-liabilities-amendments-ias12.html)
- [IFRS 16 — IAS Plus (Deloitte)](https://www.iasplus.com/en/standards/ifrs/ifrs-16)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-18 | Initial — research note answering Morre's six leased-asset questions from the 2026-06-18 call. Three-layer principle (Swedish tax / RFR 2 legal entity / IFRS 16 group), initial measurement (PV not market value), depreciation (shorter of term/useful life), invoice split (principal+interest ≠ depreciation), book-vs-tax delta → deferred tax, short-term/low-value exemptions (LVA tie-in), IC arm's-length + group elimination, BC mechanics mapping, open items. Companion to `ifrs-posting-layer-rfc_v1.0.md` §6. |
| 1.1 | 2026-06-22 | Resolved open fork #1 from the 2026-06-17 Carla Rogers meeting: capitalize at the **legal entity** (Done1), not group (D1). Added **UK FRS 102 (2026)** row to the three-layer table and OBR vs IBR to the discount-rate items. Updated §2 consequence, §8 integration decision (now "integrated, at the legal entity"), and §9 open items. New companion: `ifrs-16-uk-frs102-bc-implementation_v1.0.md`. |
| 1.2 | 2026-06-22 | Added §1 point 3 — the **ownership spectrum** (buy → loan-purchase → lease → rent) from Morre's Part 4 session: a lease ≠ rent; it capitalizes because it sits on the *owning* side. Concrete BC/account decisions from that session live in the implementation report v1.3. |