# Journals & Payments — Hands-On Testing Playbook

**Version**: 1.0 *(Parts 1–3 complete from Chris's first run; Parts 4–5 land next session)*
**Created**: 2026-07-15
**Type**: Sandbox exercise sheet (do-it-yourself). Companions: `fixed-assets-testing-playbook.md`, `dimensions-testing-playbook.md`, study schedule **Sprint 3**.
**Goal**: go from "seen it" → "done it" on **Journals & Payments** — MB-800's **heaviest domain (D4, 30–35%)**. Build the **payment → apply → close** cycle on *both* the AP and AR sides, then (next) **reverse** and **bank reconciliation**.

> **Reading convention — three voices:**
> - **Numbered steps = the standard Microsoft way** (what MB-800 tests).
> - 🏢 **TENTIXO PRACTICE** = how Morre's sandbox is wired (batch-per-bank, real posting codes).
> - ⚠️ **FIELD NOTES** = what actually bit on the first run (2026-07-15). These are the time-savers.
>
> **Core idea:** posting happens in **only two ways — a journal or a document** (invoice). Everything here is one of those two, and the magic that closes an invoice is **Apply** (linking a payment to the invoice it pays).

---

## ⚑ Before you start — don't disrupt the shared sandbox
- **Prefix everything `CTEST-`**. Build your own fictitious **vendor + customer** to pay/receive against — **never apply a payment to a *real* open invoice** (you'd mark someone's live AP/AR as paid).
- **Never post into a journal batch that already holds lines** (the `BANK` gen-journal batch held the live lease entries). Use an **empty** batch.
- Note the **company**.

---

## What you'll learn (and the MB-800 boxes it ticks)

| Step | MB-800 domain |
|---|---|
| Set up a vendor & a customer (posting groups, terms) | D2/D3 — *master data* (pulled forward from Sprint 4) |
| Post purchase & sales invoices | D4 — *process purchases / sales* |
| Payment Journal → **apply** → close AP | D4 — *process journals & payments* |
| Cash Receipt Journal → **apply** → close AR | D4 — *payment registration / apply entries* |
| Reverse & unapply *(Part 4, next)* | D4 |
| **Bank reconciliation** *(Part 5, next — the checkpoint)* | D4 |

---

## Part 1 — Stage the master data + open entries

You need an **open AP** entry to pay and an **open AR** entry to receive. Build the counterparties from scratch (great D2/D3 training) — but the trick is to **reuse existing, complete posting groups; don't invent new codes** (new codes reopen "missing setup" holes).

### 1a. Fictitious vendor
`Alt+Q` → "Vendors" → **+ New** → Name `Ctest Cleaning Co`. **Invoicing** FastTab (the load-bearing three): **Gen. Bus. Posting Group** = `EXT`, **VAT Bus. Posting Group** = the matching domestic one, **Vendor Posting Group** = an existing payables group (~2465). **Payments**: Payment Terms (`30 DAYS`), Payment Method.

### 1b. Purchase invoice → open AP
`Alt+Q` → "Purchase Invoices" → **+ New** → Vendor = `Ctest Cleaning Co`, **Vendor Invoice No.** = `CTEST-PINV-01` (required). Line: **Type = G/L Account**, an expense account (`5061`), Amount 1,000. **Post** → open Vendor Ledger Entry of 1,250 (incl. 25% VAT).

> ⚠️ **FIELD NOTE:** *"Purch. Account is missing in General Posting Setup"* is a **warning, not a blocker** for a **direct G/L-account line** — the account is explicit, so it posts. (It only *blocks* for **Item** lines, where BC derives the account from the posting setup.) Post through it.

### 1c. Fictitious customer
`Alt+Q` → "Customers" → **+ New** → Name `Ctest Customer AB`. **Invoicing** FastTab: **Gen. Bus. Posting Group** = `EXT`, **VAT Bus. Posting Group** = `DOM`, **Customer Posting Group** = existing receivables (~1511). **Payments**: terms + method.

### 1d. Sales invoice → open AR *(the VAT gauntlet)*
`Alt+Q` → "Sales Invoices" → **+ New** → Customer = `Ctest Customer AB`. Line: **Type = G/L Account**, a **revenue** account, Amount 1,000. Aim for **Total VAT = 250** → **Post** → open Customer Ledger Entry of 1,250.

> ⚠️ **FIELD NOTES — sales VAT (this is where the first run lost an hour):**
> - **Sales posting strictly enforces VAT Posting Setup** (`Sales-Post.CheckBlockedPostingGroups`). Both VAT groups must resolve to a **complete, unblocked** cell.
> - **VAT Prod. Posting Group is NOT on the customer** — it's on the **WHAT** (the item/G/L account). Morre's **WHO × WHAT matrix**: customer gives **Gen. Bus. + VAT Bus.**; the account gives **Gen. Prod. + VAT Prod.**; BC crosses them for the accounts + VAT rate.
> - **A G/L account with no default VAT Prod → the line is blank → (VAT Bus × blank) is a deliberately Blocked cell** → *"Setup is blocked in VAT Posting Setup for … DOM and … [blank]."* This was the root cause of the whole saga.
> - **Fix:** give the line a VAT Prod. Posting Group. Either (a) set it on the account card (e.g. `S-FULL` on a 31xx services account — the *correct* default), or (b) show the column via **Personalize** and set `S-FULL` on the line.
> - **Personalize gotcha:** the *"Add Field to Page"* list is scoped to the **focused page-part** — searching "VAT Prod" from the header shows *nothing*; **click into the Lines grid first**, then add the field.
> - **Diagnose with the matrix:** `Alt+Q` → **"VAT Posting Setup"** (export to Excel). It lists **VAT Bus × VAT Prod → Blocked? / VAT % / Sales VAT Account**. Here **DOM × S-FULL = 25%, Sales VAT Acct 2611, not blocked** ✅; **DOM × blank = Blocked**. Reading this *is* the D2 skill.
> - *"Sales VAT Account is missing"* = that matrix cell has a rate but no VAT G/L account. **VAT = 0 is fine and postable** (a valid 0-rate cell).

---

## Part 2 — Payment Journal → apply → close the AP

1. `Alt+Q` → **"Payment Journals"** → batch **`LCY-MAIN`**.
2. Line: **Posting Date** = today, **Document Type** = **Payment**, **Account Type** = **Vendor**, **Account No.** = `Ctest Cleaning Co`.
3. **Apply** → **Apply Entries** → tick the open invoice → **Set Applies-to ID** → the **Amount auto-fills (+1,250)**.
4. **Balance = 0** → **Post.**

**Expected**: G/L **Dr [AP ~2465] 1,250 / Cr [Bank] 1,250**; the invoice's Vendor Ledger Entry → **Open = No, Remaining 0**.

> 🏢 **TENTIXO PRACTICE:** the **`LCY-MAIN` batch pre-wires the main SEK bank as the Bal. Account** — Morre runs **one payment-journal batch per bank account**, so you pick the *batch*, not the account.
> ⚠️ **FIELD NOTES:** **Apply = `Set Applies-to ID`** is the load-bearing step — skip it and you post a *floating* payment that leaves **both** the invoice and payment open (a mess Masha then has to clean up). Sign: **+Amount debits the vendor** (clears the payable), bank is credited. Verify via **"Open in Excel"** on Vendor Ledger Entries (**Open = No** = closed) — that's the D4 *data-analysis* skill for free.

---

## Part 3 — Cash Receipt Journal → apply → close the AR *(mirror of Part 2)*

1. `Alt+Q` → **"Cash Receipt Journals"** → an empty batch.
2. Line: **Document Type** = **Payment**, **Account Type** = **Customer** *(set this first!)*, **Account No.** = `Ctest Customer AB`, **Bal. Account Type** = Bank Account, **Bal. Account No.** = `LCY-MAIN`.
3. **Apply Entries** → tick the open sales invoice → **Set Applies-to ID** → **Amount fills (−1,250)**.
4. **Balance = 0** → **Post.**

**Expected**: G/L **Dr [Bank] 1,250 / Cr [AR ~1511] 1,250**; the sales invoice → **Open = No, Remaining 0**.

> ⚠️ **FIELD NOTES:** **Account Type drives the Account No. lookup** — if the No. field shows the **Chart of Accounts**, your Account Type is still `G/L Account`; set it to **Customer** first. Also: the **`BANK` batch does *not* pre-fill the Bal. Account** (unlike `LCY-MAIN`) — set the bank manually, or use an `LCY-MAIN` receipt batch.

---

## Part 4 — Apply / unapply + Reverse *(next session)*

- **Unapply**: on a closed entry, *Unapply* to re-open it (the corrective inverse of Apply).
- **Reverse**: on a posted G/L/ledger entry, **Reverse Transaction** creates a mirror-image posting (vs *correcting* a document). Understand reverse-vs-correct-vs-credit-memo.

## Part 5 — Bank Reconciliation *(next session — the checkpoint 🎯)*

Reconcile the bank account against a statement: import/enter statement lines, **match** them to the payment (Part 2) + receipt (Part 3), resolve differences, **Post** the reconciliation. This is the Sprint 3 checkpoint deliverable. *(Ties to Masha's bank-XML method — `masha-bc-sessions.md §11`.)*

---

## What "good" looks like — self-check

- [ ] Built a fictitious **vendor + customer** using **existing** posting groups.
- [ ] Posted a **purchase invoice** (open AP) and a **sales invoice** (open AR), VAT resolving cleanly.
- [ ] **Paid** the vendor (Payment Journal + **Apply**) → invoice **Open = No**.
- [ ] **Received** from the customer (Cash Receipt Journal + **Apply**) → invoice **Open = No**.
- [ ] Can **explain to Morre**: why **Apply / Set Applies-to ID** is essential; the **WHO × WHAT VAT matrix**; how to read **VAT Posting Setup** to diagnose a "blocked/missing" error.
- [ ] *(Pending Part 4–5)* reversed an entry; posted a **bank reconciliation**.

---

## When to pull in Morre (Anchor 2)
- **Incomplete VAT Posting Setup** (e.g. a `DOM` full-rate cell missing its Sales VAT Account) — his shared config; flag, don't silently "fix" in a live company.
- **Bank reconciliation setup** (bank account, statement import format) — do Part 5 with him / Masha.

---

*Tentixo AB — Business Central Advisory. First-run field notes from Chris's solo session, 2026-07-15.*
