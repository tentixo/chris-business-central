# Ergon: IFRS 15 — Revenue Recognition (Step 5)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 15.31-45, B2-B19
**Intent**: Recognize revenue when (or as) each performance obligation is satisfied. Mapped to xtValue patterns.
**Chain**: ergon-ifrs-15-chain_v1.0.md (step 5)
**Depends on**: POs identified (steps 1-2), price allocated (steps 3-4)

---

## The Core Rule

IFRS 15.31: Recognize revenue when entity **satisfies a performance obligation** by transferring a promised good or service to the customer. Transfer = customer obtains **control**.

Control = ability to direct the use of and obtain substantially all remaining benefits from the asset.

**This IS xtValue.** The moment control transfers = the moment xtValue comes into existence for the buyer.

---

## Over-Time or Point-in-Time? [IND for edge cases, MACH for clear cases]

```
IFRS 15.35: Recognize over time IF ANY ONE of three criteria met:

  a) Customer simultaneously RECEIVES AND CONSUMES the benefits
     as entity performs.
     → hItem: consulting (client learns as consultant works)
     → hItem.labor: cleaning, security (consumed immediately)
     → gItem.energy: electricity, gas (consumed as delivered)
     → vItem.e-svc subscription: access consumed as provided

  b) Entity's performance creates or enhances an asset
     that the CUSTOMER CONTROLS as created/enhanced.
     → Construction on customer's land
     → Software built on customer's servers
     → Customization of customer's existing asset

  c) Entity's performance does NOT create an asset with
     ALTERNATIVE USE to the entity AND entity has enforceable
     RIGHT TO PAYMENT for performance completed to date.
     → Custom software (no alternative use — built to spec)
     → hItem.consulting Fixed Price with right to payment for work done
     → Manufactured goods built to customer specification

  IF NONE of a/b/c met → POINT-IN-TIME (IFRS 15.38):
    Recognize when control transfers.
    Indicators: right to payment, legal title, physical possession,
    significant risks and rewards, customer accepted.
```

### Mapped to xItem Types

| xItem type | Over-time criterion | Progress method | Practical notes |
|---|---|---|---|
| **gItem.physical** (standard product) | None → **point-in-time** | N/A — recognize at delivery/acceptance | Most common. Incoterms determine WHEN control transfers. |
| **gItem.physical** (custom-built to spec) | (c) No alternative use + right to payment | Input (cost) or output (milestones) | Must prove: can't redirect to another customer AND have right to payment for done work |
| **gItem.energy** | (a) Simultaneous receive/consume | Output (metered units) | Each kWh/m³ consumed as delivered |
| **vItem.e-svc** (one-time download/access) | None → **point-in-time** | N/A — recognize at download/access grant | Like selling a gItem but virtual |
| **vItem.e-svc** (subscription/SaaS) | (a) Simultaneous receive/consume | Time-elapsed (ratable over subscription period) | Stand-ready obligation. Revenue = allocated price / period. BC Subscription Billing handles via Contract Deferrals. |
| **hItem.consulting** (T&M) | (a) Simultaneous receive/consume | **Right to invoice practical expedient** (IFRS 15.B16): recognize at amount entity has right to invoice | Simplest over-time method. Revenue = hours × rate. Each period. |
| **hItem.consulting** (Fixed Price) | (c) No alternative use + right to payment (or (a) if client consumes as delivered) | Input (cost incurred / total expected cost) or output (milestones completed / total milestones) | HitL: which method more faithful? Input simpler but distorted by inefficiency. |
| **hItem.labor** (installation) | (b) Customer controls asset being enhanced (installing on customer's property) | Output (milestones) or input (cost) | Usually short-duration → may recognize at completion (point-in-time) if immaterial |
| **xPackage.project** | Each PO per its own pattern | Mixed — each PO separately | Most complex. Some POs point-in-time, others over-time, each on its own schedule. |

---

## Measuring Progress (for over-time) [IND for method choice, MACH for calculation]

### Input methods

```
Cost-to-cost: costs incurred to date / total expected costs = % complete
  Revenue = % complete × allocated_price

  Advantage: data readily available (actual costs from BC project)
  Disadvantage: inefficiency distorts % (spending doesn't always = progress)

Hours-to-hours: hours worked / total estimated hours = % complete
  Revenue = % complete × allocated_price

  Advantage: closer to effort, less distorted by cost rate differences
  Disadvantage: still input-based — hours worked ≠ value delivered
```

### Output methods

```
Milestones: milestones achieved / total milestones = % complete
  Revenue = milestones × allocated_price_per_milestone (if evenly allocated)
  OR: % complete × allocated_price

  Advantage: measures actual output
  Disadvantage: uneven milestone spacing → lumpy revenue

Units delivered: units delivered / total units = % complete
  Revenue = % complete × allocated_price

  Advantage: objective, measurable
  Disadvantage: only works for discrete deliverables

Time-elapsed: days elapsed / total contract days = % complete
  Revenue = % complete × allocated_price

  Advantage: simplest. Perfect for stand-ready (SaaS, subscriptions).
  Disadvantage: only appropriate when value transfers evenly over time
```

### Right to invoice practical expedient (IFRS 15.B16)

```
For T&M contracts where entity has right to invoice for hours worked:
  Revenue = amount entity has right to invoice (hours × rate)
  No % completion calculation needed.
  Simplest method. Eliminates estimation.

Conditions: right to invoice = directly corresponds to value delivered.
  Most T&M consulting contracts qualify.
```

---

## Contract Balances [MACH]

```
After recognition, one of three states exists:

  TRADE RECEIVABLE:
    Revenue recognized + invoice sent + not yet collected.
    → Normal AR. BC handles via Sales Invoices → Customer Ledger.

  CONTRACT ASSET ("accrued revenue"):
    Revenue recognized + NOT yet invoiced (but right to consideration conditional
    on something other than passage of time — e.g., milestone not yet hit).
    → Asset on BS. BC: may need manual accrual or project WIP.

  CONTRACT LIABILITY ("deferred revenue"):
    Invoice sent + cash collected + revenue NOT yet recognized
    (performance obligation not yet satisfied).
    → Liability on BS. BC: Subscription Billing handles via Contract Deferrals.

Record:
  edge:org-org → sells_to.contract_balance_type = receivable / contract_asset / contract_liability
  BC tracks the actual amounts in GL.
```

---

## Output

| Target | What |
|---|---|
| BC P&L | Revenue recognized per period per PO per xtValue pattern |
| BC BS | Contract assets, contract liabilities, trade receivables |
| `xPackage.performance_obligations[]` | recognition_pattern, progress_method, period_start/end, satisfaction_date |
| `edge:org-org → sells_to` | contract_balance_type updated each period |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Over-time when should be point-in-time | Revenue recognized too early (spread over period when should be at delivery) | #3 Optimistic — ESMA finding |
| Point-in-time when should be over-time | Revenue delayed, then lumpy recognition at delivery | Conservative but wrong |
| Wrong progress measure (cost-to-cost with inefficiency) | Revenue overstated if costs overrun allocated budget | #3 Optimistic |
| Not recognizing contract liability | Revenue overstated (collected but not yet earned) | #3 Optimistic (Prosolvia) |
| T&M right-to-invoice applied when conditions not met | Revenue recognized at invoiced amount when value not yet delivered | #3 Optimistic |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — over-time vs point-in-time mapped to xItem types, progress methods, contract balances, right-to-invoice expedient. |
