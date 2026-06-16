# Ergon Chain: IAS 33 — Earnings Per Share

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 33 (complete standard)
**Intent**: Calculate basic and diluted EPS. Required for listed entities only. Mechanical calculation — reads final net income from Done2 + share data.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 5 — completion, parallel)
**Simplest ergon in the chain.** Pure math once inputs are available.

---

## When Required

IAS 33.2: Only entities whose ordinary shares or potential ordinary shares are **publicly traded** (or in process of listing).

For a Swedish listed group on NASDAQ Stockholm: **mandatory** on the consolidated income statement.

---

## Two Numbers on the Face of the Income Statement

```
BASIC EPS = Net income attributable to ordinary equity holders of the PARENT
            ÷ Weighted average number of ordinary shares outstanding

DILUTED EPS = Adjusted net income
              ÷ Adjusted weighted average shares (including dilutive potential shares)
```

Both presented for:
- Profit/loss from **continuing operations**
- **Total** profit/loss attributable to parent

If discontinued operations exist (IFRS 5): EPS for discontinued operations disclosed (on face or in notes).

---

## Single Ergon: Calculate EPS [MACH]

### Step 1: Determine numerator (net income) [MACH — reads from Done2]

```
BASIC:
  Net income attributable to ordinary equity holders of the parent.
  = Consolidated net income
    − NCI share (already calculated by IFRS 10 NCI ergon)
    − Preference dividends (if any preference shares exist)

  Source: BC Consolidated P&L → net income line
          minus node:org → NCI allocation (from IFRS 10 step 3)

DILUTED:
  Adjust numerator for effects of dilutive potential shares:
    + Interest on convertible bonds (net of tax) — if converted, no interest expense
    + Dividends on dilutive preference shares
    − Any other changes in income that would result from conversion

  These adjustments are typically small or zero for many companies.
```

### Step 2: Determine denominator (share count) [MACH]

```
BASIC:
  Weighted average number of ORDINARY shares outstanding during the period.

  Weighted = time-proportioned:
    If 1M shares outstanding Jan-Jun, then 1.2M shares Jul-Dec (200k new shares issued Jul 1):
    = (1M × 6/12) + (1.2M × 6/12) = 1.1M weighted average

  Adjustments:
    - Bonus issues / stock splits: treat as if they occurred at START of earliest period
      (restate comparatives). No cash raised → retroactive adjustment.
    - Rights issues: adjust for bonus element in the rights price.
    - Share buybacks: reduce count from date of buyback.

DILUTED:
  Add to basic denominator: all DILUTIVE potential ordinary shares.

  Potential ordinary shares:
    a) Share options / warrants (employee stock options, IFRS 2):
       Treasury stock method: assume options exercised at start of period.
       Proceeds from exercise used to "buy back" shares at average market price.
       Dilutive effect = shares issued − shares "bought back"
       = (exercise price < average market price) → dilutive
       = (exercise price > average market price) → anti-dilutive → EXCLUDE

    b) Convertible instruments (convertible bonds, convertible preference):
       If-converted method: assume conversion at start of period.
       Add: shares that would be issued on conversion.
       Also adjust numerator (remove interest/dividends on the converted instrument).

    c) Contingently issuable shares (earn-outs, performance shares):
       Include if conditions are met (or would be met if period-end = end of contingency).

  DILUTION TEST: only include if they DECREASE EPS (or increase loss per share).
  Anti-dilutive instruments → EXCLUDE from diluted EPS.
  Test each instrument separately, then in sequence from most to least dilutive.
```

### Step 3: Calculate and present [MACH]

```
Basic EPS = numerator_basic / denominator_basic
Diluted EPS = numerator_diluted / denominator_diluted

Present on FACE of income statement (not just notes):
  - Basic EPS for continuing operations
  - Diluted EPS for continuing operations
  - Basic EPS total (if discontinued ops exist, show separately)
  - Diluted EPS total

  Round to a precision that doesn't mislead (typically 2 decimal places in SEK).
```

### Step 4: Disclosures [MACH]

```
IAS 33.70:
  a) Amounts used as numerators: basic and diluted, reconciled to net income
  b) Weighted average share counts: basic and diluted, reconciled
  c) Instruments that could dilute in the future but were anti-dilutive this period
  d) Transactions after reporting date that would have significantly changed
     share count (bonus issue, split, buyback after period-end)
```

---

## Data Sources (no new node/edge properties needed)

| Input | Source | Already exists? |
|---|---|---|
| Net income attributable to parent | BC Consolidated P&L (after all Done2 adjustments) | Yes — Done2 output |
| NCI share of net income | IFRS 10 NCI ergon output | Yes |
| Preference dividends | BC — if preference shares exist | Entity-specific |
| Shares outstanding | BC Company Information or share register | Yes (not in graph — in BC or external register) |
| Share transactions during period | BC or share register (issues, buybacks, bonus) | External data |
| Options/warrants outstanding | IFRS 2 share-based payment register | External data |
| Convertible instruments | BC — financial liabilities with conversion feature | Entity-specific |
| Average market share price | Stock exchange data (for treasury stock method) | External data |

**No new graph properties.** EPS is a pure calculation reading from Done2 output + share register.

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Correct weighted average shares? Bonus issues retroactively adjusted? Anti-dilutive excluded? Comparatives restated for splits? | EPS is on the FACE of the income statement — wrong EPS = misstated headline number. |
| **Reserve** | Dilution: how much do outstanding options/convertibles dilute? If all exercised → EPS drops by how much? | Dilution = transfer of value from existing to new shareholders. |
| **Sword** | EPS trend: growing or declining? EPS vs peer group (relative performance). | Market judges by EPS. Analysts forecast EPS. Miss = share price impact. |

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong share count (forgot a mid-year issue) | EPS wrong → misstated headline number → market misled |
| Bonus issue not retroactively adjusted | Current and prior EPS not comparable → misleading trend |
| Anti-dilutive instruments included in diluted EPS | Diluted EPS overstated (looks better than it is) |
| Discontinued operations EPS not shown separately | Investors can't see continuing business EPS → decision-useless |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — basic + diluted EPS, treasury stock method, if-converted method, no new properties (pure calculation from Done2 output + share register) |
