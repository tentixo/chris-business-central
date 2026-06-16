# Ergon: IAS 21 — FX Monitors (Entropy Patrol)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 21.13 (reassessment), IAS 29 (hyperinflation)
**Intent**: Continuous monitoring of FX-related risks. Detect: reference rate divergence, hyperinflation triggers, FCTR KBR impact, functional currency reassessment needs.
**Chain**: ergon-ias-21-chain_v1.0.md (ongoing)
**Nature**: Walker — Reality Observer Path

---

## Monitor 1: Reference Rate Divergence [MACH — Walker]

```
Monthly:
  For each currency pair used across entities:
    Compare: Riksbanken rate vs ECB rate (inverted as needed)

  Threshold: divergence > 0.05 SEK (or > 0.5% relative)

  IF exceeded:
    → Anomaly: "Reference rate divergence {currency}: Riksbanken {X} vs ECB {Y} on {date}"
    → Investigate: market stress? Fixing time difference? Data feed error?

  Why: ensures using different reference sources per entity doesn't create
  material inconsistency at consolidation.
```

---

## Monitor 2: Hyperinflation Detection [MACH — Walker]

```
Quarterly:
  For each subsidiary's functional currency:
    Check: cumulative inflation approaching or exceeding 100% over 3 years

  Sources: IMF data, World Bank, local central bank statistics

  IAS 29 qualitative indicators (any of these = investigate):
    - General population prefers to keep wealth in non-monetary assets
      or in a relatively stable foreign currency
    - Prices quoted in a stable foreign currency rather than local
    - Credit sales/purchases at prices compensating for expected inflation
    - Interest rates, wages, prices linked to a price index
    - Cumulative inflation approaching 100% over 3 years

  Currently relevant currencies (as of 2025-2026):
    Turkey (TRY) — active hyperinflation
    Argentina (ARS) — active hyperinflation
    Others may emerge — this monitor detects them

  IF triggered:
    → Anomaly: "Hyperinflation indicator for {currency}. IAS 29 applies."
    → Subsidiary must: restate financials (IAS 29) BEFORE translation
    → Translation method changes: ALL items at closing rate (exception)
    → ergon-ias-21-consolidation-translation Step 5c activates
```

---

## Monitor 3: FCTR Equity / KBR Impact [MACH — Walker]

```
Monthly (at minimum):
  For each foreign subsidiary:
    Read: node:org → fctr_balance (accumulated FCTR)
    Read: node:org → equity_latest
    Read: node:org → registered_share_capital (parent company)

    Calculate: group equity sensitivity to FX:
      For each major currency:
        "IF EUR/SEK moves 10%, FCTR changes by {X} SEK"
        "This changes group equity by {X} SEK"
        "KBR headroom changes from {current} to {stressed}"

  IF stressed KBR headroom < 20% of share capital:
    → Anomaly: "FX sensitivity threatens KBR headroom.
       Current headroom: {X}. 10% {currency} move: headroom drops to {Y}.
       Board must be informed."

  This is the GHOST TRAP: FCTR erodes equity without affecting cash.
  Board members can become personally liable (ABL 25:13) because
  an FX rate moved, not because the business deteriorated.
```

---

## Monitor 4: Functional Currency Reassessment Triggers [MACH — Walker]

```
Quarterly:
  For each entity:
    Check x-history on node:org:
      - Revenue currency mix shifted materially?
      - Cost currency mix shifted materially?
      - New major customer/supplier in different currency?
      - Operations relocated?

    Check edge:org-org:
      - IC trading direction/volume shifted materially?
      - New IC loans in different currency?

  Heuristic:
    IF revenue_currency_mix changed by >20% from last assessment
    OR cost_currency_mix changed by >20%
    → Anomaly: "Functional currency reassessment may be needed for {org}.
       Revenue mix shifted from {old} to {new}."
    → Triggers: ergon-ias-21-functional-currency reassessment

  This is rare but material. A wrong functional currency
  cascading for months/years creates large restatement risk.
```

---

## Monitor 5: Rate Feed Health [MACH — Walker]

```
Daily:
  For each entity's reference rate source:
    Is today's rate available?
    Is the rate within reasonable bounds (not 0, not outlier)?

  IF rate missing:
    → Alert: "No {currency} rate from {source} for {date}.
       Transactions cannot be posted at reference rate."
    → Fallback: use previous business day rate (document)

  IF rate is outlier (>5% move in one day):
    → Alert: "Unusual rate movement {currency}: {old} → {new} ({pct}% change).
       Verify with alternative source."
    → This catches: data feed errors, currency crises, market disruptions
```

---

## S-R-S View

| Monitor | S-R-S Zone | Why |
|---|---|---|
| Rate divergence | Shield | Ensures reference sources are consistent |
| Hyperinflation | Shield | IAS 29 compliance — wrong method if not detected |
| FCTR/KBR impact | **Reserve** (critical) | The Ghost that silently eats KBR headroom |
| Functional currency trigger | Shield | Wrong functional currency = systemic translation error |
| Rate feed health | Shield | No rates = can't post = close delayed |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — 5 monitors: divergence, hyperinflation, FCTR/KBR, functional currency triggers, rate feed health |
