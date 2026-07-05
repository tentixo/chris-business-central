# Lease Accounting at the Legal Entity — UK FRS 102 & BC Implementation Plan

**Branch**: `ifrs-16-research`
**Date**: 2026-06-22
**Sources**: "IFRS in BC" meeting 2026-06-17; Morre working sessions 2026-06-22 (`Call with Lars Mårelius (10)/(11)/(12).docx`); Morre's W-H-S walk `whs-ifrs16-k3-leases-2026-06-22.md`.
**Participants**: Camilla Höög, Lars Mårelius (Morre), Chris Mansson, **Carla Rogers (Lasernet UK)**
**Companions**:
- [`ifrs-16-leased-assets-research_v1.0.md`](ifrs-16-leased-assets-research_v1.0.md) — the *principle/measurement* note (this report resolves its open fork #1 and adds the UK jurisdiction).
- [`ifrs-posting-layer-rfc_v1.0.md`](ifrs-posting-layer-rfc_v1.0.md) §6 — the layer classification (entity vs group).
- **Forthcoming (Morre):** `ergon-ifrs16-k3-leases_v1.0.md` + anchor **COA-017** — the K3-leases ergon doc this validated mechanism feeds.

> This is an **execution/decisions** record, not a principle note. The measurement mechanics (PV, depreciation, interest split, deferred tax) live in the research note; here we capture the **decisions taken**, the **UK FRS 102 driver**, the **BC setup**, and the **rollout plan**.

---

## 0. Headline decisions from the meeting

| # | Decision | Owner / next step |
|---|---|---|
| D1 | **IFRS 16 / lease capitalization is done in the LEGAL ENTITY (Done1), not at group level.** | Resolves research-note fork #1. New-flow principle. |
| D2 | UK leases capitalize at the entity because **FRS 102 now requires it** (periods from **1 Jan 2026**) — the "newish UK regulation" Carla is implementing. | Carla, this period. |
| D3 | Use the BC **fixed-asset register** for the ROU **asset leg** (auto depreciation, write-down, insurance). The financing leg is posted separately (see D7). | Lars/Chris: ~1 day setup. |
| D4 | A **"right-of-use" FA subclass + posting group is MISSING** in pristine and must be added. | Lars/Camilla: add subclass code + accounts. |
| D5 | Mid-lease UK adoption: book **from 1 Jan as if correct**, use **deferrals** to land the net in **June** (open period) — preserves auditor traceability, no reopening closed months. | Carla + Emma agree opening figures. |
| D6 | Deliverable: a **step-by-step guide** so the setup can be **rolled out** UK → other entities (DE, SE). | Chris (documentation). |
| D7 | **Keep all three natures on the FA, natively:** depreciation (asset value) + **principal as Custom 1 → 2398** + **interest as Custom 2 → 8421**, with Custom 1/2 set **not part of book value**. Financing rides *on* the asset for traceability without corrupting its value. | §3. **Built & validated live in BC by Morre 2026-06-22.** Supersedes the earlier "interest outside FA / Excel schedule." |
| D8 | **Lease liability = dedicated BAS `2398`**; **interest = `8421`**; **clearing/transit = `1261`** (new). Acquisition: Dr 1260 / Cr 2398 from the contract. | §3.1. **Picked & built live by Morre 2026-06-22.** |

**One-line takeaway:** *Leases go on-balance-sheet in each legal entity (UK mandatorily, from FRS 102 2026): the ROU asset (1260/1267) depreciates straight-line in BC's FA module, while each monthly lessor invoice is scanned to a clearing account (1261) and an FA G/L Journal splits it into Custom 1 (principal → 2398) + Custom 2 (interest → 8421) — keeping everything on the asset, no extension, BC as the source of truth. Deferred tax = (Depreciation − Principal) × 20.6%, posted at close.*

> **SOLVED & validated live (2026-06-22):** Morre + his Claude Code (W-H-S `whs-ifrs16-k3-leases-2026-06-22.md`) designed it; **Morre then built it end-to-end in BC test and it worked** (Calls 11 & 12) — clearing account nets to 0, principal/interest/depreciation all on the FA Ledger, no extension. Scope locked to **K3 legal entity**. The one remaining input is the **amortization convention** (annuitet vs rak amortering) from the real lease contracts — it decides whether deferred tax arises (§5.2) and whether the monthly principal is fixed or scheduled. → Carla next-steps (§6).

---

## 1. The strategic shift — push IFRS down to Done1

Lars's framing (from the "new flow" analysis of all IFRS/IAS rules):

> *"IFRS 16 should be handled in the legal entity, not at group level… most of what's done now in the consolidation company should be done on the legal entities (Done1)."*

Why it matters operationally:
- **Done1** (legal entity) already has reporting currency + proper FX revaluation (JEV) → it can carry far more than before.
- Push lease capitalization (and most IFRS recognitions) **down to Done1** → BC's **vanilla consolidation reconciliation** works automatically *if the right accounts carry the right numbers*, with **no complex Auro mapping**.
- **Done2** (the consolidation company — a side company, *not* a legal entity) is then left with only genuine **group-level** IFRS adjustments (special valuations, eliminations). A small residual "we don't yet know" part remains.
- **Done3** = report production; any reporting tool (Auro sits between Done2 and Done3) can consume correct Done2 numbers.

This **resolves the open fork** in the research note: for these entities the answer is *capitalize in the legal entity*, not take the operating-lease exemption and push it to group. UK has no choice (FRS 102, §2); the others follow the same principle by design.

---

## 2. The UK driver — FRS 102 lease changes (2026)

Carla: *"This is all quite new for me… we've not done it in the UK before or had to do it."* That's the **FRS 102 periodic-review amendments**, effective for accounting periods **beginning on or after 1 January 2026**: Section 20 lessee accounting is replaced by a **single on-balance-sheet model** aligned with IFRS 16.

| Feature | IFRS 16 (group / SE if elected) | **FRS 102 (2026) — UK entity** | Practical effect for Carla |
|---|---|---|---|
| Lessee model | All leases on-balance-sheet (ROU + liability) | **Same** — operating/finance distinction removed for lessees | Must recognize ROU + liability for the UK leases now. |
| **Discount rate** | Implicit rate, else **IBR** | Implicit rate, else **OBR** (Obtainable Borrowing Rate) — *simpler to compute* | Carla's "discount rate we have to apply" = the OBR. |
| Short-term (≤12m) exemption | Yes | **Yes** | Available. |
| Low-value exemption | ~USD 5,000 guide | **Yes, more permissive, no fixed threshold** (entity judgement) | Wider scope to expense small leases. |
| Exempted-lease disclosure | Not required | **Maturity analysis required** | Extra note for short-term/low-value leases. |

**Measurement is otherwise as the research note §3–§5**: ROU = PV of payments at the OBR; depreciate over the shorter of lease term and useful life; the monthly payment splits into **interest + principal**, with **depreciation a separate charge**. Lars's instinct in the meeting — *"two lines: the actual rental value of the car, and the interest… and then depreciation, done automatically"* — is exactly right.

> Note for SE/other entities: Sweden's RFR 2 still *permits* the operating-lease exemption in the legal entity, but per **D1** the group chooses to capitalize at Done1 anyway for a uniform model. (Confirm per-jurisdiction — §6.)

---

## 3. BC implementation — SOLVED & validated live in BC (2026-06-22)

> **Status: SOLVED.** Morre + his Claude Code worked this out (W-H-S walk `whs-ifrs16-k3-leases-2026-06-22.md`) and **Morre then built it live in BC test, end-to-end, and it worked** (Calls 11 & 12). This **supersedes** the earlier "interest lives *outside* the FA in an Excel/ISV amortization schedule" draft: the financing now stays **inside BC, linked to the asset**, with **no extension**. Scope is **K3 legal entity**. Feeds a forthcoming ergon doc + anchor **COA-017** (Morre's side).

**The unlock — one lease, three natures, all traceable on the FA.** The breakthrough is posting the **principal** and **interest** as **Custom 1 / Custom 2** FA Ledger entries that are configured to **not affect book value or depreciation**. They ride *on the asset* (so "link every event to the FA" is satisfied, BC stays the source of truth — no ghost register/Excel), but they don't corrupt the ROU asset's straight-line depreciation.

| Nature | What | How it's posted | Affects ROU book value? |
|---|---|---|---|
| **Asset** | ROU depreciation, straight-line | `Calculate Depreciation` → Dr 78xx / Cr 1267 | **Yes** (this is the asset) |
| **Financing — principal** | ↓ lease liability | FA G/L Journal, **Custom 1** → 2398 | **No** (`Part of Book Value` OFF) |
| **Financing — interest** | OBR interest expense | FA G/L Journal, **Custom 2** → 8421 | **No** (`Part of Book Value` OFF) |
| **Tax** | book-cost vs tax-cost timing diff | computed from the FA Ledger (§5), posted at close | n/a |

### 3.1 Accounts (BAS) — confirmed live against pristine CoA

| Role | BAS account | Notes |
|---|---|---|
| ROU asset (gross) | **1260** Leasade tillgångar | Acquisition cost = PV of payments at OBR/IBR, from the **contract**. |
| Accumulated **depreciation** (contra) | **1267** | Filled only by monthly depreciation. (Generic BAS uses 1269; pristine uses **1267** — `1269` not used.) |
| Accumulated **write-down** (impairment) | **1268** | Only if a lease ROU is impaired. |
| **Lease-clearing / transit** | **1261** *(new)* | Temp account between invoice scan and the FA G/L journal. **Must net to 0 every month** — non-zero = error (built-in control). Clusters with 1260/1267/1268. |
| **Lease liability — long-term** | **2398** (dedicated, in the **2390** Övriga långfristiga skulder range; 2394 was taken) | Acquisition balancing account; Custom 1 destination. |
| Lease liability — current portion | 2840 / 2890 | <1-year part; reclassify (year-end is fine). |
| **Interest expense (OBR)** | **8421** Räntekostnader, kreditinstitut | Custom 2 destination. |
| Depreciation expense | **78xx** | Routed by the FA posting group. |
| Deferred tax | **8940** (P&L) · **2240** (DTL) / **1370** (DTA) | §5. |

### 3.2 The monthly process — 4 steps (validated live)

Worked numbers (car, PV 328,700, OBR 0.5%/mo): month-1 depreciation **9,131**, principal **8,356**, interest **1,644**, payment **10,000**.

**Commencement (once, at contract start)** — manual FA G/L Journal, Posting Type = Acquisition Cost, **Bal. Account = 2398** (no acquisition invoice exists — the value comes from the **contract**):
```
Dr 1260  ROU asset        328,700      Cr 2398  Lease liability   328,700
```

**Each month:**
```
Step 1 — Scan the lessor invoice (normal AP scan, no special handling):
   line = "LEASE-CLEARING" item → posts the gross amount to the clearing acct
   Dr 1261  Lease-clearing   10,000      Cr 2440  Vendor (AP)       10,000   (no VAT — financial)

Step 2 — Calculate Depreciation on the LEASED-FA book (automatic):
   Dr 78xx  Depreciation       9,131     Cr 1267  Accum. depreciation  9,131

Step 3 — FA G/L Journal: split the clearing balance onto the FA via Custom 1/2,
         balancing to 1261 (clears it to 0):
   FA line  Custom 1  (principal)  8,356  → 2398   ┐ both balanced to
   FA line  Custom 2  (interest)   1,644  → 8421   ┘ 1261  →  Cr 1261  10,000
   ⇒ 1261 nets to 0 (the control); 2398 ↓ by principal; 8421 carries interest;
     all three (depreciation, principal, interest) now sit on the FA Ledger.

Step 4 — Deferred tax (at close, see §5): (Depreciation − Principal) × 20.6% → 8940 / 2240(or 1370)
```

> Depreciation (9,131) ≠ payment (10,000) ≠ principal (8,356) — three different numbers. The Custom 1/2 entries are **records on the asset**, not part of its value: open the FA book value and you see only depreciation; the principal/interest appear as Custom entries. That separation is the whole trick.

### 3.3 Load-bearing configuration (do this once)

| Element | Setting |
|---|---|
| FA Class / Subclass | Tangible → **`RIGHT-OF-USE`** (`ROU-CAR`, `ROU-OFFICE`). Morre: *"right of use, that's a very good tag."* |
| Depreciation book **LEASED-FA** | **Integrated** with G/L (per D1). Straight-line over the lease term (10 yrs for the office in the live test). |
| **FA Posting Group (leased)** | acquisition → **1260**, accum. dep. → **1267**, dep. expense → **78xx**, **Custom 1 Account → 2398**, **Custom 2 Account → 8421**. |
| **FA Posting Type Setup — the 🔑** | **Custom 1 and Custom 2: `Part of Book Value` = OFF and `Include in Depr. Calculation` = OFF.** Without this, principal/interest would corrupt the ROU value and depreciation. |
| Sign | Custom 1/2 must allow **both debit and credit** (a vendor credit memo reverses them). |
| "LEASE-CLEARING" item | An **internal clearing item** (Morre's "Z-item" — a 4th category, "just for moving things"), product posting group → **1261** on both sales & purchase. Lets the invoice scan normally — the scanner needn't know it's a lease (special-casing the scan = anti-pattern). |

### 3.4 Why it works — the constraints, resolved

- **Purchase-invoice FA lines can only post Acquisition Cost / Maintenance — *not* Custom 1/2.** ← the exact blocker Morre/Chris hit reading the invoice. That's why Step 1 lands on a **clearing account** and Step 3 (an **FA G/L Journal**, which *can* post Custom 1/2) moves it onto the FA. *(Earlier reports concluded "interest lives outside the FA" — now superseded: interest is a non-value **Custom 2** FA entry.)*
- **D7 — OBR is per-asset (1260 holds many leases) → no global auto-account.** Holds: the per-lease principal/interest come from that lease's **amortization schedule** and are entered on its own FA G/L Journal lines. (The old "Automatic Account / allocation" idea stays abandoned.)
- **D8 — an FA Posting Group routes one account *per posting type*.** Resolved by using **two** posting types: **Custom 1 → 2398** (principal) and **Custom 2 → 8421** (interest) — distinct buckets, distinct accounts, **one** posting group, all on the same FA. *(This refines the earlier "interest is not an FA posting" wording — it now is, as a non-value Custom 2 entry.)*
- **`Calculate Depreciation` posts only depreciation** (confirmed) — it cannot emit the interest/principal, so Step 3 is a separate recurring FA G/L Journal run **after** depreciation. Run it **manually each month** (HitL: not a Job Queue, for now).
- **Built-in control:** 1261 = 0 after Step 3. Anything left on 1261 at month-end ⇒ something broke.
- **No extension, no Excel, no ISV.** Base BC has **no native lease engine** (the "Asset leasing" module is *D365 Finance*, not BC; Subscription Billing is sell-side billing) and **no native deferred-tax engine** — but the FA module + clearing item + recurring FA G/L Journal carry it natively. (SOFT4Lessee on AppSource exists if vanilla is ever abandoned.)

---

## 4. Mid-lease adoption — the deferral technique (UK, this period)

The UK leases are **already ~halfway through** and prior months (Jan–May) are **closed**. Adopting from **1 Jan** without reopening closed periods:

**Method (D5)** — a **two-step** process confirmed in the live session:
1. Agree the **opening figures** with **Emma / Carla** — ROU value, term, interest rate, monthly invoice split.
2. **Acquire** the FA from the contract (Dr 1260 / Cr 2398), then **run the normal monthly Steps 1–4 (§3.2) for each closed month, Jan → May** — exactly the same routine you'll run every month going forward.
3. **Deferral push:** remove those Jan–May postings via **deferrals** so the **net lands in June** (the open period) — nothing changes in closed months, full audit trail preserved. *Only June carries this extra step; Steps 1–4 are identical every month.*
4. From June onward, **continue normally**.

> ⚠️ The **deferral push-back step (3) was NOT yet built/tested** in the live session — Morre flagged "let me think that through." **Must be tested in the sandbox** before doing it for real. Rejected alternative: force-pushing into closed months (changes closed numbers — Carla: *"I'd not do that."*).

---

## 5. Deferred tax (account 8940)

### 5.1 Worked example (continuing the §3.2 car)

The deferred tax tracks the **temporary difference** between book expense and tax deduction. Two routes to the same number for **month 1**:

| Route | Calculation | Result |
|---|---|---|
| **P&L difference** | book expense 10,775 (dep 9,131 + interest 1,644) − tax deduction 10,000 (Swedish tax deducts the *whole lease fee*) | **775** |
| **Balance-sheet (IAS 12 method)** | lease liability 320,344 − ROU NBV 319,569 (both vs tax base 0) | **775** |

**Deferred tax to book = 775 × tax rate** — a net deferred tax **asset** (book expensed more than tax allows early on → pay more tax now, recover later):

| Rate | Month-1 deferred tax |
|---|---|
| Sweden 20.6% | 775 × 20.6% ≈ **160** |
| UK 25% | 775 × 25% ≈ **194** |

Journal (BAS, Sweden, ≈160):
```
Dr 1370  Deferred tax asset (BS)     160
   Cr 8940  Deferred tax (P&L)           160   ← reduces tax expense
```

**Behaviour over the lease life:**
- **Day 1 = zero.** DTA and DTL are equal (both on the full PV) and net to nil — the 2023 IAS 12 amendment requires recognizing both. Deferred tax appears only *as the two legs diverge*.
- **Moves every month.** Period temp diff = book expense − 10,000; **positive while book > cash** (early), shrinks, **turns negative** later (book expense falls below the flat cash), and **nets to zero** at lease end. Book the *movement* each period, not 775 forever.
- **Depends on the tax rule.** Assumes tax deducts the **full lease fee** (Swedish rental treatment). Where local tax instead **follows the accounts** (some UK lease cases), there's little/no temporary difference — which is exactly why Carla saw no IFRS 16 deferred tax locally and the **auditor computes it**. Confirm local treatment before booking.
- **Immaterial per lease** (~160–194/month) — supports "don't over-couple the lease setup to deferred-tax automation."

### 5.2 Computing it FA-natively (validated approach)

Because Step 3 now puts **principal (Custom 1)** and **interest (Custom 2)** on the FA Ledger alongside **Depreciation**, the temporary-difference movement reduces to two FA Ledger figures — **interest cancels** (deductible under both book and tax):
```
Δ temp diff = (Depreciation + Interest) − (Principal + Interest)   [tax deducts the lease fee = principal+interest]
            =  Depreciation − Principal          = FA "Depreciation" − FA "Custom 1"
Deferred-tax movement = (Depreciation − Principal) × 20.6%
```
- **Correctness rule:** Σ Depreciation = Σ Principal over the term ⇒ the temporary difference **reverses to zero** (it's a timing difference). If they don't net (e.g. fixed principal ≠ straight-line depreciation forever), the asset value and the liability schedule are out of sync — an alarm, not a result.
- A **Financial Report / Account Schedule / Power BI** reads `Depreciation − Custom 1` × 20.6 % (the rate is a formula constant — no native rate table). **Calc native, post manual.**

### 5.3 Practicalities

- Account **`8940`** (deferred tax, P&L) was **missing from pristine** — add it. BS side: **`1370`** DTA / **`2240`** DTL.
- **No native BC deferred-tax engine — confirmed absent** (MS Learn, 2026 wave 1). The earlier "BC v28 supports deferred tax" was a misread: first of the **Deferrals** feature (spreads prepaid/unearned across periods — *not* income tax), then of **Withholding Tax** (källskatt on payments — also not deferred tax). Nothing in base BC computes a book-vs-tax temporary difference and posts DTA/DTL. *(The full lease engine "Asset leasing" is D365 **Finance**, not BC.)*
- ⇒ **The report computes; the human posts one journal at close.** Deferred tax is a close-process judgment aggregating all temporary differences + loss carryforwards + rate — don't fragment per-asset or auto-post. (Optional: a non-integrated **TAX depreciation book** can hold the tax-base view inside BC, useful register-wide for owned-asset accelerated depreciation; for the lease, `Depreciation − Custom 1` already gives the figure on one book.)
- **UK practicality:** a **"helper" (advisors, not the auditor** — you can't audit what you book) gives Carla the figure and she posts it; *"it doesn't matter who calculated it; it's how it's posted that matters."* They must give her a **rate (%)**, not just an amount, so it can be booked from the FA figures — especially where the contract states **no OBR**. Emma's group figure is the **translation to the common IFRS baseline** (Done2). The other deferred-tax accounts Emma requested are a **separate issue, not driven by IFRS 16** locally — don't over-couple.

---

## 6. Rollout & open actions

**Lease population (from Carla's spreadsheet):** UK = **2 leases** (one office just vacated), plus a **German** lease and some **Swedish** leases. UK goes first; push the pattern to other entities (~Monday) so each can adopt when ready.

### 6.1 Next step with Carla — settled at the end of Call 12

The mechanism is built and proven; the gate now is **real data + a sandbox dry-run**, then walk Carla through it. In order:

1. **Chris pings Carla — "we've figured it out, send us the real data."** Specifically, for each UK lease:
   - the **lessor invoices** + the **values** (ROU value from the contract);
   - the **interest rate** — and if the contract states none, the **helper/advisor must supply a rate (%)** (not just a deferred-tax amount), so it's bookable;
   - the **depreciation period** (how many years);
   - the **opening figures** (with Emma) for the mid-lease catch-up.
2. **Stand up / use the sandbox** (not production) — Camilla to be pinged. Reasons: Carla gets her head around it, **and** the **depreciation** + the **deferral push-back (June)** steps still need testing (Morre hasn't built the push-back yet).
3. **Build & test in sandbox with the real numbers** — run e.g. January through Steps 1–4, then the deferral push so the net lands in June; confirm the clearing account (1261) nets to 0 and the postings match expectation.
4. **Walk Carla through it** in the sandbox (she does it with Chris/Lars), and **hand her the step-by-step guide** (→ `ifrs16-lease-setup-guide-bc_v1.0.md`).
5. **Decide deployment**: do the dry-run in sandbox first; only then replicate in production. Then roll the pattern to DE/SE.

### 6.2 Action register

| # | Action | Owner | When |
|---|---|---|---|
| A1 | Add `RIGHT-OF-USE` FA subclass + FA **posting group** (1260 / **1267** / 78xx; **Custom 1 → 2398**, **Custom 2 → 8421**); set Custom 1/2 **not part of book value** | Lars / Camilla | Before any booking |
| A2 | Add accounts: **1261** clearing, **8940** deferred tax (BS 1370/2240); confirm **2398** liability, **1267/1268** dep./write-down | Camilla | — |
| A3 | Create the **LEASE-CLEARING item** (internal "Z-item", posting group → 1261, no VAT) | Lars / Chris | Before any booking |
| A4 | **Get real data from Carla** (invoices, values, interest **rate %**, depreciation years, opening figures) — §6.1 | Chris → Carla/Emma | **Now — the gate** |
| A5 | **Sandbox dry-run** with real numbers: run Steps 1–4 for a month; build & test the **deferral push-back to June**; confirm 1261 = 0 | Lars + Chris | tentixo **test** sandbox |
| A6 | **Walk Carla through** the sandbox + hand over the **step-by-step guide** | Chris + Carla | After A5 |
| A7 | Replicate in **production**; then roll the pattern to **DE / SE** | Chris | After A6 |
| A8 | (Open) settle the **amortization convention** (annuitet vs rak amortering / residual) from the contracts → fixes principal schedule & whether deferred tax arises | Carla / Lars | With A4 |

**Context constraint:** Lasernet may be **acquired**; Carla wants to **avoid large changes** now. Mitigant: the buyer reportedly **uses BC** too, so BC wouldn't change — only the reporting tool (Auro) might; and a correct Done1/Done2 setup survives an acquisition audit. Net: proceed (≈18h already invested; saves ≈8h/month), defer reporting-tool rework.

---

## 7. Side topic — VAT basis (France/Veronique), for the record

Briefly raised at the top of the call and **already covered** elsewhere — no new decision:
- A group company **may** use **unrealized (cash-basis) VAT** vs invoice-basis; VAT is **per-entity, never consolidated**, so daughters may differ. → [`ifrs-posting-layer-rfc_v1.0.md`](ifrs-posting-layer-rfc_v1.0.md) §7, [`meeting-prep-vat-deferral-fr_v1.0.md`](meeting-prep-vat-deferral-fr_v1.0.md).
- **Recommendation:** switch France from unrealized → **realized** for operational consistency (BC setup identical; reduces hand-over/cover risk for Veronique). A **one-off reconciliation** on the quarter of change; France must clear it with the FR tax authority — Carla to look at it with Veronique.

---

## Sources

- [Amendments to FRS 102 on lease accounting (PwC Viewpoint UK)](https://viewpoint.pwc.com/dt/uk/en/pwc/uk_in_depths/uk_in_depths_UK/amendments-to-frs-102.html)
- [What has changed under amended FRS 102? (Grant Thornton UK)](https://www.grantthornton.co.uk/insights/what-has-changed-under-amended-frs-102/)
- [FRS 102 (2026): OBR explained vs IFRS 16 (House of Control)](https://www.houseofcontrol.com/blog/discount-rates-in-frs-102)
- [FRS 102 lease changes 2026 compared with IFRS 16 (House of Control)](https://www.houseofcontrol.com/blog/frs-102-lease-changes-compared-with-ifrs-16)
- [FRS 102 vs IFRS 16: key comparisons (FinQuery)](https://finquery.com/blog/frs-102-vs-ifrs-16-key-comparisons-between-the-lease-accounting-standards/)
- [FRS 102 lease accounting changes 2026 (Forvis Mazars UK)](https://www.forvismazars.com/uk/en/insights/financial-and-corporate-reporting-updates/frs-102-lease-accounting-changes-2026)
- [BAS — kort-/långfristig del av leasingavgift](https://www.bas.se/2020/04/24/ska-forhojd-leasingavgift-delas-upp-i-kort-och-langfristig-del/)
- [Svenska Ekonomiska — redovisning av leasingbil (finansiell leasing, Kr 2390)](https://svenskaekonomiska.se/redovisning-av-leasingbil/)
- [Kontoplan BAS 2025](https://www.metricaccounting.se/wp-content/uploads/2025/07/Kontoplan-BAS-2025.pdf)
- [Wolters Kluwer — viktigt att veta vid redovisning av leasing](https://www.wolterskluwer.com/sv-se/expert-insights/viktigt-att-veta-vid-redovisning-av-leasing)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-22 | Initial — from the 2026-06-17 "IFRS in BC" meeting with Carla Rogers (Lasernet UK). Headline decisions (lease capitalization at Done1; UK FRS 102 driver; FA-register approach; ROU subclass to add; mid-lease deferral adoption; rollout). UK FRS 102 (2026) vs IFRS 16 comparison (OBR vs IBR, exemptions, disclosure). BC implementation, deferred-tax (8940) practicalities, rollout actions with owners, VAT side-note. Companion to `ifrs-16-leased-assets-research_v1.0.md` (resolves its open fork #1). |
| 1.1 | 2026-06-22 | Rewrote §3 with the **two-leg model** (asset leg in FA module; financing leg — interest+principal — posted *outside* FA per a per-lease amortization schedule). Added BAS account map (1260 ROU / 1269 accum. dep. / **2390 lease liability** / 84xx interest / 78xx depreciation), the commencement + monthly journal entries, and §3.4 resolving the two BC constraints (per-asset OBR → schedule not auto-account; one-account-per-posting-group → interest isn't an FA posting). Added decisions **D7** (two-leg split) and **D8** (2390 liability). Dropped the earlier "interest via FA posting group + subclass + JEV report" approach. Updated §4 step 2, actions A1/A2/A4/A5, BAS sources. |
| 1.2 | 2026-06-22 | Added §5.1 **worked deferred-tax example** (month-1 temp diff 775 via both P&L-difference and balance-sheet methods; ≈160 SE / ≈194 UK; net DTA; day-1 zero; movement/reversal over life; dependence on local tax rule; immateriality). Added BS deferred-tax accounts 1370 / 2240. |
| 1.3 | 2026-06-22 | Folded in **Part 4 working session** (Morre, 1h, `Call with Lars Mårelius (10).docx`). Concrete account decisions: lease liability **2390 → dedicated 2398**; accumulated depreciation **1269 → 1267** (+ **1268** write-down; 1269 unused) per Morre's live CoA check. Marked D1/D7/D8 + the two-leg model **confirmed by Morre** (incl. his quotes and his prior failed FA-card interest test → needs line posting). Added the "no acquisition invoice — value from contract" framing. Added §2 validation banner. Deferred-tax §5.2: BC v28 advanced handling (varies over 5yr, not auto-account; pension-insurance analogy). A5 now testable in tentixo test sandbox. 1267 depreciation / 1268 write-down confirmed. |
| **1.4** | 2026-06-22 | **SOLVED.** Folded in Morre's W-H-S walk + **live BC build** (Calls 11 & 12). **§3 rewritten** to the validated native mechanism: financing rides **on the FA** as **Custom 1 (principal → 2398)** + **Custom 2 (interest → 8421)** with `Part of Book Value` OFF, via a **1261 clearing account** + monthly 4-step process (scan→clearing, depreciate, FA G/L split, deferred tax). **Supersedes the v1.1–1.3 "interest outside FA / Excel schedule"** conclusion — interest *is* an FA (Custom 2) posting; D7/D8 reworked. New accounts **1261** clearing, **8421** interest. §5 deferred tax rewritten to the **FA-native formula (Depreciation − Custom 1) × 20.6%** (interest cancels), correctness rule (Σdepr=Σprincipal ⇒ reverses), and **no-native-engine** verification (Deferrals/Withholding Tax ≠ deferred tax; Asset leasing = D365 Finance). §4 mid-lease = run Steps 1–4 per closed month + untested deferral push to June. **§6.1 Carla next-steps** + reworked action register. Companion step-by-step guide created. |