# Ergon: IAS 36 — Impairment Indicator Assessment (Step 1)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 36.12-14
**Intent**: At each reporting date, check whether indicators suggest an asset (or CGU) may be impaired. If indicators found → trigger the impairment test. For goodwill: test annually regardless.
**Chain**: ergon-ias-36-chain_v1.0.md (step 1)

---

## Trigger

| Type | Detail |
|---|---|
| **Periodic** | Each reporting date: check indicators for ALL assets/CGUs |
| **Periodic** | Annual: goodwill + indefinite-life intangibles tested regardless of indicators |
| **Event** | Significant adverse event (customer loss, market crash, technology shift) |

---

## Indicators (IAS 36.12)

### External indicators [MACH can detect most]

| # | Indicator | Detection method | S-R-S source |
|---|---|---|---|
| E1 | Asset's **market value declined significantly** more than expected from passage of time or normal use | Market data, comparable transactions, broker estimates | Reserve (fair value monitoring) |
| E2 | Significant adverse changes in **technology, markets, economy, law** affecting the entity | News feeds, industry reports, regulatory alerts | Shield (regulatory monitoring) + Sword (market intelligence) |
| E3 | **Market interest rates** increased → affects discount rate for VIU → recoverable amount likely decreased | Central bank rates, yield curves | Reserve (rate monitoring) |
| E4 | **Market capitalization < book value** of net assets (entire company level) | Stock price × shares vs consolidated equity | Reserve — THE loudest indicator. If market says company worth less than books → something is overstated. |

### Internal indicators [IND + MACH]

| # | Indicator | Detection method | S-R-S source |
|---|---|---|---|
| I1 | Evidence of **obsolescence or physical damage** | Asset register review, physical inspection | Shield (asset condition monitoring) |
| I2 | Significant adverse changes in **how the asset is used or expected to be used** | Management plans, restructuring, business changes | Sword (strategic decisions affect asset value) |
| I3 | Plans to **discontinue or restructure** the operation the asset belongs to | Board decisions, restructuring plans | Sword → Shield trigger |
| I4 | Plans to **dispose of the asset** before expected date | IFRS 5 classification process | Shield (disposal triggers IFRS 5, but also IAS 36 check) |
| I5 | **Economic performance** of the asset is or will be worse than expected | Actual revenue/profit vs projections for the CGU. Budget vs actual (or rolling forecast vs actual). | Sword (performance Shaw Lens) + Reserve (forecast monitoring) |

### The market cap test (E4) — the loudest signal

```
IF market_capitalization < consolidated_book_value_of_equity:

  The ENTIRE GROUP may have impaired assets.
  The market is saying: "your net assets are overstated."

  This does NOT automatically mean individual CGUs are impaired
  (the discount could be market sentiment, not asset-specific).

  But it DOES require investigation:
    - Which CGUs are underperforming?
    - Is goodwill still supportable?
    - Are asset carrying amounts reasonable?

  ESMA treats this as a near-mandatory trigger for detailed testing.
  Auditors will always challenge if market cap < book value and no impairment recognized.

  Source data:
    market_cap = share price × shares outstanding (real-time, from stock exchange)
    book_value = consolidated equity (from latest reporting, or estimate)

  For FGGE: this is a Reserve + Shield monitor.
    If market_cap / book_value < 1.0 → flag immediately.
    If market_cap / book_value < 0.8 → critical: detailed impairment test required.
```

### Goodwill and indefinite-life intangibles — no indicators needed

```
IAS 36.10: Regardless of indicators, test goodwill and
indefinite-life intangibles for impairment ANNUALLY.

  - Can test at any time during the year, BUT
  - Must test at the SAME TIME each year (consistency)
  - If indicators appear between annual tests → test immediately (don't wait)

  Common practice: test at year-end (aligns with annual reporting).
  Some companies test at Q3 (gives time to finalize before year-end).
```

---

## Assessment Process [MACH + IND]

```
For EACH reporting date:

  1. MACH scans external indicators:
     - Market data for asset values (E1)
     - Interest rate changes (E3)
     - Market cap vs book value (E4)
     - News/regulatory changes (E2)

  2. IND assesses internal indicators:
     - Business plan changes (I2, I3)
     - Performance vs expectations (I5)
     - Asset condition (I1)
     - Disposal plans (I4)

  3. For each CGU with goodwill:
     - Is annual test due? → test regardless
     - Indicators found? → test now (don't wait for annual)
     - No indicators + not annual test date → no test needed this period
       (but document that indicators were assessed)

  4. For each other asset:
     - Indicators found → test
     - No indicators → no test (but document assessment)

Output:
  For each CGU/asset: "indicators assessed, [found/not found], [test triggered/not triggered]"
  node:anomaly created if indicators found: "Impairment indicator for CGU {X}: {description}"
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Were indicators assessed at every reporting date? Is annual goodwill test scheduled? Were ALL indicators checked (not just the convenient ones)? | Compliance: must assess. Not assessing = failing to detect impairment = Carillion. |
| **Reserve** | Market cap < book value? Interest rates rising (discount rate up = VIU down)? Revenue declining in any CGU? | Early warning: impairment approaching = equity drop = KBR headroom shrinking. |
| **Sword** | Which CGUs underperform? Where is economic performance below expectation? | Strategic input: fix, restructure, or exit underperforming CGUs. |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Not assessing indicators | Impairment not detected until too late. Carillion: 19 years without adequate challenge. | #3 Optimistic + #6 Auditor complacency |
| Ignoring market cap < book value | ESMA will ask: "your market says you're overvalued — why no impairment?" No good answer. | #3 Optimistic |
| Not testing goodwill annually | IAS 36.10 violation. Auditor qualification. | Shield failure |
| Testing at too high a level (group, not CGU) | Profitable CGUs mask loss-making ones → impairment hidden. THE Carillion pattern. | #3 Optimistic — ESMA #1 finding |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — external + internal indicators, market cap test, annual goodwill test requirement, assessment process |
