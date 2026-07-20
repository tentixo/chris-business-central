# Sales with Subscription — Setup Guide

**Version**: 1.0
**Created**: 2026-07-20
**Author**: Tentixo AB
**Scope**: End-to-end setup of the **Sales with Subscription** pattern in Business Central — an item **sold once** *plus* a **recurring** charge billed through a subscription contract.
**Audience**: BC functional consultant or administrator (client delivery).
**Companions**: `subscription-billing-setup.md` (the *pure retainer* / Subscription Item pattern) · `ai/project-docs/bc-taxonomy-reference_v1.0.md` (the "Service means 4 things" + item-type/option rules).
**Provenance**: Built from a live, posted end-to-end run in the TXO sandbox (2026-07-20, verified with Morre).

---

## When to use this (vs the pure retainer)

BC has **two** recurring-billing shapes on the item card's **Subscription Option** field. Pick by whether there's a **one-off sale**:

| | **Subscription Item** *(see `subscription-billing-setup.md`)* | **Sales with Subscription** *(this guide)* |
|---|---|---|
| One-off invoice line? | **No** — pure recurring | **Yes** — the item bills once, *plus* recurring |
| Item Type allowed | **Non-Inventory only** | **Any** — Inventory, Non-Inventory, or Service |
| Recurring charge carried by | the item itself (via contract) | a separate **Non-Inventory "Invoicing Item"** (mandatory) |
| Typical use | retainer, membership, SaaS seat | hardware + support plan, installation + monthly, equipment + extended warranty |

> **Rule of thumb:** *"Sell something once and keep billing for it"* → **Sales with Subscription**. *"Only ever a recurring charge"* → **Subscription Item**.

> ⚠️ **Type constraint (verified):** the **Subscription Item** option is **only** selectable on a **Non-Inventory** item — selecting it on a Service/Inventory item throws *"The value 'Subscription Item' can only be set if the option 'Non-Inventory' is selected in the 'Type' field."* **Sales with Subscription** has **no** type restriction, which is why it's the path for physical goods and directly-sold services.

---

## The moving parts (build in this order)

1. **The sold item** — what the customer buys once (Service or Inventory).
2. **The Invoicing Item** — a Non-Inventory item that carries the *recurring* line (the sold item can't bill recurringly itself).
3. **The Subscription Package** — the recurring terms (rhythm, price %, billing via contract).
4. **Assignment** — wire the package onto the sold item.
5. **Sell → ship** — the sale creates the subscription.
6. **Contract → invoice** — the subscription is billed on a schedule.

---

## Step 1 — The sold item (Sales with Subscription)

`Alt+Q` → "Items" → **+ New**

| Field | Value |
|---|---|
| Description | e.g. `Onboarding Service` |
| **Type** | `Service` (or `Inventory` for a physical good) |
| Base Unit of Measure | `EA` |
| Gen. Prod. Posting Group | your service/goods category (e.g. `C-MAIN1`) |
| VAT Prod. Posting Group | `S-FULL` (or the correct VAT category) |
| **Unit Price** | the **one-off** price, e.g. `5000` — this bills on the sale |
| **Subscription Option** (Prices & Sales FastTab) | **`Sales with Subscription`** |

Save clean.

---

## Step 2 — The Invoicing Item (Non-Inventory)

This item carries the **recurring** billing line and its revenue posting. It is never put on a document directly — it only appears on the generated subscription invoice.

`Alt+Q` → "Items" → **+ New**

| Field | Value |
|---|---|
| Description | e.g. `Support Subscription (billing)` |
| **Type** | **`Non-Inventory`** *(required for the Invoicing Item option)* |
| Base Unit of Measure | `EA` |
| Gen. Prod. Posting Group | `C-MAIN1` (drives the recurring revenue account) |
| VAT Prod. Posting Group | `S-FULL` |
| Unit Price | `0` — the recurring amount comes from the package (Step 3) |
| **Subscription Option** | **`Invoicing Item`** |

> 💡 `Invoicing Item` is accepted here precisely because the item is **Non-Inventory** — the mirror of the constraint in Step 1.

---

## Step 3 — The Subscription Package (the recurring terms)

`Alt+Q` → "Subscription Packages" → **+ New**

- **Header**: `Code` (e.g. `SUB-1M`), `Description`.
- **Add one line**:

| Field | Value | Meaning |
|---|---|---|
| **Partner** | `Customer` | customer-side billing |
| **Invoicing via** | **`Subscription Contract`** | makes it a *billed* recurring line (vs `Sales` = info-only, e.g. a warranty) |
| **Invoicing Item No.** | your Invoicing Item (Step 2) | which item's posting groups carry the recurring revenue |
| **Calculation Base Type** | `Document Price` | derive the recurring amount from the sale line |
| **Calculation Base %** | `10` | recurring = 10% of the one-off (adjust as needed) |
| **Billing Base Period** | `1M` | the amount relates to one month |
| **Billing Rhythm** | `1M` | invoice monthly |

*(Leave Initial/Subsequent Term, Notice Period blank unless the contract needs a minimum term / cancellation logic.)*

> **Fixed price instead of %?** Set Calculation Base Type = `Item Price` and put the recurring price on the Invoicing Item (Step 2), or use a price list.

---

## Step 4 — Assign the package to the sold item

On the Subscription Package → **Assigned Items** → add the **sold item** (Step 1).
- Set it as **Standard** so the subscription line **auto-attaches** whenever the item is sold (no pop-up). Otherwise it's offered optionally on the sales line.

---

## Step 5 — Sell it (sales order)

`Alt+Q` → "Sales Orders" → **+ New** → Customer → line **Type = Item**, the **sold item**, Qty 1.

**What you'll see:**
- The line bills the **one-off** price (e.g. 5,000 + VAT).
- A **Subscription Lines** indicator shows **1** — the recurring line auto-attached (Standard package).
- **The recurring amount is *not* in the order total** — subscription lines bill separately through the contract.

> Click the **Subscription Lines** count to inspect the recurring line (amount, 1M rhythm, via the Invoicing Item) before posting.

---

## Step 6 — Post the shipment (subscription is born)

**Post → Ship** (or **Ship and Invoice**).
- **Ship** creates the **Subscription** (the recurring engine) from the delivered line.
- **Invoice** (if chosen) posts the **one-off** sale invoice; the subscription line is excluded from it.

**Check:** `Alt+Q` → **"Subscriptions"** — a new subscription now exists, referencing the customer and the sold item, with the recurring line inside it. Its **Subscription Contract No.** is still blank — that's Step 7.

---

## Step 7 — Put the subscription line in a Customer Subscription Contract

The subscription can't bill until its line sits in a contract.

1. `Alt+Q` → **"Customer Subscription Contracts"** → **+ New** → Customer.
2. Ribbon → **"Get Subscription Lines"** → select the customer's **unassigned** subscription line → confirm.
   - The line lands on the contract; back on the subscription, **Subscription Contract No.** now shows the contract.

> ⚠️ **Naming gotcha:** on the *Subscription* card, "**Assign Subscription Lines**" *adds lines from packages* — it does **not** attach to a contract. The line→contract link is made from the **contract** via **"Get Subscription Lines."**

---

## Step 8 — Bill the recurring charge

On the Customer Subscription Contract → **"Create Contract Invoice"** (set a *Billing to Date* covering the Next Billing Date if prompted).

**Result:** a **Sales Invoice** for the recurring amount (e.g. 500 + VAT), for the **billing period**, **posted through the Non-Inventory Invoicing Item** — not the sold item. Review and **Post**.

*(For many contracts at once, use a **Billing Template / Create Billing Proposal → Create Documents** instead of per-contract invoicing.)*

---

## Field notes (learned the hard way)

- **Subscription Item is Non-Inventory-only**; **Sales with Subscription** is the path for Service/Inventory items and anything sold-once-plus-recurring.
- **The Invoicing Item is mandatory** for Sales with Subscription — *"the item sold once cannot be used for billing recurringly."*
- **Recurring amounts never hit the sales-order/one-off invoice total** — they bill via the contract.
- **Subscriptions are created on *shipment*** (posting the delivery), not on order entry.
- **`Get Subscription Lines`** (on the contract) attaches the line; **`Assign Subscription Lines`** (on the subscription) does *not*.
- Verify ledgers with **Open in Excel** on Subscriptions / Customer Ledger Entries.

---

## The end-to-end shape (one line)

> **Sold item (Service/Inventory) + Sales with Subscription** → sold once → **Subscription created on shipment** → **Customer Subscription Contract** (`Get Subscription Lines`) → **Create Contract Invoice** → recurring invoice via the **Non-Inventory Invoicing Item**, on the billing rhythm.

---

*Tentixo AB — Business Central Advisory. Verified end-to-end in sandbox 2026-07-20. Companion to `subscription-billing-setup.md`; definitions in `ai/project-docs/bc-taxonomy-reference_v1.0.md`.*
