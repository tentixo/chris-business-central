# FGGE Scope and Toolchain — What Goes Where

**Version**: 1.0
**Created**: 2026-04-01
**Purpose**: Define FGGE's boundary (Done2 cut-off), what BC handles, what FGGE scripts add, what Power BI shows, and what's outside FGGE scope (Done3). Eliminates the assumption that a "fancy consolidation tool" is needed.
**Provenance**: W-H-S sessions on S-R-S governance, IFRS ergon chains, IC elimination analysis, xItem taxonomy

---

## The Cut-Off: Done2

FGGE's boundary is **Done2 = all numbers correct.** Everything after is presentation, formatting, and filing — a different problem domain.

```
Done1 (entity-level close)     → Each entity produces IFRS-compliant trial balance in BC
Done2 (group numbers correct)  → FGGE's domain. Consolidated trial balance is correct.
Done3 (report production)      → Outside FGGE. Annual report formatting, ESEF, tax filing.
```

---

## What Done2 Produces

When Done2 is complete, BC's Consolidation Company contains:

```
A CORRECT CONSOLIDATED TRIAL BALANCE

  All entities consolidated (IFRS 10 scope)
  All PPA adjustments booked (IFRS 3)
  All IC eliminated — vanilla + extra (IFRS 10.B86)
  FX translated at correct reference rates (IAS 21)
  Impairment recognized where needed (IAS 36)
  Revenue correctly recognized per xtValue pattern (IFRS 15)
  Leases on balance sheet (IFRS 16)
  Insurance contracts measured (IFRS 17, if applicable)
  Deferred tax on ALL adjustments (IAS 12)

  = A set of GL BALANCES that are IFRS-compliant.
    Every number traceable to a journal entry.
    Every journal entry traceable to an ergon in the master chain.
```

This is a **flat list of account balances.** That's ALL that downstream tools need. Tables, notes, commentary, ESEF — all downstream formatting of these balances.

---

## The Monthly Cycle (Reverse and Re-Do)

Each month-end, the bookkeeper:

```
1. Each entity closes (Done1) → trial balance in BC
2. Consolidation company: REVERSE prior period's consolidation adjustments
3. Re-run: IC elimination (fresh — IFRS 10.B86 requires from scratch)
4. Re-run: FX translation (new closing/average reference rates)
5. Re-book: PPA amortization (monthly portion)
6. Re-assess: impairment indicators? New acquisitions? Disposals?
7. Re-calculate: deferred tax on new temporary differences
8. Result: updated consolidated trial balance
```

This is standard bookkeeping:
- BC supports recurring journals (auto-reverse)
- FGGE scripts recalculate adjustments with updated amounts
- Each run produces journal entries posted to BC Consolidation Company
- Repeat each period

Not complex software. A bookkeeper does this. FGGE scripts make it faster, less error-prone, and auditable.

---

## The FGGE Stack

### 1. The Graph (knows the structure)

```
node:org          → Legal entities, governance properties, CGU, KBR headroom
node:xitem        → What we sell (g/v/h taxonomy), SSP, cost, posting groups
edge:org-org      → Bilateral relationships: ownership, IC trading, lending,
                    guarantees, PPA, disposal, pipeline (tamagos_summary)
doc:tamagos       → Pre-contract deals: Ladder Gate, T, Vector Events
edge:ind-org      → Board members, KMP, auditors (personal liability links)
```

The graph knows WHO is in the group, WHO owns WHOM at what %, WHO trades with WHOM selling WHAT xItems, and WHERE the Tamagos pipeline stands.

### 2. The Ergon Chains (know what to do)

12 IFRS chains + master chain defining WHAT to do, WHEN, WHO does it (IND/MACH), in WHAT ORDER:

```
Master chain execution order per reporting period:

Phase 1: IFRS 10 (Scope)           → who is in the group
Phase 2: IFRS 3 + IFRS 5           → acquisitions + disposals
Phase 3: IAS 21, IC Elim, IAS 36,  → adjustments (parallel)
         IFRS 15, IFRS 16, IFRS 17,
         IAS 19, IAS 37
Phase 4: IAS 12 (Tax)              → deferred tax on ALL adjustments
Phase 5: IFRS 8, IAS 33, IAS 24,   → completion (parallel)
         ABL KBR
Phase 6: Done2 complete             → consolidated trial balance
```

Each ergon specifies: input data (from graph + BC), calculation, output (journal entries or anomalies), HitL moments (where human judgment required), Rim consequence (what happens if wrong).

### 3. The Scripts (calculate)

Python or AL scripts that read from the graph + BC and produce journal entries:

| Script | What it calculates | Input | Output |
|---|---|---|---|
| IC matching | Compare both sides of every IC pair | BC Customer/Vendor Ledger + edge:org-org | Match report. Anomalies for mismatches. |
| IC unrealized profit | Markup × unsold inventory at buyer | edge:org-org → sells_to.price + xItem.cost + BC inventory | Journal: Dr COGS / Cr Inventory |
| FX translation | Closing rate × BS, average rate × P&L | BC trial balance + Riksbanken/ECB rates | Translated balances + FCTR movement |
| NCI calculation | Graph traversal × ownership percentages | edge:org-org → owns (chain multiplication) | NCI % per entity → BC Business Unit |
| Deferred tax | Temp diff identification × tax rates | All Phase 3 outputs + local tax rates | DTA/DTL journals |
| PPA amortization | Monthly portion of identified intangibles | edge:org-org → ppa.intangibles[] | FA depreciation (already in BC if FA card set up) |
| Impairment indicators | External + internal data scan | Market data, BC performance, interest rates | Indicator report → trigger or not |
| KBR monitor | Equity vs 50% of share capital | node:org → equity_latest, registered_share_capital | Alert if headroom < threshold |

These scripts are NOT complex. Each is a focused calculation reading from known data locations and producing journal entries. A senior developer builds the full set in weeks, not months.

### 4. The Monitors (detect problems — Entropy Patrol)

Continuous or periodic Walkers that watch for Rim danger:

| Monitor | What it watches | Cadence | S-R-S zone |
|---|---|---|---|
| KBR headroom | Equity vs share capital threshold | Monthly (daily recommended) | Shield (CRITICAL — personal liability) |
| FCTR sensitivity | FX impact on equity via translated goodwill/reserves | Monthly | Reserve |
| IC balance matching | Zero-tolerance IC reconciliation | Monthly | Shield |
| Impairment indicators | Market cap vs book value, revenue decline, rate changes | Each reporting date | Shield + Reserve |
| Reference rate divergence | Riksbanken vs ECB consistency | Monthly | Shield |
| Hyperinflation | Cumulative inflation in subsidiary currencies | Quarterly | Shield |
| Functional currency triggers | Revenue/cost mix shifts | Annual + triggers | Shield |
| Rate feed health | Daily rate availability | Daily | Shield |
| Lease count vs contracts | Missing embedded leases | Quarterly | Shield |
| DTA recoverability | DTA relative to equity + future profitability | Quarterly | Reserve |

### 5. The Shaw Lenses (show Reality — Power BI)

Power BI dashboards reading from BC consolidated data + graph:

| Shaw Lens | S-R-S zone | What it shows |
|---|---|---|
| Rim Status | Shield | KBR headroom, covenant compliance, close progress checklist, IC matching status, overdue ergons |
| Cash Forecast | Reserve | 13-week rolling, DSO/DPO/DIO, covenant headroom, lease commitments, FX sensitivity |
| Risk Heatmap | Reserve | Impairment headroom per CGU, DTA exposure, concentration risk, country risk |
| Segment Discovery | Sword | Clusters from xItem × ORG.buyer × edge data. Margin by cluster. Where value concentrates. |
| Pipeline | Sword | Tamagos by Ladder Gate, T/dT/dt, weighted pipeline value, dBFFB/dt, Gray→White conversion |
| Revenue Analysis | Sword | By xItem type (g/v/h), by geography, by buyer type. Growth trends. Unit economics. |

**Analysis stays in Power BI, NOT in the consolidation process.** The numbers in BC are Stockdale truth (brutal facts). The Shaw Lenses let the CODM see them from three angles without massaging.

### 6. BC Does the Bookkeeping

BC's role — the engine:

| BC function | What it does |
|---|---|
| General Ledger | Books all journal entries (entity-level + consolidation) |
| Business Units | Consolidation setup per entity (NCI %, currency, method) |
| Consolidation function | Vanilla IC elimination, entity aggregation |
| Fixed Assets | ROU assets (IFRS 16), PPA intangibles, goodwill (depreciation/amortization) |
| Subscription Billing | Recurring revenue (vItem.e-svc), contract deferrals |
| Jobs/Projects | hItem delivery (time tracking, WIP, project revenue) |
| Sales/Purchase | Transaction processing, IC trading |
| Bank Account Cards | Loans (AST/DBT), lease liabilities, IC lending |
| Currency Exchange Rates | Reference rate table (Riksbanken/ECB feed) |
| Posting Groups | Gen. Prod. (= xItem type), VAT Prod. (= vat_class), Gen. Bus. (= ORG type) |

**FGGE tells BC WHAT to book. BC books it.**

---

## What FGGE Does NOT Build

| Outside FGGE scope | Why | What handles it |
|---|---|---|
| **Annual Report formatting** | Done3 — presentation, not numbers | AR software, Word, InDesign |
| **Disclosure management** (notes templating) | Done3 — formatting + workflow | AR software or manual (Word) |
| **ESEF/iXBRL tagging** | Done3 — regulatory filing format | Parseport, Workiva, or consolidation platform ESEF module |
| **Tax return filing** | Separate domain — tax compliance | Tax software (Wolters Kluwer, Thomson Reuters) |
| **CbCR filing** | Tax filing | Tax software |
| **TP documentation** | Tax documentation | TP tools + legal |
| **Audit software** | Auditor's tools | Auditor's own tools (CaseWare, etc.) |
| **CRM / pipeline management** | Sword operational tool | CRM feeds Tamagos data INTO FGGE graph |

---

## The "Fancy Tool" Question Resolved

### What people think they need a specialized consolidation tool for

| Claimed need | What actually does it | Fancy tool needed? |
|---|---|---|
| "Consolidation engine" | BC's GL + recurring journals + FGGE scripts | **No** |
| "IC elimination" | BC vanilla + FGGE scripts for extra | **No** |
| "FX translation" | BC currency functions + FGGE rate policy | **No** |
| "Multi-entity consolidation" | BC Business Units + FGGE graph (scope, NCI) | **No** |
| "IFRS adjustments" | BC journals calculated by FGGE ergon chains | **No** |
| "Roll-forward / movement schedules" | Python script: read opening + journals → produce movement table | **No** |
| "Financial statement tables" | Power BI or Python: read trial balance → format tables | **No** |
| "Disclosure management" | Outside FGGE scope (Done3) | **Maybe** — depends on group size |
| "ESEF tagging" | Outside FGGE scope (Done3) | **Yes** — specialized tool needed |
| "Financial analysis" | Power BI Shaw Lenses (NOT in consolidation tool) | **No** — and SHOULD NOT be in the same tool |

### When specialized tools earn their keep

```
SMALL GROUP (≤10 entities):
  BC + FGGE scripts + Power BI + ESEF tool
  Done2: fully handled
  Done3: Word + ESEF tool (Parseport ~SEK 50-150k/year)

MEDIUM GROUP (10-30 entities):
  BC + FGGE scripts + Power BI + ESEF tool
  Done2: fully handled
  Done3: notes templating becomes painful in Word → evaluate disclosure management
  Decision point: is notes templating worth a tool license?

LARGE GROUP (30+ entities):
  BC + FGGE scripts + Power BI
  Done2: still handled by BC + FGGE
  Done3: disclosure management + ESEF → specialized tool (Lucanet/Tagetik ESEF module)
  OR: keep BC + FGGE for Done2, add Parseport for ESEF, add AR tool for notes

  The consolidation platform (Lucanet/OneStream/Tagetik) replaces the WHOLE stack
  (Done2 + Done3) but charges accordingly. FGGE's position: prove that BC + scripts
  can't handle Done2 FIRST, then evaluate the platform for Done3 if needed.
```

### The cost comparison

```
FGGE stack:
  BC Essential license:     already owned
  FGGE graph + scripts:     development cost (one-time) + maintenance
  Power BI Pro:             ~SEK 1,200/user/year
  ESEF tool (Parseport):    ~SEK 50-150k/year
  Total recurring:          SEK 100-300k/year + development amortization

Consolidation platform:
  Lucanet / Tagetik / OneStream: SEK 500k-2M+/year (license + implementation)
  + still need BC for entity-level bookkeeping
  + still need Power BI for analysis (the platform's BI is not as good)
  Total recurring:          SEK 700k-2.5M+/year

Delta: SEK 400k-2M/year saved by FGGE approach.
The question: does the group NEED what the platform provides beyond Done2?
If only ESEF → just buy ESEF tool. Don't buy the whole platform.
```

---

## The Handoff: Done2 → Done3

```
FGGE completes Done2:
  BC Consolidation Company has correct, IFRS-compliant consolidated trial balance.
  Every number traceable through ergon chain → journal entry → source data.
  Shaw Lenses (Power BI) show S-R-S views.
  Monitors confirm Rim intact.

HANDOFF to Done3:
  Export from BC (OData API / Excel / Python):
    - Consolidated trial balance (all accounts with balances)
    - Comparative data (prior period, same structure)
    - Movement schedules (opening → journals → closing, per account group)
    - Segment data (trial balance filtered per segment ctx-v)
    - Sub-ledger details for notes (aging, maturity, concentration)

  Done3 tools receive and format:
    - Annual Report software → tables, notes, commentary, design
    - ESEF tool → iXBRL tagging of the annual report
    - Tax software → tax returns, CbCR, TP documentation
    - Auditor → access to BC + graph + ergon chain documentation
```

---

## FGGE's Value Proposition (Summary)

| Layer | What FGGE provides | What it replaces |
|---|---|---|
| **Structure** | Graph (ORG, xItem, edge:org-org, Tamagos) | Spreadsheets tracking group structure, ownership, IC relationships |
| **Process** | Ergon chains (12 IFRS + master) | Tribal knowledge of "what to do when" |
| **Calculation** | Scripts (IC matching, unrealized profit, FX, DT, NCI) | Manual Excel calculations, copy-paste errors |
| **Monitoring** | Walkers (KBR, FCTR, impairment, IC matching, rates) | "Nobody was watching" → Carillion, Wirecard |
| **Insight** | Shaw Lenses (Power BI: Shield/Reserve/Sword views) | Static monthly reports, budget-vs-actual (noise) |
| **Compliance** | Ergon chains define what each IFRS standard requires, with HitL flags | "We think we're compliant" without structured verification |

**What FGGE does NOT replace:**
- BC (the bookkeeping engine)
- Human judgment (HitL moments in every ergon chain)
- Done3 tools (formatting, ESEF, tax filing)
- The auditor

**What FGGE eliminates:**
- The assumption that a "fancy consolidation tool" is needed for Done2
- Ghost terms in governance (replaced with grounded xItem/xtValue vocabulary)
- Budget-as-governance (replaced with S-R-S + Shaw Lenses)
- "Nobody was watching" failures (replaced with continuous monitors)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — Done2 cut-off, FGGE stack (graph + chains + scripts + monitors + lenses), BC role, Done3 handoff, "fancy tool" assessment, cost comparison, value proposition |
