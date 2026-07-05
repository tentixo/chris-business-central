# Research — IC Item Mapping · Item Best-Practice · Lease Valuation (no stated value/rate)

**Branch**: `ifrs-16-research`
**Date**: 2026-06-24
**Source**: Call with Lars Mårelius (Morre), 2026-06-24 (7 min) — `docs/Call with Lars Mårelius (13).docx`
**Type**: Research note (informative). **Does NOT make the held decisions** — the CoA-number discrepancy and the IC Items-vs-G/L direction are still for the Chris ↔ Morre sit-down. This note gives Morre the background he asked for on three topics.
**Companions**: [`ic-postings-issues-meeting_v1.0.md`](ic-postings-issues-meeting_v1.0.md) (Topics A/B), [`ifrs-16-uk-frs102-bc-implementation_v1.0.md`](ifrs-16-uk-frs102-bc-implementation_v1.0.md) (Topic C).

---

## The three asks (verbatim intent)

1. **IC item-number mapping** — the IC Partner card setting for "what item number to use" (Morre recalled "order" + "common" + a forgotten third); how the group-common-number translation works; he leans toward "order."
2. **Item best-practice** — normal items vs purchase items vs internal items (incl. the leased-asset item); how to set them up.
3. **Lease valuation — the delicate one** — how to handle a lease when the lessor **won't state the asset value, nor the interest rate**. "Very much IFRS territory… we might literally face that."

---

## Topic A — IC item-number mapping (the "common number" mechanism)

### Correction up front: there are **4** options, not 3 — and "order" isn't one of them
The IC Partner card sets the **item-no. type** that controls how an item is identified when a document crosses between companies. The four options:

> **✅ Corrected & confirmed live with Morre (Call 14, 2026-06-25).** Morre checked the **actual IC Partner card** in BC. My v1.0 web-sourced answer **conflated three different mechanisms** and wrongly said "order isn't an option" — **"Order" *is* a real option** on the IC Partner, and Morre's recommendation. Corrected below; the v1.0 table is superseded.

### The actual IC Partner item-no. type (sales) — three options, per the live card
On the **IC Partner**, the **item-no. type for sales** has **three** options (plus the vendor side uses the vendor/internal item number):

| Option | What it means | Use |
|---|---|---|
| **Order** | The item **code is the same in both** companies — the order coming in **auto-maps** to your item. No per-item mapping. | **Recommended for Lasernet** — all legal entities share the **same item codes** (Morre: *"the codes of the items are the same"* — note: *codes*, not number series). Set on **both** sides. |
| **Common Item** | Companies use **different** codes → they **agree a shared "common item number"** entered on each item card; sender posts their number → the **outbox carries the common number** → receiver translates the common number to its local item. | Only if codes differ. **Maintenance trap:** once chosen, **every new item must have the common item number filled in** or you get a warning — people fudge a value and "ruin everything." |
| **Item Reference** | Map via the **Item Reference** table (the partner's number for the item). | Heterogeneous numbering. |

### The recommendation: **Order**
Because Lasernet's legal entities use the **same item codes**, **Order** is the choice — same code both sides, the inbound order auto-maps, nothing to maintain. (My v1.0 called this "Internal No." — the live partner-card label is **Order**.) Set Order on **both** partners. Avoid **Common Item** here: it's for differing codes and carries the per-new-item warning that invites bad data.

### What I conflated in v1.0 — three distinct mechanisms
Morre separated these on screen; they are **not** the same thing:

1. **IC Partner item-no. type** *(the IC thing above)* — Order / Common Item / Item Reference.
2. **Item Reference (per vendor)** — on the **vendor/item**, map *a vendor's* item number to your item so **invoice scanning is automatic** (the vendor's line carries an item number → maps to your item → its posting group books it, e.g. to ~5810). *Per vendor* (same screw from two vendors = two references).
3. **Map text → account (on the vendor)** — for vendors whose invoices carry **descriptive text, not an item number** (e.g. *"hotel night"*): on the vendor you say "this text → this account" (e.g. ~5810/5830). Handles invoices that have no item number at all.

(1) is for **intercompany**; (2) and (3) are **AP-scanning** aids — useful background for the IC/items education module, but a different layer.

---

## Topic B — item best-practice (normal / purchase / internal items)

BC item **types** and how they post:

| Type | Posts to inventory G/L? | Use |
|---|---|---|
| **Inventory** | Yes (cost reconciles to G/L) | Things you stock, buy/sell, manufacture. |
| **Non-Inventory** | **No** (cost is non-invtbl.) | Physical items you don't track as stock. |
| **Service** | **No** | Non-physical (time, labour). |

Non-Inventory/Service items **don't need an Inventory Posting Group**; they route to G/L purely via **Gen. Bus. Posting Group × Gen. Prod. Posting Group**. That combination is the whole trick behind Morre's three categories:

1. **Normal items** — Inventory; the things you actually sell (and buy, if you manufacture).
2. **Purchase / expense items** — a Non-Inventory/Service item standing in for a cost (his "hotel costs" example) **instead of booking straight to a G/L account**. Why: the item carries the **Gen. Prod. Posting Group**, so **VAT and the posting accounts resolve automatically** — no hand-keyed G/L line, fewer errors. *(This is the same principle behind "use Items, not G/L, in IC postings" — see the held IC decision.)*
3. **Internal items** — e.g. the **LEASE-CLEARING item** (Morre's "Z-item"). Purely to land the invoice on the right account at once. Many internal items only need a **purchase account + sales account** set on the Gen. Prod. Posting Group; copy the values from the other items (they're mostly identical) — the **only** real difference is the purchase/sales account (external vs group vs associated). If invoices arrive in **different currencies**, you must also set the **automatic account** (auto-account) so currency is handled.

Related best-practice: for freight/landed costs use the **Charge (Item)** line type (allocates onto item cost) rather than a raw G/L line — a charge increases the item's value; a G/L line doesn't.

> **Connection to the held IC decision:** this is the mechanical case *for* Morre's "Items not G/L in IC" direction — an item carries posting-group + VAT + dimensions automatically, which is exactly the manual pain Carla hit on the G/L-line receipts (missing GL code, missing dimensions). It supports the direction but **doesn't decide it** — Carla's workflow change still needs the sit-down.

---

## Topic C — lease valuation when the lessor states neither value nor rate

> **✅ Confirmed live with Morre (Call 14, 2026-06-25).** Walking through Carla's actual workbook on screen, Morre **accepted both conclusions**: the **auditor supplies the rate** (Carla's **5%** — *"that's what the auditor tells them… this is acceptable for us"*; she's given it, doesn't calculate it), and the **value = the lease liability** (he read off *"Initial measurement of lease liability = 102,810"* = the ROU asset value, with zero market/fair value needed). His words: *"that's a value… that's a rule then. That's typical IFRS — if you don't have the market value, pick this, otherwise you do this; they have these layers of how to evaluate things."* **Topic resolved — not just researched.**

This is the "delicate" one, and the reassuring headline is: **this is the *normal* case under IFRS 16, not an exception — the standard is built for it.**

### "They won't tell us the interest rate" → you weren't going to use it anyway
IFRS 16's discount-rate hierarchy:
1. **Interest rate implicit in the lease** — *if readily determinable*. It rarely is: it depends on the lessor's cost, profit margin and the asset's residual value — **lessor-internal data they won't share**. IFRS explicitly **expects** the implicit rate to be unavailable.
2. **→ Fall back to the lessee's Incremental Borrowing Rate (IBR).**

So a lessor refusing the rate just puts you on the **normal IBR path**. The **IBR** = *the rate you'd pay to borrow, over a similar term, with similar security, the funds to obtain an asset of similar value, in a similar economic environment.* Build it up:
- start from a **readily observable reference rate** (government/swap rate for the lease's **currency and term**), then
- **adjust** for the entity's **credit risk**, the **security/collateral**, the funding amount, and the economic environment.

*(Carla's UK workbook already uses **5%** as the discount rate on both leases — that's an IBR-style rate, not a lessor-stated implicit rate. So we have a live worked example of exactly this path.)*

### "They won't tell us the asset's value" → you don't need it
The ROU asset is **not** measured from the lessor's stated value. Initial measurement:
- **Lease liability = present value of the lease payments** (which you *do* know — they're in the contract/invoice), discounted at the **IBR**.
- **ROU asset = that liability** + payments at/before commencement + initial direct costs + dismantling estimate − incentives.

So **value is derived from the payments + your IBR**, both of which you have. The lessor's own valuation of the office/car is irrelevant to lessee measurement. *(The asset's **fair value** only feeds the **implicit-rate** definition and some classification tests — i.e. precisely the route you're **not** taking.)*

### The genuinely hard residual
Where Morre's instinct ("evaluate to correct value… IFRS territory") really bites is **not** the headline measurement but:
- **estimating a defensible IBR** (the reference-rate + adjustments methodology — set a group policy), and
- **judgement inputs in the payments**: the **lease term** (renewal/termination options reasonably certain?), **variable payments**, **residual-value guarantees**, and any **purchase option**.

These are the real "IFRS valuation" calls — not the discount rate refusal, which is routine.

> **One-line answer for Morre:** even when the lessor states neither the value nor the rate, you can still measure the lease — **value = PV(known payments) discounted at your own IBR**; the lessor's rate and valuation are not required. The real work is a defensible **IBR methodology** + the **lease-term / options judgement**, which is where IFRS expertise (and the advisor/helper) earns its keep.

---

## Open items / for the sit-down

- **A (IC item no.):** ✅ settled with Morre — use **Order** on both partners (Lasernet shares item codes). Avoid Common Item (per-new-item warning). Ties to the held **IC Items-vs-G/L** decision; feeds the IC/items education module.
- **B (items):** if "Items not G/L in IC" is adopted, the internal/purchase-item pattern above is the build; needs the workflow-change discussion with Carla. Vendor item-reference + map-text-to-account are AP-scanning aids for the same education module.
- **C (valuation):** ✅ resolved with Morre — value = lease liability (PV of payments), auditor supplies the rate (UK 5%). Still worth a **group IBR/rate policy** for leases where no auditor figure is given.
- **CoA-number discrepancy (UK vs SE)** remains the separate held item — not touched here.

---

## Sources

- [Setting up item no. type on the IC partner card (UseDynamics)](https://usedynamics.com/intercompany/setting-up-item-no/)
- [Set up intercompany transaction posting (Microsoft Learn)](https://learn.microsoft.com/en-us/dynamics365/business-central/intercompany-how-setup)
- [Use item references (Microsoft Learn)](https://learn.microsoft.com/en-us/dynamics365/business-central/inventory-how-use-item-cross-refs)
- [Understand item types (Microsoft Learn)](https://learn.microsoft.com/en-us/dynamics365/business-central/inventory-about-item-types)
- [Item Charges in BC — and why to avoid G/L accounts (M. F. Ferrari)](https://en.marcofrancescoferrari.it/post/item-charges-in-business-central-how-to-use-them-and-why-you-should-avoid-g-l-accounts)
- [IFRS 16 — Understanding the discount rate (Grant Thornton)](https://www.grantthornton.global/en/insights/ifrs-16/ifrs-16---understanding-the-discount-rate/)
- [Determining the discount rate under IFRS 16 (RSM)](https://www.rsm.global/sites/default/files/media/rsm_insight_determining_the_discount_rate_under_ifrs_16.pdf)
- [How to determine the discount rate for lessees under IFRS 16 (CPDbox)](https://www.cpdbox.com/032-discount-rate-incremental-borrowing-rate-lessees-ifrs-16/)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-24 | Initial — research for Morre's 2026-06-24 call. (A) IC item-no. mapping: corrected 3→4 options, mapped Morre's "order/common" to **Common Item No.**, recommended **Internal No.** if numbering is uniform. (B) Item best-practice: Inventory/Non-Inventory/Service, purchase/expense items via Gen.Prod.Posting Group, internal/clearing items, Charge(Item). (C) Lease valuation with no stated value/rate: implicit-rate normally unavailable → **IBR**; ROU = PV(payments) at IBR, lessor valuation not needed; real work = IBR policy + term/options judgement. Informative only — held decisions untouched. |
| 1.1 | 2026-06-25 | Reviewed live with Morre (Call 14). **(A) corrected against the actual IC Partner card:** options are **Order / Common Item / Item Reference** (not my v1.0 "Internal No./Common/Cross-Ref/Vendor"); **"Order" is real and recommended** (Lasernet shares item codes — same code both sides, auto-maps). Documented the three mechanisms I'd conflated: IC-partner item-no. type vs vendor Item Reference (scanning) vs map-text-to-account. Common Item flagged for its per-new-item warning trap. **(C) confirmed resolved:** Morre accepted value = lease liability (PV of payments) and auditor-supplied rate (UK 5%) walking Carla's workbook live. Open items updated (A/C now settled). |
