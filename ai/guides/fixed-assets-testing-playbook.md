# Fixed Assets — Hands-On Testing Playbook

**Version**: 1.1
**Created**: 2026-07-05
**Updated**: 2026-07-06 — accounts verified against the sandbox CoA export (`docs/Chart of Accounts (1).xlsx`); English names, Computers family (1250/1259/7835)
**Type**: Sandbox exercise sheet (do-it-yourself). Companion to the *knowledge* in `ai/reports/lease-accounting-setup.md`.
**Goal**: go from "seen Morre do it" → "done it myself" on **Fixed Assets** — the fastest 🟡→🟢 conversion in the MB-800 plan, and the on-ramp to the live Lasernet lease work.
**FLIGHT-PLAN fit**: Anchor 3 (*try first, Morre as backstop*) + Anchor 2 (*done-before = go*). Do Exercise 1 solo; pull Morre in only where flagged.

> **How to use this:** work top to bottom in the BC **Test** environment. Every step has an **Expected result** — that's your built-in error check (same idea as the lease clearing account netting to zero). If what you see doesn't match, stop and figure out why *before* moving on. That diagnosis **is** the learning.

---

## ⚑ Before you start — don't clutter a shared sandbox

The Tentixo test environment is shared. So:
- **Prefix everything you create** with `CTEST-` (asset cards, FA class/group codes if you make new ones) so it's obvious what's yours and easy to clean up.
- **Ask Morre one thing first**: *"Can I create my own FA class + depreciation book in test, or should I reuse existing ones?"* If reuse — use his codes and skip the setup you'd otherwise create (Part 1), just read it to understand it.
- Pick a company to work in and note which one (the exercise posts to the G/L).

**What you need**: BC Test access; the Fixed Assets module enabled; ~45 minutes.

---

## What you'll learn (and the MB-800 boxes it ticks)

| Exercise step | MB-800 domain |
|---|---|
| FA classes, subclasses, depreciation book (G/L-integrated), FA posting group | D2 — *Fixed assets (setup)* |
| Acquisition, depreciation run, disposal | D4 — *Process fixed asset transactions* |
| Reading FA Ledger Entries + G/L impact | D4 — *basic tasks / inspect*, transaction-based thinking |

By the end you'll understand the **three questions every FA setup answers**: *where does the asset's value live, how does it write down over time, and where does the write-down land in the P&L* — which is exactly the foundation the lease's Custom 1/2 trick is built on.

---

## The worked numbers (use these so results are predictable)

A simple owned asset — a laptop/equipment, **not** a lease:

| Thing | Value |
|---|---|
| Acquisition cost | **60,000** |
| Useful life | **5 years**, straight-line |
| ⇒ Annual depreciation | 12,000 |
| ⇒ Monthly depreciation | **1,000** |
| Acquisition date | first of a month, e.g. `2026-01-01` |

---

## Part 0 — Orientation (5 min, no posting)

1. `Alt+Q` → **"Fixed Assets"** → open the list. Empty or full? Note how a card looks.
2. `Alt+Q` → **"Fixed Asset Setup"**. Note the **Default Depr. Book** field — BC's idea of "the main book".
3. `Alt+Q` → **"Depreciation Books"**, **"FA Classes"**, **"FA Subclasses"**, **"FA Posting Groups"**. Just look — you're mapping the furniture before you rearrange it.

> **Reflection:** which of these decides the *accounts*, and which is just a *tag*? (Answer emerges in Part 1.)

---

## Part 1 — One-time setup

*(Skip and reuse Morre's if he said so — but read it, you'll be asked to explain it.)*

### 1a. Accounts — confirm they exist
`Alt+Q` → "Chart of Accounts". A laptop is a **Computer**, so use the Computers account family. **Verified against the sandbox CoA export** (`docs/Chart of Accounts (1).xlsx`, 2026-07-06) — note the sandbox uses **English** account names:

| Account | Name (sandbox CoA) | Role |
|---|---|---|
| 1250 | Computers | Asset (acquisition cost) |
| 1259 | Accumulated depreciation of computers | Accumulated depreciation (contra) |
| 1258 | Accumulated write-downs of computers | Write-down (only if impaired) |
| 7835 | Depreciation on computers | Depreciation expense (P&L) |
| 3973 / 7973 | Capital gains / Losses on sale of machinery and equipment | Gain / loss on disposal (**shared** — there is no computer-specific disposal account) |

> **Pattern:** every FA type follows the same shape — `12x0` asset / `12x9` accum. depreciation / `78xx` expense. E.g. *Equipment and tools* = 1220 / 1229 / 7832, *Cars* = 1240 / 1249 / 7834. Pick the family that matches the asset.

### 1b. Depreciation book
`Alt+Q` → "Depreciation Books" → **+ New** (or reuse):
- **Code**: `CTEST-BOOK`
- **G/L Integration** — turn the relevant toggles **On** (Acquisition, Depreciation, Disposal). *This is what makes FA postings hit the ledger.*

### 1c. FA Class / Subclass
- **FA Class**: `TANGIBLE` (likely exists).
- **FA Subclass** (`Alt+Q` → "FA Subclasses") → **+ New**: `CTEST-COMP`, class = TANGIBLE. *(A subclass is only a **tag** — it groups/report-splits, it doesn't decide accounts.)*

### 1d. FA Posting Group — **this is where accounts get decided**
`Alt+Q` → "FA Posting Groups" → **+ New** `CTEST-COMP`:

| Field | Account |
|---|---|
| Acquisition Cost Account | 1250 |
| Accum. Depreciation Account | 1259 |
| Write-Down Account | 1258 |
| Depreciation Expense Acc. | 7835 |
| Gains Acc. / Losses Acc. | 3973 / 7973 |

> **The key idea:** the **FA Posting Group** answers "which accounts?", the **Depreciation Book** answers "integrated with G/L, and what method?", the **Subclass** is just a label. Same architecture as posting groups everywhere in BC (Morre's "the magic").

---

## Part 2 — Create the asset card

`Alt+Q` → "Fixed Assets" → **+ New**:
- **Description**: `CTEST-Laptop`
- **FA Subclass Code**: `CTEST-COMP` → *watch the FA Posting Group auto-fill* from the subclass default (or set it).
- On the **Depreciation Book** line (in the card): **Depreciation Method** = Straight-Line, **No. of Depreciation Years** = `5`, **Depreciation Starting Date** = `2026-01-01`.

**Expected result**: a card with Book Value = 0 (nothing acquired yet).

---

## Part 3 — Acquire the asset

Two routes — **do route A**, and just read route B so you know both exist.

**Route A — FA G/L Journal** (fastest for the exercise):
`Alt+Q` → "FA G/L Journals":
- FA Posting Type = **Acquisition Cost**, FA No. = your card, **Amount = 60,000**, Bal. Account = a bank/clearing G/L (e.g. 1930 bank, or 2440 if you model a vendor).
- **Post.**

**Route B — Purchase Invoice** (the real-world way): a purchase invoice with an **FA line** (Type = Fixed Asset), 60,000. *(Note the constraint you'll meet again in the lease: a purchase-invoice FA line can only post **Acquisition Cost / Maintenance** — not Custom types. That limitation is *why* the lease needs a clearing account.)*

**Expected result**:
- G/L: **Dr 1250 60,000 / Cr [bank/vendor] 60,000**
- FA card **Book Value = 60,000**
- One **FA Ledger Entry** of type Acquisition Cost. *(Open it: `Alt+Q` → "FA Ledger Entries".)*

---

## Part 4 — Run depreciation (3 periods)

Repeat this **three times**, once per month (Jan, Feb, Mar):

`Alt+Q` → "Calculate Depreciation":
- Depreciation Book = `CTEST-BOOK`, FA Posting Date / Posting Date = period end (e.g. `2026-01-31`).
- It creates lines in an FA G/L Journal → **review → Post**.

**Expected result each month**: **Dr 7835 1,000 / Cr 1259 1,000**. After 3 months:
- Book Value = **57,000** (60,000 − 3×1,000)
- Accumulated depreciation (1259) = 3,000

> **Check like Morre would:** open **FA Statistics** on the card (Acquisition, Depreciation, Book Value) and reconcile it to the **G/L** balances on 1250 / 1259. If FA and G/L disagree, G/L Integration is off or a step was skipped — that reconciliation habit is the whole point.

---

## Part 5 — Inspect (the payoff)

Before disposing, read the story the ledger tells:
1. `Alt+Q` → "FA Ledger Entries" (filter to your FA): one Acquisition + three Depreciation entries.
2. `Alt+Q` → "General Ledger Entries" for 1250, 1259, 7835 — confirm they match.
3. Open the FA card → **FA Statistics**.

**Reflection:** the FA subledger and the G/L are two views of the same truth. Where does the "book value" live — on the asset, in the G/L, or both?

---

## Part 6 — Dispose (the exam gap the lease never teaches)

Sell the laptop for **58,000** at end of March.

`Alt+Q` → "FA G/L Journals":
- FA Posting Type = **Disposal**, FA No. = your card, **Amount = 58,000** (proceeds), Bal. Account = bank.
- **Post.**

**Expected result** — BC nets book value vs proceeds and books the difference as a **gain**:
- Book value at disposal = 57,000; proceeds 58,000 → **gain 1,000** → posts to **3973**.
- The asset's cost (1250) and accumulated depreciation (1259) are cleared out; Book Value = 0.

**Then repeat on a second asset, scrapping it for 0** → you'll book a **loss** (whole remaining book value → 7973). Seeing both a gain and a loss is the point.

**Expected result (scrap)**: proceeds 0, book value X → **loss X** to 7973; asset cleared.

---

## What "good" looks like — self-check

- [ ] FA Statistics reconciles to the G/L (1250, 1259) at every stage.
- [ ] Monthly depreciation is exactly 1,000 and hits 7835.
- [ ] Disposal clears 1250 + 1259 and books the gain/loss to 3973/7973.
- [ ] You can **explain to Morre** why the subclass didn't decide the accounts (the posting group did).

---

## Bridge to Exercise 2 — the Lasernet lease (engagement A5)

Now the lease's clever bit will make sense, because it's the *same machinery with two extra buckets*:

| Vanilla FA (this exercise) | Lease version (`lease-accounting-setup.md`) |
|---|---|
| Acquisition = a real purchase | Acquisition = **from the contract** (Dr 1260 / Cr 2398 liability) |
| Depreciation (only thing moving book value) | **Same** — straight-line on the ROU asset |
| — | **Custom 1** = principal → 2398, **Custom 2** = interest → 8421, both `Part of Book Value = OFF` |
| Disposal at end | Lease runs to term (no disposal) |
| — | 1261 clearing account nets to 0 = the monthly control |

Do Exercise 1, then run the lease guide as Exercise 2 in the same sandbox — that's the real client deliverable (A5), and you'll be doing it, not watching.

---

## When to pull in Morre (Anchor 2)

- **Before Part 1** — confirm: make your own FA class/book, or reuse his?
- **If G/L doesn't reconcile to FA** and you can't find why in ~15 min — that's a good "solve it together" moment.
- **Exercise 2 (lease)** — the deferral push-back step (mid-lease catch-up) *he hasn't built yet*, so do that part with him.

---

*Tentixo AB — Business Central Advisory*
</content>
