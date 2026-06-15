# Config Package → XML Export — Quick Guide

**Version**: 1.0
**Created**: 2026-06-15
**Author**: Tentixo AB
**Scope**: Exporting BC table data (e.g. Chart of Accounts) as structured XML via Configuration Packages (RapidStart)
**Source**: Morre (Lars Mårelius), taught June 11 2026

---

## Why

To share BC table data for analysis or migration, export it as **XML** rather than screenshots. The format is structured, complete, and machine-readable. This is the same RapidStart mechanism BC uses for data-migration imports.

**The "secret"**: a `.rapidstart` file is just a **gzipped XML** file. Decompress it and you have clean XML.

---

## Steps

### 1. Create the Configuration Package
`Alt+Q` → **Configuration Packages** → **+ New**

| Field | Value | Notes |
|---|---|---|
| Code | Short identifier, underscores not spaces (e.g. `COA`, `NO_SERIES`) | |
| Description | Human-readable name (e.g. "Chart of Accounts") | |
| Product Version | Current BC version (e.g. `28.0`) | Records *when* the export was taken |
| Exclude Config. Tables | ✅ tick | Keeps the package to your chosen tables only |

### 2. Add the table(s)
On the **Lines** subpage:
- **Table ID** → use the `…` lookup → search (magnifying glass) for the table by name → select it.
- To add more tables, **arrow-down** to a new line — **not Tab** (BC web-client quirk in config packages).

### 3. Export
Use **Export Package** (⚠️ *not* "Export to Excel"). BC downloads a `.rapidstart` file.

### 4. Convert `.rapidstart` → `.xml`
1. Rename the file extension `.rapidstart` → `.gzip`
2. Decompress it (double-click on macOS)
3. Rename the decompressed result to `.xml`

### 5. Verify & use
Open the `.xml` in Chrome to confirm it's readable (it's UTF-16 with full structured table data). Drop it in `/docs` for analysis.

---

## Common table names to export

| Need | Table to search for |
|---|---|
| Chart of Accounts | **G/L Account** |
| Number series | **No. Series** |
| VAT setup | **VAT Posting Setup** |
| Posting account wiring | **General Posting Setup** |
| Project WIP account wiring | **Project Posting Group** (a.k.a. Job Posting Group) |

---

## Tips

- One package can hold **multiple tables** — add a line per table.
- Name codes consistently (no spaces) so they sort and reference cleanly.
- The same `.rapidstart` format can be **re-imported** for RapidStart data migration — exports and migration templates are interchangeable.

---

*Tentixo AB — Business Central Advisory*