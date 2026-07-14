# Fixed Assets — Hands-On Testing Playbook

**Version**: 1.4
**Created**: 2026-07-05
**Updated**: 2026-07-06 — rebuilt on the **standard-Microsoft spine + Tentixo-practice callouts** pattern; all 3 acquisition routes; dimensions woven in; LVA + Inactive/Blocked from Masha §8. Accounts verified against `docs/Chart of Accounts (1).xlsx`.
**Updated**: 2026-07-13 (v1.3) — refined the §1e dimensions callout with Morre's Call-16 nuance (8 tag fields / calcification, not a flat "never use"; Cost Accounting as the allocation alternative).
**Updated**: 2026-07-14 (v1.4) — folded in **field notes from Chris's first solo run** (2026-07-13/14): dimension visibility (global vs shortcut) + "set before acquire" + can't-rename-a-default; Calculate-Depreciation remembers last-used filter; **post-each-month-before-next** (double-count); no posting groups / no Gen. Posting Type on FA + balance-sheet lines; unique Document No. per posting; reconcile via FA Statistics not the shared 1250/1259 balance; correct page name **"Fixed Asset G/L Journals"**; disposal sign + fan-out. Full lifecycle completed & verified (Book Value 57k → disposal gain 1k). **FA → 🟢.**
**Type**: Sandbox exercise sheet (do-it-yourself). Companions: `ai/reports/masha-bc-sessions.md` §8 (Tentixo practice), `ai/reports/lease-accounting-setup.md` (Exercise 2).
**Goal**: go from "seen it" → "done it" on **Fixed Assets** — the fastest 🟡→🟢 in the MB-800 plan, and the on-ramp to the Lasernet lease work.

> **Reading convention** — two voices, deliberately:
> - **Numbered steps = the standard Microsoft way** (what MB-800 tests, what most clients run).
> - 🏢 **TENTIXO PRACTICE** callouts = how Masha actually does it here (`masha-bc-sessions.md §8`). Learn the standard first; treat the callout as one informed option you can weigh later. *(See [[feedback-standard-first-learning]].)*
>
> **How to use:** work top to bottom in BC **Test**. Every step has an **Expected result** — your built-in error check. If it doesn't match, stop and diagnose *before* moving on. That diagnosis is the learning.

---

## ⚑ Before you start — don't clutter a shared sandbox

- **Prefix everything `CTEST-`** (assets, class/group codes) so it's obvious what's yours and easy to clean up.
- **Ask Morre first**: *"Can I create my own FA class + depreciation book in Test, or reuse existing ones?"* If reuse — use his codes and just read Part 1.
- Note which **company** you're in (the exercise posts to the G/L).
- **What you need**: BC Test access; Fixed Assets module; ~1 hour.

---

## What you'll learn (and the MB-800 boxes it ticks)

| Step | MB-800 domain |
|---|---|
| FA classes, subclasses, depreciation book (G/L-integrated), FA posting group | D2 — *Fixed assets (setup)* |
| **Dimensions**: set up a shortcut dimension, default it on the asset, watch it flow | D1 — *Set up dimensions* (exam-critical) |
| Acquisition via **all three** standard routes; depreciation; disposal | D4 — *Process fixed asset transactions* |
| Reading FA Ledger vs G/L; analysing by dimension | D4 — *inspect / data analysis* |

---

## The worked numbers

A **main** fixed asset — office equipment, **not** a lease:

| Thing | Value |
|---|---|
| Acquisition cost | **60,000** |
| Useful life | **5 years**, straight-line |
| ⇒ Monthly depreciation | **1,000** |
| Acquisition date | first of a month, e.g. `2026-01-01` |

> 🏢 **TENTIXO PRACTICE (§8):** Masha splits assets by Swedish threshold — **LVA** (low-value, 2,000–20,000 SEK) written off immediately, vs **Main** (> 20,000 SEK) depreciated over N years (**laptops = 3 years** here). Our 60,000 asset is a **Main**. The LVA variant is at the end.

---

## Part 0 — Orientation (5 min, no posting)

1. `Alt+Q` → **"Fixed Assets"** — open the list; note how a card looks.
2. `Alt+Q` → **"Fixed Asset Setup"** — note **Default Depr. Book**.
3. Skim **"Depreciation Books"**, **"FA Classes"**, **"FA Subclasses"**, **"FA Posting Groups"**.

> **Reflection:** which of these decides the *accounts*, and which is just a *tag*?

---

## Part 1 — One-time setup

*(Reuse Morre's if he said so — but read it, you'll be asked to explain it.)*

### 1a. Accounts (verified against the sandbox CoA — English names)
A laptop/equipment uses the **Computers** family (`12x0/12x9/78xx` pattern; pick the family matching the asset — Equipment and tools = 1220/1229/7832, Cars = 1240/1249/7834):

| Account | Name (sandbox CoA) | Role |
|---|---|---|
| 1250 | Computers | Asset (acquisition cost) |
| 1259 | Accumulated depreciation of computers | Accum. depreciation (contra) |
| 1258 | Accumulated write-downs of computers | Write-down (if impaired) |
| 7835 | Depreciation on computers | Depreciation expense (P&L) |
| 3973 / 7973 | Capital gains / Losses on sale of machinery and equipment | Gain / loss on disposal (**shared** — no computer-specific one) |

### 1b. Depreciation book
`Alt+Q` → "Depreciation Books" → **+ New**: Code `CTEST-BOOK`; **G/L Integration** toggles (Acquisition, Depreciation, Disposal) **On**. *This is what makes FA postings hit the ledger.*

### 1c. FA Class / Subclass
- **FA Class** = `TANGIBLE`.
- **FA Subclass** → **+ New** `CTEST-COMP`, class = TANGIBLE. *(A subclass is only a **tag** — it groups/reports, it doesn't decide accounts.)*

### 1d. FA Posting Group — **where accounts get decided**
`Alt+Q` → "FA Posting Groups" → **+ New** `CTEST-COMP`:

| Field | Account |
|---|---|
| Acquisition Cost Account | 1250 |
| Accum. Depreciation Account | 1259 |
| Write-Down Account | 1258 |
| Depreciation Expense Acc. | 7835 |
| Gains Acc. / Losses Acc. | 3973 / 7973 |

> **The key idea:** the **FA Posting Group** answers "which accounts?", the **Depreciation Book** answers "G/L-integrated + what method?", the **Subclass** is just a label. Same posting-group architecture as everywhere in BC.

### 1e. Dimensions (standard, exam-critical) 🎯
BC uses **dimensions** to tag postings for cost-centre/segment reporting. Set one up so you can watch it flow through the FA postings.

1. `Alt+Q` → "Dimensions". If a usable one exists (e.g. **DEPARTMENT**), use it; if not, **+ New** `CTEST-DEPT` with two **Dimension Values** (e.g. `ADM`, `SALES`) — *creating a dimension + values is itself an exam skill (D1)*.
2. `Alt+Q` → "General Ledger Setup" → **Dimensions** — set your dimension as a **Shortcut Dimension** (so it shows as a column on journals). *(Global vs shortcut is exam material — note the difference.)*

> 🏢 **TENTIXO PRACTICE:** Morre *minimises* dimensions — Tentixo segments via CoA/account structure instead — so the Test env may have few set up. But his refined position (Call 16) is **not** "never": a dimension is just **one of 8 tag fields**, trivial to use, and worth learning the standard way for the exam. The real objection is **calcification** — a dimension on a posting is *permanent*, so using one to carry a revisable decision (e.g. a 60/40 cost split) bakes that decision onto the raw posting and forces a reverse-and-re-post to change it. Learn dimensions here regardless; apply the "minimise" judgment for clients. *(See playbook §3.13; the separate-ledger alternative for cost allocation is Cost Accounting.)*

---

## Part 2 — Create the asset card

`Alt+Q` → "Fixed Assets" → **+ New**:
- **Description**: `CTEST-Laptop`
- **FA Subclass Code**: `CTEST-COMP` → *watch the FA Posting Group auto-fill*.
- Depreciation Book line: **Method** = Straight-Line, **No. of Depreciation Years** = `5`, **Depreciation Starting Date** = `2026-01-01`.
- **Default dimension**: FA card → **Related ▾ → Dimensions** (opens *Default Dimensions*) → **+ New** → e.g. `DEPARTMENT = ADMIN`. *So it flows onto every posting for this asset.*

**Expected result**: card with Book Value = 0 and a default dimension set.

> ⚠️ **FIELD NOTES (first run, Jul 2026) — dimensions:**
> - **Set the default *before* you acquire.** Defaults apply from the moment they're set, *not* retroactively — if you acquire first, the acquisition entry won't carry the dimension (only later postings will).
> - **To actually *see* the dimension flow, use a *global* dimension** (here `DEPARTMENT`). Global dims (Global 1/2) show as their own **column** (Department Code / Project Code) on every entry list. A **custom/shortcut** dim (e.g. a `CTEST-DEPT` you invent) is *invisible* in the lists — you'd have to drill each entry's **Dimension Set** to see it. Create the custom one once for the D1 exam skill, but use a global one for the "watch it flow" payoff.
> - **You can't *rename* a Default Dimension line.** To change it you **delete the row and add a new one** (`+ New`) — typing over the Dimension Code throws *"You can't rename a Default Dimension."*
> - The **global-vs-shortcut assignment** lives on **General Ledger Setup → General FastTab** (Global Dimension 1/2 + Shortcut Dimension 3–8), *not* behind the **Dimensions** button on that page (that button just opens the master list of dimensions).

---

## Part 3 — Acquire the asset (the three standard routes)

MB-800 expects you to know **all three**. Do Route 1 (the most common), then try Route 2 on a second asset; read Route 3.

### Route 1 — Purchase Invoice with an FA line ✅ *the standard vendor purchase*
`Alt+Q` → "Purchase Invoices" → **+ New**: Vendor = the supplier; line **Type = Fixed Asset**, No. = your FA, Direct Unit Cost = 60,000, add VAT as normal. **Post.**
- Handles **VAT + AP + the asset** in one canonical document.

> 🏢 **TENTIXO PRACTICE (§8):** *this is Masha's route* — the receipt/purchase invoice books the money + VAT, then the asset is registered "ex-VAT, since VAT was already handled in the receipt." So the standard Microsoft way and the Tentixo way are the **same** here.

### Route 2 — FA G/L Journal *(opening balances / no vendor invoice)*
`Alt+Q` → **"Fixed Asset G/L Journals"** (that's the full page name — searching "FA G/L Journals" finds nothing; and don't pick the lookalike **"Fixed Asset Journals"** without "G/L", which is subledger-only): FA Posting Type = **Acquisition Cost**, FA No. = your card, **Amount = 60,000**, Bal. Account = bank. **Post.** *(Simpler, but no VAT/vendor — use for balances or manual acquisitions.)*

> 💡 The **"Acquire"** button / blue banner on the FA card is just a wizard wrapper around **Route 2** — it asks for cost + date + a balancing account and posts an FA G/L Journal behind the scenes. Fine to use; know it's Route 2 under the hood.

### Route 3 — FA Journal *(non-integrated books)* — read only
The plain **FA Journal** posts to the FA subledger **only, not the G/L** — used when a depreciation book isn't G/L-integrated (e.g. a parallel tax book). *(You'll meet this again with the lease's separate books.)*

**Expected result (Route 1)**: G/L **Dr 1250 60,000 / Cr Vendor (AP)** (+ VAT line); FA **Book Value = 60,000**; one **FA Ledger Entry** (Acquisition Cost) **carrying your dimension**. Check: `Alt+Q` → "FA Ledger Entries".

---

## Part 4 — Run depreciation (3 periods)

Repeat **three times** (Jan, Feb, Mar): `Alt+Q` → "Calculate Depreciation": Depreciation Book = your asset's book, **Posting Date = period end** (`2026-01-31`, then `2026-02-28`, then `2026-03-31`) → review the journal it creates → open **Fixed Asset G/L Journals** → **Post.**

> 🏢 **TENTIXO PRACTICE (§8):** Masha runs this monthly via **Actions → Tasks → Calculate Depreciation** — same action, different navigation.

> ⚠️ **FIELD NOTES (first run) — the four that bit, in order:**
> 1. **The Calculate Depreciation dialog remembers the *last-used* book + filter.** It came pre-filled with the wrong `Depreciation Book` and a wrong `Filter: No.` (someone else's asset). **Always re-check** Depreciation Book = *your* asset's book and Filter: No. = *your* FA before OK.
> 2. **Post each month *before* calculating the next.** Calculate Depreciation nets against what's *already posted*, not against unposted journal lines. Queue up Feb + Mar unposted and March double-counts (comes out **2,000**, because it can't see the unposted Feb). Rhythm: **Calculate → Post → Calculate → Post.**
> 3. **Depreciation lines must carry NO posting groups and NO Gen. Posting Type.** If the `7835` line comes in with a `Gen. Prod. Posting Group` (e.g. `GL_ACC` inherited from the account card), posting fails with *"Posting to Account 7835 must be of type Purchase or Sale…"* → **clear that field on the line** (depreciation is an internal G/L move, not a trade line).
> 4. **Each depreciation posting needs a *unique* Document No.** per FA + book (*"Document No. … already exists…"*). Easiest fix: let the number series assign a fresh one, or set each period's pair to a different number.

**Expected result each month**: **Dr 7835 1,000 / Cr 1259 1,000**, and **the depreciation entry carries your default dimension** (visible in the Department Code column if you used a global dim). After 3 months: Book Value = **57,000**; accum. depreciation (1259) = 3,000.

> **Check like Morre would:** open **FA Statistics** and reconcile — see Part 5 for *which* view to reconcile against (it's **not** the raw G/L account balance).

---

## Part 5 — Inspect (the payoff)

1. `Alt+Q` → "FA Ledger Entries" (your FA): one Acquisition + three Depreciation entries. *(Scroll right for the **Amount** column, or ⚙ Personalize to add it — it's off-screen by default.)*
2. **Reconcile the single asset via FA Statistics / FA Ledger Entries — NOT the raw G/L account balance.**
3. **By dimension**: on the entries, read the **Department Code** column (or use **data analysis / Edit in Excel**) — see the depreciation grouped by your global dimension. *That's the reporting payoff dimensions give you (D4 data-analysis skill).*

> ⚠️ **FIELD NOTE (first run) — why the G/L account "doesn't match" your asset:** accounts **1250 / 1259** are **FA-Posting-Group accounts shared across *every* computer asset** in the company. On the first run they showed **175,000 / −4,528** — the *aggregate*, not this asset's 60,000 / −3,000. So **don't** reconcile a single asset against the account balance. Reconcile against **FA Statistics** (per-asset). To find *your* slice inside the shared account, open the account's ledger entries and **filter** (by Posting Date `2026-01..03`, or by Department Code = your dim). This is the account-categories lesson in miniature: the account shows the total; you *drill/filter* for the granular (in production, Power BI does this).

**Reflection:** the FA subledger and the G/L are two views of one truth; the dimension is the third axis (who/where the cost belongs to); the G/L *account* is the aggregate of many assets.

---

## Part 6 — Dispose

Sell the laptop for **58,000** at end of March. `Alt+Q` → **"Fixed Asset G/L Journals"**: on the line set **Account Type = Fixed Asset**, FA No. = your card, FA Posting Type = **Disposal**, **Amount = −58,000** (proceeds; a sale *credits* the asset side), **Bal. Account Type = G/L Account** (or Bank Account), **Bal. Account No.** = a real bank/cash account in the **19xx** range (`1930` may not exist — use the lookup; e.g. `1970`). Confirm **Total Balance = 0** → **Post.**

> ⚠️ **FIELD NOTES (first run) — disposal:**
> - **The blank starter row is not a leftover.** A fresh FA G/L Journal shows one empty line pre-filled with today's date + a Document No. — **Number of Lines = 0** confirms it's just the template row. Type your disposal into it.
> - **Sign:** proceeds go in as **negative** (`−58,000`) with the bank as the balancing debit. If the result comes out as a *loss* or a double figure, flip to `+58,000`. The **gain-of-1,000** check tells you it's right.
> - **No Gen. Posting Type / no posting groups on the disposal line** — same rule as depreciation. A stray `Gen. Posting Type` throws *"Gen. Posting Type must not be … "* → **clear it** (blank). If the bank G/L account keeps re-defaulting it, switch **Bal. Account Type = Bank Account** and pick a bank record (those have no Gen. Posting Type).

**Expected result**: book value 57,000 vs proceeds 58,000 → **gain 1,000** → **3973**; Book Value = 0. In **FA Ledger Entries** the disposal fans out into: **Proceeds on Disposal −58,000**, **Gain/Loss −1,000** (a credit = gain), **Acquisition −60,000** (clears 1250) and **Depreciation +3,000** (clears 1259) — all carrying your dimension.

**Then scrap a second asset for 0** → whole remaining book value → **loss** to **7973**. Seeing both a gain and a loss is the point.

> 🏢 **TENTIXO PRACTICE (§8):** the disposal posting does **not** deactivate the card — Masha then **manually sets the FA card to Inactive + Blocked**. She also records **serial numbers** on cards for the audit trail. (Standard BC leaves the card active; this cleanup is Tentixo housekeeping.)

---

## Bonus variant — LVA (low-value asset) 🏢 Tentixo split

Create `CTEST-LVA-Chair` (value 8,000, in the 2,000–20,000 band). Acquire it, but set **Depreciation Starting Date = Ending Date** (same day) → the whole value writes off at once, **Book Value → 0 immediately**, no monthly runs. *(This is the Swedish LVA convention Masha uses; the standard mechanic underneath is just a full first-period depreciation.)*

---

## What "good" looks like — self-check

- [ ] **FA Statistics** (per-asset) shows the right Book Value at every stage — *this* is your reconciliation, not the shared 1250/1259 account balance.
- [ ] Monthly depreciation is exactly 1,000, hits 7835, **and carries the dimension** (visible as a column because you used a global dim).
- [ ] You posted **each month before calculating the next** (no double-count).
- [ ] You acquired via **at least two** of the three routes and can say when each applies.
- [ ] Disposal clears 1250 + 1259, books gain/loss to 3973/7973, and Book Value → 0.
- [ ] You can **explain to Morre**: why the subclass didn't decide the accounts; what a dimension gives you that an account split doesn't; and why FA/balance-sheet lines carry no posting groups or Gen. Posting Type.

---

## Bridge to Exercise 2 — the Lasernet lease (engagement A5)

The lease is the *same machinery with two extra buckets*:

| Vanilla FA (this exercise) | Lease version (`lease-accounting-setup.md`) |
|---|---|
| Acquisition = purchase/journal | Acquisition = **from the contract** (Dr 1260 / Cr 2398 liability) |
| Depreciation (only thing moving book value) | **Same** — straight-line on the ROU asset |
| — | **Custom 1** = principal → 2398, **Custom 2** = interest → 8421, both `Part of Book Value = OFF` |
| Disposal at end | Lease runs to term (no disposal) |
| — | 1261 clearing account nets to 0 = the monthly control |

Do Exercise 1, then run the lease guide as Exercise 2 — that's the real client deliverable (A5), and you'll be doing it, not watching.

> ⚠️ **Open with Morre (see `ai/working/CONFUSION-lease-accum-depreciation-account.md`):** the lease docs use **1267** for accumulated depreciation, but this sandbox has **1269** for that (1267 = *appreciation*). Confirm before wiring the lease FA posting group.

---

## When to pull in Morre (Anchor 2)

- **Before Part 1** — own FA class/book, or reuse his?
- **If G/L doesn't reconcile to FA** and you're stuck ~15 min — good "solve it together" moment.
- **Exercise 2 (lease)** — the deferral push-back (mid-lease catch-up) isn't built yet; do it with him.

---

*Tentixo AB — Business Central Advisory*
</content>
