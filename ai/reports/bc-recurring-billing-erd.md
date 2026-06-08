# BC Recurring Billing Module — Entity Relationship Diagram

**Version**: 1.0
**Status**: Reference
**Created**: 2026-06-08
**Updated**: 2026-06-08
**Scope**: Table structure and relationships for the BC Subscription Billing module (from microsoft/BCApps)
**Source**: `microsoft/BCApps` → `src/Apps/W1/Subscription Billing/App/`

> The Recurring Billing module (officially "Subscription Billing") was added to BC as a first-party
> app. It handles subscription contracts, recurring invoicing, revenue deferrals, price updates,
> and contract renewals. This document maps the entity structure.

---

## 1. Entity overview — 44 tables in 7 layers

| Layer | Purpose | Key tables |
|-------|---------|------------|
| **Setup** | Configuration and templates | Subscription Contract Setup, Subscription Contract Type, Sub. Package Line Template |
| **Package** | Reusable subscription definitions | Subscription Package, Sub. Package Line, Item Subscription Package |
| **Subscription** | The service object + monetary lines | Subscription Header, Subscription Line |
| **Contract** | Customer/vendor agreements | Customer/Vendor Subscription Contract, Contract Lines |
| **Billing** | Invoice generation | Billing Template, Billing Line, Billing Line Archive |
| **Deferral** | Revenue/cost recognition | Cust./Vend. Contract Deferral |
| **Lifecycle** | Renewals, price updates, analysis | Planned Subscription Line, Price Update Template, Sub. Contract Analysis Entry |

---

## 2. ERD — core entities and relationships

*(Full-resolution diagram: `ai/docs/diagrams/recurring-billing-erd.png`)*

### 2.1 The key flow (how entities connect end-to-end)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SETUP                                                                       │
│  Item (Subscription Option) ←→ Item Sub. Package ←→ Subscription Package   │
│                                                      ↓                      │
│                                              Sub. Package Lines             │
│                                              (uses Templates)               │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ Sales document with subscription lines
                               ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ SUBSCRIPTION (created on shipment posting)                                  │
│  Subscription Header ──1:N──→ Subscription Lines                           │
│  (the "what")                 (the "how much / how often")                  │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ Assigned to contract
                               ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ CONTRACT                                                                    │
│  Customer Subscription Contract ──1:N──→ Cust. Sub. Contract Lines         │
│  (Sell-to, Bill-to, terms)               (→ Subscription Header + Line)    │
│                                                                             │
│  Vendor Subscription Contract ──1:N──→ Vend. Sub. Contract Lines           │
│  (Buy-from, Pay-to, terms)              (→ Subscription Header + Line)     │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ Billing Template drives proposal
                               ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ BILLING                                                                     │
│  Billing Template ──→ Billing Lines ──→ Sales/Purchase Invoice              │
│  (schedule, grouping)  (one per contract line per period)                   │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ On posting
                               ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEFERRAL                                                                    │
│  Cust. Contract Deferral ──→ G/L Entry (revenue spread over period)        │
│  Vend. Contract Deferral ──→ G/L Entry (cost spread over period)           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Item Subscription Option (the starting point)

Items get a new field `Subscription Option` that controls their behavior:

| Value | Meaning |
|-------|---------|
| **No Subscription** | Normal item — no subscription behavior |
| **Sales with Subscription** | Item sold normally + subscription lines auto-created from linked package |
| **Subscription Item** | Item exists only as a subscription — no standalone sale |
| **Invoicing Item** | Used as the invoice line item when billing subscription contract lines |

### 2.3 Subscription Package → Subscription Line flow

```
Subscription Package (template)
  └── Sub. Package Lines (1:N)
        ├── Partner: Customer or Vendor
        ├── Invoicing Via: Sales or Subscription Contract
        ├── Calculation Base: Item Price / Document Price / Doc Price + Discount
        ├── Billing Base Period: e.g., 1M
        ├── Billing Rhythm: e.g., 1M
        ├── Initial Term: e.g., 1Y
        ├── Extension Term: e.g., 1Y (auto-renewal)
        └── Notice Period: e.g., 3M

        ↓ (instantiated on shipment)

Subscription Line (on a Subscription Header)
  ├── Same fields as above, now with actual dates
  ├── Next Billing Date
  ├── Calculation Base Amount → Price → Amount
  └── Assigned to a Contract Line
```

### 2.4 Contract structure

```
Customer Subscription Contract
  ├── Sell-to Customer No.
  ├── Bill-to Customer No.
  ├── Contract Type (→ Sub. Contract Type: harmonized billing, deferrals)
  ├── Currency, Payment Terms, Salesperson
  ├── Billing Base Date (for harmonized billing across lines)
  ├── Active (Boolean)
  │
  └── Cust. Sub. Contract Lines (1:N)
        ├── Contract Line Type: Comment | Item | G/L Account
        ├── → Subscription Header (the subscription)
        └── → Subscription Line (the monetary commitment)
```

### 2.5 Billing flow

```
Billing Template
  ├── Partner: Customer or Vendor
  ├── Billing Date/To Date Formulas
  ├── Group by: None | Contract | Contract Partner
  ├── Customer Document per: Contract | Sell-to | Bill-to
  ├── Automation: None | Create Billing Proposal and Documents
  │
  └── generates → Billing Lines (1:N)
        ├── For each contract line with due billing
        ├── Billing From / To dates
        ├── Amount
        ├── → Document Type: Invoice or Credit Memo
        ├── → Document No. (Sales/Purchase Header)
        └── → Document Line No. (Sales/Purchase Line)
```

**Billing Template automation** can run on a schedule (Minutes between runs) to auto-generate proposals and documents.

### 2.6 Revenue deferrals

When `Create Contract Deferrals = Yes` on the contract type (or overridden per line):

- Posting the invoice creates **Cust. Contract Deferral** entries
- Each entry represents a portion of revenue for a specific period
- Deferrals are released on their posting date → creates **G/L Entries** spreading revenue across the contract period
- Same pattern on vendor side for cost deferrals

### 2.7 Contract lifecycle

**Renewals**: Before a contract line's term expires, a **Planned Subscription Line** is created to stage the renewal. When the current line is fully invoiced, the planned line replaces it.

**Price updates**: **Price Update Template** defines the method (% of calculation base, % of price, or recent item prices). Generates **Price Update Lines** as a worksheet for review before applying.

**Analysis**: **Sub. Contract Analysis Entry** captures snapshots for contract analytics, tagged by type (None, Contract Renewal, Price Update).

---

## 3. Connections to core BC

| Core BC entity | How the module connects |
|----------------|----------------------|
| **Customer** | Sell-to / Bill-to on contracts and subscriptions |
| **Vendor** | Buy-from / Pay-to on vendor contracts |
| **Item** | Source of subscription (Subscription Option field), invoicing item on lines |
| **G/L Account** | Alternative source type on subscriptions; line type on contracts |
| **Sales Header/Line** | Billing Lines generate sales invoices/credit memos |
| **Purchase Header/Line** | Billing Lines generate purchase invoices/credit memos |
| **G/L Entry** | Deferrals post to G/L on release |
| **Customer Price Group** | Drives pricing on packages, subscriptions, contracts |
| **Contact** | Linked to contracts via Sell-to/Bill-to Contact No. |
| **Dimension Set Entry** | Contracts and subscription lines carry dimension sets |
| **Job** | Contracts can inherit dimensions from a Job |

---

## 4. Usage-based billing extension

The module includes a **usage-based billing** sub-system for metered/consumption pricing:

| Table | Purpose |
|-------|---------|
| Usage Data Supplier | External service providers (e.g., Azure, AWS) |
| Usage Data Import | Import headers for usage data |
| Usage Data Billing | Billing data generated from usage records |
| Usage Data Supplier Reference | Maps supplier IDs to BC subscriptions |
| Usage Data Generic Import | Generic CSV/file import format |

This extends the flat-rate subscription model to support per-unit, tiered, or consumption-based pricing.

---

**Version History**

| Version | Date       | Changes           |
|---------|------------|-------------------|
| 1.0     | 2026-06-08 | Initial ERD from microsoft/BCApps source |
