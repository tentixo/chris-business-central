# Beads Workflow Hard Rules (Process)

**Scope**: Epic → Task → Sub-task hierarchy for Beads
**Version**: 1.1
**Based on**: ai/beads-workflow-hard-rules.md
**Updated**: 2026-01-04

---

## Critical Warning

> **Beads allows ANY structure.** These rules exist because Beads has NO built-in enforcement.
> AI MUST self-enforce these rules.

---

## MUST (Required)

### BEADS-MUST-1: Three-Level Hierarchy

| Level    | Type          | Pattern      | Parent Required       |
|----------|---------------|--------------|-----------------------|
| Epic     | `--type=epic` | `bd-xxx`     | NO (top-level)        |
| Task     | `--type=task` | `bd-xxx.N`   | YES (`--parent=EPIC`) |
| Sub-task | `--type=task` | `bd-xxx.N.M` | YES (`--parent=TASK`) |

```bash
# Epic: NO --parent
bd create --title="TMM: E1-Cert Four Boxes" --type=epic

# Task: --parent points to Epic
bd create --title="Fill FOUNDATION box" --type=task --parent=69n

# Sub-task: --parent points to Task
bd create --title="AI: Extract hard-rules" --type=task --parent=69n.1
```

### BEADS-MUST-2: AI Work Pattern

- MUST create TWO sub-tasks when AI receives implementation work:

```
Task: [Description]
  └─ Sub-task .N.1: AI: [work description]
  └─ Sub-task .N.2: Human: [validation description]
```

### BEADS-MUST-3: Parent Flag Usage

- MUST use `--parent=EPIC_ID` when creating Task
- MUST use `--parent=TASK_ID` when creating Sub-task
- MUST NOT create orphan tasks without `--parent`

### BEADS-MUST-4: Closure Order

```
1. Close all Sub-tasks first (.N.1, .N.2, ...)
2. Then close Task (.N)
3. When all Tasks closed, close Epic
```

- MUST NOT close Task while Sub-tasks are open
- MUST NOT close Epic while Tasks are open

---

## MUST NOT (Forbidden)

### BEADS-MUSTNOT-1: Orphan Tasks

- MUST NOT create Tasks without `--parent=EPIC`
- MUST NOT create Sub-tasks without `--parent=TASK`

### BEADS-MUSTNOT-2: Skip Levels

- MUST NOT create Sub-task directly under Epic (skips Task level)
- MUST NOT nest deeper than 3 levels (no Sub-sub-tasks)

### BEADS-MUSTNOT-3: Premature Closure

- MUST NOT close Task before Human validation Sub-task is closed
- MUST NOT close Task while any Sub-task is open

---

## Quick Reference

| Action          | Command                               | Check                |
|-----------------|---------------------------------------|----------------------|
| Create Epic     | `bd create --type=epic`               | No parent            |
| Create Task     | `bd create --type=task --parent=EPIC` | Parent is Epic       |
| Create Sub-task | `bd create --type=task --parent=TASK` | Parent is Task       |
| Close Sub-task  | `bd close ID`                         | Work complete        |
| Close Task      | `bd close ID`                         | All Sub-tasks closed |
| Close Epic      | `bd close ID`                         | All Tasks closed     |
