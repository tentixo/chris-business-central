# BC Taxonomy Reference — "Service", Item Types & Subscription Billing

**Version**: 1.0
**Status**: Draft (one row pending a sandbox test — see §7)
**Purpose**: Single reference that de-conflicts the overloaded word **"Service"** in Business Central, pins down the three **Item Types**, and states the **Subscription Billing** item-type rules — grounded in Microsoft Learn, not intuition.
**Scope**: BC-product terminology (base app + Service Management). For the FGGE governance model, see `fgge-taxonomy-reference_v1.0.md`.
**Provenance**: Research + sandbox tests driven by **Lars Mårelius (Morre)** on 2026-07-16/17, cross-checked against Microsoft Learn (see §8). Prompted the correction of the subscription-item-type guidance in `subscription-billing-setup.md`, `bc-best-practice-playbook.md`, `project-billing-setup.md`.

---

## 1. Why this exists — "Service" means (at least) four things

The word **Service** collides across tables, modules, and licences. Most of the subscription-item-type confusion traces to this overload. Keep these strictly separate:

1. **`Item.Svc`** — an *Item* whose **Type = Service** (a labour/time unit).
2. **`Item.nInv`** — an *Item* whose **Type = Non-Inventory** (physical-but-untracked good).
3. **`SvcItem`** — a **Service Item** in the *Service Management* module (the customer's equipment you repair). *"Service items have nothing to do with regular or catalog items."* — MS Learn.
4. **Service Consumption / Service Contracts (`SvcSub`)** — recurring service agreements in Service Management (a *different* billing engine from Subscription Billing).

---

## 2. Notation (Morre's shorthand)

| Token | Means | BC object | Licence |
|---|---|---|---|
| **Item.Inv** | Item, Type = **Inventory** | Item (tbl 27) | Essential |
| **Item.nInv** | Item, Type = **Non-Inventory** | Item (tbl 27) | Essential |
| **Item.Svc** | Item, Type = **Service** | Item (tbl 27) | Essential |
| **SvcItem** | **Service Item** (customer equipment serviced) | Service Item (tbl 5940) | **Premium** |
| **SubBill** | **Subscription Billing** ("srb" module) | base app | Essential |
| **SvcSub** | **Service Contract** (recurring, Service Mgmt) | Service Contract | **Premium** |

---

## 3. The three Item Types (base app)

**Definitions** (MS Learn, *Understand item types*, verbatim):

| Type | Definition | Really is | Tracked (qty + value)? |
|---|---|---|---|
| **Item.Inv** | *"Physical things, such as bicycles, telephones, and desks… fully track item values and availability."* | physical + stocked | **Yes** |
| **Item.nInv** | *"Typically… physical things, such as bolts or pens, that your business consumes but doesn't fully track."* | **physical (Goods), untracked** | No |
| **Item.Svc** | *"A **labour time unit, such as a consultancy hour**, for limited business support."* | **non-physical (labour/time)** | No |

**Feature matrix** (load-bearing rows; `Yes`/`No` per MS Learn):

| Feature | Item.Inv | Item.nInv | Item.Svc |
|---|---|---|---|
| Sales / Purchasing | Yes | Yes | Yes |
| Job / Service Consumption | Yes | Yes | Yes |
| Assembly / Production **Consumption** | Yes | **Yes** | **No** |
| **Warehousing** (pick/ship) | **Yes** | **No** | **No** |
| **Planning** | **Yes** | **No** | **No** |
| Inventory Costing / Item Tracking / Reservation | Yes | No | No |
| Order Planning | Yes | Yes | Yes |

**Key takeaways:**
- **Warehousing + Planning are `Inventory`-only.** A physical good you want to stock, pick/ship, plan, or manufacture **must be `Item.Inv`**.
- `Item.nInv` and `Item.Svc` are both non-stocked; their only functional gap from each other is **Assembly/Production Consumption** (nInv yes, Svc no).
- Edge case: an `Item.Inv` *can* represent a non-physical thing (software licence, subscription) **if it carries identification numbers (serial no.)** — MS Learn.

---

## 4. SvcItem — a separate entity, not an Item Type

A **SvcItem** (Service Management) is a record for **a specific physical unit at the customer that you service/repair** (their printer, machine). It is **not** an Item and has **no Type of its own**.

- It **references** an Item via *Item No.* — and that link accepts **any Item type** (`Item.Inv`, `Item.nInv`, `Item.Svc`). *Empirically confirmed 2026-07-17.* So the underlying Type doesn't gate the SvcItem.
- BC can auto-create a SvcItem when you **post the shipment** of the sold item.
- **Why the "not our inventory" itch resolves here:** the sold unit left your stock, so BC gives it a *separate* record (SvcItem) rather than tracking it as your inventory. The `Item.Inv` remains *your product master* (stock ↓ on sale); the SvcItem tracks *the customer's unit*. Decoupled by design.

---

## 5. Subscription Billing (SubBill) — item-type rules by Subscription Option

The **Subscription Option** field (Item Card → *Prices and Sales* FastTab) governs behaviour and constrains the Item Type (MS Learn, *Subscription lines for items*):

| Subscription Option | Item Type allowed | Behaviour |
|---|---|---|
| **No Subscription** | any | Default. Ordinary sale, no subscription. |
| **Sales with Subscription** | **any — incl. `Item.Inv`** | Physical good sold once + recurring billing. *"a subscription is created automatically upon delivery."* Ships/picks/plans normally. |
| **Subscription Item** | **`Item.nInv` only** — *"You can select this option only if the item's Type is Non-Inventory."* | Pure recurring (retainer, membership). Delivered line auto-set to **Invoiced**; item/value ledger entries at **0** amount. |
| **Invoicing Item** | **`Item.nInv` only** | The recurring **billing line** for a *Sales with Subscription* item. Can't be used on document lines directly. |

**The semantic-vs-technical trap (this is the whole saga in one line):**
> A consulting retainer is *semantically* a **service** (`Item.Svc`), which is why Morre — reasonably — questioned "Non-Inventory". **But** BC's **Subscription Item** option is a *technical* constraint: it requires **`Item.nInv`**. So the correct type for a SubBill retainer is **`Item.nInv`**, even though it "feels" like `Item.Svc`. A true `Item.Svc` is for **directly-billed consultancy hours** (job/resource style), *not* subscription-contract billing.

**Physical-product subscription pattern** (e.g. hardware + service plan): `Item.Inv` product (sold once, ships/picks/plans normally) with **Sales with Subscription** → recurring charge carried by a separate `Item.nInv` **Invoicing Item**. Subscription auto-created on shipment; **Inventory Pick** supported (start date from posting/shipment date).

---

## 6. Two recurring-billing engines — don't cross them

| | **SubBill** (Subscription Billing) | **SvcSub** (Service Contracts) |
|---|---|---|
| Module | `srb`, base app | Service Management |
| Licence | Essential | **Premium** |
| Bills against | `Item.nInv` Subscription/Invoicing Items | **SvcItems** (customer equipment) |
| Use case | Retainers, memberships, hardware-as-a-service | Maintenance/warranty agreements on serviced equipment |

Tinky's retainer = **SubBill**. Nothing to do with SvcItems or SvcSub.

---

## 7. Open questions / pending sandbox tests

| # | Question | MS Learn prediction | Status |
|---|---|---|---|
| 1 | Is **`Item.Svc` → Subscription Option = "Subscription Item"** selectable? | **Blocked** (Subscription Item = `Item.nInv` only) | ⏳ **PENDING** — test with Chris |
| 2 | Confirm **`Item.Inv` → Sales with Subscription** works end-to-end (ship → subscription created) | Allowed | ⏳ pending |

> When Test #1 resolves: if **blocked** → the three how-to docs revert to **`Item.nInv`** for the retainer (the original was right; the "Service or Non-Inventory" fix over-corrected). If **allowed** → document "nInv (Svc also accepted in this build)."

---

## 8. Sources

- [Understand item types — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/inventory-about-item-types)
- [Subscription lines for items — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/srb/masterdata/items)
- [Sales with subscription lines — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/srb/sales/sales-service-commitments)
- [Welcome to subscription billing — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/srb/welcome)

---

*Tentixo AB — Business Central Advisory. Companion to `fgge-taxonomy-reference_v1.0.md`; feeds the how-to guides in `ai/guides/` and the best-practice playbook.*
