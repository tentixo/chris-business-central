# Masha BC Sessions — Tentixo Bookkeeping Operations

**Version**: 1.0
**Status**: Active (living document)
**Created**: 2026-06-05
**Updated**: 2026-06-05
**Scope**: How Masha does Tentixo's day-to-day bookkeeping in BC — operational reference, not best-practice prescription

> Masha handles all Tentixo bookkeeping. These sessions document her actual workflow. Some
> patterns are small-company shortcuts (manual where automation would be appropriate at scale).
> Flag these when extracting to client-facing material.

---

## Session 1 — June 4, 2026 (1h 15m)

**Topic**: Full monthly bookkeeping cycle — receipts, salaries, tax, fixed assets, invoicing, payment reconciliation

---

### 1. Monthly workflow overview

Masha's monthly cycle, roughly in order:

1. **General ledger entries** — receipts and bank costs
2. **Salary bookkeeping** — from Nmbrs (external payroll system) via journal templates
3. **Skatteverket entries** — distribute tax payments to specific accounts
4. **Fixed asset maintenance** — new acquisitions, depreciation runs
5. **Sales invoices** — create and send to customers
6. **Purchase invoices** — manual or via Tungsten Automation (scanning)
7. **Payment reconciliation** — match bank XML to open entries, apply payments

**Source of truth**: The bank statement. Every entry must have a matching receipt or invoice. Receipts must be kept 10 years (electronic OK if received electronically; physical receipts still need paper).

### 2. General ledger entries — receipts

Masha posts receipts one-by-one from the bank statement into General Journal entries:

- **Balancing account**: Always the bank account (Danske Bank)
- **Posting groups**: Purchase / Domestic / then VAT rate depends on expense type
- **Document number**: Auto-assigned. Masha stamps the physical receipt with the document number for traceability.
- **Date**: Bank statement date is source of truth (may differ from receipt date)
- **Document type**: Left blank for receipts (only used for invoices/payments/credit memos)

**Journal batch setup**: Masha has pre-configured journal batches with different default balancing account types:
- "Danske" batch → default balancing = Bank Account (for receipts)
- "Default" batch → default balancing = G/L Account (for salary distribution etc.)

**Cheat sheet**: Masha maintains a personal quick-reference of frequently used account numbers and the monthly process steps.

### 3. Swedish VAT rates in practice

| Rate | VAT Prod. Posting Group | Applies to |
|------|------------------------|------------|
| 25%  | SERVICE (standard)     | Most goods and services in Sweden |
| 12%  | SERVICE MEDIUM         | Hotels in Sweden, restaurant food in Sweden |
| 6%   | SERVICE LOW            | Transport (cabs, flights) domestic Sweden |
| 0%   | SERVICE ZERO           | Foreign services (Uber abroad, hotel abroad, international flights), insurance, health/gym, banking costs |

**Key rules**:
- Cabs/hotels: VAT rate tied to **location of use**, not location of purchase. Spanish hotel = 0%, Swedish hotel = 12%.
- International flights (SE → abroad) = 0%. Domestic flights within SE = 6%.
- Tips (e.g., Uber) = 0% VAT even if the ride itself has 6%.
- Business dinners: max 300 SEK/person deductible. Alcohol is always non-deductible. Food-only portion gets 12% VAT.

### 4. Multi-line postings (split VAT)

When a single bank transaction contains items at different VAT rates, Masha splits it across multiple journal lines under the **same document number**:

**Example — Uber with tip** (227 SEK total):
```
Line 1: 5890 (cab expense)     200 SEK   Service Low (6%)    "Uber trip"
Line 2: 5890 (cab expense)      27 SEK   Service Zero (0%)   "Uber tip"
Line 3: Bank account           -227 SEK   (no posting groups)  balancing
```
Total balance = 0. One document number, three lines.

**Business dinner calculator**: Tentixo has a spreadsheet that splits restaurant receipts into deductible food (up to 300 SEK/person, 12% VAT) and non-deductible portions (alcohol, excess). Output feeds the multi-line posting.

### 5. Employee reimbursements

When an employee pays a company expense from a personal card:

- Post the expense as a G/L entry, but use **Employee account** (not bank) as balancing account
- This creates an open entry on the employee ledger showing the company owes them
- When salary is paid, the reimbursement nets against the salary advance
- Employee ledger shows open entries that need to be "glued together" (applied) to close them

### 6. Salary bookkeeping

**External system**: Nmbrs (Visma-owned payroll system, separate from BC). Produces two outputs:
1. Per-employee salary specification (breakdown of gross, tax, net)
2. Consolidated monthly summary with account numbers and amounts

**BC process**:
- Use a **saved journal template** ("Standard Journals") pre-populated with the recurring salary accounts
- Verify and adjust amounts month-to-month (amounts vary due to benefits, car allowance, etc.)
- Salary accounts are split per employee group: 7211 (salary to shareholders), 7221 (salary to staff) — likewise for employer contributions (7511, 7512)
- Post as a single G/L batch where balancing account = bank. Total must net to zero.

**No integration** between Nmbrs and BC — Morre has confirmed this. Manual transfer via saved journal templates is the only path.

### 7. Skatteverket (tax authority) entries

Tax payments flow from the bank to a **tax account** (Skattekonto), then get distributed to specific accounts:

- The bank statement shows one lump payment to Skatteverket
- Masha posts: Bank → Tax account (one line)
- Then distributes from Tax account to individual accounts (preliminary tax, social contributions, etc.) using the Skatteverket statement as source
- Accounts used: 2518, 2650, 2710, 2730, 8423, etc.
- No posting groups needed on tax distribution lines (already within the tax system)

Masha keeps a cheat sheet of account numbers since they're roughly the same each month.

### 8. Fixed assets

**Two categories** (Swedish standard):

| Category | Threshold | Depreciation | BC treatment |
|----------|-----------|-------------|--------------|
| **LVA** (low-value asset) | 2,000–20,000 SEK | Written off immediately (start date = end date) | Acquisition cost only, book value → 0 |
| **Main fixed asset** | > 20,000 SEK | Over N years (e.g., 3 years for laptops) | Monthly depreciation calculation |

**Process for new asset**:
1. Create Fixed Asset card (number, description, FA class: tangible LVA or tangible main)
2. Post acquisition cost via **Fixed Asset Journal** (amount ex-VAT, since VAT already handled in receipt posting)
3. For main assets: set depreciation period on the card
4. Monthly: run **Calculate Depreciation** (Actions → Tasks → Calculate Depreciation) — creates journal lines moving value from FA account to depreciation expense account

**For LVA**: Acquisition cost posts and book value immediately goes to zero (depreciation start = end date).

**Disposal**: When an asset is retired, post disposal in FA journal. Then manually set status to Inactive and Blocked on the FA card (this is not automated by the disposal posting).

**Serial numbers**: Should be recorded on FA cards for audit trail, though not required for reporting.

### 9. Sales invoices

- Created from the Customer card → New Document → Sales Invoice
- Lines can be: Resources (people), Items (licenses), or G/L Accounts
- Sent directly from BC as PDF email attachment (email integration configured)
- Credit memos for corrections
- Tentixo skips Quotes and Orders — goes straight to Sales Invoice (small company, simple sales cycle)

### 10. Purchase invoices

**Two methods**:

1. **Manual**: Vendor card → New Document → Purchase Invoice → manually enter lines. Used for most vendors at Tentixo.

2. **Tungsten Automation** (formerly AP Essentials): Invoice scanning tool integrated with BC.
   - Upload PDF invoices → system reads/OCRs the data
   - Verify extracted data (amounts, dates, vendor)
   - Click OK → appears in BC's Incoming Documents
   - From Incoming Documents → Create Document → auto-creates Purchase Invoice linked to correct vendor
   - Still requires manual validation before posting

New suppliers need vendor card setup before scanning works.

### 11. Payment reconciliation

**Semi-automated via bank XML import**:

1. Download XML transaction file from Danske Bank (monthly)
2. In BC: Payment Reconciliation Journal → Import Bank Transactions → upload XML
3. BC auto-matches transactions to open invoices
4. Masha removes receipt lines (those were already posted as G/L entries)
5. Validates remaining matches — checks that BC picked the right invoice (especially for same-amount, different-month cases)
6. Posts the reconciliation

**Manual payment application** (when needed):
- Sales Journals → Payment document type → select Customer → Apply Entries → select open invoice → post
- Purchase Journals → same flow for vendor payments
- Can also apply after the fact: go to Customer/Vendor ledger → Apply Entries

### 12. Foreign currency and exchange rate differences

When paying in foreign currency (EUR, USD), the exchange rate at posting may differ from the rate at payment.

**Two accounts**:
- Exchange gains (7xxx)
- Exchange losses (7xxx)

**The asymmetry bug**: When Tentixo *overpays* (exchange rate moved against them), BC offers "Transfer Difference to Account" — one-click resolution. When Tentixo *underpays* (exchange rate moved in their favor / they made money), this option is **not available**. Masha must manually create a journal entry to record the gain. She considers this a BC bug.

**Workaround for exchange gains**: Create a manual G/L journal entry: Vendor + payment amount → balancing account = exchange gain account.

**Recurring foreign-currency expenses** (GitHub, Docker, Google Workspace, Cloudflare): Come in USD/EUR, so SEK amount varies monthly due to exchange. Can't easily template these.

### 13. Tools and integrations

| Tool | Purpose | Integration with BC |
|------|---------|-------------------|
| **Danske Bank** | Banking | XML export for payment reconciliation |
| **Nmbrs** (Visma) | Payroll calculation | Manual (no integration) |
| **Tungsten Automation** (AP Essentials) | Invoice scanning/OCR | Integrated — creates Incoming Documents |
| **Email** | Invoice delivery | Integrated — send PDF directly from BC |
| **Business dinner calculator** | Entertainment expense compliance | Spreadsheet (no integration) |

---

### Observations and flags

**Small-company shortcuts** (not recommended for clients):
- Manual receipt posting one-by-one from bank statement
- Manual salary transfer from Nmbrs to BC via templates (no integration)
- Manual purchase invoice creation for most vendors
- Physical receipt stamping for document number tracing
- Skipping Quotes and Orders in the sales flow
- Quarterly bank reconciliation instead of monthly

**Genuine best practices** (transferable to clients):
- Bank statement as source of truth
- Journal batch presets per workflow (Danske vs Default)
- Saved journal templates for recurring salary postings
- XML bank import for payment reconciliation
- Tungsten Automation for purchase invoice scanning
- Split-VAT multi-line posting technique
- Fixed asset LVA vs main classification with correct depreciation handling

**Open questions for Morre**:
- ~~Is there a Nmbrs ↔ BC integration that Masha hasn't explored?~~ **Confirmed: no integration exists.** (Morre explored this.)
- The exchange rate gain/loss asymmetry — is this a known BC limitation or a configuration issue?
- Could receipt posting be automated via the same XML bank import used for payment reconciliation?
- Employee ledger vs. salary posting — is Masha's approach standard or is there a cleaner pattern?

---

**Version History**

| Version | Date       | Changes                    |
|---------|------------|----------------------------|
| 1.0     | 2026-06-05 | Session 1 documented       |
