# Business Central — Tentixo Playbook

**Version**: 1.0
**Status**: Active
**Created**: 2026-05-26
**Updated**: 2026-06-05
**Scope**: BC knowledge capture — architecture, operations, bookkeeping, client status

> Living document. Captures what Chris has learned about BC from Morre, current client setups,
> and conventions to follow when working with Claude Code on BC-related tasks.

---

## 1. Context

**Me**: Chris Mansson, Client Director at Tentixo (Stockholm-based boutique Nordic cybersecurity + ERP advisory firm).

**Co-founder & technical lead**: Lars Mårelius ("Morre"). He's the deep BC operator and architect. He teaches Socratically — drills the architecture before the UI — and is strongly opinionated about doing things the "right" way the first time rather than patching later.

**My BC level**: Learning. Strong on commercial/strategic framing, conceptually solid on architecture, weak on UI muscle memory and edge cases.

**Active BC engagements**:
- **Tinky Minds Lab AB** — first practical setup. 18,000 SEK Heat Map engagement (incl. 2 workshops). Used as a real-world exercise to learn the full customer→project→invoice flow in Tentixo's sandbox.
- **Formpipe** — newly signed BC-support contract. Spinning up a new Microsoft tenant in October 2026. Engagement scope: optimise finance operations and evaluate which third-party integrations (TimeLog, Younium, Rillion, etc.) can be replaced by BC-native functionality.
- **Lasernet** — ongoing BC governance programme (separate engagement, less active for me personally).

---

## 2. How Morre teaches (working conventions)

When I'm getting help on BC tasks, default to these patterns — they match how Morre frames things:

- **Architecture before UI.** Always orient on which layer of the hierarchy you're touching (see §3) before walking through buttons and field names.
- **Think before you do.** For each step, name the decision being made and surface trade-offs explicitly rather than picking the obvious default silently.
- **Posting groups are the magic.** Most "how do I make BC do X" answers route through posting group setup, not workflow customisation.
- **Pricing belongs in price lists, not items.** Item Unit Price should usually be 0 (or a reference catalogue price). Customer-specific or project-specific prices override via price lists.
- **Resources = "we sell you". Employees = "you work for us".** Separate records, both needed for people-driven engagements.
- **Service-type Items, not Inventory.** Inventory type triggers stock tracking, negative inventory traps, valuation noise — wrong for consulting.
- **Transaction-based, not database-based.** BC's strength vs systems like TimeLog: posted entries stay in the ledger. Reversals create audit trail. Avoid any pattern that suggests "just edit the value."

---

## 3. Core architectural model

### 3.1 The layered hierarchy

Every layer depends on the one below. Get a lower layer wrong → everything above breaks.

```mermaid
graph TD
    L0["<b>Layer 0</b><br/><i>Number Series</i>"]
    L1["<b>Layer 1</b><br/><i>Chart of Accounts</i>"]
    L2["<b>Layer 2</b><br/><i>Posting Groups</i><br/>(General + VAT,<br/>Business + Product,<br/>Customer, Project)"]
    L3["<b>Layer 3</b><br/><i>Master Data</i><br/>(Customers, Items,<br/>Resources, Employees)"]
    L4["<b>Layer 4</b><br/><i>Project</i>"]
    L5["<b>Layer 5</b><br/><i>Project Journal →<br/>Project Invoice</i>"]

    L0 --> L1 --> L2 --> L3 --> L4 --> L5

    style L0 fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style L1 fill:#E74C3C,stroke:#0E474E,stroke-width:2px,color:#fff
    style L2 fill:#E67E22,stroke:#0E474E,stroke-width:2px,color:#fff
    style L3 fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style L4 fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style L5 fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
```

**Five "people" registers in BC** — the same person can appear in multiple registers, each serving a different purpose:

| Register        | Purpose                                   | Used by                                   |
|-----------------|-------------------------------------------|-------------------------------------------|
| Employee        | "You work for us" — payroll, HR           | Payroll, employment records               |
| Resource        | "We sell you" — billable rates            | Project Journal lines, time sheets        |
| Contact         | CRM — relationships, interactions         | Person Responsible on Project card         |
| User            | System login — controls who can post      | Project Manager, posting restrictions      |
| Customer/Vendor | Business entity                           | Invoicing, AP/AR                          |

*Person Responsible on the project card pulls from **Contacts**. Project Manager pulls from **Users** (or Employee/Resource — check which register the field draws from).*

### 3.2 GVH framework (Goods / Virtual / Human)

Tentixo's chart of accounts is organised around three sales categories. The CoA's intent is to expose **cost structure**, not just categorise the deliverable.

| Range | Type    | Cost driver            | Examples                        |
|-------|---------|------------------------|---------------------------------|
| 30xx  | Goods   | Physical, shipping     | Hardware resale                 |
| 31xx  | Virtual | Low marginal, self-serve | Licenses, electronic services |
| 32xx  | Human   | Employees, HR          | Consulting, advisory            |

**Litmus test**: if we remove humans, can we still deliver? If no → Human, regardless of pricing model. *Heat Map is Human (Consulting) — fixed price doesn't override delivery reality.*

**CoA intent = cost structure, not product type.** A Virtual item (e.g., a fixed-price package) can land on a Human/Consulting account (32xx) if it's human-bound — because the chart of accounts exposes *what costs the company carries* (employees, HR, shipping), not what the deliverable looks like. This is the conversation you need to have with every client and they never have time for.

**VAT subcategory — Electronic Service**: Within Virtual, there's a VAT-significant distinction. A license downloaded from a website = electronic service (specific VAT rules for cross-border EU). Same license shipped on a CD-ROM = still Virtual, but not electronic service. Reactive support *can* be electronic service if minimal human involvement; heavy support is just "service." The VAT Prod. Posting Group handles this (separate rows in the VAT Posting Setup for SERVICE vs ELECTRONIC SERVICE).

### 3.3 BC module map

*(diagram: `ai/docs/BC_CentralParts-chris.png`)*

```mermaid
graph LR
    subgraph Finance
        GL["<b>General Ledger</b><br/><i>Receivables, Payables,<br/>Cash Mgmt, G/L Budget,<br/>Cost Acc.</i>"]
        FA["Fixed Assets"]
        DOC["Documents"]
        ITEM["Items"]
        APR["Approval<br/>[Workflow]"]
    end

    subgraph Sales
        MKT["Marketing"] --> SALES["Sales"] --> ORD["Order"]
    end

    subgraph Supply Chain
        PUR["Purchase"] --> PLAN["Planning"] --> MFG["Manufacturing<br/><i>(Premium)</i>"]
        MFG --> WH["Warehouse / Bin"]
        WH --> INV["Inventory"]
    end

    subgraph Services
        HR["HR"] --> RES["Resources<br/><i>Person / Machine</i>"]
        RES --> PROJ["Jobs<br/>[Projects]"]
        PROJ --> SVC["Services<br/><i>(Premium)</i>"]
        PROJ --> SUB["Subscription<br/>Billing"]
    end

    ITEM --> APR

    style GL fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style FA fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style PROJ fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style RES fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style ITEM fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style MFG fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#E0F7FA
    style WH fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#E0F7FA
    style SVC fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
```

**Document lifecycle**:

```mermaid
graph LR
    OPP["Opportunity"] --> QUO["Quote"] --> ORD["Order"] --> INV["Invoice"]
    CON["Contact"] --> CUST["Customer"]
    CON --> VEND["Vendor"]
    CON --> EMP["Employee"]
    CON --> RES["Resource"]

    style OPP fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style QUO fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style ORD fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style INV fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
    style CON fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style CUST fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style VEND fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style EMP fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style RES fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
```

**Contact is the root of "people"**: Contact → branches into Customer, Vendor, Employee, Resource. A single contact can spawn multiple entity types.

### 3.4 The WHO × WHAT posting matrix

BC's core elegance — and the lens Morre uses to evaluate every implementation:

- **Business Posting Group** on the Customer = WHO we sell to (EXT, NATIONAL, INTERCO)
- **Product Posting Group** on the Item/Resource = WHAT we sell (CONSULTING1/2/3, SERVICES, GOODS)
- **General Posting Setup** = the matrix that maps every (WHO, WHAT) combination to a specific G/L revenue account
- **Same logic for VAT**: VAT Bus × VAT Prod → correct moms rate + accounts

Companies that skip this either duplicate items (e.g., "Heat Map - Sweden" vs "Heat Map - Norway") or fall into dimension overload (Formpipe's pre-acquisition mistake).

### 3.5 Posting flow — how journal entries reach the ledger

*(diagram: `ai/docs/BC-Posting-chris.png`)*

```mermaid
graph TD
    JRN["<b>Journal</b><br/><i>Batch + settings</i>"]
    VAL{{"Validation"}}
    POST["<b>Post</b>"]
    PG["Posting Groups<br/>+ Tags"]
    LED["<b>Ledger(s)</b>"]

    JRN --> VAL --> POST --> PG --> LED

    style JRN fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style POST fill:#E74C3C,stroke:#0E474E,stroke-width:2px,color:#fff
    style PG fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style LED fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
```

**G/L Account posting in detail** (e.g., document GJ1234):

1. General Journal entry in a batch
2. **Post** triggers the posting engine
3. Engine reads **Gen Posting Type** (Purchase / Sale / Settlement) and the **four posting groups**:

| Posting Group | Question it answers                            |
|---------------|------------------------------------------------|
| Gen Business  | **Whom?** (who are we doing business with)     |
| Gen Product   | **What?** (what are we selling/buying)         |
| VAT Business  | **Who + Where?** (jurisdiction of counterparty)|
| VAT Product   | **What + Level?** (what type, at what VAT rate)|

4. **"All Five or None!"** — Gen Posting Type + all four posting groups must be set together, or none at all. You can't partially specify.
5. Output: document number → **General Ledger (CoA)** entry on the resolved account (e.g., 3010), and VAT% matched by Biz+Prod → **VAT Entries** ledger.

### 3.6 Document posting — invoices and fixed assets

*(diagram: `ai/docs/BC-Posting-from-document-chhris.png`)*

**Fixed Asset Vendor Invoice posting** — more complex, touches more ledgers:

```mermaid
graph TD
    VI["Vendor Invoice"] --> PJ["Purchase Journal"]
    FAR["FA Register<br/><i>FA Class, Subclass,<br/>Location</i>"] --> PJ
    INS["Insurance Register"] --> PJ
    PJ --> POST["<b>Post</b>"]
    POST --> GL["General Ledger<br/>(CoA)"]
    POST --> VAT["VAT Entries"]
    POST --> VL["Vendor Ledger"]
    POST --> ICL["Insurance Coverage<br/>Ledger"]
    POST --> FAL["FA Ledger"]

    style POST fill:#E74C3C,stroke:#0E474E,stroke-width:2px,color:#fff
    style GL fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
    style VAT fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style VL fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style FAL fill:#E67E22,stroke:#0E474E,stroke-width:2px,color:#fff
    style ICL fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style VI fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style FAR fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style INS fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
```

- Prerequisites: FA Card must exist (FA Class, FA Subclass, FA Location). Insurance Card if the asset is covered.
- Tags: Posting Type, Document Type, FA Posting Type, Depr. Book Code
- Posting Groups: Gen Business, Gen Product, VAT Business, VAT Product, **Vendor**, **FA**

**Vendor Invoice Payment registration**:

- Purchase Journal (with Bank Account as balancing account) → Post → "Apply Payment to Invoice" on the Vendor Ledger
- Posting Groups: Vendor + Bank Account → writes to General Ledger + Bank Account Ledger

### 3.7 Project module ERD

*(diagram: `ai/docs/BC-Project-ERD-Chris.png`)*

```mermaid
graph TD
    CUST["<b>Customer</b>"] -->|"Bill-to<br/>Customer No."| JOB["<b>Job Card</b><br/>(Project)"]
    CUST ---|"Price"| ITEM["<b>Item</b>"]
    JOB --> JTN["Job Task No."]
    JTN --> PL["<b>Planning Lines</b><br/><i>Billable / Budget /<br/>Both</i>"]
    PL -->|"Create Job<br/>Sales Invoice"| IL["Invoice Lines"]
    IL --> IH["<b>Invoice Head</b><br/><i>Pre-posted → Posted</i>"]
    IL --> IR["Item / Resource"]
    JOB ---|"Price"| WT["Work Type"]
    RES["<b>Resource</b><br/><i>IND / MACH</i>"] --> WT
    RES --> RG["Resource Group"]
    RG --> AVAIL["Availability"]
    GLA["G/L Account"] -.-> PL
    TS["Time Sheet"] -.->|"?"| PL
    CAL["Calendar"] -.->|"?"| TS

    style JOB fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style CUST fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style PL fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style IH fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
    style RES fill:#E67E22,stroke:#0E474E,stroke-width:2px,color:#fff
    style ITEM fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style WT fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#E0F7FA
```

- **Planning Lines** are the journal entries: Billable, Budget, or Both Billable and Budget
- **"Create Job Sales Invoice"** pulls Planning Lines → Invoice Lines → Invoice Head
- **G/L Account** can also appear on Planning Lines (for non-item, non-resource costs)
- **Time Sheet** and **Calendar** connections shown with "?" — integration points that may or may not be enabled

### 3.8 VAT Business Posting Groups — geographic model

*(diagram: `ai/docs/BC-VAT-pg-Chris.png`)*

```mermaid
graph TD
    subgraph EU
        subgraph SE
            GGRSE(("GGRSE"))
            CUSTSE["Cust"]
        end
        subgraph DK
            CUSTDK["Cust<br/>w/ VAT"]
        end
        GGRSE -->|"DOM"| CUSTSE
        GGRSE -->|"ORG-EU"| CUSTDK
    end
    subgraph GB
        GGRGB(("GGRGB"))
        CUSTGB["Cust"]
        GGRGB -->|"DOM"| CUSTGB
    end
    GGRSE -->|"EXP"| CUSTGB
    GGRGB -->|"EXP"| CUSTSE
    GGRGB -->|"EXP"| CUSTDK

    style GGRSE fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style GGRGB fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style CUSTSE fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style CUSTGB fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style CUSTDK fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
```

- Each country has its own **GGR** (effectively the VAT Bus. Posting Group for that entity)
- **DOM** = domestic (same country), **EXP** = export (cross-border), **ORG-EU** = EU organisation (intra-community VAT rules)
- DK customer "with VAT" shows that some jurisdictions require VAT registration on the customer card
- This is why the WHO × WHAT matrix is so powerful — same item, different customer country, correct VAT treatment automatically

### 3.9 Warehouse module

*(diagram: `ai/docs/BC-Warehous-ERD-Chris.png`)*

Not directly relevant for consulting/services, but important for Goods-type engagements and Formpipe's product lines.

```mermaid
graph TD
    IPG["Inventory<br/>Posting Group"] --> LOC["<b>Location</b>"]
    LOC --> ZONE["Zone"]
    ZONE --> BIN["Bin<br/><i>Fixed / Floating /<br/>(Adjustment)</i>"]
    BIN --> PITEM["pItem"]
    LOC -.->|"Directed:<br/>Bin Types +<br/>Bin mandatory"| BIN
    ZONE ---|"Movement<br/>Worksheet"| ZONE

    style LOC fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style ZONE fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style BIN fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style PITEM fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
```

**Inbound flow**: Purchase Order → Receipt (Released) → Put-Away (Released)

**Outbound flow**: Sales Order (Released) → Pick (Register) → Shipment (Post) → Invoice

If Bin is **not mandatory**: just "Recording" (simplified tracking without bin-level precision).

### 3.10 Why Project (not direct Sales Invoice) for "messy" engagements

Project model wins over direct invoicing when:
- Engagement is evolving, not a one-off transaction
- Mixed billing (fixed-price + hours + travel + future licenses) in one container
- Need analytical granularity per sub-element preserved through to invoicing
- Want budget vs actual and margin reporting

Keep recurring/subscription billing **outside** the project — keeps project P&L clean.

---

## 4. Operational playbook — the 8-step flow

Morre's prescribed order for setting up a new consulting engagement. Order matters because of layer dependencies.

```mermaid
graph LR
    S1["<b>1. Customer</b>"] --> S2["<b>2. Contact</b>"] --> S3["<b>3. Item</b><br/><i>(Service-type)</i>"]
    S3 --> S4["<b>4. Resource</b>"] --> S5["<b>5. Employee</b>"] --> S6["<b>6. Project</b>"]
    S6 --> S7["<b>7. Project<br/>Journal</b>"] --> S8["<b>8. Create<br/>Invoice</b>"]

    style S1 fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#fff
    style S2 fill:#1E3A45,stroke:#0E474E,stroke-width:2px,color:#E0F7FA
    style S3 fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style S4 fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style S5 fill:#006D75,stroke:#0E474E,stroke-width:2px,color:#fff
    style S6 fill:#00838F,stroke:#0E474E,stroke-width:2px,color:#fff
    style S7 fill:#E74C3C,stroke:#0E474E,stroke-width:2px,color:#fff
    style S8 fill:#27AE60,stroke:#0E474E,stroke-width:2px,color:#fff
```

### Step 1 — Customer

| Field                    | Tentixo convention (domestic SE B2B) |
|--------------------------|--------------------------------------|
| Gen. Bus. Posting Group  | `EXT`                                |
| VAT Bus. Posting Group   | `EXT`                                |
| Customer Posting Group   | `DOMESTIC`                           |
| Country/Region Code      | `SE`                                 |
| Registration No.         | org.nr (e.g. `5566778899`)           |
| VAT Registration No.     | `SE` + org.nr + `01`                 |
| Payment Terms            | `30D`                                |

`Registration No.` is on General FastTab (newer BC) or Invoicing FastTab (older). Don't confuse with `VAT Registration No.`

### Step 2 — Contact

Creating a Customer auto-creates a company-type Contact card. Open it and **add person contacts** (decision-maker, billing/AP, technical lead).

Watch for duplicate contacts if the same company is both customer and vendor (Idonex pattern). Merge via Contact → Actions → Merge.

### Step 3 — Item (Service-type)

| Field                    | Value                                |
|--------------------------|--------------------------------------|
| Type                     | `Service`                            |
| Base Unit of Measure     | `PCS`                                |
| Gen. Prod. Posting Group | `CONSULTING1` (Human-bound delivery) |
| VAT Prod. Posting Group  | `VAT25`                              |
| Inventory Posting Group  | blank                                |
| Unit Price               | `0` (override via price list)        |

### Step 4 — Resource (the "we sell you" side)

| Field                    | Value                                              |
|--------------------------|----------------------------------------------------|
| Type                     | `Person`                                           |
| Base Unit of Measure     | `HOUR`                                             |
| Unit Cost                | `560` (my internal cost rate)                      |
| Unit Price               | `1400` (default sell rate — override per client/project) |
| Gen. Prod. Posting Group | `CONSULTING1`                                      |
| VAT Prod. Posting Group  | `VAT25`                                            |

**Trap**: Unit Cost and Unit Price sit next to each other. Don't change Unit Cost when you mean Unit Price (Morre caught me on this).

### Step 5 — Employee (the "you work for us" side)

Parallel record to Resource. Where the Resource card links via `Employee No.`, populate it. Payroll-side setup is a separate workstream.

### Step 6 — Project

| Field                 | Value                                                  |
|-----------------------|--------------------------------------------------------|
| Bill-to Customer No.  | the customer                                           |
| Project Posting Group | a consulting-aligned group with WIP account configured |
| Status                | `Open`                                                 |
| Person Responsible    | the lead consultant                                    |

**Project Tasks**: start with **one** posting-type task (e.g., `1000 Heat Map`). Add sub-tasks only when engagement splits (retainer + project work, or pre-study/execution/post). Don't pre-optimise.

**WIP method must match project type.** If a T&M project has WIP method set to "Fixed Price" (or vice versa), the WIP postings hit the wrong chart-of-accounts entries. Check WIP Method on the project card before any WIP calculation.

### Step 7 — Project Journal

**Journal batch hygiene**: Before posting, check which batch you're in (top of the journal page). Batches let multiple people work in the same journal simultaneously without collisions. There's a dedicated **API batch** with its own number series — never post manually to it. Use the `DEFAULT` batch for manual work.

Two line types for fixed-price engagements:

```
Line 1 (revenue capture):
  Type=Item, No.=HM-LITE, Project Task=1000, Qty=1,
  Unit Price=18000 (override), Line Type=Billable

Line 2 (cost capture):
  Type=Resource, No.=CHRIS, Project Task=1000, Qty=16,
  Line Type=Non-Billable
```

For T&M instead: Resource lines are `Billable`, no Item line needed.

**Posting date shortcuts**: Type `T` + Tab for today's date. For prior months, type the short date directly (e.g., `0430` for April 30).

**Unit Price vs Unit Price (LCY)**: If the project is in a foreign currency, set the price in `Unit Price`. `Unit Price (LCY)` is the local-currency equivalent and auto-calculates. For SEK projects, they're the same — but edit `Unit Price`, not the LCY field.

**Late hours**: Post old hours to the correct past month (posting date = when the work happened). BC's invoicing picks up anything uninvoiced regardless of date, so late-reported hours get captured automatically on the next invoice run.

Post the journal (F9).

### Step 8 — Create Project Invoice

**Two ways to create the invoice:**
1. **Global**: Search → "Create Project Sales Invoice" → OK. Takes all uninvoiced billable lines across projects.
2. **Per task line**: From the project task, Manage → Line → Documents → Create Sales Invoice. Invoices just that task — useful when you want to bill pre-study separately from execution.

The draft Sales Invoice is linked to the project. **Project-linked lines are locked** — you can't change quantities or prices on them. You *can* add extra lines (e.g., comments, one-off charges), but those additions won't be tracked in the project.

**Work Description field** (under "Show more" on the invoice header): Text that appears above the line items on the printed invoice. Use it for engagement descriptions, period references, etc.

Review header/lines/Statistics (F7), then Post & Send.

**Invoice structure (useful for API work)**: An invoice is just Head + Lines. The "head" contains everything that visually appears in the header *and* footer of the printed invoice — customer, payment terms, dates, addresses. Lines are the billable items.

After posting, the project ledger marks those lines as "invoiced" (a dot/boolean). **BC will never invoice the same line twice** — this is the core safety net for automation.

After posting, open Project Statistics for budget vs actual, billable vs non-billable, cost vs revenue, margin.

---

## 5. Bookkeeping fundamentals

*From Morre session, June 2026*

### 5.1 Double-entry: always zero

Every transaction has a plus and a matching minus — the books must always net to zero. This is "double-entry Italian bookkeeping." Start every transaction by thinking about the bank: did money come in, go out, or stay?

**The sign convention** (counterintuitive until you internalise it):

| Account type       | Sign  | Why                                                              |
|--------------------|-------|------------------------------------------------------------------|
| Bank (assets, 1000s)     | **+** | You have money — makes sense                              |
| Liabilities (2000s)      | **−** | You owe money — balances the asset                        |
| Revenue (3000s)          | **−** | A sale puts + in the bank, so the revenue entry must be − |
| Costs (4000s+)           | **+** | Paying salary takes − from the bank, so the cost entry is + |

**Example — share capital**: Shareholders invest 100,000. Bank = +100,000, Share Capital = −100,000 (you owe it back). Net = zero.

**Example — salary**: Pay 10,000 salary. Cost = +10,000, Bank = −10,000. Net = zero.

**Example — sale with VAT**: Sell 80,000 + 20% VAT = 100,000 collected. Bank = +100,000, Revenue = −80,000, VAT liability (2640) = −20,000. Net = zero.

### 5.2 Chart of accounts — the number logic

| Range       | Type                | Sign  | What lives here                              |
|-------------|---------------------|-------|----------------------------------------------|
| 1000s       | Assets              | +     | Bank (1930), fixed assets, receivables       |
| 2000s       | Liabilities         | −     | Loans, VAT payable (2640), share capital     |
| 3000s       | Revenue             | −     | Sales income                                 |
| 4000s       | Cost of goods sold  | +     | Costs directly tied to a sale (mirror of 3000s) |
| 5000s–7000s | Operating costs     | +     | Salaries, depreciation, rent, etc.           |

**The 3000/4000 mirror**: Revenue account 3011 (goods revenue) pairs with 4011 (purchase of goods). Same structure — one digit apart. This is deliberate.

**GVH in the 3000s** (Tentixo/Formpipe convention):
- 30xx — Goods
- 31xx — Services (virtual, low-marginal)
- 32xx — Human (consulting)
- 33xx — Odd sales (one-offs you want separated from core revenue)

**Tree rule**: The chart of accounts is a tree (each account has one parent). If you use granular child accounts, you must not also post to the parent — they overlap. Pick one level. *(Formpipe violated this with manual bookings — led to confusion.)*

### 5.3 Cost vs. investment — fixed assets

Buying something expensive (a building, equipment) is not a cost — it's converting one asset form (cash) to another (fixed asset). Both stay on the balance sheet:

- Bank (1930) = −1,000,000 (cash out)
- Fixed Asset (e.g., buildings) = +1,000,000 (value in)

Net effect on income statement: zero. You looped within the balance sheet.

### 5.4 Depreciation and appreciation

**Depreciation**: The asset wears down. Each year, move value from the balance sheet to the income statement:
- Fixed Asset = −10,000 (value decreases)
- Depreciation cost (e.g., 7821) = +10,000 (cost recognized)

**Appreciation**: A repair increases the asset's value beyond what was there:
- Bank = −20,000 (paid for repair)
- Fixed Asset = +20,000 (value increases)
- Appreciation account (7xxx) = −20,000 (effectively profit — you created value)

### 5.5 Revenue recognition — when did it happen?

**Critical distinction** (Swedish terms are more precise than English here):

| Swedish          | English    | What it means                                                        |
|------------------|------------|----------------------------------------------------------------------|
| **Inbetalning**  | Payment in | Cash hits the bank (balance sheet event)                             |
| **Intäkt**       | Revenue    | The earning event — when you can say "I earned this" (income statement event) |

These are **different events at different times**. Getting paid in advance ≠ earning the revenue. Invoicing in June for May work → revenue belongs in May, not June. The income statement cares about *when the value was delivered*, not when cash moved.

### 5.6 Work in progress (WIP) and recognized revenue

IFRS requires showing revenue you know you'll earn (signed contracts, partially completed projects) — otherwise the company looks undervalued.

**The mechanism**: Book revenue as − (income statement) and a matching + on a "fake bank account" (a WIP/recognized receivable on the balance sheet). When the real invoice goes out, cancel both entries and replace with the real sale + real receivable.

**BC-specific flow**: Project module handles this. Mark project as X% complete → press a button → BC books the WIP entries. When you create the actual invoice, the WIP entries get reversed automatically.

**BC "shipped not invoiced"**: Goods shipped but not yet invoiced sit on a specific account — this is the "fake money" that represents revenue earned but not yet billed.

### 5.7 Pre-booked revenue from signed orders (the Formpipe/HubSpot pattern)

When a firm order is signed (e.g., 12-month contract), BC books forward-looking revenue:
1. Signed order creates 12 monthly sales orders in BC
2. Each month, order → invoice, which cancels the pre-booking and replaces it with a real entry
3. Revenue moves from "recognized/pre-booked" to "actual" one month at a time

### 5.8 Incoterms — when risk transfers

For physical goods, the revenue event depends on **Incoterms** (international trade terms, ~200 years old):
- **Ex Works**: risk transfers when buyer picks up the package outside your warehouse
- **Alongside Ship**: risk transfers at the crane — quay side vs. ship side determines whose insurance pays

The point: there must be zero ambiguity about *when* the sale happened. Bookkeeping follows the risk transfer, not the payment.

---

## 6. Operational patterns (from Masha sessions)

*See `ai/reports/masha-bc-sessions.md` for full session notes. Below captures what's generally useful.*

### 6.1 Swedish VAT rates in practice

| Rate | VAT Prod. Posting Group | Applies to                                           |
|------|------------------------|------------------------------------------------------|
| 25%  | Standard               | Most goods and services in Sweden                    |
| 12%  | Medium                 | Hotels in Sweden, restaurant food in Sweden          |
| 6%   | Low                    | Domestic transport (cabs, flights within SE)         |
| 0%   | Zero                   | Foreign services, international flights, insurance, health, banking |

**Location-based rule**: VAT rate follows where the service is consumed, not purchased. Swedish hotel = 12%. Spanish hotel = 0%. Cab in Amsterdam = 0%. Cab in Stockholm = 6%.

**Split-VAT transactions**: When one bank line contains items at different rates (e.g., Uber ride + tip), post as multiple journal lines under the **same document number**. Each line gets its own posting groups. Bank balancing line has no posting groups. Total must be zero.

**Business dinners**: Max 300 SEK/person deductible. Alcohol is always non-deductible. Only the food portion (up to the limit) gets 12% VAT.

### 6.2 Fixed assets — Swedish thresholds

| Category              | Value range        | Depreciation                         |
|-----------------------|-------------------|--------------------------------------|
| **LVA** (low-value)   | 2,000–20,000 SEK  | Written off immediately at acquisition |
| **Main fixed asset**  | > 20,000 SEK      | Depreciated over N years (e.g., 3 years for laptops) |

- Post acquisition cost via **Fixed Asset Journal** (amount ex-VAT — VAT already handled in the receipt posting)
- For main assets: run **Calculate Depreciation** monthly (Project card → Actions → Tasks). Creates journal lines moving value from FA account to depreciation expense account.
- LVA: depreciation start date = end date → book value immediately zero.
- On disposal: post in FA journal, then **manually** set FA card to Inactive + Blocked (disposal posting doesn't update the card status automatically).

### 6.3 Payment reconciliation via bank XML

Semi-automated matching of bank transactions to open invoices:

1. Download XML transaction file from bank (monthly)
2. BC: Payment Reconciliation Journal → Import Bank Transactions → upload XML
3. BC auto-matches most transactions to open invoices
4. Remove receipt lines (already posted as G/L entries)
5. Validate matches — check that BC picked the correct invoice (watch for same-amount different-month false matches)
6. Post the reconciliation

This is the main mechanism for "gluing" payments to invoices at scale. For one-off manual matching: Sales/Purchase Journals → Payment document type → Apply Entries.

### 6.4 Foreign currency — exchange rate gain/loss

When paying invoices in foreign currency (EUR, USD), the exchange rate at invoicing vs. payment creates a difference:

- **Exchange losses** (overpayment): BC offers "Transfer Difference to Account" in the payment reconciliation — one-click resolution to the exchange loss account.
- **Exchange gains** (underpayment): This option is **not available** in BC. Must create a manual G/L journal entry to record the gain. Masha considers this a BC bug; worth verifying with Morre whether it's a configuration issue.

### 6.5 Employee reimbursements

When an employee pays a company expense from a personal card:

- Post the expense to the correct G/L account, but use **Employee account** (not bank) as balancing account
- Creates an open entry on the employee ledger (company owes them)
- Apply against salary or separate reimbursement payment to close the entry

### 6.6 Journal batch presets

BC allows different journal batches with different default balancing account types. Useful for workflow efficiency:

- "Danske" batch → default balancing = Bank Account (for receipt posting)
- "Default" batch → default balancing = G/L Account (for salary distribution, tax entries)
- "API" batch → reserved for automated postings (never use manually)

**Saved journal templates** ("Standard Journals"): Pre-populated recurring entries (e.g., monthly salary lines). Load template, verify amounts, post. Useful when the same accounts repeat but amounts vary.

---

## 7. Common gotchas (lessons learned the hard way)

- **Wrong tenant**: Tentixo company vs Cronus demo. Check top-right tenant selector before anything else.
- **Inventory item type for services**: triggers negative inventory + valuation drama. Always `Service` for what we sell.
- **Unit Cost vs Unit Price** on the Resource card: adjacent fields, easy to confuse. Cost = what I cost the firm; Price = what the firm sells me for.
- **Hard-coded prices in items**: don't. Use price lists. Items at 0 (or reference price), overrides on the project/invoice line.
- **Project Journal columns scrolled off-screen**: Project Journal lines have ~20 columns; only the leftmost fit. Personalize the layout (gear icon → Personalize) and pull Quantity, Unit Price, Line Type into view. Hide irrelevant ones (Location Code).
- **Job vs Project terminology**: Microsoft renamed Jobs → Projects in BC 2023 wave 1. Older sandboxes/extensions may still say "Job Journal". Same functionality.
- **VAT lookup populates address on one line**: cut/paste into separate fields.
- **Country/Region = SE is mandatory** for VAT validation.
- **Finalize WIP before closing a project**: If a project is at 90% WIP and you close it without running the final WIP calculation, the cancelling entries don't fire — you're left with orphaned WIP postings and manual cleanup. Always run WIP to 100% (or final state) before changing project status to closed.
- **Don't mix parent and child accounts in the CoA**: Post to either the summary account or its children, never both. Formpipe did this with manual bookings and it obscured what was what.
- **Cancelling entry on the wrong account type**: In the Formpipe/Sikri carve-out, a correction for a prepaid contract (2171) was accidentally booked to a post-pay account (1470). Automated code correctly treated it as post-pay, producing a ~500,000 SEK discrepancy. Then a manual fix compounded the error (minus instead of plus — doubling the mistake). Lesson: the account you post to determines how code and reports interpret the entry. A "small" misposting cascades.
- **Exchange rate gain asymmetry**: BC can auto-transfer exchange losses (overpayment) to the loss account via "Transfer Difference to Account" in payment reconciliation. But exchange gains (underpayment) require a manual journal entry — the auto-transfer option doesn't appear. Possibly a bug, possibly a configuration issue. Check with Morre.
- **FA disposal doesn't update the card**: After posting a disposal in the Fixed Asset Journal, the FA card status remains active. Manually set to Inactive + Blocked, otherwise it clutters the active asset list.

---

## 8. Tentixo posting group conventions (sandbox state)

| Group type                | Codes in use                                                                                              |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| Gen. Bus. Posting Group   | `EXT`, `NATIONAL`, `INTERCO`                                                                              |
| VAT Bus. Posting Group    | `EXT`, `NATIONAL`                                                                                         |
| Customer Posting Group    | `DOMESTIC` (1511 AR), `INTERCO` (1565 AR)                                                                 |
| Gen. Prod. Posting Group  | `CONSULTING1` (employees), `CONSULTING2` (sub-consultants), `CONSULTING3` (training, cost-only), `SERVICES`, `GOODS` |
| VAT Prod. Posting Group   | `VAT25`, `VAT12`, `VAT6`, `VAT0`                                                                         |
| Project Posting Group     | (consulting-aligned, with WIP account)                                                                    |

**CONSULTING tiers**:
- `CONSULTING1` — employees (highest margin)
- `CONSULTING2` — sub-consultants (e.g., Jeff)
- `CONSULTING3` — consultants in training (cost only, not sold)

---

## 9. Terminology cheat sheet (EN ↔ SV)

| English                  | Swedish                      | Notes                                                      |
|--------------------------|------------------------------|------------------------------------------------------------|
| Chart of Accounts        | Kontoplan                    | BAS-kontoplan is the Swedish standard                      |
| Posting Group            | Bokföringsmall               | Often kept in English                                      |
| General Posting Setup    | Allmän bokföringsinställning  | The WHO×WHAT matrix                                        |
| Customer Posting Group   | Kundbokföringsmall           | Drives AR account                                          |
| Item                     | Artikel                      | Service-type for consulting                                |
| Resource                 | Resurs                       | Type=Person for consultants                                |
| Project (was: Job)       | Projekt                      | Renamed BC 2023 wave 1                                     |
| Project Journal          | Projektjournal               | Where hours/items hit the project                          |
| Project Ledger           | Projektreskontra             | The transaction record                                     |
| WIP                      | PIA (Pågående arbete)        | Work in progress                                           |
| Registration No.         | Organisationsnummer          | Bolagsverket ID                                            |
| VAT Registration No.     | Momsregistreringsnummer      | `SE` + org.nr + `01`                                       |
| ORG Scheme               | Identifierarschema           | Peppol e-invoicing identifier code                         |
| EORI                     | EORI                         | EU customs ID — services don't need it                     |
| T&M                      | Löpande räkning              | Modern usage often just "T&M"                              |
| Retainer                 | Retainer-avtal               | Modern Swedish                                             |
| Double-entry bookkeeping | Dubbel bokföring             | Italian origin — every entry needs a balancing counter-entry |
| Balance sheet            | Balansräkning                | Assets (1000s) and liabilities (2000s) — must net to zero  |
| Income statement         | Resultaträkning              | Revenue (3000s) and costs (4000s+) — profit and loss       |
| Revenue (the event)      | Intäkt                       | When you earned it — not when cash arrived                 |
| Payment in               | Inbetalning                  | When cash actually hits the bank                           |
| Depreciation             | Avskrivning                  | Annual write-down of fixed asset value                     |
| Appreciation             | Uppskrivning                 | Increase in asset value (e.g., renovation)                 |
| Fixed asset              | Anläggningstillgång          | Long-lived asset on balance sheet, not expensed immediately|
| Recognized revenue       | Upparbetad intäkt            | Revenue booked before invoicing (WIP / IFRS requirement)   |
| Shipped not invoiced     | Levererat ej fakturerat      | Goods/services delivered but invoice not yet sent          |
| Incoterms                | Incoterms                    | International trade terms defining when risk transfers     |
| Prepaid                  | Förskottsbetald              | Payment received before service delivered (liability until earned) |
| Electronic service       | Elektronisk tjänst           | VAT subcategory of Virtual — self-serve, no human involvement |
| Journal batch            | Journalgrupp                 | Envelope for journal entries; separate batches for API vs manual |
| Base Unit of Measure     | Basenhet                     | International code matters for e-invoicing (EA = each, not PCS) |

---

## 10. Useful shortcuts

| Shortcut                     | What                                                             |
|------------------------------|------------------------------------------------------------------|
| `Alt+Q`                      | Tell Me search (find any page/action)                            |
| `F7`                         | Statistics on current document                                   |
| `F9`                         | Post                                                             |
| `T` + Tab (in date field)    | Today's date                                                     |
| Gear icon → Personalize      | Customise column layout per page (per user, safe to change)      |
| Right-click column header    | Hide / re-order columns                                          |
| Renumber Document Numbers    | Action in journals to fix numbering gaps after batch work        |

---

## 11. Active client status

### Tinky Minds Lab AB

- **Engagement**: Heat Map project (incl. 2 workshops), agreed 18,000 SEK ex moms
- **Customer card**: created in Tentixo sandbox. VAT validated, address populated (had to cut/paste from one-line VAT lookup). Country/Region SE set.
- **Contact card**: auto-created from customer. Person contacts to be added.
- **Item**: `HM-LITE`, Service type, CONSULTING1, VAT25, Unit Price = 0 (override on invoice)
- **Resource**: Chris (Person, HOUR, CONSULTING1, VAT25, cost 560, price 1400)
- **Employee**: Chris — record exists, linked to Resource
- **Project**: linked to Tinky, one task (`ITSEC`). Person Responsible = Chris (from Contacts). WIP method = Sales Value.
- **Status**: **First invoice posted** (May 27, 2026). Item line: 1× HM-LITE @ 18,000 SEK. Posted to ledger, visible in posted sales invoices.
- **Open question**: keep as catalogue SKU (HM-LITE with override pricing) or as one-off custom item? Morre says keep same item, override price via price lists — don't lock pricing into the item.

### Formpipe — TimeLog discovery

- **Engagement**: BC-support contract, optimise finance ops for October 2026 new tenant cutover
- **Tactical approach** (Morre): "We get the freedom, we interview people, set it up the way we want, then show them the granularity they can gain." Don't argue the architectural layer with the client — know it, implement it, demonstrate the value. Get CFO-level buy-in for structural changes; don't try to push bottom-up.
- **Discovery meeting 27 May 2026**: Therese Baly (Project Controller, Finance)
- **Key findings**:
  - **No TimeLog ↔ BC integration**. Manual PDF + Teams chat + Finance re-keys into BC. TimeLog may have had a BC integration partially configured but never completed.
  - **No customer key mapping**. Names diverge; no org.nr linkage. Greenfield mapping needed. Morre needs a two-column table (TimeLog customer ID ↔ BC customer No.) for automation.
  - **~100% T&M** in TimeLog. Licenses via Younium (separate). Fixed-price hacked as T&M @ 1000 SEK/h avg.
  - **Excel-based retainer reservation tracking** is the highest-risk manual process. Retainers are pre-invoiced; overages billed the following month.
  - **Internal/non-billable projects invisible to Finance** (live only in TimeLog). Key question: do they have non-invoiceable lines (e.g., project entertainment costs)?
  - **Late hour reporting** is a real issue — need to understand how often hours arrive months late and how that affects invoicing.
  - **Denmark is the political blocker** (runs payroll in TimeLog). Sweden wants out.
  - **Therese is change-receptive**. Already worked with Gustav Kinnander ("Gurra") on a near-shipped BC time-reporting solution.
  - **TimeLog has project management features** (Gantt, milestones, task planning) beyond just time reporting — someone may depend on these.
- **What Morre needs for API automation**: How hours map to invoice lines (the "fakturaunderlag"), contract types (T&M vs fixed, pre-pay vs post-pay), and whether there's a super-user who plans all projects in TimeLog.
- **Next steps**:
  - Follow-up with Therese for sample `fakturaunderlag` PDFs
  - Excavate the Gurra-Therese BC solution that almost shipped
  - Decide whether to talk to Finance (hand-keying team) and STG BI/reporting team
  - Decide DK scope (carve out or address)
  - Get customer ID mapping table (or determine it doesn't exist yet)

---

## 12. Open questions / things to learn next

- Project Posting Groups in depth — WIP completion methods, when each fires, how to avoid the "close without final WIP" trap *(partially covered in §5.6 — need hands-on practice)*
- Recurring billing in BC (Younium replacement question) — what BC offers natively
- Multi-entity / intercompany — relevant for Formpipe SE/DK split
- BC + Power BI as single source of truth (Therese explicitly asked for this)
- Graph API / Business Central API patterns for automation (Python tooling Morre and I are building)
- Sales Price Lists in detail — customer-specific, project-specific, resource-specific overrides
- Time Sheet feature — when to enable on Resource cards, approval flow setup
- Dimensions strategy — when to use vs. when posting groups are sufficient (avoid Formpipe's dimension overload)
- Revenue recognition timing for physical goods — Incoterms + BC's handling of shipped-not-invoiced *(Morre flagged he needs to research this further)*
- Prepaid vs. post-pay account handling in carve-out scenarios — the 2171/1470 distinction and how to keep automated code safe

---

## 13. Using this file with Claude Code

- Keep as `ai/reports/business-central-playbook.md`. Source material (.docx, .png) lives in `ai/docs/`.
- Update the "Active client status" and "Open questions" sections as engagements evolve.
- When Morre walks me through a new BC area, append a section here before the knowledge fades.
- Treat the conventions in §2 as standing instructions — if Claude Code suggests a pattern that conflicts (e.g., hardcoded item prices, Inventory-type for services), push back.

---

**Version History**

| Version | Date       | Changes                                                                                          |
|---------|------------|--------------------------------------------------------------------------------------------------|
| 1.0     | 2026-06-04 | Consolidated from three Morre sessions + six architecture diagrams. Applied TXO look and feel.   |
| 1.1     | 2026-06-05 | Added §6 operational patterns from Masha session (VAT rates, fixed assets, payment reconciliation, exchange rates). New gotchas. |
