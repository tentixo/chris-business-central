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

The **Subscription Option** field (Item Card → *Prices and Sales* FastTab) governs behaviour and constrains the Item Type (MS Learn, *Subscription lines for items*).

**Two clarifications that dissolve most confusion:**
- **"Subscription Item" is a *role*, not a fourth Type.** *Type* (Inv/nInv/Svc) and *Subscription Option* are two independent Item-card fields. A "Subscription Item" = a **Non-Inventory** item whose Subscription Option = Subscription Item.
- **A subscription line ≠ a normal line.** A subscription line is a **recurring** obligation (fields: Billing Rhythm, Billing Base Period, Calculation Base %, Initial/Subsequent Term, Notice Period), billed **only via a Contract** — *never on the sales invoice*, and created automatically when the item is **delivered** (shipment posting). A normal line bills once, on the invoice.


| Subscription Option | Item Type allowed | Behaviour |
|---|---|---|
| **No Subscription** | any | Default. Ordinary sale, no subscription. |
| **Sales with Subscription** | **any — incl. `Item.Inv`** | Physical good sold once + recurring billing. *"a subscription is created automatically upon delivery."* Ships/picks/plans normally. |
| **Subscription Item** | **`Item.nInv` only** — *"You can select this option only if the item's Type is Non-Inventory."* | Pure recurring (retainer, membership). Delivered line auto-set to **Invoiced**; item/value ledger entries at **0** amount. |
| **Invoicing Item** | **`Item.nInv` only** | The recurring **billing line** for a *Sales with Subscription* item. Can't be used on document lines directly. |

**The semantic-vs-technical trap (this is the whole saga in one line):**
> A consulting retainer is *semantically* a **service** (`Item.Svc`), which is why Morre — reasonably — questioned "Non-Inventory". **But** BC's **Subscription Item** option is a *technical* constraint: it requires **`Item.nInv`**. So the correct type for a SubBill retainer is **`Item.nInv`**, even though it "feels" like `Item.Svc`. A true `Item.Svc` is for **directly-billed consultancy hours** (job/resource style), *not* subscription-contract billing.

**Physical-product subscription pattern** (e.g. hardware + service plan): `Item.Inv` product (sold once, ships/picks/plans normally) with **Sales with Subscription** → recurring charge carried by a separate `Item.nInv` **Invoicing Item**. Subscription auto-created on shipment; **Inventory Pick** supported (start date from posting/shipment date).

### 5.1 Worked example — a *Service* item billing recurringly, end-to-end (verified live 2026-07-20)

Proves `Item.Svc` **can** drive subscription revenue via **Sales with Subscription** (never as a standalone Subscription Item):

1. **`Item.Svc`** `CTEST-SVC-SUBTEST` (Type = Service), Subscription Option = **Sales with Subscription** (*Subscription Item* was validation-blocked), Unit Price 5,000.
2. **`Item.nInv` Invoicing Item** `CTEST-INVITEM` (Subscription Option = **Invoicing Item** — *accepted*, the mirror of the Service block). Carries the recurring billing line.
3. **Subscription Package** `CTEST-SUB-1M`: Partner = Customer, Invoicing via = **Subscription Contract**, Invoicing Item = CTEST-INVITEM, Calc Base = **Document Price 10%**, Billing Rhythm **1M**. Assigned to the Service item as **Standard**.
4. **Sales order** → Service item: bills the **one-off 5,000** *and* auto-attaches the subscription line (Subscription Lines = 1; the recurring amount is **excluded** from the order total). **Ship & Invoice** → one-off invoice **6,250** *and* **Subscription B-SUB00002** created on shipment.
5. **Customer Subscription Contract B-SCC00002** → **Get Subscription Lines** pulls the unassigned line in → **Create Contract Invoice** → recurring invoice **B-SX000007 = 500 + VAT (625)**, monthly, **posted via CTEST-INVITEM** (the Non-Inv item, *not* the Service item).

**Takeaway:** the recurring charge always bills through the **Non-Inventory Invoicing Item**; the Service item is the *sold-once* line that *spawns* the subscription. Contrast with a pure retainer (`Item.nInv` + Subscription Item, e.g. B-SUB00001), which has no one-off and bills the item directly via contract.

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

| # | Question | Result | Status |
|---|---|---|---|
| 1 | Is **`Item.Svc` → Subscription Option = "Subscription Item"** selectable? | **BLOCKED** — Subscription Item is offered *only* for `Item.nInv`. `Item.Svc` and `Item.Inv` can pick **Sales with Subscription** but **not** Subscription Item. | ✅ **RESOLVED 2026-07-17** (matches MS Learn) |
| 2 | Does **Sales with Subscription** drive recurring billing end-to-end (incl. from a `Item.Svc`)? | **YES — proven live 2026-07-20** with a *Service* item: sold once → Subscription **B-SUB00002** born on shipment → Contract **B-SCC00002** → recurring invoice **B-SX000007** (500 + VAT), **posted**. | ✅ **RESOLVED** (see worked example §5.1) |

**Resolution:** Subscription Item = **`Item.nInv` only** (confirmed). The "Service or Non-Inventory" wording (added 2026-07-16 after Morre's semantic challenge) **over-corrected** — the *original* `Item.nInv` was right. How-to docs reverted 2026-07-17.

**Verbatim BC error** (selecting `Subscription Item` on a `Service` item, 2026-07-20): *"The value 'Subscription Item' can only be set if the option 'Non-Inventory' is selected in the 'Type' field."* — the validation rule surfaced directly (no AL source needed). The Subscription Option enum *lists* all four values, but the Type constraint is enforced **on selection**, not by hiding options.

---

## 8. Sources

- [Understand item types — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/inventory-about-item-types)
- [Subscription lines for items — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/srb/masterdata/items)
- [Sales with subscription lines — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/srb/sales/sales-service-commitments)
- [Welcome to subscription billing — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/srb/welcome)

---

*Tentixo AB — Business Central Advisory. Companion to `fgge-taxonomy-reference_v1.0.md`; feeds the how-to guides in `ai/guides/` and the best-practice playbook.*
