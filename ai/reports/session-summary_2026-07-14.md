# Session Summary — 2026-07-14

**Span**: 2026-07-13 → 07-14 (one continuous session) · **Risk**: LOW
**Focus**: MB-800 study-plan execution — Morre Call 16 fold-in, then Fixed Assets + Dimensions sandbox exercises, testing playbooks, and strategic-doc updates.

---

## Accomplishments

1. **Morre Call 16 (dependency-graph teaching) folded into all docs** — foundation spine (number series → CoA/Direct Posting → posting groups → journals-vs-documents → VAT settlement), **Rim-vs-Crafted** golden rule, **dimensions = 8 tag fields** (exam-vs-Morre friction resolved), **Cost Accounting** (non-exam, Formpipe), account categories, year-end close. Captured in internal playbook **v1.4**, client playbook **v0.4**, gap-analysis **v1.3**, study schedule **v1.1** (+ `docs/FGGE-Machinery_v4.png` reference). Added `ai/docs/requirements.txt` and regenerated branded PDFs.
2. **Sprint 1 — Fixed Assets ✅🟢** — ran the full lifecycle **solo**: acquisition (Route 1 purchase invoice) → 3× monthly depreciation → disposal (**gain 1,000 → 3973**), Book Value 57,000 verified via FA Statistics. Debugged ~8 BC quirks unaided.
3. **Sprint 2 — Dimensions ✅🟢** — all six mechanics **solo**: create+values, default-on-FA, global-vs-shortcut, blocking combinations, **dimension correction** (RIM-vs-crafted live — re-tagged a posted entry ADM→SALES, amount untouched), default priorities.
4. **Milestone Gate 1 (FA + Dimensions green) hit ~3.5 weeks early** (was due 7 Aug).
5. **Testing playbooks** — FA **v1.4** (all field notes folded in at the point of pain) + new **Dimensions v1.0**. Established the **per-session testing-playbook convention** (`ai/guides/<topic>-testing-playbook.md`).
6. **Strategic/tactical docs updated** — study schedule (Sprints 1 & 2 done, exam pinned to **week of 9 Nov 2026**), gap-analysis v1.3, **FLIGHT-PLAN v1.2** (new Progress block, "ahead of schedule").
7. **Housekeeping** — `.gitignore` rule for ad-hoc screenshots; PDF-gen requirements pinned.

## Key decisions
- **Per-session hands-on testing playbook** convention (memory: `feedback-playbook-per-session`).
- **Cost Accounting = non-exam / Formpipe-driven** — not a cert study item.
- **Exam pinned to the week of 9 Nov 2026** (early-mid Q4).

## Field-tested gotchas captured (in the FA/Dimensions playbooks)
- Calculate Depreciation nets only vs **posted** entries → **post each month before calculating the next**.
- **Unique Document No.** per FA depreciation posting.
- **No posting groups / no Gen. Posting Type** on FA + balance-sheet lines.
- Reconcile a single asset via **FA Statistics**, not the shared 1250/1259 G/L balance.
- A **global** dim shows as a column; custom/shortcut needs a Dimension-Set drill.
- A dimension needs a **value** (code alone is discarded); you **can't rename** a default.
- Blocking combinations enforced at **post** time (this tenant).

## Commits (today, all pushed to origin/main)
`cd23fae` FLIGHT-PLAN v1.2 · `921e7c3` Dimensions playbook · `967887c` schedule Sprint 2 done · `bc824c6` gitignore screenshots · `bfe0113` FA playbook v1.4.
*(2026-07-13: `7951cca` Call-16 fold-in · `b4aa14a` drop schedule v1.0 · `4a39e01` FA playbook v1.3.)*

## Next session
- **Sprint 3 — Journals & payments** (the heaviest remaining 🔴 gap): payment/cash-receipt journals, apply/undo entries, reversals, **bank reconciliation** → produce `journals-payments-testing-playbook.md`.
- **Open threads**: Cost Accounting sketch (w/ Morre); FA **LVA variant** + **loss disposal**; Lasernet **lease Exercise 2** (A5, needs Morre) — also resolves the open **1267/1269** CONFUSION doc.

## Environment notes
- PDF generator needs Homebrew **`/usr/local/bin/python3.14`** (weasyprint), not the project `.venv`.
- macOS keychain: `git-credential-osxkeychain` prompt appears after a Git/CLT update — **Always Allow** (legit helper; was behind the push hangs today).
