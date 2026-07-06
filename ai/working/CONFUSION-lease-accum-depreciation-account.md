# CONFUSION — Lease accumulated-depreciation account: 1267 vs 1269

**Raised**: 2026-07-06
**Status**: OPEN — needs Morre
**Trigger**: verifying the sandbox CoA export (`docs/Chart of Accounts (1).xlsx`) against the imported lease docs.

---

## The conflict

The **sandbox CoA** maps the leased-asset accounts on the standard BAS pattern (`12x7` appreciation / `12x8` write-down / `12x9` depreciation — identical to Computers 1257/1258/1259, Equipment 1227/1228/1229):

| Account | Sandbox CoA name |
|---|---|
| 1267 | Accumulated **appreciation** of leased assets |
| 1268 | Accumulated write-downs of leased assets |
| **1269** | Accumulated **depreciation** of leased assets |

The **imported lease docs** map it differently:

- `lease-accounting-setup.md` (Step 1) and `ifrs-16-uk-frs102-bc-implementation_v1.0.md` (§3.1) list **1267 = accumulated depreciation**.
- The impl doc's **v1.3 changelog** says explicitly: *"accumulated depreciation 1269 → 1267 … 1269 unused; pristine uses 1267 per Morre's live CoA check."*

## Why it matters

In **this** sandbox that mapping is backwards: posting lease depreciation to **1267** would land it in the **appreciation** account, while **1269** (the real accumulated-depreciation account) exists and is categorised as *Depreciation property, plant and equipment*. If the guide is followed as written, the FA posting group's Accum. Depreciation Account would be wrong.

## Possible explanations (for Morre)

1. **The lease guide has an error** for this environment → Accum. Depreciation Account should be **1269**, not 1267.
2. **Different company / pristine** — Morre's "live CoA check" was on a different sandbox/company than this export, where 1267 may genuinely be repurposed.
3. Deliberate repurpose of 1267 in Morre's pristine (seems unlikely given the standard pattern holds for every other asset class in this export).

## Action

- **Ask Morre**: in the Tentixo test environment, is the leased-asset **accumulated depreciation** account **1267** or **1269**? Confirm which company his CoA check was on.
- If 1269 is correct here → the lease docs (setup guide §Step 1 + impl §3.1) need the account corrected. **Do not edit the IFRS engagement docs until Morre confirms** — this is his engagement.

## Related

- Not the same as the still-open **8940 deferred tax** gap (that account is confirmed *missing* from this CoA; this one is a *mislabel*).
- Touches the FA posting-group setup that the `fixed-assets-testing-playbook.md` (vanilla FA) exercises — the playbook itself uses the Computers family (1250/1259) correctly.
