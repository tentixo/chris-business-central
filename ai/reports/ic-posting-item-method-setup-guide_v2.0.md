# Intercompany Posting (Item Method) — Setup Guide

**Version**: 2.0  *(supersedes v1.0 — corrected against the live Lasernet setup + Morre review, 2026-06-30)*
**Updated**: 2026-06-30
**Author**: Tentixo AB
**BC version**: 28.2
**Scope**: Intercompany (IC) document exchange between Lasernet legal entities, using **shared service Items** (not manual G/L lines)
**Audience**: BC functional user / administrator
**Decision recorded**: IC postings use **Items, not G/L accounts**. Basis in `ai/reports/ic-items-lease-valuation-research_v1.0.md`.

> **Draft note (remove before client):** open items pending confirmation are listed at the end — the **7066 / DeskPro** cases (Morre), the **Country-dimension automation** (Jeb), and the exact **cross-environment wizard** steps (sandbox).

---

## What this guide covers

Setting up IC so an invoice raised in one Lasernet company flows **automatically** into the partner company and posts with the **correct account, VAT and dimensions — with nothing hand-keyed on the receiving end**. Every line is a **service Item**; the account and VAT are resolved from posting groups, not typed in.

By the end you'll have:

- The **IC Partner** connected and set to the **de-facto Lasernet values** (Item No. Type = **Order**)
- Shared **service items** carrying the right posting groups
- A **send → receive → accept** flow that posts clean — no missing account, no empty dimensions (bar the one Country gotcha)

---

## How it actually posts — the five tags

The item does **not** carry an account. Posting is resolved from **five tags**:

| Tags | Resolves | Where | Carried by |
|---|---|---|---|
| **Gen. Bus.** × **Gen. Prod.** Posting Group + posting type (sale/purchase) | the **G/L account** (sales account when selling, purchase account when buying) | **General Posting Setup** | Gen. Bus. on the **IC partner** (as customer/vendor); Gen. Prod. on the **item** |
| **VAT Bus.** × **VAT Prod.** Posting Group | the **VAT** | **VAT Posting Setup** | VAT Bus. on the partner; VAT Prod. on the item |

So when LN_LTD **sells** a service, BC reads "sale" → posts the **sales account**; when the partner **receives** it, BC reads "purchase" → posts the **purchase account**. Same setup, opposite ends — which is exactly why *"a sale here is a cost there"* needs no special handling. **VAT Posting Setup is already complete — you change nothing there.**

---

## Prerequisites (admin / Camilla — already in place)

These are **global** settings, done by the administrator — **not** user steps:

- **IC Chart of Accounts** + **IC Dimensions** mapped.
- **General Posting Setup** complete — the account matrix below.
- **VAT Posting Setup** complete.
- **Item codes identical across the entities** — this is what lets **Order** auto-map (same code both sides).

**The account matrix (General Posting Setup) — reference, where the account comes from** (Sales account / Purch. account):

| Gen. Prod. ↓ \ Gen. Bus. → | EXT (external) | IC-DAUG (daughter) | IC-MOTH (mother) | IC-OTHR (other group) |
|---|---|---|---|---|
| **S-MAIN** — Main Revenue Services | 3011 / 4011 | 3015 / 4015 | 3014 / 4014 | 3016 / 4016 |
| **S-GEN** — Service General | 3421 / 4681 | 3425 / 4685 | 3424 / 4684 | 3426 / 4686 |

*(VAT Prod. for both = **S-FULL**. `IC-DAUG/MOTH/OTHR` are picked by the group relationship — daughter / mother / other group company. `PMARGIN` partner-margin and `P-GEN` products exist but are outside this guide — Lasernet sells services.)*

---

## Step 1 — Connect the IC Partner (cross-environment)

Lasernet's companies live in separate environments, so partners are connected **cross-environment**.

**Open**: `Intercompany Partners` → the partner → **Connect Externally Setup**

- Link the partner company in its environment. **Company Name is set automatically** by the connection — you don't type it.

> *(A partner that happens to sit in the **same** environment would show `Transfer Type = Database` instead — but the Lasernet standard is the cross-environment connection.)*

---

## Step 2 — IC Partner values (set these)

On each partner card. **The settings are identical for every partner in every legal entity — except Auto. Accept, which is OFF for the Danish receiving companies.**

| Field | Set to | Note |
|---|---|---|
| **Outbound Sales Item No. Type** | **Order** | The decision — same code both sides → auto-maps. The only field that genuinely needs setting/validating. |
| **Outbound Purch. Item No. Type** | **Order** | Same, purchase side |
| **Auto. Send Transactions** | **On** | Always on |
| **Auto. Accept Transactions** | **On** | **Off** only when the **receiving** company is **Danish** |
| Customer No. / Vendor No. | the partner's customer / vendor card | |
| Receivables / Payables Account | the partner's IC control accounts | admin-set (e.g. `1566` / `2466` for LN_LTD) |
| Country/Region · Currency | the partner's own | e.g. `GB` · `GBP` |

> **Why Order (not the others):** Lasernet entities **share item codes**, so *Order* auto-maps the inbound line to your item with nothing to maintain. *Common Item* (for differing codes) warns on every new item and invites bad data; *Item Reference* is for heterogeneous numbering — neither is needed here.

---

## Step 3 — The service items (set these)

**Open**: `Items` → the item

| Field | Set to | Note |
|---|---|---|
| **Type** | **Service** | **Not** Inventory (no physical stock) and **not** Non-Inventory (that means goods held in someone else's stock). Service only. |
| **Gen. Prod. Posting Group** | **S-MAIN** *(main revenue services)* or **S-GEN** *(general services)* | Picks the account row in the matrix above |
| **VAT Prod. Posting Group** | **S-FULL** | Service with full VAT |
| Base Unit of Measure | per item | |
| **Default Dimensions** | per Camilla's dimension naming | Item → **Dimensions**. So dimensions flow with the line |

No account is set on the item — it resolves from the posting groups (the five tags). Default dimensions live on the **item** (or a G/L account), **never on a posting group**.

---

## Step 4 — Send an IC document (outbox)

**Open**: `Sales Invoices` (or Sales Orders) → **+ New**, in the **sending** company.

1. Select the partner (as **Customer**).
2. Add lines as **Item** with the shared service item.
3. With **Auto. Send** on, the document delivers to the partner's inbox.

---

## Step 5 — Receive, accept & post (inbox)

**Open**: `IC Inbox Transactions`, in the **receiving** company.

1. Find the inbound document. *If it isn't there, check the inbox manually — see Troubleshooting (notification gap).*
2. **Accept** (or it auto-accepts, unless this is a Danish receiver). BC creates a **purchase document**: the **shared item auto-maps via Order**, the **account + VAT resolve** from the five tags, and the item's **default dimensions populate**.
3. **Verify, then Post**:

| Check | Expected |
|---|---|
| Item line | mapped to your local item (same code) |
| Account | resolved (purchase account from the matrix) — no blank G/L |
| VAT | calculated (F7 → Statistics) |
| Dimensions | populated — **except Country** (next step) |

---

## Step 6 — The Country dimension gotcha

The **Country** dimension legitimately **differs** sender vs receiver:

- The sender sells **to** Sweden → posts Country = **SE**.
- A **Danish** receiver received it **from** Denmark → must set Country = **DK**.

So Country is the one dimension the receiver may need to **correct on receipt**. (The other dimensions — Function, Product, Revenue Type, Cust_group — carry through via the item's default dimensions.)

> **Pending (Jeb):** there may be an automation that fixes the sender→receiver Country swap. Unknown if it shipped, and it may not be in the new sandboxes — **validate once the sandboxes are up**; until then, treat Country as a manual correction on the Danish receiving side.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "The IC G/L Account does not exist. No.=''" | A non-item line hit an unmapped IC G/L account | Keep lines as **items** (they resolve via posting groups); the IC G/L map itself is admin/Camilla |
| Inbound document never appeared | IC notification gap | Check **IC Inbox Transactions** manually; Auto. Accept covers trusted (non-Danish) partners |
| Item line didn't auto-map | `Item No. Type` not **Order**, or codes differ | Set **Order** (both sales & purch) on the partner; align item codes |
| Item posted, but "things went haywire" | Item **Type** set to Inventory or Non-Inventory | Set **Type = Service** |
| Country dimension wrong on receipt | Sender's country ≠ receiver's | Receiver sets its own Country (Step 6) |
| Other dimensions empty | Item has no **Default Dimensions** | Set them on the item (Step 3) |
| VAT missing/incorrect | Item has no **VAT Prod. Posting Group** | Set **S-FULL** |
| Keying a G/L code **wipes** description + dimensions | A comment/G-L line, not an item line | Use an **item** line — it keeps everything intact |

---

## Known environment blockers (define, don't fix here)

If a problem appears only in DK/SE or for one entity, suspect an extension **before** re-checking the setup:

- **SweBase** (Swedish reporting) — blocks *some* issues; retire only after replacement reports are built and confirmed. **Define what it blocks.**
- **Danish digital voucher** — affects receiving on the **Danish** side (AS and GmbH); re-test after BC updates.
- **MS native IC digital voucher** — Microsoft has acknowledged it "is not perfect"; chase the roadmap.

---

## Architecture note — why Items, not G/L

A **service item** carries its **Gen. Prod.** and **VAT Prod.** posting groups; the **IC partner** (as customer/vendor) carries the **Gen. Bus.** group; **General Posting Setup** then resolves the **account by posting type** — sales account when selling, purchase account when receiving. The receiver hand-keys **nothing**.

A raw **G/L line** carries none of that, so the receiver must hand-key the account and dimensions — the exact failure the team hit (*"IC G/L Account does not exist"*, empty dimensions, comment lines wiping data, and typing G/L codes into the invoice description so the receiver knows where to post). Moving IC onto **items** puts that knowledge on the master data once, reused on every document, and it rolls out across the group (UK → DE/SE/DK/FR/US).

---

## Open items — confirm before client (internal)

- **7066 salary / management-fee recharge — fits the item method** *(confirm build with Morre).* The CoA shows `7066` = "Intercompany invoiced salaries, IC-OTHR", part of a clean IC series — `7064` (IC-MOTH), `7065` (IC-DAUG), `7066` (IC-OTHR), Gen. Posting Type = Purchase — i.e. the same shape as the S-MAIN revenue accounts. **Build:** add a dedicated **Gen. Prod. Posting Group** for the salary recharge and set its **General Posting Setup** purchase accounts to **7064 / 7065 / 7066** (by IC-MOTH / IC-DAUG / IC-OTHR); then it's an ordinary service item. The accounts already exist — only the posting-group → account mapping is missing.
- **DeskPro → ~5420 (P4) — the genuine exception.** `5420` = "Software and licenses" is a **plain cost account, not IC-suffixed**, so the "one entity pays, credit the real cost" case has no IC variants. Treat as a **deliberate mapping / documented exception**, not a standard shared-item line — **decide with Morre**.
- **Data gap — `4686` missing.** General Posting Setup row `IC-OTHR × S-GEN` points to purchase account **`4686`, which does not exist** in the CoA (`4684`/`4685` do). Create the account or fix the mapping — **with Camilla**.
- **Country-dimension automation** (Jeb): shipped? in the sandboxes? → validate.
- **Cross-environment connection**: exact wizard steps in BC 28.2 — capture from the sandbox / the setup reference doc.

---

*Tentixo AB — Business Central Advisory*
