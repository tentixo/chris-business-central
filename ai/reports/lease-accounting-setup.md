# Finance Lease Accounting — Setup Guide

**Version**: 1.0
**Created**: 2026-06-22
**Author**: Tentixo AB
**Scope**: End-to-end setup of finance-lease accounting (IFRS 16 / FRS 102 / K3) in Business Central — right-of-use asset, lease liability, monthly interest/principal split, and deferred tax
**Audience**: BC functional user or administrator

---

## What this guide covers

Recording a finance lease in Business Central so the asset, the loan-like liability, and the monthly interest all live **on the Fixed Asset** — using only the standard FA module, **no add-on app**. By the end, you'll have:

- A right-of-use **fixed asset** that depreciates straight-line
- A **lease liability** that amortizes down each month
- A repeatable **monthly routine** that splits each lessor invoice into principal and interest
- The figures you need to post **deferred tax**

**Prerequisites**: Fixed Assets module available; the chart-of-accounts entries in Step 1; and, for each lease, the contract data below.

**Gather from each lease contract first**:

| You need | Why |
|---|---|
| Asset value (present value of the payments) | The amount you capitalize |
| Lease term in years | The depreciation period |
| Interest rate (OBR/IBR) | Splits each payment into interest vs principal. *If the contract states none, your advisor must supply a **rate (%)**.* |
| Monthly payment + its principal/interest split | The monthly posting amounts |

---

## Step 1 — Confirm the Chart of Accounts

**Open**: `Alt+Q` → "Chart of Accounts"

These accounts must exist before you start. Create any that are missing (+ New), following your company's CoA conventions.

| Account | Name (Swedish) | Name (English) | Role |
|---|---|---|---|
| 1260 | Leasade tillgångar | Leased assets | Right-of-use asset (gross value) |
| 1261 | Lease clearing | Lease clearing | Temporary transit account — **must be 0 at month-end** |
| 1267 | Ack. avskrivningar leasade | Accumulated depreciation, leased assets | Accumulated depreciation |
| 1268 | Ack. nedskrivningar leasade | Accumulated write-downs, leased assets | Accumulated write-down (only if impaired) |
| 2398 | Leasingskuld | Lease liability | Lease liability |
| 8421 | Räntekostnader, kreditinstitut | Interest expense, credit institutions | Interest expense |
| 78xx | Avskrivningar | Depreciation | Depreciation expense |
| 8940 / 1370 / 2240 | Uppskjuten skatt / Uppskjuten skattefordran / Uppskjuten skatteskuld | Deferred tax / Deferred tax asset / Deferred tax liability | Deferred tax |

**Why a clearing account (1261)?** Each lessor invoice is parked here, then moved onto the asset. It nets to zero every month — so a non-zero balance is an instant signal that a step was missed.

---

## Step 2 — Set up the Fixed Asset class and depreciation book

**Open**: `Alt+Q` → "FA Subclasses" → + New

| Field | Value | Notes |
|---|---|---|
| Code | `ROU-OFFICE` (and `ROU-CAR`) | One subclass per asset type |
| Description | "Right-of-use — office" | Appears on the FA card |
| FA Class Code | `TANGIBLE` | Leases are tangible (you can touch the office/car) |

**Open**: `Alt+Q` → "Depreciation Books" → + New (or reuse a dedicated lease book)

| Field | Value | Notes |
|---|---|---|
| Code | `LEASED-FA` | The lease accounting book |
| G/L Integration — all toggles | **On** | Postings hit the general ledger |
| Default Depreciation Method | **Straight-Line** | ROU assets depreciate evenly over the term |

---

## Step 3 — Configure the FA Posting Group (the critical step)

This is where principal and interest get their accounts — and where you stop them from corrupting the asset's value.

**Open**: `Alt+Q` → "FA Posting Groups" → + New (e.g. `LEASED`)

| Field | Value |
|---|---|
| Acquisition Cost Account | 1260 |
| Accum. Depreciation Account | 1267 |
| Write-Down Account | 1268 |
| Depreciation Expense Acc. | 78xx |
| **Custom 1 Account** | **2398** (principal lowers the liability) |
| **Custom 2 Account** | **8421** (interest) |

Then **Open**: `Alt+Q` → "FA Posting Type Setup" (or the **FA Posting Type Setup** action on the `LEASED-FA` depreciation book).

For **Custom 1** and **Custom 2**, set:

| Field | Value | Why |
|---|---|---|
| Part of Book Value | **No** | Principal/interest must **not** change the asset's value |
| Include in Depr. Calculation | **No** | …and must **not** affect depreciation |
| Depreciation Type | **No** | They're records, not depreciation |

**The FA Posting Types** (the buckets available on a fixed asset):

| Type | What we use it for |
|---|---|
| Acquisition Cost | The lease's opening value (Step 5) |
| Depreciation | Monthly straight-line write-down |
| Write-Down / Appreciation | Impairment / revaluation (rare) |
| **Custom 1** | **Principal** repayment → 2398 |
| **Custom 2** | **Interest** → 8421 |

**Why Custom 1 / Custom 2?** A finance lease has three natures — an asset, a loan, and an interest cost — but BC only depreciates the asset. By repurposing the two free "Custom" buckets (and switching off their effect on book value), the principal and interest get recorded **on the same fixed asset** for full traceability, without distorting the depreciation.

---

## Step 4 — Create the lease-clearing item

The lessor invoice arrives like any other and gets scanned by someone who doesn't know it's a lease. This item lets that happen — it simply moves the invoice amount to the clearing account.

**Open**: `Alt+Q` → "Items" → + New

| Field | Value | Notes |
|---|---|---|
| No. | `LEASE-CLEARING` | |
| Description | "Lease clearing" | |
| Type | **Service** (or Non-Inventory) | No stock — it only moves money |
| Gen. Prod. Posting Group | A group whose account is **1261** | Both purchase and sales post to 1261 |
| VAT Prod. Posting Group | A **no-VAT / 0%** group | Financial items carry no VAT |
| Unit Price | `0` | Amount is keyed on the invoice |

**Why an item, not a direct G/L line?** The accounts-payable scanner treats every invoice the same. A clearing item means no special handling at scan time — special-casing the scan would be an anti-pattern.

---

## Step 5 — Set up one lease and record its value

**Open**: `Alt+Q` → "Fixed Assets" → + New

| Field | Value |
|---|---|
| Description | The lease (e.g. "Leased office — London") |
| FA Subclass Code | `ROU-OFFICE` |
| Depreciation Book | `LEASED-FA` |
| Depreciation Starting Date | Lease start (e.g. `2026-01-01`) |
| No. of Depreciation Years | The lease term (e.g. `10`) |
| Depreciation Method | Straight-Line |

**Record the opening value (acquisition).** A lease has **no supplier invoice** for the full value — it comes from the contract — so post it manually:

**Open**: `Alt+Q` → "FA G/L Journals"

| Field | Value |
|---|---|
| FA Posting Type | **Acquisition Cost** |
| FA No. | Your new lease asset |
| Amount | The asset value, e.g. `328,700` |
| Bal. Account Type / No. | G/L Account / **2398** |

Click **Post**. Result: **Dr 1260 / Cr 2398** for the full value.

**Verify**: the FA card shows Book Value = 328,700; account 2398 shows the liability.

---

## Step 6 — The monthly cycle

After setup, this is the routine each month, per lease. Worked figures: payment `10,000` = principal `8,356` + interest `1,644`; depreciation `9,131`.

### 6a. Register the lessor invoice

**Open**: `Alt+Q` → "Purchase Invoices" → + New

| Field | Value |
|---|---|
| Vendor | The lessor |
| Line Type / No. | Item / `LEASE-CLEARING` |
| Quantity / Direct Unit Cost | 1 / `10,000` (the full payment, no VAT) |

**Post**. Result: **Dr 1261 (clearing) 10,000 / Cr Vendor 10,000**.

### 6b. Run depreciation

**Open**: `Alt+Q` → "Calculate Depreciation"

| Field | Value |
|---|---|
| Depreciation Book | `LEASED-FA` |
| FA Posting Date / Posting Date | Period end |

Run it, review the journal it creates, then **Post**. Result: **Dr 78xx 9,131 / Cr 1267 9,131**. *(This is the only step that changes the asset's value.)*

### 6c. Split the clearing balance onto the asset

**Open**: `Alt+Q` → "FA G/L Journals" — enter **two lines** on this lease's FA:

| Line | FA Posting Type | Amount | Bal. Account No. |
|---|---|---|---|
| 1 | **Custom 1** (principal) | `8,356` | 1261 |
| 2 | **Custom 2** (interest) | `1,644` | 1261 |

**Post**. Result: principal → **2398** (liability falls), interest → **8421**, and **1261 clears to 0**. All three movements now sit on the fixed asset's ledger.

### 6d. Deferred tax (at close)

The temporary difference is just two FA figures (interest cancels — it's deductible both ways):

```
Deferred-tax movement = (Depreciation − Principal) × tax rate
                      = (9,131 − 8,356) × 20.6%  =  775 × 20.6%  ≈  160
```

BC does **not** post this automatically. A Financial Report / Power BI reads `Depreciation − Custom 1 × rate`; a person posts one journal at close: **Dr 1370 / Cr 8940** (a deferred-tax asset early in the lease; it reverses later).

### ✅ Month-end check
**Account 1261 = 0.** Anything left there means a step was missed or an amount is wrong — fix it before closing.

---

## Step 7 — Starting a lease partway through the year

If the lease has been running but isn't yet in BC (e.g. live since January, you're setting up in June, Jan–May closed):

1. Do Steps 1–5, then **run Step 6 for each closed month** (January, February, …) exactly as normal.
2. Use **deferrals** to push the net effect into the **open month** (June) — the closed months stay untouched, but the full history is recorded.
3. From the open month onward, just continue the normal monthly cycle.

**Test this in a sandbox first** with the real numbers before doing it in production. Never force postings into closed periods.

---

## Monthly effort after setup

| Scenario | Steps | Time |
|---|---|---|
| One lease | Register invoice → Calculate Depreciation → split journal → check 1261 = 0 | ~3 minutes |
| Deferred tax | Read report figure → post one journal | At close only |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Can't pick Custom 1/2 on a purchase invoice | Purchase lines only allow Acquisition Cost / Maintenance | Use the clearing item (Step 4), then the FA G/L Journal (Step 6c) |
| Asset book value jumps when you post principal/interest | Custom 1/2 still count toward book value | Set Custom 1 & 2 → Part of Book Value = No, Include in Depr. Calc. = No (Step 3) |
| 1261 not zero at month-end | A step was skipped, or principal+interest ≠ invoice | Re-check Step 6c amounts against the invoice |
| Can't post a credit memo to a Custom line | Sign restriction on the posting type | Allow both debit and credit on Custom 1/2 |
| Deferred tax never reverses | Principal schedule doesn't match depreciation | Confirm the amortization convention (equal-principal vs annuity) from the contract |

---

## Architecture note

A finance lease is **one event with three natures**, and this setup keeps each in its proper place while linking all of them to the fixed asset:

- **Asset** — the right-of-use value, depreciated straight-line (the only thing that moves book value).
- **Financing** — the liability amortizes as principal (Custom 1 → 2398); interest (Custom 2 → 8421) is a cost. Recorded *on* the asset, but flagged not to affect its value.
- **Tax** — the timing gap between book cost (depreciation + interest) and the tax-deductible lease fee, carried as deferred tax.

Business Central has **no native lease engine** (the full "Asset leasing" module belongs to Dynamics 365 *Finance*, not BC) and **no deferred-tax engine** — but the standard Fixed Assets module, a clearing item, and a recurring journal carry the whole thing natively, with BC as the single source of truth. This is deliberately a vanilla-first design: no extension to license, maintain, or migrate.

---

*Tentixo AB — Business Central Advisory*
