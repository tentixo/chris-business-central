# Dimensions — Hands-On Testing Playbook

**Version**: 1.0
**Created**: 2026-07-14 — built from Chris's first solo Dimensions run (all 6 mechanics in one sitting).
**Type**: Sandbox exercise sheet (do-it-yourself). Companions: `ai/guides/fixed-assets-testing-playbook.md` (dimensions first appear there, in the FA context), study schedule Sprint 2, playbook §3.13 (Dimensions vs Cost Accounting).
**Goal**: go from "seen it" → "done it" on **Dimensions** — the D1 exam sub-area — by running all six mechanics yourself: **create → default → global-vs-shortcut → blocking → correction → priorities.**

> **Reading convention — three voices:**
> - **Numbered steps = the standard Microsoft way** (what MB-800 tests).
> - 🏢 **TENTIXO PRACTICE** callouts = Morre's stance (minimise dimensions; *calcification*; Cost Accounting as the alternative).
> - ⚠️ **FIELD NOTES** = things that actually bit on the first run (14 Jul 2026) — read these, they'll save you 20 minutes each.
>
> **Mental model up front (Morre, Call 16):** a dimension is **not a module — it's 8 tag fields** on a transaction. The *usage* is trivial; the *consequences* need thought (a tag on a posting is permanent → the RIM-vs-crafted problem, see Part 5/adjunct). **Learn the mechanics for the exam; apply the "minimise" judgment for clients.** No conflict between the two.

---

## ⚑ Before you start — don't clutter a shared sandbox

- **Prefix everything `CTEST-`** (dimensions, values) so it's obvious what's yours.
- **Never block a combination involving a heavily-used *global* dimension** (DEPARTMENT × PROJECT) — you'd break other people's postings. Block *your own* `CTEST-` dimension instead.
- **Never test-post into a journal batch that already has lines** — they may be someone else's work (on the first run the `BANK` batch held the live Lasernet lease entries). Use an **empty** batch.
- Note which **company** you're in.

---

## What you'll learn (and the MB-800 boxes it ticks)

| Step | MB-800 domain |
|---|---|
| Create a dimension + values | D1 — *Set up dimensions* |
| Default dimensions on master records | D1 — *defaults* |
| **Global vs Shortcut** | D1 — *the exam-critical distinction* |
| Blocking combinations (Blocked vs Limited) | D1 — *combinations* |
| **Dimension correction** on posted entries | D4 — *process journals / correct dimensions* |
| Default Dimension Priorities | D1 — *priorities / conflict resolution* |

---

## Part 0 — Orientation (5 min, no posting)

1. `Alt+Q` → **"Dimensions"** — this is the **master list of dimension *types*** (AREA, DEPARTMENT, PROJECT, CUSTOMERGROUP…). Note which exist.
2. `Alt+Q` → **"General Ledger Setup"** → **General** FastTab → note **Global Dimension 1 / 2 Code** (the two privileged ones).

> **Reflection:** which dimensions are *global* (stamped on every entry, shown as their own column) versus just available as tags? That difference drives everything in Part 3.

---

## Part 1 — Create a dimension + values

1. `Alt+Q` → "Dimensions" → **+ New**: Code `CTEST-DEPT`, Name `Ctest-dept`, Description e.g. "chris test dimension".
2. Select it → **Dimension Values** (Related → Dimension → Values, or the **Values** action) → **+ New** → add at least two: `ADM` (Admin), `SALES` (Sales).

> ⚠️ **FIELD NOTE:** a dimension with **no values can't be used anywhere** — you can't put it on a line, and a dimension-set row that has a *code* but no *value* is **silently discarded** when you close. **Always add ≥1 value first.** (First-run trap: added the code to a journal line, closed, reopened → gone, because no value was set.)

---

## Part 2 — Default dimensions (make it flow)

Attach a default to a **master record** (Customer / Item / G/L Account / **Fixed Asset**) so every posting for it is auto-tagged:

1. Open the record → **Related ▾ → Dimensions** (opens *Default Dimensions*) → **+ New**.
2. Set **Dimension Code** *and* **Dimension Value Code** (both required) → commit the row (Tab/Enter).

**Expected**: any posting for that record now carries the dimension.

> ⚠️ **FIELD NOTES:**
> - **Set the default *before* you post.** Defaults apply from the moment they're set, **not retroactively** — a record's earlier postings won't get it.
> - **You can't *rename* a default-dimension line.** To change it, **delete the row and add a new one** (typing over the code throws *"You can't rename a Default Dimension."*).

🏢 **TENTIXO PRACTICE:** Morre *minimises* defaults that carry a crafted decision — see the calcification rationale in Part 5 and the adjunct.

---

## Part 3 — Global vs Shortcut (the exam distinction)

| | Global (Dim 1 & 2) | Shortcut (3–8) |
|---|---|---|
| Stored on every entry? | **Yes** — its own column (e.g. Department Code) | No — data-entry convenience |
| Filter reports / analysis / account schedules directly? | **Yes** | No |
| Cost to change | **High** — *Change Global Dimensions* batch rewrites all entries | Trivial |
| How many | Exactly **2** | Up to 6 |

- **Where you assign them:** **General Ledger Setup → General FastTab** (Global Dimension 1/2 Code + Shortcut Dimension 3–8 Code).

> ⚠️ **FIELD NOTES:**
> - The **"Dimensions" button on the GL Setup ribbon does *not* open the global/shortcut assignment** — it opens the master list of dimensions. The assignment fields are on the **page body** (General FastTab; click **Show more** if 3–8 are hidden).
> - **To actually *see* a dimension flow on entries, use a *global* one** — it shows as a column. A custom/shortcut dim is **invisible** in entry lists; you'd have to drill each entry's **Dimension Set**. (First-run: switched the demo from `CTEST-DEPT` → `DEPARTMENT` precisely so it would show as a column.)

---

## Part 4 — Blocking combinations

**Concept:** a matrix of dimension **types**; each intersection is one of:
- **(blank) No Limit** — free to combine.
- **Limited** — only certain *value-pairs* allowed (defined in **Dimension Value Combinations** — value-level).
- **Blocked** — the two **types can never coexist** on one posting (type-level).

**Steps:**
1. `Alt+Q` → **"Dimension Combinations"** → set **`CTEST-DEPT` × `DEPARTMENT` = Blocked** (use your own dim so the block stays isolated).
2. Test: `Alt+Q` → "General Journals" → **switch to an empty batch** → one balanced line → open **Line → Dimensions**, add **both** `CTEST-DEPT=ADM` and `DEPARTMENT=…` → **Post**.

**Expected**: post rejected — *"The combination of dimensions … CTEST-DEPT - DEPARTMENT … is blocked."* Nothing lands in the ledger. (Details panel: Source = *Dimension Combination*, Field = *Combination Restriction*.)

> ⚠️ **FIELD NOTES:**
> - **This BC enforces the block at *post* time, not at dimension entry** — adding both dimensions to the line was *allowed*; only **Post** was rejected. (Version-dependent; some check at entry.)
> - Clean up: delete the test line; optionally set the cell back to **No Limit**.

**Bonus (2 min):** set the cell to **Limited** instead, then `Alt+Q` → **"Dimension Value Combinations"** to allow/deny specific value-pairs — that's the *value-level* control vs Blocked's *type-level*.

---

## Part 5 — Dimension correction (the RIM-vs-crafted star ⭐)

Change a dimension on an **already-posted** entry **without reversing it** — the money never moves. This is the literal tool Morre points to instead of "bake it in and reverse 200 postings."

1. `Alt+Q` → **"G/L Entries"** (or Chart of Accounts → an account like **7835** → its ledger entries) → select a posted entry that carries a dimension (e.g. a depreciation entry, Department Code = ADM).
2. Toolbar → **Correct Dimensions** → opens a **Dimension Correction** (Draft). It pre-loads the entry's dimension with **New Dimension Value Code = "No Change."**
3. Set **New Dimension Value Code** → a different value (e.g. `ADM` → `SALES`).
4. **Validate Dimension Changes** → then **Run**. Status → Completed.

**Expected**: the entry's **Department Code changes** (ADM → SALES), **Amount unchanged**, an audit record is kept, and **only the selected entries** change.

> 🏢 **THE LESSON:** you fixed the *crafted* analysis tag on a *posted* entry with **zero reversal and zero change to the books** — exactly the RIM-vs-crafted separation from Morre's FGGE diagram. Analysis tags are fixable after the fact; the RIM ledger stays untouched.

---

## Part 6 — Default Dimension Priorities

**Concept:** one line can inherit defaults from **several master records at once** (Customer, Item, G/L Account…). If two define the **same dimension differently → conflict.** Priorities resolve it **per Source Code**: **lowest number wins.** *(Trap: two tables with the **same** priority + different values → BC **blocks** the post until fixed.)*

1. `Alt+Q` → **"Default Dimension Priorities"** → **Source Code** = `SALES`.
2. Add rows (Table ID lookup shows names, so no need to memorise IDs):

| Source Code | Table | Priority |
|---|---|---|
| SALES | Customer (18) | **1** ← wins |
| SALES | Item (27) | 2 |
| SALES | G/L Account (15) | 3 |

> 💡 The **"Initialize Dimension Priorities"** button auto-seeds a standard set — handy, but doing it by hand is more instructive.

**Optional live demo (~10 min):** put `DEPARTMENT=SALES` on a Customer and `DEPARTMENT=ADM` on an Item, make a sales line with both → without priorities it **blocks** (conflict); with Customer=1 it silently resolves to SALES.

---

## Adjunct — Dimensions vs Cost Accounting 🏢 *(non-exam / Formpipe)*

Dimensions **calcify**: a tag on a posting is *permanent*, so using one to carry a revisable decision (a 60/40 cost split) bakes that crafted decision onto the RIM posting — to change it you'd reverse and re-post. **Cost Accounting** is the alternative: a **separate ledger** where re-allocations happen freely without touching the original posting. They "stand against each other." **Not in the MB-800 basic exam**, but Morre wants it for **Formpipe** — sketch it separately. See playbook §3.13.

---

## What "good" looks like — self-check

- [ ] Created a dimension **with ≥1 value**.
- [ ] Defaulted a dimension on a master record and **saw it flow** as a column (using a global dim).
- [ ] Can explain **global vs shortcut** and where each is assigned.
- [ ] **Blocked** a combination and saw the post rejected; can state Blocked (type) vs Limited (value).
- [ ] **Corrected** a dimension on a posted entry **without changing the amount**.
- [ ] Set **Default Dimension Priorities** and can state the **tie = block** rule.
- [ ] Can **explain to Morre**: why dimensions calcify, and what Cost Accounting offers instead.

---

## When to pull in Morre (Anchor 2)

- **Cost Accounting setup** — he'll use it for Formpipe; do it with him.
- **Before blocking combinations on shared global dimensions** — could disrupt others.
- **Dimension strategy for a real client** — when to reach for dimensions vs registers vs cost accounting.

---

*Tentixo AB — Business Central Advisory. First-run field notes from Chris's solo session, 2026-07-14.*
