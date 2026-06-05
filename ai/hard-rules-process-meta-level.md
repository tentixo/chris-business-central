# Meta-Level Hard Rules (Process)

**Scope**: META vs EXECUTION level separation for TMM and planning workflows
**Version**: 1.0
**Based on**: ai/meta-level-hard-rules.md
**Updated**: 2026-01-04

---

## MUST (Required)

### META-MUST-1: Explicit Level Declaration
- MUST state current level at session start or after `/clear`
```
"Starting session on META-LEVEL: improving TMM Stage N"
"Starting session on EXECUTION: following design spec for E1-Cert"
```
Source: META-LEVEL-1

### META-MUST-2: Level Switch Approval
- MUST get explicit human approval before switching levels
```
META → EXECUTION: "Spec complete. Switch to EXECUTION to implement? (approved?)"
EXECUTION → META: "Implementation done. Return to META for review? (approved?)"
```
Source: META-LEVEL-3

### META-MUST-3: Deliverable Before Execution
- MUST have deliverable listed in plan/spec before creating it in EXECUTION
- Rationale: Plan first, execute second
- Exception: Quick fixes, typos, explicit human override
Source: META-LEVEL-5

---

## SHOULD (Recommended)

### META-SHOULD-1: Confusion Signal
- SHOULD stop and ask if about to create file not in plan
```
"CONFUSION: I'm about to create [filename] but it's not in the spec.
Are we on META (should I add it first) or EXECUTION (proceed to create it)?"
```
Source: META-LEVEL-4

### META-SHOULD-2: Level Indicators
**META indicators** (working ON the plan):
- Editing TMM docs, templates, workflow
- Discussing architecture improvements
- Creating design specs

**EXECUTION indicators** (working FROM the plan):
- Creating deliverables named in specs
- Writing code referenced in design
- Validating against success criteria
Source: META-LEVEL-2

---

## Quick Reference

| Action | Level | What to Do |
|--------|-------|------------|
| Improve TMM docs | META | Edit ai/prompts/TMM/*.md |
| Create design spec | META | Write {entity}-design.md |
| Implement from spec | EXECUTION | Follow spec, create code |
| File not in spec | STOP | Ask which level we're on |
