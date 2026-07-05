# Capitalization of Development Work — IAS 38 (Reference Note)

**Branch**: `ifrs-16-research`
**Date**: 2026-06-22
**Source**: Call with Lars Mårelius (Morre), 2026-06-22 — Part 3 of the conversation (`docs/Call with Lars Mårelius (9).docx`). Morre's "little quick research" on *aktivering* (capitalizing work hours).
**Type**: Reference note for future use — **not** an immediate action item. Captures Morre's reasoning + grounding.
**Related**: [`ifrs-posting-layer-rfc_v1.0.md`](ifrs-posting-layer-rfc_v1.0.md) (Done1/Done2 layering), [`node-xitem_v1.0.md`](../project-docs/node-xitem_v1.0.md) (the X-item/X-package/license model this depends on).

> **Scope note:** this note covers **Part 3 (Capitalization)** only. Parts 1–2 are out of scope (Morre said ignore). **Part 4 (Lease reporting)** is *not in this transcript* — it cut off as Chris said "can I show you what I've done?" See the handoff note at the end.

---

## 1. What it is

**Capitalizing development work** (Swedish *aktivering*) = treating developers' time spent building a product as an **investment (intangible asset)** rather than an immediate **expense**. Governed by **IAS 38 Intangible Assets**.

Effect: the dev cost goes onto the **balance sheet** (capitalized) instead of the **P&L** → current-period costs are lower → revenue/profit looks bigger, presented as an investment. Formpipe does this; Lasernet is doing it.

In the Done1/Done2 model this is a **Done2 (group/Captive) item they want to push down to Done1 (legal entity)** — same new-flow principle as IFRS 16.

---

## 2. The core rule — research vs development, and the "direct revenue" test

IAS 38 splits an internal project into two phases:

| Phase | Treatment |
|---|---|
| **Research** (incl. Morre's "truth graph"-style work, anything *not* coding) | **Expense** — always. Even research done *while* coding can't be capitalized. |
| **Development** (the actual *building*) | **Capitalize** — but only if the recognition criteria are met (IAS 38.57: technical feasibility, intent + ability to complete and use/sell, **probable future economic benefits**, resources available, cost measurable reliably). |

Morre's sharpened version of "probable future economic benefits": **you must be able to point to DIRECT revenue** from what you capitalize.

- **Standalone new product / brand-new platform from scratch** → easy to justify (clear direct revenue).
- **Improvement of an existing system** → **must be expensed**, not capitalized. Going 2.0 → 2.1 "just making it better" / more desirable = **no**. A **commercial version bump is not a basis** — capitalization requires a **new capability that will touch the market**, not a marketing-driven version number.
- **A platform/layer that only enables modules** → has **no direct revenue of its own**, so it's hard/impossible to capitalize directly even though it's a technical prerequisite. This is the messy core case.

---

## 3. Capitalize first, then write off (and the one-way trap)

The operating rule Morre lands on:

1. **Capitalize first.** When you start building something you believe will generate revenue, capitalize it.
2. **Start depreciating when it's "done."** The trigger is the **commercial layer** — when it has its intended functionality / **touches the market**. Then write it off (depreciate) over the local useful life (5 yrs in Sweden, §5). You may capitalize over 6–7 years of build, then depreciate over 5 once the product is done.
3. **If it turns out there's no direct revenue → write it off.** A defensible bet, not a guarantee.

> **The trap:** if you **don't** capitalize a new module **when you build it**, you can **never capitalize it later.** So the safe rule of thumb: *always capitalize what you think will make revenue, and be ready to write it off.*

---

## 4. Time tracking is mandatory

To capitalize, you **must track internal vs external hours**. Bookkeeping capitalization is based on **how long it took** (hours × cost), even though Morre philosophically prefers "value of what you did, not how long it took." No time tracking → no defensible capitalization.

---

## 5. Country differences — Done1 vs Done2 (the key new finding)

Capitalization rules differ **by country**, so each legal entity (**Done1**) must follow its **local** rule:

| Country | Write-off period | Extra condition |
|---|---|---|
| **Norway** | ~10 years | — |
| **Sweden** | **5 years** (default useful life if not reliably determinable) | **Must move an equal amount from free equity to a restricted *fond för utvecklingsutgifter* (English: *development expenditure fund* — *bundet eget kapital* / restricted equity).** Capitalize 10M → tie up 10M of own equity; the fund is released back to free equity as the asset depreciates. |

The Swedish reserve requirement is the anti-abuse mechanism: it forces you to **show your own money**, so a company can't inflate equity by capitalizing fictitious value and stay solvent on paper. (K2 does **not** permit capitalization at all — capitalizing requires K3. → confirms the "do it properly or not at all" stance.)

**Done2 (IFRS group):** because Done1 entities follow different national rules, the group must **pick one IFRS rule and "twerk"/translate** every entity onto it — a **transformation step**, conceptually like FX translation. So the **Done1 (legal, per country) / Done2 (group IFRS, translated)** split holds here exactly as it does for IFRS 16. (E.g. a Norwegian entity and a Swedish entity both buying dev from Ukraine get **different Done1** treatments, reconciled at Done2.)

---

## 6. The real-world / materiality reality

Chris pressed on "what actually happens vs the rule book." Morre: "all of the above."

- **Companies fake it.** Many capitalize mere improvements that should be expensed. Morre believes **Formpipe has ~58M capitalized**, likely including improvements that shouldn't qualify.
- **Auditors often aren't proficient** — it's complex, so it isn't reliably caught.
- **Worst case if caught: write off the capitalized amount** (e.g. the full 58M). Beyond the write-off it's a **materiality + judgment** matter (you need a defensible basis / "probe"); effectively a **board/CFO/CEO decision** — the cash is already spent, so capitalizing is a *defensible bet*, not free money.
- **What makes it defensible:** if a new module drives a **visible revenue increase**, auditors tend to accept it; if large amounts were capitalized and **nothing shows** (no revenue, no value change), that invites scrutiny and write-off.

---

## 7. Why this is a strong argument for the X-item / license model

The punchline Morre and Chris agreed on: **you can only capitalize defensibly if you can attribute revenue to what you built** — and that requires structure.

- **Licensing** (modules you can switch on/off — e.g. an inbox module) → a **direct correlation** between a module and its revenue. Capitalization is provable.
- **X-package** (modules always sold bundled) → you **cannot** isolate which module carries the direct revenue → capitalization is unprovable.
- The **Virtual Item (vItem) / X-pact / license / projects / recurring-billing** model gives the **anchors** to track module-level revenue. Without it, "you have no control" and "you can't" capitalize.

> **Strategic use:** this is a strong "back-pocket" argument for setting up BC the recommended way (license + services structure). *"Why structure it like this?"* → because without it you cannot track or defend capitalization. Ties capitalization to the [X-item model](../project-docs/node-xitem_v1.0.md) and the S-R-S tracking thesis.

---

## 8. Open / to revisit

- IAS 38 is flagged as an under-covered standard in the ergon library (alongside IFRS 2 / IAS 23) — this note is the first capture; a full chain/lens can follow if capitalization becomes an active workstream.
- The Done2 translation mechanics for multi-country capitalization (§5) parallel IAS 21 FX translation — worth a worked example when consolidation is built.
- Morre's dependency-graph framing ("two graphs with cross-sections", platform → modules → market touch) is his S-R-S/xItem lens applied to capitalization; not formalized here.

---

## Link — Part 4 (Lease reporting)

This transcript (Part 3) ends as Chris says *"can I show you what I've done?"* — the **Part 4 lease-reporting** working session is the separate recording `Call with Lars Mårelius (10).docx`, now processed and folded into the lease reports ([`ifrs-16-uk-frs102-bc-implementation`](ifrs-16-uk-frs102-bc-implementation_v1.0.md) v1.3, [`ifrs-16-leased-assets-research`](ifrs-16-leased-assets-research_v1.0.md)). Part 4 also touched capitalization briefly: Morre noted **amortization** (write-off of capitalized intangibles) is the **same principle as depreciation** (write-off of purchased assets) — the term differs, the mechanic doesn't.

---

## Sources

- [Recognition and Cost of Intangible Assets — IAS 38 (IFRS Community)](https://ifrscommunity.com/knowledge-base/recognition-and-cost-of-intangible-assets/)
- [Research and development — IAS 38 (ACCA)](https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f7/technical-articles/rd.html)
- [Fond för utvecklingsutgifter (FAR Online)](https://www.faronline.se/dokument/rattserien/redovisa-ratt/f/rr_fondforutvecklingsutgifter/)
- [Egenupparbetade immateriella tillgångar — fond för utvecklingsutgifter (Accountor)](https://www.accountor.com/sv/sweden/nyheter/egenupparbetade-immateriella-tillgangar-fond-utvecklingsutgifter)
- [Bokföra fond för utvecklingsutgifter / aktivering av IT-investeringar (PwC)](https://blogg.pwc.se/foretagarbloggen/bokfora-fond-utvecklingsutgifter-aktivering-it-investeringar)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-22 | Initial — summary of Part 3 (Capitalization / IAS 38) from the 2026-06-22 Morre call. Research-vs-development + direct-revenue test, capitalize-first-then-write-off rule, time tracking, country differences (Norway 10y / Sweden 5y + *fond för utvecklingsutgifter*), Done1/Done2 translation, real-world materiality/audit reality (Formpipe ~58M), and the X-item/license argument. Part 4 (lease reporting) not in transcript — handoff noted. |
