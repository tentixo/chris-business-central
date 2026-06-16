# Ergon Chain: IAS 19 — Employee Benefits (Pensions + Other)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 19 (complete standard), IFRIC 14 (asset ceiling)
**Intent**: Measure and report employee benefit obligations across the group. The critical part: defined benefit pensions — a Ghost that moves equity through OCI without touching P&L. Country-specific pension systems mean EACH subsidiary may have different rules.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — parallel)
**Nature**: COUNTRY-DEPENDENT — pension systems differ materially by jurisdiction. Each subsidiary's obligations depend on local employment law and pension regulations.

---

## Why Country Matters

Unlike most IFRS standards (which apply the same everywhere), IAS 19 interacts with LOCAL pension systems that vary radically:

| Country | Main system | DB or DC? | Complexity for IAS 19 |
|---|---|---|---|
| **Sweden** | ITP1 (born ≥~1979): DC. ITP2 (born <~1979): DB. Alecta manages ITP2 (multi-employer). | Mixed — shifting toward DC | Medium. Alecta ITP2 = multi-employer problem (see below). |
| **UK** | Final salary schemes (legacy DB, mostly closed). Auto-enrolment DC (new). | DB closing, DC growing | HIGH. UK has huge legacy DB obligations + complex funding regulations (The Pensions Regulator). |
| **France** | Indemnités de fin de carrière (IFC) — retirement indemnity. DB by law. Plus IDR (indemnités de départ à la retraite). | DB (legally mandatory) | Medium. Every French entity owes retirement indemnity. Actuarial valuation required. Amount depends on tenure + collective agreement. |
| **Denmark** | ATP (mandatory DC state pension). Company pensions mostly DC (bidragsdefineret). Some legacy DB. | Mostly DC | Low. Unless legacy DB plans exist. |
| **Germany** | Direktzusage (direct promise — DB, unfunded, on BS). Pensionskasse (funded). | DB common (Direktzusage) | HIGH. German DB is often UNFUNDED (no plan assets) → full obligation on BS. Very sensitive to discount rate. |
| **Norway** | OTP (mandatory DC). Legacy ytelsespensjon (DB, mostly closed). AFP (early retirement — complex). | DC growing, DB declining | Medium. AFP multi-employer scheme = similar to Alecta problem. |
| **USA** | 401(k) (DC). Legacy DB plans (some large companies). | Mixed | High if DB exists. ERISA regulations. |
| **Netherlands** | Industry-wide pension funds (DB-like, multi-employer). Complex solidarity mechanisms. | DB characteristics | HIGH. Multi-employer funds with complex risk-sharing → classification challenge. |

**For a Swedish listed group with subsidiaries in multiple countries:** EACH subsidiary's pension obligations must be measured under IAS 19 using LOCAL pension rules + IFRS measurement principles. The GROUP consolidation aggregates all of them.

---

## Chain Overview

```
┌──────────────────────────────────────────────┐
│  STEP 1: INVENTORY ALL BENEFIT PLANS         │
│  Per entity, per country: what plans exist?   │
│  DC or DB? Funded or unfunded?                │
│  Multi-employer?                              │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 2: DEFINED CONTRIBUTION → EXPENSE      │
│  Simple: expense = contributions due          │
│  IAS 19.51-54                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 3: DEFINED BENEFIT → ACTUARIAL VALUE   │
│  External actuary calculates DBO             │
│  Plan assets at fair value (IFRS 13)         │
│  Net deficit/surplus on BS                   │
│  IAS 19.55-119                               │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 4: P&L vs OCI SPLIT                    │
│  Service cost + net interest → P&L            │
│  Remeasurements → OCI (never recycled)        │
│  IAS 19.120-130                              │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 5: SPECIAL CASES                       │
│  Multi-employer (Alecta, NL funds, AFP)       │
│  Asset ceiling (IFRIC 14)                     │
│  Plan amendments / curtailments / settlements │
│  IAS 19.155-171, IFRIC 14                    │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  ONGOING: ASSUMPTION MONITORING              │
│  Discount rate sensitivity                    │
│  Mortality updates                           │
│  Salary growth + inflation                   │
└──────────────────────────────────────────────┘
```

---

## Step 1: Inventory All Benefit Plans [IND + MACH]

```
For EACH entity in the group (each node:org in consolidation scope):

  Identify ALL employee benefit obligations:

  a) Short-term benefits:
     Salary, vacation accrual, bonus accrual, social contributions
     → Expense as incurred. BC handles via payroll. No IAS 19 complexity.

  b) Post-employment — Defined Contribution:
     Entity pays fixed % to external fund. No further obligation.
     → Expense = contributions due for the period. Simple.

     Examples by country:
       SE: ITP1, ITPK, SAF-LO (DC portions)
       UK: Auto-enrolment DC (NEST, NOW Pensions)
       FR: AGIRC-ARRCO mandatory supplementary (DC-like)
       DK: ATP contributions, company DC plans
       DE: Pensionskasse (if DC structure)

  c) Post-employment — Defined Benefit:
     Entity promises a specific benefit. Carries the risk.
     → Complex. Actuarial valuation. Steps 3-5.

     Examples by country:
       SE: ITP2 (Alecta — multi-employer, see step 5)
       UK: Final salary schemes (legacy, mostly closed to new members)
       FR: Indemnités de fin de carrière (IFC) — MANDATORY for all French entities
       DK: Legacy ytelsespensjon plans (rare, closing)
       DE: Direktzusage (direct promise — UNFUNDED, on BS)
       NO: Ytelsespensjon (closing), AFP (multi-employer)

  d) Other long-term benefits:
     Jubilee awards, long-service leave, deferred compensation
     → Simplified DB measurement (IAS 19.153-154)
     → Remeasurements in P&L (not OCI — different from post-employment DB)

  e) Termination benefits:
     Severance when committed to termination plan
     → Recognize when entity can no longer withdraw the offer (IAS 19.165-170)

Record per entity:
  Plan inventory: { plan_name, type (DC/DB), country, funded (yes/no),
                    multi_employer (yes/no), active_members, obligation_estimate }
```

---

## Step 2: Defined Contribution [MACH — trivial]

```
IAS 19.51-54:

  Expense = contributions payable for the period.
  If contributions not yet paid → accrue as liability.
  If prepaid → asset (only to extent of cash refund or future reduction).

  BC handles: payroll posts contributions to expense account (BAS 7411-7419).
  No FGGE script needed. Just validate: are all DC plans correctly expensed?
```

---

## Step 3: Defined Benefit Measurement [external actuary + IND]

```
IAS 19.55-119:

This is WHERE THE COMPLEXITY LIVES. Almost always requires an external actuary.

THREE COMPONENTS on the balance sheet:

  1. Defined Benefit Obligation (DBO):
     Present value of ALL future benefit payments earned to date.
     Calculated using Projected Unit Credit Method (IAS 19.67).

     Key inputs (HitL — each is a judgment):
       a) Discount rate: high-quality corporate bond rate (or govt if no deep market)
          → THE sensitivity driver. 1% change = 10-20% change in DBO.
          → Country-specific: different bond markets, different rates.
            SE: Swedish corporate bonds or govt (iBoxx Sweden, etc.)
            UK: AA-rated corporate bonds (iBoxx Sterling)
            DE: German corporate bonds (iBoxx EUR)
            FR: EUR corporate bonds (same as DE typically)
       b) Mortality tables: country-specific life expectancy
          SE: DUS (Dödlighetsundersökning)
          UK: S3 tables (CMI model for mortality improvement)
          DE: Heubeck tables
          FR: TGH/TGF (INSEE)
       c) Salary growth: expected future salary increases (for final-salary plans)
       d) Inflation: for index-linked benefits
       e) Employee turnover: probability of leaving before vesting

  2. Plan assets (fair value):
     Assets held in a separate fund to pay benefits.
     Measured at fair value per IFRS 13.
       Level 1: quoted equities, bonds
       Level 2: pooled funds with observable NAV
       Level 3: property, private equity, hedge funds

     IMPORTANT: not all DB plans are FUNDED.
       SE ITP2 via Alecta: FUNDED (Alecta holds assets)
       UK: typically FUNDED (trust holds assets)
       FR IFC: typically UNFUNDED (book reserve — obligation on BS, no separate assets)
       DE Direktzusage: UNFUNDED (obligation on BS, no separate assets)

     Unfunded = plan assets = 0 → full DBO on BS as liability.

  3. Net defined benefit liability (or asset):
     = DBO − plan assets

     Deficit (DBO > assets) → LIABILITY on BS → reduces equity → KBR
     Surplus (assets > DBO) → ASSET on BS → BUT: asset ceiling may limit (IFRIC 14)
```

---

## Step 4: P&L vs OCI Split [MACH + actuary provides data]

```
IAS 19.120-130:

  P&L:
    Current service cost:
      New pension earned by employees during this period.
      → Operating expense (BAS 7412 or similar)

    Past service cost:
      Plan amendment or curtailment effect.
      → Recognize immediately in P&L when amendment occurs.
      → Operating expense

    Net interest on net deficit/surplus:
      = net deficit × discount rate at start of period
      → Financial expense (BAS 8420 or similar)
      NOTE: both sides (interest on obligation AND expected return on assets)
      use the SAME discount rate. The "expected return" concept is gone —
      IAS 19 uses the discount rate for both.

  OCI (NEVER reclassified to P&L — IAS 19.120):
    Actuarial gains/losses on DBO:
      From changes in financial assumptions (discount rate moved)
      From changes in demographic assumptions (mortality updated)
      From experience adjustments (actual ≠ expected)

    Return on plan assets EXCLUDING net interest:
      Actual return minus the discount rate × assets.
      If assets earned 8% but discount rate was 3% → 5% excess to OCI.
      If assets lost 2% but discount rate expected 3% → -5% to OCI.

    Asset ceiling changes (IFRIC 14):
      If surplus exceeds what you can access → limit the asset → change to OCI.

  THE GHOST:
    Remeasurements in OCI → equity moves → KBR headroom changes.
    Board sees: "P&L looks fine." But equity dropped 50M from OCI remeasurement.
    This is how pension deficits silently erode KBR headroom.
```

---

## Step 5: Special Cases [IND — HitL]

### Multi-employer plans (Alecta ITP2, NL pension funds, Norwegian AFP)

```
IAS 19.32-39:

A multi-employer plan = one fund, many employers share the risk.
The NORMAL treatment: account as DB (because it IS DB).
BUT: if the plan administrator cannot provide entity-specific
     allocation of assets and obligation → INSUFFICIENT INFORMATION.

If insufficient information (IAS 19.34):
  → Account as DEFINED CONTRIBUTION (just expense the contributions)
  → PLUS: extensive disclosure about the plan:
     - Description of the plan and funding arrangements
     - Entity's obligation if the plan is wound up or entity withdraws
     - Expected contributions next period
     - Any known surplus or deficit and what it means for the entity

ALECTA (Sweden):
  Manages ITP2 for Swedish employers.
  Alecta is a multi-employer plan.
  Historically: Alecta has NOT provided sufficient information for
  individual employers to account for ITP2 as DB.
  → Most Swedish companies account for Alecta ITP2 as DC
     with extensive disclosure.
  → This is a KNOWN issue. Auditors accept it.
  → But: Alecta publishes its collective funding ratio.
     If funding ratio drops significantly → risk for participating employers.

NETHERLANDS pension funds:
  Industry-wide funds (e.g., ABP for government, PME for metal/electrical).
  Similar issue: multi-employer, insufficient entity-specific data.
  Complex solidarity and risk-sharing mechanisms.
  → Often accounted as DC with disclosure.
  → The Dutch pension reform (Wet toekomst pensioenen, 2023+)
     is changing this → more DC-like structures.

NORWEGIAN AFP:
  Multi-employer early retirement scheme.
  Similar problem: insufficient entity-specific allocation.
  → Often accounted as DC.
```

### Asset ceiling (IFRIC 14)

```
If plan is in SURPLUS (assets > DBO):
  Can you recognize the surplus as an asset?

IFRIC 14: The asset is limited to the LOWER of:
  a) The surplus itself
  b) The present value of future economic benefits available to the entity:
     - Refunds from the plan
     - Reductions in future contributions

  If the plan rules don't allow refunds and future contributions are fixed
  → you can't access the surplus → asset = 0 (even though there IS a surplus).

  Changes in asset ceiling → OCI.

  Country relevance:
    UK: trustees control many plans → refund may require trustee consent → ceiling applies.
    DE Direktzusage: unfunded → no surplus possible → ceiling irrelevant.
    SE Alecta: collective surplus → no individual entity access → ceiling applies (moot — accounted as DC anyway).
```

### Plan amendments, curtailments, settlements

```
Plan amendment (benefit changed):
  → Past service cost → P&L immediately (not spread).
  → Even if change is "positive" for employees (benefit increase).

Curtailment (significant reduction in members or future accrual):
  → Gain or loss → P&L immediately.
  → Example: closing DB plan to new entrants.

Settlement (paying out obligations, e.g., buy-out with insurance company):
  → Recognize gain or loss → P&L.
  → Remove the settled obligation and related assets.
  → UK: "bulk annuity buy-in/buy-out" — common settlement strategy.
```

---

## Country-Specific Examples in Practice

### Swedish subsidiary

```
ITP1 (DC): expense contributions monthly via payroll. Done. ~4.5% of salary.
ITP2 (Alecta, DB): account as DC (insufficient info). Disclose Alecta funding ratio.
Retirement age: 65 (moving to 67-68 gradually).
Social contributions: ~31.42% (including pension contributions).
Vacation pay accrual: mandatory under Semesterlagen. Short-term benefit.
```

### UK subsidiary

```
Legacy DB scheme (closed to new entrants, maybe closed to future accrual):
  Full IAS 19 DB treatment. Annual actuarial valuation.
  Discount rate: iBoxx Sterling AA corporate bond index.
  Mortality: S3 tables + CMI projection model.
  DBO: can be GBP hundreds of millions for old industrial companies.
  Plan assets: held in trust. Trustees make investment decisions.
  Funding: triennial valuation + recovery plan if deficit.
  The Pensions Regulator oversees. Can demand additional contributions.

Auto-enrolment DC: expense contributions. Simple.
UK-specific: GMP (Guaranteed Minimum Pension) equalization — complex.
```

### French subsidiary

```
Indemnités de fin de carrière (IFC):
  MANDATORY for all French entities. DB obligation.
  Employee receives lump sum at retirement based on tenure + collective agreement.
  Often UNFUNDED (book reserve). Some companies fund via insurance contract.
  Actuarial valuation required. Discount rate: EUR corporate bonds (iBoxx EUR).
  Mortality: INSEE TGH/TGF tables.
  Social charges on the indemnity: ~45% on top → increases the obligation.

  Relatively small per-employee amounts (EUR 5-50k typically).
  BUT: mandatory for every French entity → every acquisition in France creates this.

AGIRC-ARRCO: mandatory supplementary pension. DC. Expense contributions.
```

### German subsidiary

```
Direktzusage (direct pension promise):
  DB. Often UNFUNDED (no separate plan assets → full obligation on BS).
  Can be very large for old companies (Daimler, Siemens: billions in pension obligations).
  Discount rate: iBoxx EUR AA corporate (same curve as France).
  Mortality: Heubeck 2018 G tables.
  UNFUNDED means: no plan assets → net liability = full DBO.
  Very sensitive to discount rate (long duration obligations + no asset offset).

  Some companies use Pensionskasse or Unterstützungskasse (external vehicles).
  Pensionskasse may be DC or DB depending on structure.

CTA (Contractual Trust Arrangement): employer funds trust.
  → Plan assets exist → partially offset DBO.
```

### Danish subsidiary

```
ATP: mandatory state pension. DC. Small fixed contributions.
Company pensions: mostly DC (bidragsdefineret) since 1990s reform.
Legacy DB: rare, mostly in large old companies.
If DB exists → standard IAS 19 treatment.
Low complexity for most Danish entities.
```

---

## Node Properties

### On node:org → type_data.pensions

| Field | Type | x-history | Why required | Ref |
|---|---|---|---|---|
| `has_db_plans` | boolean | yes | Does this entity have defined benefit obligations? If no → DC only, trivial. | IAS 19.55 |
| `db_plan_country` | string | no | Which country's pension rules apply (determines mortality, discount, legal requirements) | IAS 19 + local law |
| `dbo` | decimal | yes | Defined Benefit Obligation (present value of all future benefit payments earned). Ghost: sensitive to discount rate. | IAS 19.63 |
| `plan_assets_fv` | decimal | yes | Fair value of plan assets (if funded). IFRS 13 hierarchy. Zero if unfunded. | IAS 19.113 |
| `net_pension_deficit` | decimal | yes | DBO − plan_assets. Liability on BS. Reduces equity → KBR. | IAS 19.63 |
| `net_pension_surplus` | decimal | yes | plan_assets − DBO. Asset on BS (subject to asset ceiling IFRIC 14). | IAS 19.63 |
| `asset_ceiling_applied` | boolean | no | Is the surplus limited by IFRIC 14? If yes → asset may be less than actual surplus. | IFRIC 14 |
| `remeasurement_oci_period` | decimal | yes | OCI movement this period from actuarial gains/losses + asset return. THE Ghost. | IAS 19.120 |
| `remeasurement_oci_cumulative` | decimal | yes | Accumulated OCI remeasurements. Never recycled to P&L. Sits in equity permanently. | IAS 19.122 |
| `service_cost_period` | decimal | yes | Current + past service cost → P&L (operating). | IAS 19.66 |
| `net_interest_period` | decimal | yes | Net deficit × discount rate → P&L (financial). | IAS 19.123-126 |
| `discount_rate` | decimal | yes | Key assumption. Shield monitors: is it defensible? Reserve monitors: sensitivity? | IAS 19.83 |
| `discount_rate_sensitivity_1pct` | decimal | no | Impact on DBO of ±1% discount rate change. Disclosure required + Reserve input. | IAS 19.145(a) |
| `mortality_table` | string | no | Which country-specific mortality table used (DUS, S3/CMI, Heubeck, INSEE). | IAS 19.144 |
| `multi_employer_as_dc` | boolean | no | Is a DB plan accounted as DC due to insufficient info? (Alecta, NL funds, AFP) | IAS 19.34 |
| `alecta_funding_ratio` | decimal | no | SE-specific: Alecta's collective funding ratio (publicly reported). | IAS 19.148 |
| `expected_contributions_next_year` | decimal | no | Cash outflow commitment. Reserve input. | IAS 19.147(b) |

---

## Rim Monitoring

| Monitor | Threshold | Consequence | Cadence |
|---|---|---|---|
| `net_pension_deficit` relative to equity | Deficit > 15% of equity | Ghost eroding KBR. Board must be aware. | Quarterly |
| `discount_rate` vs market | Entity's rate deviates from market observable by >25bps | Rate may be stale or manipulated. ESMA focus. | Each reporting date |
| `discount_rate_sensitivity_1pct` | DBO change > 10% of equity for ±1% rate move | High sensitivity → small rate change = material equity swing | Each reporting date |
| `remeasurement_oci_period` | Large swing (>5% of equity) | Board must understand: equity moved but P&L didn't show it | Each reporting date |
| `alecta_funding_ratio` (SE) | Below 125% (Alecta's own threshold) | Risk of reduced benefits or increased contributions | Quarterly (Alecta publishes) |
| UK subsidiary: Pensions Regulator demands | Recovery plan contributions increase | Cash outflow commitment increases → Reserve impact | When communicated |
| French subsidiary: IFC unfunded | Growing with headcount | Every new French hire adds to the obligation | Annual |
| German subsidiary: Direktzusage unfunded | Large obligation, discount rate sensitive | Rate drop = massive liability increase (no assets to offset) | Quarterly |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Actuarial valuation obtained? Discount rate defensible (market-observable)? Mortality tables current? Correct P&L vs OCI split? Multi-employer plans disclosed properly? Asset ceiling applied? | IAS 19 compliance. ESMA checks discount rates and sensitivity disclosures. |
| **Reserve** | Net deficit: how much equity is consumed? Sensitivity: how much does ±1% rate move change equity? Cash commitments: expected contributions next year? UK recovery plans? | Pension risk = equity risk (Ghost) + cash risk (contributions). |
| **Sword** | Pension cost per subsidiary: which countries are expensive? DB plans closing: when does the obligation peak and decline? Acquisition DD: what pension liability comes with a French/German/UK acquisition? | M&A due diligence: pension obligation is a HIDDEN cost of acquisition. FGGE should flag it in IFRS 3 PPA. |

---

## Connection to Other Chains

| Chain | Connection |
|---|---|
| **IAS 12** | Deferred tax on pension deficit (DTA) and remeasurements (DT in OCI, not P&L) |
| **IAS 36** | Pension deficit is a liability in CGU carrying amount (affects headroom) |
| **IFRS 3** | Acquiring a company with DB pension → fair value the obligation in PPA. French IFC + German Direktzusage = hidden acquisition cost. |
| **IAS 21** | Foreign sub's pension in foreign currency → translated at closing rate → FCTR on the pension deficit too |
| **ABL KBR** | Pension deficit → equity ↓ → KBR headroom ↓. Remeasurement OCI swing → equity ↓ → KBR headroom ↓. Double Ghost. |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Discount rate too high | DBO understated → deficit understated → equity overstated → KBR buffer illusory | #3 Optimistic |
| Not obtaining actuarial valuation | Stale DBO → material misstatement | Shield failure |
| Multi-employer plan accounted as DC without sufficient disclosure | IAS 19.34 violation | Shield compliance |
| Remeasurement in OCI not communicated to board | Board doesn't know equity moved → KBR surprise | Ghost trap |
| French IFC not recognized for new acquisition | Hidden liability → balance sheet understated | #3 Optimistic + IFRS 3 PPA failure |
| German unfunded obligation sensitivity not disclosed | Investors can't assess downside from rate moves | Shield disclosure failure |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — country-specific (SE/UK/FR/DE/DK/NO/NL), multi-employer (Alecta, NL funds, AFP), DB measurement, P&L vs OCI Ghost, asset ceiling, plan inventory per entity, 15 node:org properties, Rim monitors per country |
