# Ergon Chain: IAS 7 — Statement of Cash Flows

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 7 (complete standard), 2024 amendments (supplier finance arrangements)
**Intent**: Produce the consolidated cash flow statement. Operating / investing / financing classification. Reconciliation of liabilities from financing activities. The REALITY CHECK: P&L says profit, but did cash actually arrive?
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 5/6 — produced from Done2 consolidated data)
**WARNING**: Cash flow at monthly granularity hides daily spikes. See `whs-cashflow-fractal-2026-04-02.md` for the fractal problem.

---

## Why Cash Flow Is the Reality Check

```
P&L can be manipulated (revenue recognition timing, provisions, estimates).
Balance sheet can have Ghosts (goodwill, FCTR, DTA).
Cash flow is HARD TO FAKE (cash either arrived in the bank or it didn't).

The cash flow statement reconciles the STORY (P&L) to REALITY (bank balance).
If profit is high but operating cash flow is low → investigate.
  - Revenue recognized but not collected? (DSO problem)
  - Profit from non-cash items? (goodwill, fair value, accruals)
  - Working capital consuming cash? (inventory build, receivables growth)

For investors/analysts: operating cash flow is often MORE trusted than net income.
```

---

## Three Categories (IAS 7.10-17)

```
OPERATING ACTIVITIES:
  Principal revenue-producing activities of the entity.
  THE main indicator of whether operations generate enough cash.

  Includes: cash from customers, cash to suppliers/employees, interest paid/received
  (classification CHOICE for interest — see below), tax paid.

INVESTING ACTIVITIES:
  Acquisition and disposal of long-term assets + investments.
  Shows: is the entity investing for the future or consuming its asset base?

  Includes: purchase/sale of PP&E, intangibles, subsidiaries (IFRS 3/10),
  investments (IFRS 9), loans made to others.

FINANCING ACTIVITIES:
  Changes in equity and borrowings.
  Shows: how is the entity funded?

  Includes: proceeds from share issues, dividends paid, loan drawdowns/repayments,
  lease liability payments (IFRS 16 principal portion).
```

---

## Classification Choices (IAS 7.31-34)

```
IAS 7 gives CHOICES for certain items. Once chosen → apply consistently.

| Item | Operating OR Financing? | Operating OR Investing? |
|---|---|---|
| Interest PAID | Either (most choose operating) | |
| Interest RECEIVED | | Either (most choose operating) |
| Dividends PAID | Either (most choose financing) | |
| Dividends RECEIVED | | Either (most choose operating) |
| Tax PAID | Operating (default). Can split if identifiable to investing/financing. |

IFRS 18 (effective 2027) REMOVES some choices:
  Interest paid → FINANCING (mandatory)
  Interest received → INVESTING (mandatory)
  Dividends received → INVESTING (mandatory)
  Tax → OPERATING (default, split if clearly identifiable)

  This will change cash flow classification for many groups.
  Plan BC chart of accounts accordingly.
```

---

## Two Methods for Operating Activities

### Indirect Method (IAS 7.18-20) — overwhelmingly common

```
Start: profit before tax (from P&L)
Adjust for NON-CASH items:
  + Depreciation and amortization (non-cash P&L charge)
  + Impairment losses (non-cash)
  + Provisions (increase = add back; decrease = deduct)
  + Unrealized FX gains/losses (non-cash)
  + Share-based payment expense (IFRS 2 — non-cash)
  + Fair value changes on financial instruments (non-cash)
  + Share of profit of associates (non-cash; add back, replace with dividends received)
  ± Other non-cash items

Adjust for WORKING CAPITAL changes:
  − Increase in receivables (cash used)
  + Decrease in receivables (cash received)
  − Increase in inventory (cash used)
  + Decrease in inventory (cash released)
  + Increase in payables (cash retained)
  − Decrease in payables (cash paid out)
  ± Changes in contract assets/liabilities (IFRS 15)
  ± Changes in other working capital items

  − Tax paid (actual cash tax, not P&L tax expense)
  = NET CASH FROM OPERATING ACTIVITIES

Why indirect is popular:
  Starts from a number everyone knows (profit).
  Shows the BRIDGE: how does profit become cash?
  Easier to prepare (BC can automate most adjustments).
```

### Direct Method (IAS 7.18(a)) — rare but more informative

```
  Cash received from customers
  − Cash paid to suppliers
  − Cash paid to employees
  − Cash paid for other operating expenses
  − Tax paid
  = NET CASH FROM OPERATING ACTIVITIES

More useful (shows actual cash flows).
BUT: harder to prepare (need actual cash receipts/payments by type).
IAS 7.19: IASB encourages the direct method. Most entities use indirect.
```

---

## Investing and Financing Activities (IAS 7.21-24)

```
INVESTING:
  − Purchase of PP&E, intangibles, development costs capitalized (IAS 38)
  + Proceeds from sale of PP&E, intangibles
  − Acquisition of subsidiaries, net of cash acquired (IFRS 3)
  + Proceeds from disposal of subsidiaries, net of cash disposed (IFRS 5)
  − Loans made to third parties
  + Repayment of loans made to third parties
  − Purchase of financial assets (IFRS 9)
  + Proceeds from sale of financial assets

  CRITICAL for acquisitions/disposals:
    Show the NET cash effect: cash paid/received minus cash balances in the acquired/disposed entity.
    IAS 7.39-42: disclose aggregate amounts of assets/liabilities acquired/disposed.

FINANCING:
  + Proceeds from share issues
  + Proceeds from borrowings (new loans, bonds issued)
  − Repayment of borrowings
  − Lease liability payments: PRINCIPAL portion only (IFRS 16)
    (Interest portion → operating or financing per classification choice)
  − Dividends paid
  − Purchase of treasury shares (buybacks)

  2024 AMENDMENT — Supplier finance arrangements (IAS 7 + IFRS 7):
    If entity has supplier finance (reverse factoring, supply chain finance):
    → Disclose: terms, carrying amounts, line items where presented,
      range of payment due dates vs original.
    → Prevents hiding debt as trade payables (NMC Health pattern).
```

---

## Reconciliation of Liabilities from Financing Activities (IAS 7.44A-44E)

```
REQUIRED since 2017 amendment:

For EACH liability from financing activities:
  Opening balance
  ± Cash flows (drawdowns, repayments, lease payments)
  ± Non-cash changes:
    - New leases recognized (IFRS 16 — non-cash increase in liability)
    - Acquisitions (IFRS 3 — debt assumed)
    - FX changes on foreign-currency debt
    - Fair value changes
    - Amortization of discount/premium
  = Closing balance

Reconcile: debt (short + long term) + lease liabilities + other financing liabilities.

This disclosure CATCHES hidden debt movements:
  If opening debt = 100M, cash repayment = 20M, but closing = 120M
  → 40M of non-cash increases. What are they? New leases? Acquisition? FX?
  The reconciliation forces transparency.
```

---

## Consolidation-Specific Issues

```
IFRS 10.B86: IC cash flows ELIMINATED.
  IC loan drawdowns/repayments → eliminated (financing one, investing other → net zero)
  IC dividends → eliminated
  IC payments for goods/services → eliminated

  Only EXTERNAL cash flows appear in consolidated cash flow statement.

Foreign subsidiary cash flows:
  IAS 7.25-28: translate at exchange rate at the DATE OF CASH FLOW
  (or average rate as practical approximation — same as P&L per IAS 21).

  Unrealized FX gains/losses on cash → NOT cash flow.
  But: effect of exchange rate changes on cash held in foreign currency
  → shown as a SEPARATE reconciling item (not operating/investing/financing).

Cash and cash equivalents (IAS 7.6-9):
  Cash: cash on hand + demand deposits.
  Cash equivalents: short-term (≤3 months from acquisition), highly liquid,
  readily convertible to known cash amounts, insignificant risk of value change.

  RESTRICTED CASH: disclose but may NOT include in cash equivalents
  if not available for general use.
  Example: cash trapped in a subsidiary due to exchange controls → disclose.
  Connection: Reserve monitors: trapped cash = reduced available liquidity.
```

---

## The Fractal Problem — Cash Flow Granularity

```
WARNING: This cash flow statement shows PERIOD totals.

  Monthly: "Operating cash flow = +50M." Looks fine.
  Weekly: "+20M, +15M, -10M, +25M." Some variation but OK.
  Daily: "+5M, -200M, +30M, +50M, -15M, +180M, ..."
         DAY 2: NEGATIVE 200M. Payroll + supplier batch + quarterly tax all hit.

  The monthly/quarterly statement HIDES the daily spikes.
  A company can be "cash flow positive" every month
  while being INSOLVENT for 2 days each month.

  This is the fractal property of cash flow:
  volatility appears at finer granularity that aggregation smooths out.

  For KBR/liquidity monitoring: the DAILY minimum matters, not the monthly average.
  Taleb (F14): "Never cross a river that is on average 4 feet deep."

  See: whs-cashflow-fractal-2026-04-02.md for the full walk on this.
```

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Classification correct (operating/investing/financing)? Consistent with prior year? IC cash flows eliminated? Reconciliation of financing liabilities complete? Restricted cash disclosed? Supplier finance arrangements disclosed (2024)? | IAS 7 compliance. Wrong classification = misleading. Missing reconciliation = hidden debt. |
| **Reserve** | **Operating cash flow vs profit**: is the business GENERATING cash? If profit high but OCF low → working capital problem or non-cash profit. **Daily cash position**: do we go negative intra-period? **13-week forecast**: can we meet ALL obligations at daily granularity? Trapped cash: how much is restricted? | Cash IS Reserve. The cash flow statement is Reserve's primary document. Liquidity risk = survival risk. |
| **Sword** | Free cash flow (OCF − capex): what's available for Sword investments? Cash conversion ratio (OCF / net income): how efficient? Cash flow by segment: which xItem clusters generate cash? Where is DSO shortest (fastest cash)? | Sword needs cash to deploy Vectors. FCF determines how much Sword has to aim. |

---

## Node/Edge Properties

**No new properties for the cash flow statement itself** — it's DERIVED from all the other data:
- P&L (from IFRS 15, 16, etc. ergon chains)
- Working capital movements (from BC GL: receivables, inventory, payables)
- Investment activities (from IFRS 3 acquisitions, IFRS 5 disposals, capex)
- Financing activities (from loans, leases, dividends, equity)

The 13-week daily cash forecast (Reserve) is the operational companion — already covered in Reserve Shaw Lens design.

---

## Rim Consequence

| Risk | Consequence |
|---|---|
| Wrong classification (operating inflated by including investing items) | Misleading OCF → investors overvalue cash generation. ESMA scrutinizes. |
| Financing reconciliation missing | Hidden debt movements. NMC Health pattern: supply chain finance as trade payables. |
| Restricted cash included in "cash" | Overstated available liquidity → Reserve assessment wrong → may not survive cash crunch. |
| IC cash flows not eliminated | Consolidated cash inflated by internal transfers. |
| Daily spikes hidden by monthly reporting | Board sees "positive cash flow" while company was insolvent for 2 days. KBR/liquidity Rim crossed invisibly. |
| IFRS 18 classification changes not prepared | Interest paid moves from operating to financing (2027) → OCF improves but FCF may look different. Analysts need to adjust. |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — three categories, classification choices (+ IFRS 18 changes), indirect/direct methods, financing reconciliation (2024 supplier finance), consolidation (IC elimination, FX, restricted cash), fractal problem reference, S-R-S view |
