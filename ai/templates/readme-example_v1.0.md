# README Template v1.0

> **Purpose**: Pattern for AI to generate project README.md  
> **Target**: "New developer, 15 minutes to success"  
> **Max Length**: 2 screens (~100 lines)  
> **AI Instructions**: Copy structure, replace ALL placeholders with project-specific content  

---

# [Your Project Name]

> **Problem Solved**: [What business problem does this solve]
> **Get Running**: [Time estimate] from setup to first execution

## What This Solves

**Before**:
- [Pain point 1]
- [Pain point 2]

**After**:
- [Benefit 1]
- [Benefit 2]

---

## Quick Start (5-10 Minutes)

### 1. Prerequisites

```bash
# [Required software/versions]
python --version  # Requires 3.x+
```

### 2. Setup

```bash
# Clone and install
git clone [repo-url]
cd [project-name]
pip install -r requirements.txt

# Configure
cp config/example-config.json config/my-config.json
# Edit config/my-config.json with your settings
```

### 3. Run

```bash
# Basic usage
python src/main.py [required-args]

# Expected output:
# [Example output showing success]
```

---

## Directory Structure

```
project-root/
├── config/          # Configuration files
├── src/             # Source code
├── output/          # Generated files
├── logs/            # Log files
└── tests/           # Test scripts
```

---

## Configuration Quick Reference

### Required Files

```
config/
├── [config-file-1]    # [Purpose]
└── [config-file-2]    # [Purpose]
```

### Key Settings

```json
{
  "[section]": {
    "[key]": "[description of what this controls]"
  }
}
```

---

## Common Usage Patterns

### [Pattern 1 Name]

```python
# [Brief code example]
```

### [Pattern 2 Name]

```python
# [Brief code example]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `[Error message]` | [How to fix] |
| `[Error message]` | [How to fix] |

---

## When You Need More

- **Architecture decisions**: See `ai/decided/[project]-adr_vX.Y.md`
- **Detailed configuration**: See `in-depth-readme.md`
- **Release history**: See `ai/reports/release-notes_vX.Y.md`

---

**Version:** v1.0
**Last Updated:** YYYY-MM-DD
**Domain:** [Project Domain]
**Purpose:** Quick start guide
