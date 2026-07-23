# Purchasing & AP — Hands-On Testing Playbook

**Version**: 1.0 *(all Parts 1–4 complete & verified — Chris's solo run, 2026-07-23)*
**Created**: 2026-07-23
**Type**: Sandbox exercise sheet (do-it-yourself). Companions: `journals-payments-testing-playbook.md`, `fixed-assets-testing-playbook.md`, `dimensions-testing-playbook.md`, study schedule **Sprint 4**.
**Goal**: go from "seen it" → "done it" on **Purchasing & AP** (MB-800 **D2/D3/D4**). Run the full **procure-to-pay** cycle through a *Purchase Order* (not a direct invoice), then layer on **purchase pricing**, **receipt corrections**, and **blanket orders**.

> **Reading convention — three voices:**
> - **Numbered steps = the standard Microsoft way** (what MB-800 tests).
> - 🏢 **TENTIXO PRACTICE** = how Morre's sandbox is wired (real posting codes).
> - ⚠️ **FIELD NOTES** = what actually bit on the first run (2026-07-23). These are the time-savers.
>
> **Core idea:** a **Purchase Order is a two-step document** — **Receive** (goods/service arrive) and **Invoice** (the bill) post *separately*, tracked by **Qty. to Receive** vs **Qty. to Invoice**. A direct Purchase Invoice (Sprint 3) can't do that split; the PO is where P2P lives.

---

## ⚑ Before you start — don't disrupt the shared sandbox
- **Prefix everything `CTEST-`**. Reuse the fictitious vendor **Ctest Cleaning Co** built in Sprint 3 (Gen. Bus. = `EXT`, VAT Bus. = `DOM`, its own payables group).
- **Reuse existing, complete posting groups; don't invent codes** (new codes reopen "missing setup" holes).
- Note the **company** (`TXO` / Test Txo NG AB).

---

## What you'll learn (and the MB-800 boxes it ticks)

| Part | Step | MB-800 domain |
|---|---|---|
| 1 | PO → **Receive** → **Invoice** → **Pay**, traced to the G/L | D4 — *process purchases / payments* |
| 2 | **Purchase Price List** (special price + line discount) | D3 — *purchase pricing & discounts* |
| 3 | **Partial receipt** + **Undo Receipt** | D4 — *corrections / reversals* |
| 4 | **Blanket Purchase Order** → Make Order call-off | D4 — *framework agreements* |

---

## Part 1 — The full procure-to-pay cycle (PO → Receive → Invoice → Pay)

The backbone of Sprint 4 and the part the exam leans on hardest. We use a **G/L-account line** (clean, AP-focused, no inventory).

### 1a. Create the Purchase Order
`Alt+Q` → **"Purchase Orders"** → **+ New** → **Vendor = `Ctest Cleaning Co`**.
Line: **Type = G/L Account**, **No. = `5061`** (Cleaning), **Quantity = `10`**, **Direct Unit Cost Excl. VAT = `100`** → Line Amount 1,000, Total incl. VAT **1,250**.

> ⚠️ **FIELD NOTE — Vendor Invoice No.** BC asks for it before you can post the **Invoice** step (not the receipt). It enforces **uniqueness per vendor** — a real AP control so you can't pay the same vendor invoice twice. Enter e.g. `CTEST-INV-001`.
>
> ⚠️ **FIELD NOTE — "Purch. Account is missing in General Posting Setup"** notification: **harmless for a G/L-account line** (BC posts straight to the account you named, 5061). It **only bites for an Item line**, where BC must derive the account from the posting setup. Flag to Morre: the `EXT × [5061's Gen. Prod. group]` cell has no default Purch. Account in this sandbox.

### 1b. Receive (post the receipt only)
**Post…** → in the dialog choose **● Receive** → OK.

- The PO stays **open**. Scroll the line right: **Quantity Received = 10**, **Qty. to Receive = 0**, but **Qty. to Invoice still 10**, **Quantity Invoiced = 0**. That split = *received but not invoiced* (GRNI).
- A **Posted Purchase Receipt** document is created (`Alt+Q` → "Posted Purchase Receipts").

> ⚠️ **FIELD NOTE — nothing hits the G/L on a G/L-line receipt.** The receipt only records *quantity received*. (An **Inventory item** would post an interim accrual — "received, not invoiced" — here; that's the **Sprint 5** nuance.)

### 1c. Invoice (post the bill)
**Post…** → **● Invoice** → OK. Posts cleanly (the Vendor Invoice No. satisfies the control). Open **Posted Purchase Invoices** → the new doc → **Related G/L Entries**:

| G/L Account | Name | Amount | Dr/Cr |
|---|---|---|---|
| **5061** | Cleaning | +1 000 | Dr (expense) |
| **2641** | Input VAT debited | +250 | Dr (recoverable VAT) |
| **2441** | Accounts payable | −1 250 | Cr (you owe the vendor) |

Debits 1,250 = Credit 1,250. Once fully received **and** invoiced, BC **auto-deletes the PO** from the open list — history lives in the posted receipt + posted invoice.

### 1d. Pay (payment journal → apply → close)
`Alt+Q` → **"Payment Journal"** → batch **`LCY-MAIN`** (pre-wired to bank 1931).
Line: **Account Type = Vendor**, **Account No. = `Ctest Cleaning Co`** → **Process → Apply Entries** → select the invoice → **Set Applies-to ID** → OK (the load-bearing step) → **Amount** populates **1,250**, **Bal. Account = Bank LCY-MAIN** → **Post**.

**Verify:** `Alt+Q` → "Vendor Ledger Entries" → the invoice (−1,250) and payment (1,250) both show **Remaining Amount 0.00** = closed.

```
PO (B-PO00001) → Receive → Invoice (B-P000009) → Pay → AP closed
     ↓              ↓            ↓                   ↓
  order doc     receipt doc   Dr 5061/2641         Cr bank 1931
                (no G/L)      Cr 2441 AP           invoice closed
```

---

## Part 2 — Purchase Pricing & Discounts

Pre-agree a vendor's **prices** and **discounts** once; BC auto-fills them on every PO line.

> **Key concept:** purchase pricing is **item-based** (Item × Vendor). A **G/L-account line has no price** — which is why the Part 1 PO needed a manual cost.

### 2a. Create a purchasing item
`Alt+Q` → **"Items"** → **+ New**. (No item template wired in this sandbox → set posting fields by hand.)
- **Type = `Non-Inventory`** (keeps inventory posting groups out of scope — Sprint 5)
- **Description = `CTEST Cleaning Supplies`**, **Direct Unit Cost = `100`**
- **Gen. Prod. Posting Group = `G-MERCH`** (Goods, Merchandise — the honest fit for physical *supplies*)
- **VAT Prod. Posting Group** auto-fills **`G-FULL`** (from G-MERCH's *Def. VAT Prod. Posting Group* + *Auto Insert Default*)
- **Purchasing / Vendor No. = `Ctest Cleaning Co`**

> 🏢 **TENTIXO PRACTICE — VAT is semantic, not a rate.** `G-FULL` = **goods**, `S-FULL` = **services** — both 25% full-rate, but the split records *intent* (goods vs service). Cleaning *supplies* = goods = **G-FULL**; cleaning *labour* (account 5061) = service = **S-FULL**. ("Correctness based on intent.")
>
> ⚠️ **FIELD NOTE — the posting group must actually *commit*.** Picking `G-MERCH` in the lookup can leave the field visually set but **unsaved**. The moment you drop the item on a purchase line BC errors: *"Gen. Prod. Posting Group must have a value in Item: No.=B-ITM00005. It cannot be zero or empty."* Fix: reopen the item card, re-set G-MERCH, confirm it **sticks** before retrying.

### 2b. Build the Purchase Price List
`Alt+Q` → **"Purchase Price Lists"** → **+ New**. Header: **Description** meaningful, **Assign-to Type = Vendor**, **Assign-to No. = `Ctest Cleaning Co`**. Leave **Status = Draft** while editing.

Two lines (same item, different **Defines**):

| Product No. | Minimum Qty | **Defines** (Amount Type) | Direct Unit Cost | Line Discount % |
|---|---|---|---|---|
| `B-ITM00005` | **10** | **Price** | **90** | — |
| `B-ITM00005` | **5** | **Discount** | — | **10** |

Then set **Status → Active**.

> ⚠️ **FIELD NOTE — "Defines" (= Amount Type) scopes each line.** Left at the default **"Price & Discount"**, the discount line *also* declared a **price of 0** → on a qty 5–9 PO it would hand you the item **free**, and fight the real price line at qty 10. Set each line to **one** purpose: the Price line only overrides cost; the Discount line only sets the %. Set `Price` → discount column greys out; set `Discount` → the dangerous 0-cost greys out.
>
> ⚠️ **FIELD NOTE — Status must be Active.** Draft price lists are invisible to documents.
>
> ⚠️ **FIELD NOTE — `Allow Line Disc.` gates stacking.** If a discount ever *doesn't* apply while the price does, check the winning **Price** line's **Allow Line Disc.** flag — it must permit line discounts for the % to stack. (On our run it stacked fine even unticked, but this is the first thing to check.)

### 2c. Test on a PO
New PO → Ctest Cleaning Co → line **Type = Item**, **No. = `B-ITM00005`**, **Quantity = `10`**:
- **Direct Unit Cost → 90** (Price line, qty ≥10 ✅)
- **Line Discount % → 10** (Discount line, qty ≥5 ✅)
- **Line Amount → 810** (900 − 10%)

**Tiers:** qty 3 → no price/no disc (100, 0%); qty 5–9 → 100 + 10%; qty 10+ → 90 + 10%.
*(Don't post — an item line would hit the missing-Purch.-Account gap. Pricing auto-fill is the whole lesson.)*

---

## Part 3 — Corrections (partial receipt + Undo Receipt)

Uses a **G/L-account line** again (only receiving, not invoicing → no posting-group gap).

### 3a. Partial receipt
New PO → Ctest Cleaning Co → **G/L 5061**, **Quantity 10**, cost 100. On the line set **Qty. to Receive = `4`** (only 4 of 10 turned up) → **Post… → Receive**.

Result — the order **stays open**: **Quantity Received = 4**, **Qty. to Receive = 6** (the outstanding balance), **Quantity = 10** unchanged. A partial receipt keeps the order alive for the remainder.

### 3b. Undo Receipt (the *proper* reversal)
You **can't delete** a posted receipt. `Alt+Q` → **"Posted Purchase Receipts"** → open the newest → select the line → **Lines → Functions → Undo Receipt** → confirm.

- **On the receipt:** now **two lines** — the original **4** *plus* a corrective **−4**, both flagged **Correction**. History preserved, nothing erased.
- **Back on the PO:** **Quantity Received → 0**, **Qty. to Receive → 10** again — ready to re-receive correctly.

> ⚠️ **FIELD NOTE — BC reverses by *adding a reversing entry*, never by erasing.** Same **RIM-vs-Crafted / audit-trail** principle as dimension correction and Sprint 3's Reverse Transaction.

---

## Part 4 — Blanket Purchase Order (framework → call-off)

A **Blanket PO** is a *framework agreement*: commit to a total quantity, then **call off** chunks as real POs when needed. The blanket itself never posts — it's the umbrella; child POs do the work.

### 4a. Create + call off
`Alt+Q` → **"Blanket Purchase Orders"** → **+ New** → **Vendor = `Ctest Cleaning Co`**.
Line: **Type = G/L Account**, **No. = `5061`**, **Quantity = `100`** (total commitment), **Direct Unit Cost = `100`** → Line Amount 10,000.
On the line set **Qty. to Receive = `20`** (call off 20 now) → **Home → Make Order** → confirm.

Result:
- BC creates a **new Purchase Order** (next B-PO number) for the **20** — a normal PO you'd run through the Part 1 cycle. Its line carries a **Blanket Order No.** back-reference.
- The **blanket order (B-PB00001) stays open** and tracks usage against the 100. Call off another 20 later → another child PO; the blanket keeps the running tally.

> ⚠️ **FIELD NOTE** — the "Purch. Account is missing" banner shows as a hard error on the blanket header but is **harmless**: Make Order doesn't post, and the child PO's G/L line (5061) posts fine.

---

## First-run summary (2026-07-23)

| Part | Objects created | Outcome |
|---|---|---|
| 1 P2P cycle | PO **B-PO00001**, receipt, invoice **B-P000009**, payment | AP 1,250 posted (5061/2641/2441) → paid → **closed** ✅ |
| 2 Pricing | Item **B-ITM00005**, price list **B-PL00003** | qty-10 PO auto-filled **90 + 10% = 810** ✅ |
| 3 Corrections | PO **B-PO00003** | partial receipt (4/6) → **Undo Receipt** (−4 correction) → back to 0/10 ✅ |
| 4 Blanket | Blanket **B-PB00001** | Make Order → child PO for 20; blanket stays open ✅ |

**Domains covered:** D4 process purchases (PO lifecycle, receive/invoice split, corrections, blanket), D4 payments (apply/close), D3 purchase pricing & discounts.
**Deferred to Sprint 5 (Inventory):** the receive-accrual (interim "received not invoiced" G/L posting) that only fires on **Inventory** item lines, and the missing-Purch.-Account setup gap that blocks item-line posting.
