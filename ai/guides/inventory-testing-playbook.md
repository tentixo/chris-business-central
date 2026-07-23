# Inventory — Hands-On Testing Playbook

**Version**: 1.0 *(all Parts 1–6 complete & verified — Chris's solo run, 2026-07-23)*
**Created**: 2026-07-23
**Type**: Sandbox exercise sheet (do-it-yourself). Companions: `purchasing-ap-testing-playbook.md`, `journals-payments-testing-playbook.md`, study schedule **Sprint 5**.
**Goal**: go from "seen it" → "done it" on **Inventory** (MB-800 **D3 setup + D4 transactions**) — and specifically nail **costing methods (FIFO)**, the one real content gap from Diagnostic Mock #1.

> **Reading convention — three voices:**
> - **Numbered steps = the standard Microsoft way** (what MB-800 tests).
> - 🏢 **TENTIXO PRACTICE** = how Morre's sandbox is wired.
> - ⚠️ **FIELD NOTES** = what actually bit on the first run. These are the time-savers — this sprint hit *a lot* of them.
>
> **Core idea:** inventory touches **three ledgers at once** — the **Item Ledger** (quantity), **Value Entries** (cost), and the **G/L** (money). The skill is keeping them reconciled. Costing method decides *which cost* leaves when you ship.

---

## ⚑ Before you start — don't disrupt the shared sandbox
- **Prefix everything `CTEST-`**. Build your own item.
- This sandbox has **Location Mandatory = ON** but **only blank-location Inventory Posting Setup rows** — so you *will* complete missing setup as you go. That's additive/low-risk, but **flag the list to Morre**.
- Note the **company** (`TXO`).

---

## What you'll learn (and the MB-800 boxes it ticks)

| Part | Step | MB-800 domain |
|---|---|---|
| 1 | Inventory posting **wiring drill** + create a FIFO item | D3 — inventory setup |
| 2 | The **3 setup gaps** (Location Mandatory · per-location Inv. Posting Setup · Gen. Posting Setup) | D1/D3 |
| 3 | Bring in stock via **Item Journal** (Unit Amount = cost) | D4 |
| 4 | **FIFO in action** — ship & watch oldest-cost leave | D3/D4 🎯 |
| 5 | **Transfer Order** (3-legged: from→in-transit→to) | D4 |
| 6 | **Physical Inventory** count + shrinkage | D4 |
| 7 | **Automatic Cost Posting / Adjust Cost** (seen inline) | D4 |

---

## Part 1 — The wiring, then a FIFO item

### 1a. Read the inventory posting setups (Morre's "where do postings land?")
- `Alt+Q` → **"Inventory Posting Setup"** — crosses **Location × Invt. Posting Group → Inventory Account** (+ an **Interim** account). MERCH → **1460** (balance-sheet stock), Interim **1461**.
  - 🎯 **The "(Interim)" account is the GRNI accrual** — when you *receive* an inventory item on a PO before invoicing, value lands in **1461**; on invoice it moves 1461 → 1460. (This is the two-step a G/L-line PO couldn't show in Sprint 4.)
- `Alt+Q` → **"General Posting Setup"** — the *value-movement* accounts for a Gen.Bus × Gen.Prod combo: **Inventory Adjmt.** (4960, adjustments), **COGS** (4019, sales), **Direct Cost Applied** (~4014, purchases), **Invt. Accrual (Interim)** (2991, received-not-invoiced credit).

> 📝 **Exam nugget:** **Inventory Posting Setup is per-LOCATION** (Location × Invt. Posting Group). **General Posting Setup and VAT Posting Setup are location-INDEPENDENT.** This distinction causes the errors in Part 2.

### 1b. Create the item
`Alt+Q` → **"Items"** → **+ New** (no template wired → set by hand):
- **Type = `Non-Inventory`?** No — **`Inventory`** (we want stock tracking this time).
- **Description = `CTEST Widget`**, **Base Unit of Measure = `EA`**
- **Costs & Posting:** **Costing Method = `FIFO`**, **Gen. Prod. Posting Group = `G-MERCH`** (*make it commit!*), **VAT Prod = `G-FULL`** (auto), **Inventory Posting Group = `MERCH`**
- Leave Standard/Unit Cost = 0 — FIFO builds cost from receipts.

---

## Part 2 — The 3 setup gaps (use **Preview Posting** as the gate)

Post nothing blind — **Post/Preview → Preview Posting** surfaces each missing piece safely, one at a time:

1. ⚠️ **"Location Code must have a value in Item Journal Line."** → Location Mandatory is on; put a **Location** on every line (`MAIN`).
2. ⚠️ **"The Inventory Posting Setup does not exist. Location='MAIN', Invt. Posting Group='MERCH'."** → per-location rule from 1a. **Create the row:** Inventory Posting Setup → New → `MAIN × MERCH` → Inventory `1460`, Interim `1461`. (For the transfer later you'll also need `DIST-SE × MERCH` and `IN-TR-US × MERCH`.)
3. ⚠️ *(possible)* **"Inventory Adjmt. Account is missing in General Posting Setup ⟨blank⟩ G-MERCH."** → set it to `4960` (copy from a wired row).

> ⚠️ **FIELD NOTE — Preview shows COUNTS, check AMOUNTS.** The first preview said "Value Entry: 2" and we trusted it — but the cost was **zero**. Always **drill into the Value Entry** in preview and read **Cost Amount (Actual)**.

---

## Part 3 — Bring in stock at two costs (the FIFO setup)

`Alt+Q` → **"Item Journals"** → batch `DEFAULT`. Two lines, **different cost + date** (this is what makes FIFO visible):

| Posting Date | Entry Type | Item | Location | Quantity | **Unit Amount** |
|---|---|---|---|---|---|
| `01/07/2026` | Positive Adjmt. | `B-ITM00006` | `MAIN` | `10` | **`100`** |
| `15/07/2026` | Positive Adjmt. | `B-ITM00006` | `MAIN` | `10` | **`120`** |

> ⚠️ **FIELD NOTE — the cost field is `Unit Amount`, NOT `Unit Cost`.** On a first run both layers posted at **zero cost** because the value was typed into the "Unit Cost" column (which just mirrors the item's standing cost = 0). **Unit Amount** drives a Positive Adjmt.'s cost. Fix if you slip: **Negative Adjmt.** the zero-cost units out (on-hand → 0), then re-post with **Unit Amount**.
>
> ✅ Verify in preview: **Cost Amount (Actual) = 1,000 and 1,200**. On-hand **20**, value **2,200**, two layers.

---

## Part 4 — FIFO in action 🎯

Consume 15 units and watch which layers FIFO picks.
`Alt+Q` → "Item Journals" → line: **Negative Adjmt.**, `B-ITM00006`, `MAIN`, **Quantity `15`**. **Post.**

> ⚠️ **FIELD NOTE — on OUTBOUND lines you don't set the cost.** BC auto-fills **Unit Amount = 110** (the item's running **average** — maintained as an estimate even for FIFO items). **That estimate does NOT drive the cost.** Don't confuse the line's "Amount 1,650" (15 × 110 = the *average*) with what FIFO actually removes.

**What actually posts (two value entries):**
| Entry | Cost Amount (Actual) | What it is |
|---|---|---|
| 14 | **−1,650** | initial posting at the **110 estimate** |
| 15 | **+50** | **cost adjustment** truing it up to FIFO |
| **Net** | **−1,600** | **10 @ 100 + 5 @ 120** ✅ |

- **Remaining: 5 @ 120 = 600** (FIFO ate the cheap 100s first).
- 🎯 **The +50 IS the FIFO-vs-Average difference:** Average would charge 15 × 110 = **1,650**; FIFO charged **1,600**; the gap is **50**. You watched **Adjust Cost** run live (estimate → actual).

*(This is the mock-question trap: rising prices + FIFO → COGS is **low**, ending inventory high.)*

---

## Part 5 — Transfer Order (3-legged)

Moves stock **between locations** — quantity relocates, **value doesn't** (cost rides along).

1. **Pre-empt the gap:** Inventory Posting Setup → add `DIST-SE × MERCH` and `IN-TR-US × MERCH` (both `1460`/`1461`).
2. `Alt+Q` → **"Transfer Orders"** → **+ New**: **Transfer-from `MAIN`**, **Transfer-to `DIST-SE`**, **In-Transit `IN-TR-US`**, **Direct Transfer = Off** (keeps the two-step). Line: `B-ITM00006`, **Qty `3`**.
3. **Post… → Ship** (MAIN → IN-TR-US), then **Post… → Receive** (IN-TR-US → DIST-SE). *(Ship/Receive is on the dialog after "Post…", like a PO.)*
4. Verify: `Alt+Q` → **"Items by Location"** → **MAIN 2 / DIST-SE 3 / total 5**, value still **600** (MAIN 240 + DIST-SE 360). Ledger shows 4 **Transfer** value entries (±360, netting to 0).

---

## Part 6 — Physical Inventory Count

1. `Alt+Q` → **"Physical Inventory Journals"** → **Prepare → Calculate Inventory** *(not Actions!)* → filter `B-ITM00006` → pulls **Qty. (Calculated)** lines (MAIN 2, DIST-SE 3).
2. On the **MAIN** line, enter **Qty. (Phys. Inventory) = `1`** (counted 1, system says 2) → **Tab out** to commit → the line flips to **Negative Adjmt. / Quantity 1**. DIST-SE (3=3) stays 0.
3. **Post.** → MAIN **2 → 1**; a **−1 @ FIFO cost 120 = −120** shrinkage posts.

Final: on-hand **4** (MAIN 1 + DIST-SE 3), value **480** (4 × 120).

---

## Part 7 — Cost to G/L (seen inline, not a separate step)

🏢 This sandbox has **Automatic Cost Posting = ON**, so **Cost Posted to G/L = full amount** the moment you post (Dr 1460 / Cr 4960). If it were **OFF**, value would sit in the subledger until you run **`Post Inventory Cost to G/L`** — the classic *inventory subledger ≠ G/L* reconciliation. The **Adjust Cost – Item Entries** engine (the +50 in Part 4) also ran automatically.

> ⚠️ **FIELD NOTE — a zero-cost entry posts NO G/L line.** Early on, a preview showed no G/L entry and I wrongly concluded "Automatic Cost Posting is off." It was just that the entry had **0 cost** (0 amount = no G/L). Real cost → G/L moved. Check amounts, not the presence of a line.

---

## First-run summary — the full ledger story (B-ITM00006, 2026-07-23)

```
+1,000 +1,200          inbound  (10@100, 10@120)   = 2,200
−1,650 +50             ship 15  (FIFO −1,600)      →   600
−360 +360 −360 +360    transfer 3 (nets to zero)   →   600
−120                   count shrinkage (−1@120)    →   480
                                on-hand 4 (MAIN 1, DIST-SE 3) × 120 = 480 ✓
```

**Domains covered:** D3 inventory setup (item, costing method, posting setups), D4 (item journal, FIFO costing, transfer order, physical count, cost adjustment).
**Setup gaps completed (flag to Morre):** `MAIN/DIST-SE/IN-TR-US × MERCH` Inventory Posting Setup rows; and the general **Location-Mandatory-on-but-blank-location-only** inconsistency.
**Mock #1 gap closed:** FIFO watched end-to-end — oldest cost out, +50 = FIFO-vs-Average, estimate-then-adjust mechanism.
