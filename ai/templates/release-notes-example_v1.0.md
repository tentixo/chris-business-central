# Release Notes Template v1.0

> **Purpose**: Pattern for AI to generate release notes for coding projects  
> **Target**: Users upgrading to new version  
> **Location**: `ai/reports/release-notes_vX.Y.md`  
> **When to Create**: SHOULD exist for coding projects    
> **AI Instructions**: Copy structure, fill in version-specific changes

---

# [Project Name] - Release Notes vX.Y

**Release Date**: YYYY-MM-DD
**Previous Version**: vX.Y.Z
**Status**: [Draft | Code Complete | Released]
**Breaking Changes**: [Yes (N) | No]

---

## Overview

[2-3 sentence summary of what this release accomplishes]

**Headline Features**:

- [Feature 1 with emoji]
- [Feature 2 with emoji]
- [Feature 3 with emoji]

---

## Breaking Changes

### [Breaking Change 1 Title]

**What Changed**: [Description of the change]

**Who's Affected**: [Who needs to update their code/config]

**Migration Required**: [Yes/No]

**Before**:

```python
# Old way
```

**After**:

```python
# New way
```

**Migration Steps**:

1. [Step 1]
2. [Step 2]

---

## New Features

### [Feature 1 Title]

**File(s)**: `[file path]`
**Priority**: [HIGH | MEDIUM | LOW]

[Description of the feature]

**Example**:

```python
# How to use the new feature
```

**Benefit**: [Why this matters]

---

### [Feature 2 Title]

**File(s)**: `[file path]`
**Priority**: [HIGH | MEDIUM | LOW]

[Description]

---

## Improvements

### [Improvement 1 Title]

**File(s)**: `[file path]`
**Priority**: [HIGH | MEDIUM | LOW]

**Before**: [How it was]
**After**: [How it is now]

**Benefit**: [Why this matters]

---

## Bug Fixes

### [Bug Fix 1 Title]

**Issue**: [Description of the bug]
**Solution**: [How it was fixed]
**Files**: `[file paths]`

---

## New/Enhanced ADRs

### [ADR-XXX: Title]

**Status**: [MANDATORY | RECOMMENDED | OPTIONAL]
**Purpose**: [Brief description]

**Key Points**:

- [Point 1]
- [Point 2]

---

## Migration Guide

### Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]

### Step-by-Step Migration

#### Step 1: [Step Name]

```bash
# Commands or changes
```

#### Step 2: [Step Name]

```bash
# Commands or changes
```

### Validation

```bash
# How to verify migration succeeded
```

---

## Testing

### New Tests

- `[test file 1]` - [what it tests]
- `[test file 2]` - [what it tests]

### Validation Commands

```bash
# Run tests
[test command]

# Validate syntax
[validation command]
```

---

## Technical Debt Resolved

| Priority | Item   | Status  |
|----------|--------|---------|
| HIGH     | [Item] | ✅ Fixed |
| MEDIUM   | [Item] | ✅ Fixed |
| LOW      | [Item] | ✅ Fixed |

---

## Known Issues

### Resolved During Development

- ✅ [Issue 1] - Fixed
- ✅ [Issue 2] - Fixed

### Pre-Existing (Not Addressed)

- ⚠️ [Issue] - [Reason not addressed]

---

## Statistics

### Code Changes

| Metric         | Value |
|----------------|-------|
| Files Modified | N     |
| Files Created  | N     |
| Lines Added    | ~N    |
| Lines Removed  | ~N    |
| New Tests      | N     |

### Quality Improvements

| Metric   | Before | After | Change |
|----------|--------|-------|--------|
| [Metric] | X%     | Y%    | +Z%    |

---

## Files Modified

### [Directory 1] (N files)

1. **[file.py]** - [Brief description of changes]
2. **[file.py]** - [Brief description of changes]

### [Directory 2] (N files)

1. **[file.py]** - [Brief description of changes]

---

## Documentation Updates

### New Documents

- `[document path]` - [Purpose]

### Updated Documents

- `[document path]` - [What changed]

---

## Deprecations

[List any deprecated features, or "None" if no deprecations]

---

## Dependencies

**New Dependencies**: [List or "None"]
**Updated Dependencies**: [List or "None"]
**Removed Dependencies**: [List or "None"]

---

## Rollback Plan

If issues arise:

```bash
# Option 1: Revert to tagged version
git checkout vX.Y.Z

# Option 2: Cherry-pick specific fixes
git cherry-pick <commit-hash>
```

---

## Next Steps

### Immediate (Pre-Release)

- [ ] [Task 1]
- [ ] [Task 2]

### Post-Release

- [ ] [Task 1]
- [ ] [Task 2]

---

## Summary

[1-2 paragraph summary of the release and its impact]

**Recommendation**: [Recommended action for users]

---

**Version:** vX.Y
**Release Type**: [Major | Minor | Patch | Quality Improvement]
**Stability**: [Stable | Beta | Alpha]
