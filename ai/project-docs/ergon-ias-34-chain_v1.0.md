# Ergon Chain: IAS 34 — Interim Financial Reporting

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 34 (complete standard), IFRIC 10 (interim impairment)
**Intent**: Define how the master chain executes at INTERIM reporting dates (Q1, H1, Q3). What's the same as annual, what shortcuts are allowed, what's mandatory. This is the FLIGHT SCHEDULE of the master chain.
**Master chain**: ergon-ifrs-master-chain_v1.0.md — IAS 34 governs the CADENCE, not a separate phase.

---

## When It Applies

```
NASDAQ Stockholm Rulebook for Issuers:

  Q1 report: ≤2 months after Q1 end (May 31 for calendar year)
  H1 report (halvårsrapport): ≤2 months after H1 end (Aug 31)
    → MUST comply with IAS 34 (mandatory for listed, NASDAQ rule)
  Q3 report: ≤2 months after Q3 end (Nov 30)
  Annual report: ≤4 months after year-end (Apr 30)

  The master chain runs at EACH of these dates.
  IAS 34 defines what's DIFFERENT at interim vs annual.
```

---

## Core Principle: Discrete vs Integral

```
IAS 34.28: Each interim period is a DISCRETE reporting period.

  Revenue: recognize when earned (same as annual — IFRS 15 applies normally).
  Costs: recognize when incurred (same as annual — don't spread annual costs evenly).

  DO NOT:
    - Defer a cost at interim that wouldn't be deferred at annual
    - Accrue revenue at interim that wouldn't be accrued at annual
    - Anticipate year-end adjustments ("we'll catch up in Q4")

  ONE EXCEPTION — Income tax:
    IAS 34.30(c): Use ESTIMATED ANNUAL EFFECTIVE TAX RATE at interim.
    Don't calculate full deferred tax each quarter — estimate the
    annual rate and apply it to interim pre-tax profit.
    This IS the integral approach — tax is spread based on best annual estimate.
```

---

## The Master Chain at Interim vs Annual

| Ergon chain | Annual (full) | Interim (IAS 34 shortcuts) |
|---|---|---|
| **IFRS 10 (Scope)** | Full control assessment for all entities | Same — no shortcut. Scope must be correct every quarter. |
| **IFRS 3 (Acquisitions)** | Full PPA | Same — if acquisition occurs at interim, PPA starts immediately (provisional amounts OK). |
| **IFRS 5 (Held for sale)** | Full assessment | Same — if criteria met at interim, classify immediately. |
| **IFRS 8 (Segments)** | Full disclosure | Condensed — same segments, less detail. Revenue by segment required. |
| **IFRS 13 (Fair Value)** | Full hierarchy + sensitivity | Same measurement. Disclosure can be condensed. |
| **IFRS 15 (Revenue)** | Full five-step model | Same — no shortcuts. Revenue recognized per xtValue pattern. Seasonal businesses: do NOT smooth. |
| **IFRS 16 (Leases)** | Full ROU + liability | Same — depreciation + interest each quarter. New leases recognized when they start. |
| **IFRS 17 (Insurance)** | Full measurement | Same — CSM release each quarter. |
| **IAS 21 (FX)** | Full translation at closing + average rates | Same — translate at interim closing rate (BS) and interim average (P&L). FCTR moves each quarter. |
| **IAS 36 (Impairment)** | **Annual goodwill test** (mandatory) | **NO annual test at interim** — UNLESS indicators exist. If indicators found → test immediately. **IFRIC 10: goodwill impairment at interim CANNOT be reversed at year-end.** |
| **IAS 12 (Deferred Tax)** | Full deferred tax calculation | **SHORTCUT: estimated annual effective tax rate** applied to interim pre-tax profit. Full DT calculation only if material events (acquisition, impairment). |
| **IC Elimination** | Full elimination from scratch | Same — eliminate every period. Unrealized profit recalculated. |
| **IAS 19 (Pensions)** | Full actuarial valuation | **SHORTCUT: roll forward** prior annual valuation. Update for significant events (plan amendment, curtailment, settlement). Full revaluation at year-end. |
| **IAS 37 (Provisions)** | Full assessment | Same — if new obligation or change in estimate at interim → recognize/adjust. |
| **IAS 24 (Related Party)** | Full disclosure | Condensed — disclose material RPTs during the interim period. |
| **IAS 33 (EPS)** | Full calculation | Same — but based on interim net income. |
| **IFRS 9 (Financial Instruments)** | Full ECL + classification | Same measurement — ECL updated each quarter with latest forward-looking info. No shortcut. |
| **ABL KBR** | Full equity check | Same — KBR has no concept of "interim shortcut." Equity must be monitored CONTINUOUSLY. |

---

## What's IN a Condensed Interim Report (IAS 34.8)

```
MINIMUM content:

  a) Condensed statement of financial position (BS)
  b) Condensed statement of profit or loss and OCI
  c) Condensed statement of changes in equity
  d) Condensed statement of cash flows
  e) Selected explanatory notes

"Condensed" = same line items as annual, or at minimum the headings
and subtotals from the most recent annual report.
Can aggregate more than annual — but must show all material items separately.

COMPARATIVES:
  BS: compare to most recent annual year-end (not prior interim)
  P&L/OCI/equity: compare to same interim period PRIOR YEAR
  Cash flow: compare to same interim period prior year
  YTD also shown (H1 = 6 months, 9M = 9 months)
```

---

## Selected Explanatory Notes (IAS 34.15-15C)

```
IAS 34.15: Notes should include explanation of events and transactions
SIGNIFICANT to understanding the changes since the most recent annual report.

Not a repeat of annual notes — an UPDATE.

MANDATORY disclosures (IAS 34.16A):

  a) Same accounting policies as annual (or describe changes + impact)
  b) Seasonal/cyclical nature of operations (if applicable)
  c) Unusual items: nature and amount
  d) Changes in estimates (e.g., revised ECL, revised provisions)
  e) Issuances, repurchases, repayments of debt + equity
  f) Dividends (total + per share)
  g) Segment revenue and result (IFRS 8)
  h) Events after interim period end (IAS 10-style)
  i) Changes in composition of the group (acquisitions, disposals, restructuring)
  j) Changes in contingent liabilities or contingent assets
  k) Fair value disclosure for financial instruments (IFRS 7 condensed)
  l) IFRS 16: new significant leases
  m) Revenue disaggregation (IFRS 15) — if useful for understanding interim

For H1 (halvårsrapport, IAS 34 mandatory for NASDAQ):
  Auditor REVIEW (not full audit) — gives limited assurance.
  Q1/Q3: typically UNREVIEWED (though some companies have auditor review).
```

---

## The IFRIC 10 Trap — Interim Impairment is Permanent

```
IFRIC 10: If goodwill is impaired at an interim date:
  The impairment CANNOT be reversed at the subsequent year-end
  (or any later period).

  IAS 36.124 says: goodwill impairment never reversed.
  This applies EQUALLY to interim and annual.

  Practical consequence:
    If in Q2 you identify indicators and test goodwill → impairment 50M.
    At year-end: conditions improve, headroom now positive.
    → You CANNOT reverse the 50M. It stays impaired.

  This makes interim indicator assessment CRITICAL.
  If indicators exist at interim → you MUST test.
  If you DON'T test and the impairment was real → auditor catches it at year-end.
  If you DO test and impair → it's permanent even if temporary.

  Shield monitors: indicator assessment MUST happen at EVERY interim date.
  Not just annual. The KBR chain runs every quarter — goodwill headroom
  must be checked every quarter.
```

---

## The Tax Shortcut (IAS 34.30(c)) — Estimated Annual Effective Rate

```
Instead of full IAS 12 deferred tax calculation each quarter:

  1. Estimate the ANNUAL effective tax rate for the full year.
     Consider: statutory rates, permanent differences, DTA recoverability,
     different rates in different jurisdictions.

  2. Apply this estimated rate to interim pre-tax profit.
     Interim tax expense = interim pre-tax profit × estimated annual rate.

  3. Adjust each quarter as the estimate improves.
     Q1: first estimate. Q2: refine. Q3: refine further. Q4: full calculation.

  EXCEPTION: discrete items recognized in the period where they occur.
    - Tax effect of acquisition (IFRS 3) → in the quarter of acquisition
    - Tax effect of impairment → in the quarter of impairment
    - Change in tax rate (enacted during the year) → in the quarter of enactment
    - IFRIC 23 uncertain position resolved → in the quarter of resolution

  This is the ONLY significant shortcut in interim reporting.
  Everything else follows annual rules.
```

---

## The Pension Roll-Forward (IAS 34 + IAS 19)

```
At interim, most groups do NOT obtain a new actuarial valuation.
Instead:

  Roll forward from the most recent annual valuation:
    Opening DBO (from annual actuarial report)
    + Service cost (estimated based on annual rate / 4 per quarter)
    + Interest cost (opening DBO × discount rate / 4)
    − Benefits paid during interim period
    ± Significant events (plan amendment, curtailment, settlement)
    = Estimated DBO at interim

  Plan assets:
    Opening (from annual)
    + Contributions during interim
    + Expected return (opening × discount rate / 4)
    − Benefits paid
    ± Significant market movements (if material → estimate asset FV)
    = Estimated plan assets at interim

  Remeasurements (OCI):
    If no significant changes → may be zero at interim.
    If material event (large rate move, market crash) → estimate remeasurement.

  Full actuarial valuation at YEAR-END:
    True-up: actual vs rolled-forward → adjustment in Q4 (or at year-end close).

  Country-specific:
    UK: trustees may provide interim funding updates.
    DE: actuaries sometimes provide semi-annual updates for Direktzusage.
    SE Alecta: Alecta publishes its funding ratio quarterly → monitor.
```

---

## FGGE Flight Schedule (Master Chain Cadence)

```
The master chain runs 4 times per year. IAS 34 defines the rules:

Q1 (due ≤ May 31):
  Full: scope, revenue, FX, IC elimination, IFRS 9 ECL, KBR
  Shortcut: tax (estimated annual rate), pensions (roll-forward)
  Check: impairment indicators (if found → test, permanent if impaired)
  Output: condensed Q1 report (unreviewed)

H1 (due ≤ Aug 31):
  Full: same as Q1 but with AUDITOR REVIEW (limited assurance)
  Must comply with IAS 34 (NASDAQ mandatory for halvårsrapport)
  More disclosure than Q1 (IAS 34.16A full list)
  Output: halvårsrapport (reviewed)

Q3 (due ≤ Nov 30):
  Same as Q1 cadence
  Output: condensed Q3 report (unreviewed)

Annual (due ≤ Apr 30):
  FULL everything. No shortcuts.
  Full IAS 12 deferred tax.
  Full actuarial valuation (IAS 19).
  Full goodwill impairment test (IAS 36 annual).
  Full IFRS 7 disclosures.
  Full IAS 34 N/A (annual report, not interim).
  AUDITOR FULL AUDIT.
  Output: annual report + ESEF/iXBRL
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Are all 4 reporting dates met? Same accounting policies as annual? Impairment indicators checked at EACH interim? IFRIC 10 respected (no reversal)? Tax shortcut reasonable (estimated rate vs actual trend)? | NASDAQ deadlines are hard Rim (disciplinary action for late reporting). Wrong interim = restatement risk at annual. |
| **Reserve** | Interim cash flow: is cash position deteriorating quarter by quarter? Interim KBR: equity headroom trend (improving or worsening?). ECL trend: receivables aging getting worse? | Quarterly trend analysis: problems show up in trends before they show up in annual numbers. |
| **Sword** | Quarterly revenue by xItem type and segment: where is growth? Where is decline? Pipeline (Tamagos) conversion rate per quarter: improving or stalling? | Sword reads quarterly as the DISCOVERY cadence — each quarter reveals whether Vectors are hitting or missing. |

---

## Node/Edge Properties

**No new properties.** IAS 34 governs WHEN and HOW the existing properties are updated. The same properties on node:org, edge:org-org, and node:xitem are populated at each interim date using the rules above (full or shortcut).

One addition to node:org for tracking:

| Field | Type | x-history | Why |
|---|---|---|---|
| `interim_reporting_dates` | array of dates | no | Calendar of Q1/H1/Q3/Annual reporting dates for this entity's fiscal year. Shield monitors: on track? |
| `estimated_annual_tax_rate` | decimal | yes | IAS 34.30(c) estimated annual effective rate. Updated each quarter. Shield: is the estimate reasonable vs prior year actual? |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Late interim report | NASDAQ disciplinary action. MAR: delayed inside information? |
| Different accounting policy at interim vs annual | Restatement at year-end. Auditor qualification. |
| Impairment indicators ignored at interim | IFRIC 10: if impairment should have been recognized → it's permanent. Year-end catch-up doesn't help. |
| Goodwill impaired at interim, reversed at annual | IAS 36.124 + IFRIC 10 VIOLATION. Never reverse goodwill impairment. |
| Tax estimate wildly wrong | Interim P&L misleading. Q4 "true-up" creates surprise. |
| Revenue smoothing (spreading annual revenue evenly) | IAS 34.28 violation. Revenue when earned per IFRS 15, not smoothed. |
| Pension not rolled forward at interim | Stale obligation → equity wrong → KBR wrong |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — interim cadence (NASDAQ Q1/H1/Q3/Annual), master chain shortcuts per standard, IFRIC 10 trap, tax estimated rate, pension roll-forward, flight schedule, no new properties (governs cadence not data) |
