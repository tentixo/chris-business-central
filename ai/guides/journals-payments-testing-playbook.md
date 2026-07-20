# Journals & Payments — Hands-On Testing Playbook

**Version**: 1.1 *(all Parts 1–5 complete & verified — Chris's solo run, Jul 2026)*
**Created**: 2026-07-15
**Updated**: 2026-07-20 — Parts 4 (unapply + reverse) & 5 (bank reconciliation) completed and written up with field notes; Sprint 3 → 🟢.
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

## Part 4 — Unapply + Reverse (the two "undo" mechanics)

Take the paid invoice from Part 2 and undo it — a realistic *"we paid the wrong one"* correction.

**4a — Unapply** (detach payment ↔ invoice): `Alt+Q` → "Vendor Ledger Entries" → select the **Payment** → **Process → Unapply Entries** → confirm. Both the invoice and payment flip back to **Open**.

**4b — Reverse** (mirror-post the payment out): on the now-**unapplied** payment → **Process → Reverse Transaction** → review the mirror lines (bank, AP, vendor ledger, bank ledger) → **Reverse**. A new reversal entry nets the payment to zero; the invoice stays Open/unpaid.

> ⚠️ **FIELD NOTES (first run):**
> - **You cannot Reverse an *applied* entry** — BC blocks it. **Unapply first**, and the unapply is a **posting step that must complete and re-open the invoice** before Reverse works. *(Reaching the Reverse preview screen proves nothing — the block is at the Reverse click.)*
> - **Reverse creates a NEW mirror entry** (e.g. a −1,250 counter-payment); the original **and** the reversal both stay in the ledger and close each other — that's the audit trail. Distinct from **Unapply** (just detaches), **Correct** (cancel + recreate a document), and **Credit Memo** (a new offsetting document). Four different "undo" tools.

## Part 5 — Bank Reconciliation (the checkpoint 🎯)

`Alt+Q` → **"Bank Account Reconciliations"** → **+ New** → Bank Account, Statement Date. The page has **Bank Statement Lines** (the bank's side) vs **Bank Account Ledger Entries** (BC's records).

1. **Bank → Suggest Lines** (optionally a date range) → BC creates statement lines from outstanding bank ledger entries and **auto-matches** them.
2. Set **Statement Ending Balance** so **Total Difference = 0**.
3. **Post** → the reconciliation becomes a **Bank Account Statement** (a posted record, with an **Undo** action).

> ⚠️ **FIELD NOTES (first run):**
> - On a **busy shared bank** (e.g. LCY-MAIN with a real backlog), a *fully-balanced* reconciliation needs the bank's **complete** statement. But BC will **post a *partial* reconciliation** — match just the entries on your statement (Total Difference 0), and the rest stays **outstanding** for future statements. That's a valid rec and enough to demonstrate the mechanic. *(A payment + its Part-4 reversal net to zero and match as a natural pair.)*
> - Two tools: **Bank Account Reconciliation** (statement ↔ ledger, this exercise) vs **Payment Reconciliation Journal** (imports a bank feed/CAMT and matches to *open* invoices — Masha's monthly method, `masha-bc-sessions.md §11`).
> - 🏢 Reconciling a shared bank in a Test company: **clear it with the owner first** (Morre OK'd LCY-MAIN here). For a fully-isolated clean rec, use a dedicated `CTEST-BANK` with only your own transactions.

---

## What "good" looks like — self-check

- [ ] Built a fictitious **vendor + customer** using **existing** posting groups.
- [ ] Posted a **purchase invoice** (open AP) and a **sales invoice** (open AR), VAT resolving cleanly.
- [ ] **Paid** the vendor (Payment Journal + **Apply**) → invoice **Open = No**.
- [ ] **Received** from the customer (Cash Receipt Journal + **Apply**) → invoice **Open = No**.
- [ ] Can **explain to Morre**: why **Apply / Set Applies-to ID** is essential; the **WHO × WHAT VAT matrix**; how to read **VAT Posting Setup** to diagnose a "blocked/missing" error.
- [ ] **Unapplied** a payment (re-opened the invoice), then **Reversed** it (mirror entry) — and can explain unapply vs reverse vs correct vs credit-memo.
- [ ] Posted a **bank reconciliation** (Suggest Lines → match → Post → Bank Account Statement); understand partial vs full reconciliation on a busy bank.

---

## When to pull in Morre (Anchor 2)
- **Incomplete VAT Posting Setup** (e.g. a `DOM` full-rate cell missing its Sales VAT Account) — his shared config; flag, don't silently "fix" in a live company.
- **Bank reconciliation setup** (bank account, statement import format) — do Part 5 with him / Masha.

---

*Tentixo AB — Business Central Advisory. First-run field notes from Chris's solo session, 2026-07-15.*
