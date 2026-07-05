# Setting Up a Finance Lease in Business Central — Step-by-Step Guide

**Purpose**: a practical, repeatable guide to record a finance lease (IFRS 16 / FRS 102 / K3) in Business Central — the right-of-use asset, the lease liability, the monthly interest/principal split, and the deferred tax — **all linked to the Fixed Asset, with no add-on app.**
**Audience**: the entity accountant (e.g. Carla, Lasernet UK) + whoever does the one-time setup.
**Validated**: this method was built and proven end-to-end in BC test (Morre, 2026-06-22).
**Companion**: design rationale in [`ifrs-16-uk-frs102-bc-implementation_v1.0.md`](ifrs-16-uk-frs102-bc-implementation_v1.0.md); measurement principles in [`ifrs-16-leased-assets-research_v1.0.md`](ifrs-16-leased-assets-research_v1.0.md). Morre's screen-level step-by-step is the click-by-click companion.

> **The idea in one line:** the lease's *value* depreciates like any fixed asset; each monthly invoice is parked on a **clearing account** and then split — by a Fixed Asset journal — into **principal** (lowers the liability) and **interest** (a cost), both recorded *on the asset* as "Custom" entries that don't change its value.

---

## 0. Before you start — what you need from the lease contract

For each lease, get:
- **Value of the asset** (the right-of-use value = present value of the payments — from the contract).
- **Lease term** in years (e.g. office 10 years, car 3–5).
- **Interest rate** (OBR/IBR). *If the contract doesn't state one, your advisor/helper must give you a **rate (%)**, not just an amount.*
- **Monthly payment**, and its **principal / interest split** each month (the amortization schedule).
- For a **mid-year start**: the **opening figures** (agree with Emma).

> ⚠️ The **amortization convention** matters: with *rak amortering* (equal principal) the principal is the same every month; with *annuitet* (level payment) the principal rises each month. This decides Step C3 and whether deferred tax arises (§E). Get it from the contract.

---

## A. One-time company setup (do once — admin / Camilla / Chris)

### A1. Chart of accounts — confirm these exist
| Account | Name | Role |
|---|---|---|
| **1260** | Leasade tillgångar | Right-of-use asset (gross value) |
| **1261** | Lease clearing (transit) | Temp account — **must be 0 at month-end** |
| **1267** | Ack. avskrivningar leasade | Accumulated depreciation |
| **1268** | Ack. nedskrivningar leasade | Accumulated write-down (only if impaired) |
| **2398** | Leasingskuld | Lease liability (long-term) |
| **8421** | Räntekostnader, kreditinstitut | Interest expense |
| **78xx** | Avskrivningar | Depreciation expense |
| **8940 / 1370 / 2240** | Uppskjuten skatt / DT asset / DT provision | Deferred tax |

### A2. Fixed Asset setup
1. **FA Class** = Tangible; **FA Subclass** = `RIGHT-OF-USE` (e.g. `ROU-OFFICE`, `ROU-CAR`).
2. **Depreciation Book** `LEASED-FA`: **G/L Integration ON**, method **Straight-Line**.
3. **FA Posting Group** (leased):
   - Acquisition → **1260**, Accum. Depreciation → **1267**, Write-Down → **1268**, Depreciation Expense → **78xx**
   - **Custom 1 Account → 2398** (principal), **Custom 2 Account → 8421** (interest)
4. **FA Posting Type Setup** for this book — **the critical bit** 🔑:
   - **Custom 1** and **Custom 2**: `Part of Book Value` = **OFF**, `Include in Depreciation Calculation` = **OFF**.
   - Allow **both debit and credit** signs (a vendor credit memo reverses them).
   - *Why:* this lets principal & interest sit on the asset's ledger for traceability **without changing the asset's value or depreciation.**

### A3. The clearing item
Create an internal **"LEASE-CLEARING" item** (Morre's "Z-item" — purely for moving money):
- Type = Service (or non-inventory), **no VAT**, no deferral template.
- Its product posting group posts to **1261** (both sales & purchase).
- *Why:* the lessor invoice can then be scanned like any other — the scanner needn't know it's a lease (special-casing the scan is an anti-pattern).

---

## B. Set up one lease (once per lease)

1. **Create the Fixed Asset card**: Subclass `ROU-OFFICE`/`ROU-CAR`; attach the **LEASED-FA** book; set **Depreciation Starting Date** and **No. of Depreciation Years** (the lease term); method Straight-Line.
2. **Record the asset value (acquisition)** — there is **no supplier invoice** for the full value, so post it manually from the contract:
   - **FA G/L Journal** → FA Posting Type = **Acquisition Cost**, Amount = **asset value (PV)**, **Bal. Account No. = 2398**.
   - Post. Result: **Dr 1260 / Cr 2398** for the full value.
3. **Check**: FA book value = PV; account 2398 shows the liability (credit) = PV.

---

## C. Every month (per lease) — the 4-step routine

> Worked figures below use: value 328,700 · depreciation 9,131 · principal 8,356 · interest 1,644 · payment 10,000. Use your lease's own numbers.

### C1. Register the lessor invoice → clearing
- Enter the **purchase invoice** as normal, one line = the **LEASE-CLEARING item**, amount = the **full payment** (e.g. 10,000), **no VAT**.
- Post. Result: **Dr 1261 (clearing) 10,000 / Cr Vendor (AP) 10,000**.

### C2. Run depreciation
- **Calculate Depreciation** on the **LEASED-FA** book for the period → review → **Post**.
- Result: **Dr 78xx 9,131 / Cr 1267 9,131**. *(This is the only thing that changes the asset's value.)*

### C3. Split the clearing balance onto the asset (FA G/L Journal)
- Open an **FA G/L Journal**, two lines on this lease's FA:
  - Line 1 — FA Posting Type **Custom 1**, amount = **principal** (8,356), **Bal. Account = 1261**
  - Line 2 — FA Posting Type **Custom 2**, amount = **interest** (1,644), **Bal. Account = 1261**
- Post. Result: principal → **2398** (liability falls), interest → **8421**, and **1261 is cleared to 0**.
- Now the asset's ledger carries **all three**: depreciation, principal, interest.

### C4. Deferred tax (at close — see §E)
- Compute and post the deferred-tax movement once per close.

### ✅ Month-end check
- **Account 1261 = 0.** If anything is left on 1261, a step was missed or an amount is wrong — fix before closing.

---

## D. Starting a lease partway through the year (mid-lease adoption)

When the lease has been running but wasn't in BC (e.g. live from January, but you're setting up in June, Jan–May closed):

1. Do the **one-time setup (A)** and the **lease setup (B)**.
2. **Run Section C (Steps C1–C4) for each closed month** — January, February, … — exactly as you will every month.
3. **Push the net into the open month (June)** using **deferrals**, so the closed months are untouched but the full history is recorded.
4. From June, just continue with the normal monthly routine (C).

> ⚠️ **Test this in the sandbox first.** The deferral push-back (step 3) was **not yet built/tested** at the time of writing — do a dry-run with real numbers before doing it in production. Do **not** force postings into closed months.

---

## E. Deferred tax (how to compute & post)

Because Step C3 put **principal (Custom 1)** and **interest (Custom 2)** on the asset, the temporary difference is just two figures — **interest cancels** (deductible for both book and tax):

```
Deferred-tax movement = (Depreciation − Principal) × tax rate
   e.g. (9,131 − 8,356) × 20.6%  =  775 × 20.6%  ≈  160
```
- Early in the lease, depreciation > principal → a deferred-tax **asset** builds; later it reverses; over the whole term it nets to **zero**.
- **If principal = depreciation every month** (equal-principal lease where principal = value ÷ months) there is **no deferred tax** — they cancel.
- **BC does not auto-post this.** A Financial Report / Account Schedule / Power BI reads `Depreciation − Custom 1 × rate`; **a person posts one journal at close** (Dr/Cr **8940** P&L and **1370** DTA / **2240** DTL). In the UK, the advisor/helper supplies the figure (and the **rate %**) and the accountant posts it.

---

## F. What "good" looks like (quick controls)
- **1261 = 0** at every month-end.
- **FA book value** = original value − accumulated depreciation (Custom 1/2 do **not** affect it).
- **2398** = remaining lease liability (falls by principal each month; agrees to the amortization schedule).
- **8421** = interest to date.
- When the lease ends: FA fully depreciated, 2398 = 0.

---

## Glossary
- **Right-of-use (ROU) asset** — the leased item on your balance sheet (you control its use for the term).
- **Lease liability** — what you still owe the lessor (account 2398).
- **OBR / IBR** — the discount/interest rate (UK FRS 102 = *Obtainable* Borrowing Rate; IFRS 16 = *Incremental* Borrowing Rate).
- **Custom 1 / Custom 2** — user-defined Fixed Asset "value buckets" we repurpose for principal and interest, set **not** to affect book value.
- **Clearing account (1261)** — a temporary holding account; nets to zero each month and acts as a built-in error check.
- **Deferred tax** — the timing difference between book cost (depreciation + interest) and tax-deductible cost (the lease fee).

---

## Version History
| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-22 | Initial — step-by-step from the validated BC method (Morre's live build + W-H-S walk, 2026-06-22). One-time setup, per-lease setup, monthly 4-step routine, mid-lease adoption, deferred tax, controls, glossary. ⚠ deferral push-back (D) still to be sandbox-tested. |
