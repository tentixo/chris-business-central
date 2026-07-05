# Intercompany Postings — Issues Meeting Summary

**Branch**: `ifrs-16-research`
**Date**: 2026-06-22
**Source**: "Remaining issues IC Postings" meeting, 2026-06-17 (23 min) — `docs/Remaining issue_s IC Postings.docx`
**Participants**: Camilla Höög, Chris Mansson, **Carla Rogers (Lasernet UK)**. (Lars Mårelius / "Morre" named as background deep-expertise backup.)
**Purpose**: Fact-gathering on problems Carla's team hit after IC posting was set up in the new tenant's **production** environment — what works, what doesn't, and what to fix.

---

## ⚑ Two flags to surface first

1. **We cannot test anything in the current sandbox.** IC posting was configured in **production** (it couldn't be done in test/sandbox for an unresolved reason). The sandbox was copied down from production and, with the name changes, the IC settings don't work there. So none of the granular entity-to-entity test invoicing Chris did in the *old* sandboxes has been redone. **Fix in progress — new sandboxes (with Filip) hopefully up this week**; that unblocks all testing below.
2. **Items vs G/L — needs a decision.** Carla reports problems **only with G/L-code lines, not Items** ("I don't think the items we have to change… it's just when we do GL codes"; dimensions on item lines look OK, GL lines aren't filled at all). This sits against **Morre's preference to use Items only**. But Carla raised a real complication: *a sale in one entity is a cost in the other, so it is not the same item* — item-to-item isn't always natural for cost recharges. **→ open discussion item (see §4).**

---

## 1. What works

- **Sending** IC invoices — works well; Carla does many. The problems are almost all on the **receiving** side.
- **Group costs coming down** using one specific dedicated code — believed to work.
- **6994 / 6995** ("intercompany invoiced other costs") — work when invoiced from one entity and received in another, *though dimensions are missing*.
- **Item-based lines** — appear OK (per Carla; to be confirmed by test).

## 2. Core problems (all on receipt)

| # | Problem | Detail |
|---|---|---|
| P1 | **GL code missing — blocks acceptance** | Receiving company can't accept: "GL account is missing." Typically **one line** blocks; add the GL account → it accepts. (Veronique/FR hits this most; Camilla has helped repeatedly.) |
| P2 | **GL codes (and dimensions) missing at posting** | You get through to purchase invoices, but GL codes are missing there — and **you can post without some codes** (Camilla: "a bit scary"). This is **Carla's main problem** — it surfaces at posting, not acceptance. |
| P3 | **Inconsistent behaviour** | After adding the GL account to the *blocking* line to accept, the **other** lines still show no GL account in purchase invoices. Logical to the system, not to the user. |
| P4 | **Deviation from standard IC GL codes "falls over"** | When a cost should hit the **actual cost account, not an IC code** — e.g. one entity (software co.) pays DeskPro for all entities; auditors want it as a **credit against the real cost (~5420 software)**, not an intercompany code — receipt breaks. |
| P5 | **Manual double-handling** | Carla sends invoices with 7–8 lines of different GL codes and **types them into the description** so the receiver knows where to post → manual for her *and* manual for them. |
| P6 | **Comment-line wipes data** | Lines arrive as comment lines; entering a GL code **defaults to that GL account's name and clears the rest** (description, dimensions, all info) → must re-copy manually from the sending company. |
| P7 | **Dimensions missing / cross-entity differences** | Various dimensions missing on receipt. **Country code** differs sending vs receiving (sender = one country, receiver wants another). **Customer group** may need to be flagged "intercompany" (possibly blank). Product/function/revenue should match. |

## 3. Likely root cause on our side — the mapping

- A **GL-account mapping already exists** and is **defaulted to map sender → receiver as the *same* account**. So the mapping is set, but somehow isn't applying on receipt (P1/P2).
- Where a cost should land on a **different** account at the receiver (e.g. IC send code → real cost account 5420, P4), the same-account default is **wrong** — those mappings need review/remap.
- Camilla: "mapping could definitely be improved" — **partly on our end**, not all Microsoft. Remapping *sounds* easy but **must be re-tested** (everything is interconnected).

## 4. Items vs G/L — the open decision (flag #2 expanded)

- **Observation:** item lines behave; **G/L lines are the failure surface** (P1–P7 mostly manifest on GL lines; item dimensions look filled, GL ones don't).
- **Morre's lean:** use **Items only**.
- **Carla's complication:** *a sale to one entity is a cost to the other* → "it's not the same item," so a clean item-to-item flow isn't always natural for recharged costs. She *thinks* items don't need changing on receipt, only GL codes do — **but couldn't confirm** whether an item posted on the sending side is received as an item or a GL account ("I'll take the 5th") — **needs a test**.
- **To decide (once sandbox works):** the preferred workflow per scenario — post-item/receive-item, post-item/receive-GL, or post-GL/receive-GL — and which dimensions should carry vs. differ (country code, customer group=IC).

## 5. Extension blockers (cannot fix now — must *define*)

| Extension | Scope | Status |
|---|---|---|
| **SweBase** (Swedish reporting extension) | Blocks *some* (not all) issues | Must keep for the foreseeable future; long-term plan to retire it only after new reports are built, tested, and confirmed. **Define exactly what it blocks.** |
| **Danish digital voucher** | Receiving on the **Danish** side — affects both **AS and GmbH** in the Danish environment | Not tested since the last major BC update; unclear if Microsoft fixed it. **Re-test.** |
| **MS native IC digital voucher** | Intercompany posting generally | Microsoft acknowledged at last fall's MS event it "is not perfect," promised improvement, but deprioritized → **chase them up.** |

> Not everything is an extension — mapping (§3) and workflow (§4) are on our side. Separate "extension-caused" from "we can fix/customize."

## 6. Severity

**Not urgent, not blocking** — it's manual work, annoying but workable ("it's not stopping us from working"). Heavy IC volume comes **end of June (Q2)**. Goal is still to get the **whole workflow correct/automated** so the feature is actually worth using.

## 7. Actions & owners

| # | Action | Owner | When |
|---|---|---|---|
| A1 | Stand up **new sandboxes from scratch** (so IC can be tested) | Chris + Camilla + **Filip** | This week (hopefully) |
| A2 | **Screenshot** real send→receive flows + any warnings/error codes; send over | **Carla** | Next week (recurring costs not waiting on final sales figures) |
| A3 | Redo **granular entity-to-entity test invoicing** in the new sandbox | Chris | After A1 |
| A4 | **Review/remap** IC GL-account mapping (same-account default vs. real-cost-account cases, P4); re-test | Camilla / Chris | After A1 |
| A5 | **Define & confirm preferred workflows** (Items vs G/L §4; dimensions: country code, customer group=IC) | Carla + Chris | After A1 |
| A6 | **Define what the extensions block** (SwearBase, Danish digital voucher) vs. what's standard/fixable | Camilla / Chris | After A1 |
| A7 | Consider **temporary customizations** to remove manual steps for standard (non-extension) issues | Chris | After A4–A6 |
| A8 | **Chase Microsoft** on the IC digital-voucher roadmap | Camilla | — |
| A9 | Carla to also raise any **wishes / nice-to-haves** while reviewing | Carla | Ongoing |
| A10 | **Document** the working setup → step-by-step guide (ties to the lease rollout guide) | Chris | After testing |

**Roles:** Chris + Carla = key persons; Camilla = oversight/curious; Lars (Morre) = deep-expertise backup if needed.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-22 | Initial — summary of the 2026-06-17 "Remaining issues IC Postings" meeting (Camilla Höög, Chris Mansson, Carla Rogers). Flags: cannot test in current sandbox (prod-only setup); Items-vs-G/L decision (Carla: only G/L breaks; Morre: Items-only) open. Working/broken inventory, mapping root-cause, extension blockers (SweBase, Danish digital voucher, MS native IC voucher), severity, actions with owners. |
