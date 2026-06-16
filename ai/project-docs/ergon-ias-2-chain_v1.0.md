# Ergon Chain: IAS 2 — Inventories

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 2 (complete standard)
**Intent**: Measure inventory correctly (lower of cost and NRV), handle costing methods, detect obsolescence. gItem territory — only applies to physical goods. Important for BC setup: Costing Method, Inventory Posting Groups, Item tracking.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 3 — entity-level, feeds into consolidation)
**Only applies to**: gItem.physical and gItem.energy (physical goods with inventory). NOT vItem, NOT hItem.

---

## Why IAS 2 Matters for BC Setup

IAS 2 determines HOW BC calculates inventory cost. The costing method choice in BC (FIFO, Average, Standard, Specific) IS an IAS 2 decision. Getting it wrong at setup → every inventory transaction has wrong cost → COGS wrong → margin wrong → equity wrong → KBR.

```
BC Item Card → Costing Method field → THIS IS THE IAS 2 DECISION.

  FIFO:     First In, First Out. BC tracks purchase layers.
  Average:  Weighted Average Cost. BC recalculates on each receipt.
  Standard: Predetermined standard cost. Variances to separate accounts.
  Specific: Each unit tracked individually (serial numbers).

  IAS 2 allows: FIFO, Weighted Average, Specific identification.
  IAS 2 does NOT allow: LIFO (Last In, First Out — prohibited under IFRS).
  BC supports LIFO → but MUST NOT be used for IFRS reporting.
```

---

## What IAS 2 Covers

```
IAS 2.6: Inventories are assets:
  a) Held for sale in the ordinary course of business (finished goods)
  b) In the process of production for such sale (WIP / halvfabrikat)
  c) Materials or supplies to be consumed in production or service delivery (raw materials)

IAS 2 does NOT apply to:
  - Financial instruments (IFRS 9)
  - Biological assets related to agricultural activity (IAS 41)
  - Inventories held by commodity broker-traders measured at FV-costs to sell
```

### xItem Mapping

| xItem type | IAS 2 applies? | Why |
|---|---|---|
| **gItem.physical** (finished goods) | **YES** | Held for sale. THE core IAS 2 asset. |
| **gItem.physical.raw** (raw materials, halvfabrikat) | **YES** | Materials for production. WIP. |
| **gItem.energy** | **Depends** | If stored (gas in pressured vessel) → yes. If continuous flow (electricity) → typically no inventory. |
| **vItem** (all types) | **NO** | No physical inventory. |
| **hItem** (all types) | **NO** | No physical inventory. (But: hItem.labor costs on uncompleted service contracts → IFRS 15 contract costs, not IAS 2.) |

---

## Chain Overview

```
┌──────────────────────────────────────────────┐
│  STEP 1: COST DETERMINATION                  │
│  What goes INTO the cost of inventory?        │
│  Purchase cost + conversion costs + other      │
│  IAS 2.10-18                                 │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 2: COST FORMULA (Costing Method)       │
│  FIFO, Weighted Average, or Specific ID       │
│  THE BC setup decision                        │
│  IAS 2.23-27                                 │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 3: NRV TEST (Lower of Cost and NRV)   │
│  Net Realizable Value < cost? → write down    │
│  Each period. Can reverse (but not > original)│
│  IAS 2.28-33                                 │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 4: IC INVENTORY PROFIT                 │
│  For consolidation: unrealized IC markup      │
│  on goods held by buyer at period-end         │
│  IFRS 10.B86 + IC Elimination ergon          │
└──────────────────────────────────────────────┘
```

---

## Step 1: Cost Determination [MACH — BC calculates]

```
IAS 2.10: Cost of inventories = ALL costs of:
  purchase + conversion + other costs to bring to present location/condition.

PURCHASE COSTS (IAS 2.11):
  Purchase price
  + Import duties and non-recoverable taxes
  + Transport, handling, other directly attributable costs
  − Trade discounts, rebates, similar items (reduce cost)

  BC: captured on Purchase Order → Item Ledger Entry → cost per unit.

CONVERSION COSTS (IAS 2.12-14) — for MANUFACTURED gItem:
  Direct labor (person time on production)
  + Direct materials (BOM components consumed)
  + Systematic allocation of fixed and variable production overhead:

    Fixed overhead: allocated based on NORMAL CAPACITY (not actual if abnormally low).
    IAS 2.13: "The allocation of fixed production overheads is based on
    the normal capacity of the production facilities."

    Abnormally low production → unallocated overhead → expense (NOT in inventory cost).
    This prevents: inflating unit cost when production is low → overstating inventory.

  BC: BOM (materials) + Routing (labor/machine time × rates) + Overhead (%).
    Standard costing: predetermined rates. Variances to separate GL accounts.
    Actual costing: actual costs flow through.

EXCLUDED from cost (IAS 2.16-18):
  - Abnormal waste (materials, labor, overhead) → expense immediately
  - Storage costs (AFTER production complete) → expense
    UNLESS: storage is necessary in the production process (e.g., aging wine, cheese)
  - Administrative overheads not contributing to bringing inventory to current condition → expense
  - Selling costs → NEVER in inventory cost
  - Borrowing costs → capitalize ONLY if inventory is a qualifying asset (IAS 23 — rare for inventory)
```

---

## Step 2: Cost Formula — The BC Setup Decision [IND — policy choice]

```
IAS 2.23-27:

THREE permitted methods:

1. SPECIFIC IDENTIFICATION (IAS 2.23):
   Each individual item's actual cost is tracked.
   REQUIRED for: items that are not ordinarily interchangeable,
   and goods produced for specific projects.
   Example: luxury cars (each with VIN), custom machinery, art.
   BC: Costing Method = "Specific" + Item Tracking (Serial No.).

2. FIFO — First In, First Out (IAS 2.27):
   Oldest inventory consumed first. Remaining = most recent purchases.
   In rising prices: lower COGS, higher inventory valuation, higher profit.
   BC: Costing Method = "FIFO". BC tracks purchase layers automatically.

3. WEIGHTED AVERAGE COST (IAS 2.27):
   Average cost recalculated on each receipt.
   Smooths out price fluctuations.
   BC: Costing Method = "Average". BC recalculates on each inbound.

PROHIBITED under IFRS:
   LIFO (Last In, First Out) — NOT ALLOWED by IAS 2.
   BC supports LIFO → DO NOT USE for IFRS reporting.
   Shield monitor: any entity using LIFO → anomaly.

STANDARD COST (IAS 2.21):
   Not a "cost formula" per se — it's a CONVENIENCE METHOD.
   Standard cost = pre-set cost per unit (material + labor + overhead at normal rates).
   Must be REGULARLY REVIEWED and updated to approximate actual cost.
   Variances (actual vs standard) → separate GL accounts.
   If standard ≈ actual → acceptable under IAS 2.
   If standard materially ≠ actual → adjust inventory to actual.
   BC: Costing Method = "Standard". Standard Cost field on Item Card.
       "Adjust Cost — Item Entries" batch job reconciles.

POLICY CHOICE:
  Same cost formula MUST be used for all inventories with
  SIMILAR NATURE AND USE (IAS 2.25).
  CAN use different formulas for inventories with different nature/use.
  Example: FIFO for finished goods, Weighted Average for raw materials → OK.
           FIFO for Widget A and Average for Widget B (same category) → NOT OK.

  This maps to: xItem.sub_type determines which costing method group.
  BC: set Costing Method per Item, but ensure consistency per category.
  Gen. Prod. Posting Group (= xItem classification) → should correlate with costing method.
```

---

## Step 3: NRV Test — Lower of Cost and NRV [IND + MACH]

```
IAS 2.28-33: THE measurement rule.

  Inventory carried at LOWER OF:
    a) Cost (per steps 1-2 above)
    b) Net Realizable Value (NRV)

  NRV = estimated selling price in ordinary course of business
        − estimated costs of completion (for WIP)
        − estimated costs necessary to make the sale (selling costs)

  NRV is NOT fair value (IFRS 13). NRV is ENTITY-SPECIFIC.
  Fair value = what the market would pay. NRV = what THIS entity expects to receive.
  NRV may be lower than FV (if entity has higher selling costs) or higher (loyal customers).

  WHEN TO TEST:
    Each reporting period. At minimum: each close.
    For interim (IAS 34): same test, but estimates may be less precise.

  IF NRV < COST:
    Write down to NRV. Charge to P&L (COGS or separate line).
    → Inventory carrying amount reduced → assets reduced → equity reduced → KBR.

  REVERSAL (IAS 2.33):
    If NRV subsequently INCREASES (market price recovers):
    → Reverse the write-down (but not above original cost).
    → Credit to P&L (reduce COGS).
    This is DIFFERENT from goodwill (IAS 36 — never reverse).
    Inventory write-downs CAN be reversed.

  ITEM-BY-ITEM basis (IAS 2.29):
    Test each item (or group of similar items) individually.
    NOT: offset write-downs on some items with gains on others.
    Some items may be written down while others are fine.

  COMMON TRIGGERS for NRV < cost:
    - Damage (physical → NRV drops to scrap value)
    - Obsolescence (technology shift → xItem.obsolescence_risk)
    - Declining selling prices (market → SSP drops below cost)
    - Increased completion costs (WIP → estimated costs to finish exceed selling price)
    - Expired or approaching expiry (xItem.shelf_life)

  Connection to xItem:
    xItem.cost_standard = the cost side.
    xItem.ssp = benchmark for the selling price side (but NRV uses entity-specific, not market).
    xItem.obsolescence_risk = trigger indicator for NRV test.
    gItem.shelf_life = expiry-driven write-down trigger.
```

---

## Step 4: IC Inventory Profit (Consolidation) [MACH — IC Elimination ergon]

```
Already covered in ergon-ic-elimination-chain_v1.0.md (Step 3).

When entity A sells gItem to entity B within the group:
  A's revenue includes markup.
  B's inventory at period-end includes A's markup (unrealized at group level).

  Eliminate: IC markup × unsold inventory at buyer.
  → Inventory written down to group cost at consolidation level.

  Source data: edge:org-org → sells_to.price vs xItem.cost_standard → markup %.
  Buyer's inventory balance from BC.

  IAS 2 at entity level: inventory at B is correctly valued at B's cost (= IC price).
  At GROUP level: inventory overstated by IC markup on unsold goods.
  → IC elimination ergon handles this. IAS 2 ergon ensures entity-level is correct.
```

---

## BC Setup Implications

### Item Card Setup for gItem

| BC field | IAS 2 relevance | How to set |
|---|---|---|
| **Costing Method** | THE IAS 2 cost formula choice | FIFO / Average / Standard / Specific. NEVER LIFO for IFRS. |
| **Standard Cost** | If Standard costing: the predetermined cost | From BOM + Routing calculation. Review regularly (IAS 2.21). |
| **Unit Cost** | Last actual cost (for Average costing) | BC calculates automatically |
| **Inventory Posting Group** | Determines GL accounts (BS: 1400-1499 in BAS) | Set per xItem sub-type (raw=1410, WIP=1440, finished=1450) |
| **Gen. Prod. Posting Group** | Determines COGS account (4000-4999 in BAS) | Set per xItem type. Shield validates consistency per category. |
| **Item Category Code** | Groups items for reporting | Maps to xItem.sub_type for governance |
| **Item Tracking Code** | Serial/Lot tracking | Required for Specific ID costing. Optional for FIFO/Average. |
| **Reorder Policy** | Not IAS 2 but affects inventory levels | Operational — affects NRV test (excess stock = NRV risk) |

### Key BC Processes for IAS 2

| BC process | What it does | IAS 2 connection |
|---|---|---|
| **Adjust Cost — Item Entries** | Reconciles inventory value to actual costs | Standard costing: calculates variances. Essential for IAS 2.21 compliance. |
| **Post Inventory Cost to G/L** | Posts inventory value changes to GL | Ensures BS reflects correct inventory value. |
| **Revaluation Journal** | Manual adjustment to inventory value | Used for NRV write-downs. Dr COGS / Cr Inventory. |
| **Physical Inventory Journal** | Count inventory, adjust for differences | IAS 2.9: entity should have systems to determine cost. Physical count = verification. |
| **Item Age Composition** report | Shows inventory age | Drives obsolescence detection → NRV trigger. |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | Costing method per IAS 2? No LIFO? Standard costs reviewed recently? NRV tested each period? Write-downs recognized? Reversals not exceeding original cost? IC inventory profit eliminated? | IAS 2 compliance. Wrong costing = wrong COGS = wrong margin = wrong equity. |
| **Reserve** | Inventory as % of current assets: too high = cash locked in stock. Aging: how much is >90/180/365 days old? NRV risk: how much inventory is at risk of write-down? | Inventory = cash converted to physical stuff. Slow-moving inventory = trapped cash. Write-down = equity hit → KBR. |
| **Sword** | Inventory turns by xItem type: which gItems move fast (healthy) vs slow (problem)? Which xItems have declining NRV (market shifting)? Where is DIO (Days Inventory Outstanding) too high? | Product health: fast-moving = market wants it. Slow-moving = Sword should reconsider or discount. Discovery: which gItem clusters perform? |

---

## Node/Edge Properties

### On node:xitem (gItem-specific — already partially exists)

Confirming existing + one addition:

| Field | Type | x-history | Why | Status |
|---|---|---|---|---|
| `has_bom` | boolean | no | Manufactured vs traded | Exists |
| `is_raw_material` | boolean | no | gItem.physical.raw | Exists |
| `obsolescence_risk` | enum: low/medium/high | yes | NRV trigger frequency | Exists |
| `shelf_life` | string | no | Expiry-driven write-down trigger | Exists |
| `bc_costing_method` | enum: fifo/average/standard/specific | no | THE IAS 2 cost formula. Shield: no LIFO! | **NEW** |

### On node:org (entity-level inventory summary)

| Field | Type | x-history | Why |
|---|---|---|---|
| `inventory_total` | decimal | yes | Total inventory carrying amount. Part of working capital. Reserve: cash locked. |
| `inventory_nrv_writedown` | decimal | yes | NRV write-down recognized this period. P&L hit → equity → KBR. |
| `inventory_aging_over_180d` | decimal | yes | Inventory older than 180 days. High = obsolescence risk. Shield + Reserve. |

---

## Rim Monitoring

| Monitor | Threshold | Consequence | Cadence |
|---|---|---|---|
| `bc_costing_method` on any gItem | = LIFO | **IAS 2 VIOLATION.** LIFO prohibited under IFRS. Immediate correction. | At BC setup + annual review |
| Standard cost vs actual cost | Variance > 5% | Standard cost not representative → inventory misvalued (IAS 2.21). Review standard. | Monthly (Adjust Cost batch job) |
| `inventory_aging_over_180d` relative to total | > 20% of total inventory | Obsolescence risk. NRV test required. Likely write-down. | Monthly |
| `inventory_nrv_writedown` | Material | P&L hit → equity → KBR. Board should be aware. | Each reporting date |
| Physical count vs book | Discrepancy > threshold | Inventory records unreliable. Count more frequently. | Annual minimum (more frequent for high-value) |
| IC inventory at period-end | Any gItem bought from group entity still in buyer's stock | Unrealized IC profit must be eliminated. IC elimination ergon. | Each reporting date |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| LIFO used for IFRS reporting | IAS 2 violation. Auditor qualification. Inventory + COGS misstated. | Shield bright-line |
| NRV not tested | Inventory overstated → assets overstated → equity → KBR | #3 Optimistic |
| Obsolete inventory not written down | Same — hiding losses in inventory | #3 Optimistic |
| Standard cost stale (not updated) | Inventory valuation diverges from reality → COGS wrong | Shield compliance |
| IC markup on unsold inventory not eliminated | Group inventory overstated. THE most common consolidation error. | #5 IC concealment |
| Abnormal waste included in inventory cost | Cost inflated → inventory overstated | IAS 2.16 violation |
| Physical count not performed | Inventory records unreliable. Auditor may qualify. | Shield + #2 Fictitious (Wirecard parallel: do the goods exist?) |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — cost determination, cost formula (BC Costing Method = IAS 2 decision, NO LIFO), NRV test, IC inventory profit link, BC setup implications (Item Card fields, key batch jobs), xItem mapping (gItem only), S-R-S view, inventory aging + obsolescence monitoring |
