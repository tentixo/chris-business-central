# Subscription Billing — Setup Guide

**Version**: 1.0
**Created**: 2026-06-12
**Author**: Tentixo AB
**Scope**: End-to-end setup of recurring subscription billing in Business Central
**Audience**: BC functional user or administrator

---

## What this guide covers

Setting up BC's Subscription Billing module to automatically generate monthly invoices for a recurring service (e.g., a security retainer, managed service, or support agreement). By the end, you'll have:

- A subscription item
- A customer subscription contract
- A billing template that generates draft invoices automatically

**Prerequisites**: Subscription Billing extension installed (verify via Extension Management), customer card already exists, posting groups configured.

---

## Step 1 — Configure Number Series

The Subscription Billing module needs its own number series before it can create records.

**Open**: `Alt+Q` → "Subscription Contract Setup"

Scroll to the **Number Series** FastTab. Three fields need a number series assigned:

| Field | Purpose |
|---|---|
| Customer Subscription Contract Nos. | Numbers new customer contracts |
| Vendor Subscription Contract Nos. | Numbers vendor-side contracts |
| Subscription Nos. | Numbers individual subscriptions |

If these are blank, create number series first (`Alt+Q` → "No. Series" → + New), then assign them here. Follow your company's existing number series naming convention for the codes and starting numbers.

**Also on this page** — review the **General** FastTab defaults:

| Field | Recommended value | Why |
|---|---|---|
| Default Billing Base Period | `1M` | Monthly billing cycle |
| Default Billing Rhythm | `1M` | Invoice every month |
| Default Period Calculation | Align to Start of Month | Clean billing periods |
| Create Contract Deferrals | Contract-dependent | Let each contract decide |

**Invoice Details** section — under **Arrange Texts**, set **Description** to **"Billing Period"**. This is required — without it, document creation will fail with a configuration error.

---

## Step 2 — Create the Subscription Item

The item represents what you're billing for on the subscription. It's separate from any items used in project billing.

**Open**: `Alt+Q` → "Items" → + New

| Field | Value | Notes |
|---|---|---|
| No. | A descriptive code (e.g., `SEC-RETAINER`) | |
| Description | What appears on the invoice (e.g., "Monthly Security Retainer") | |
| Type | **Non-Inventory** | Required for Subscription Items |
| Base Unit of Measure | `EA` | |
| Gen. Prod. Posting Group | Match your service category (e.g., `CONSULTING1`) | Controls which revenue account the invoice hits |
| VAT Prod. Posting Group | Match your VAT category (e.g., `SERVICE FULL`) | |
| Unit Price | `0` | Price is set on the contract, not the item |
| **Subscription Option** | **Subscription Item** | Found on the Prices & Sales FastTab. Marks this item as subscription-only — it won't appear in regular sales invoices or project billing |

**Subscription Option values** (the full enum on the Prices & Sales FastTab):

| Value | Meaning |
|---|---|
| **No Subscription** | Default. Ordinary item, no subscription behaviour. |
| **Sales with Subscription** | Item can be sold normally *and* drive a subscription (e.g., hardware sold with an attached service plan). |
| **Subscription Item** | Subscription-only — won't appear in regular sales invoices or project billing. Use this for a pure retainer. |
| **Invoicing Item** | Used as the billing line on the generated invoice, not the subscribed item itself. |

**Why Non-Inventory?** The "Subscription Item" option requires Type = Non-Inventory. This is correct for a recurring billing item — there's no stock to track, and the subscription engine drives the billing, not a shipment or service delivery event.

---

## Step 3 — Create the Customer Subscription Contract

The contract links the customer to the subscription item and defines the billing terms.

**Open**: `Alt+Q` → "Customer Subscription Contracts" → + New

### Header

| Field | Value |
|---|---|
| Customer Name | Select the customer |
| Description | A human-readable name for the contract |
| Active | On (toggle) |
| Create Contract Deferrals | Off — if revenue is earned in the month invoiced. On — if revenue needs to be spread across periods (see your company's deferral policy) |

### Lines

Click **New Line** on the Lines subpage:

| Field | Value | Notes |
|---|---|---|
| Type | Item | |
| No. | Your subscription item (e.g., `SEC-RETAINER`) | |
| Subscription Line Start Date | First billing date (e.g., `2026-07-01`) | |
| Quantity | `1` | |
| Calculation Base Amount | The recurring price (e.g., `15,000`) | |
| Billing Base Period | `1M` | Should default from setup |
| Billing Rhythm | `1M` | Should default from setup |
| Subscription Line End Date | Leave blank for open-ended contracts | Set a date if the contract has a defined end |

After saving, verify that **Next Billing Date** populates automatically based on the start date.

### Invoice Details FastTab

| Field | Recommended value |
|---|---|
| Payment Terms Code | Your standard terms (e.g., `30 DAYS`) |
| Detail Overview | `Complete` |

---

## Step 4 — Create a Billing Template

The billing template is the automation engine — it tells BC which contracts to bill and how to batch them.

**Open**: `Alt+Q` → "Billing Templates" → + New

| Field | Value |
|---|---|
| Code | A short identifier (e.g., `MONTHLY-RET`) |
| Description | What this template covers (e.g., "Monthly Retainer Billing") |
| Partner | **Customer** |

One billing template can serve multiple contracts. You don't need a separate template per customer — the template picks up all active customer contracts whose Next Billing Date falls within the billing period.

---

## Step 5 — Run the Billing Cycle

This is the monthly workflow. After initial setup, this is all you do each month.

### 5a. Create Billing Proposal

**Open**: `Alt+Q` → "Recurring Billing"

| Field | Value |
|---|---|
| Billing Template | Select your template (e.g., `MONTHLY-RET`) |
| Billing Date | The invoice date (e.g., first of the month) |
| Billing to Date | End of the billing period (e.g., last day of the month) |

Click **Create Billing Proposal**. BC scans all active contracts linked to this template and generates proposal lines for any whose Next Billing Date falls within the range.

Review the proposal lines — verify customer, amount, and period.

### 5b. Create Documents

Click **Create Documents**. A dialog appears:

| Field | Value |
|---|---|
| Document Date | The invoice date |
| Posting Date | When to post (often same as document date) |
| Post Document(s) | **Off** — review the draft first |
| Document per | **Contract** — one invoice per contract |

Click **OK**. BC generates draft Sales Invoices.

### 5c. Review and Post

Open the generated invoice (`Alt+Q` → "Sales Invoices" → find the latest draft).

**Verify**:
- Customer name and address
- Line item, quantity, and amount
- VAT calculation (check with F7 → Statistics)
- Billing period description on the line
- Posting groups on the line (scroll right or check Statistics)

When satisfied, click **Post** (or **Post & Send** to email the invoice to the customer).

---

## Monthly effort after setup

| Scenario | Steps | Time |
|---|---|---|
| Retainer only | Create Billing Proposal → Create Documents → Review → Post | ~2 minutes |
| Multiple clients on same template | Same — the template batches all contracts in one run | ~2 minutes regardless of client count |

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| "Billing Template does not exist" | No billing template selected or created | Create a Billing Template (Step 4) |
| "Configuration incomplete — Billing Period as description" | Arrange Texts → Description not set in Subscription Contract Setup | Set Description to "Billing Period" on the setup page (Step 1) |
| Billing proposal is empty | Billing to Date doesn't cover the contract's Next Billing Date | Extend Billing to Date to cover the billing period |
| "Subscription Item only available for Non-Inventory" | Item Type is set to Service | Change item Type to Non-Inventory (Step 2) |

---

## Architecture note

Subscription billing is designed for **fixed, recurring revenue** — retainers, managed services, support contracts. For **variable, project-based work** (quoted engagements, T&M hours), use BC's Project Billing module instead. These are separate billing engines by design:

- Different intent: subscriptions are predictable; projects are evolving
- Different legal requirements: subscription contracts and project contracts typically have different terms
- Separate invoices: when both are active for the same customer, they generate separate invoices — this is correct, not a limitation

Revenue from both streams can be aggregated per customer in Power BI for unified reporting.

---

*Tentixo AB — Business Central Advisory*
