# Ergon: IFRS 15 — Contract Identification + Performance Obligations (Steps 1-2)

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IFRS 15.9-30
**Intent**: Confirm the contract exists (Step 1), identify each distinct performance obligation (Step 2)
**Chain**: ergon-ifrs-15-chain_v1.0.md (steps 1-2)

---

## Trigger

| Type | Detail |
|---|---|
| **Event** | Tamagos hatches — contract signed/agreed. doc-tamagos.status → "hatched". |
| **Event** | Contract modification that creates a new contract (IFRS 15.20) |

---

## Step 1: Identify the Contract [MACH + IND]

```
IFRS 15.9 — ALL criteria must be met:

  [ ] Parties have approved the contract (written, oral, implied by practices)
  [ ] Each party's rights regarding goods/services can be identified
  [ ] Payment terms can be identified
  [ ] Contract has commercial substance (risk/timing/amount of cash flows changes)
  [ ] Probable that entity will collect the consideration

IF all met → contract exists → IFRS 15 applies.

IF not all met → no contract yet:
  Any consideration received → recognize as LIABILITY (not revenue)
  until criteria met OR: one of these events occurs:
    - No remaining obligation AND all/substantially all consideration received and non-refundable
    - Contract terminated AND consideration received non-refundable

Mapping to our model:
  doc-tamagos.status = "hatched" → contract criteria assessed
  bc.sales_order_no OR bc.subscription_contract_no → the born contract
  edge:org-org → sells_to: populated with contract data

HitL:
  Verbal agreements: does an oral agreement meet criteria? (Industry practice may make it enforceable.)
  Side letters: do side agreements modify the contract?
  Customer creditworthiness: is collection probable? (not guaranteed — just probable.)
```

### Contract combination (IFRS 15.17)

```
Must combine contracts if entered at or near the same time with same customer AND:
  a) Negotiated as package with single commercial objective, OR
  b) Consideration in one depends on the other, OR
  c) Goods/services in the contracts are a single performance obligation

IF combined → treat as ONE contract for Steps 2-5.
```

---

## Step 2: Identify Performance Obligations [IND — HitL]

```
IFRS 15.22: A performance obligation is a promise to transfer:
  a) A good or service (or bundle) that is DISTINCT, or
  b) A series of distinct goods/services that are substantially the same
     and have the same pattern of transfer (e.g., monthly cleaning)

DISTINCT test (IFRS 15.27) — BOTH conditions:
  a) CAPABLE of being distinct: customer can benefit from it alone
     or with readily available resources
     → gi-Eidos test: "Remove the base — does this survive?"
  b) DISTINCT WITHIN THE CONTRACT: separately identifiable
     (not highly interrelated, not significant customization,
      not highly dependent on other promises)

Using our xItem model:

  For each xItem in the xPackage:
    Test (a) — capable of being distinct:
      gItem → almost always YES (physical item usable alone)
      vItem.e-svc → usually YES (customer can use SaaS without vendor's help)
      hItem → depends:
        Implementation of SaaS → V (third party could do it) → YES
        Implementation of SaaS → P (only vendor can, deeply custom) → NO
        Standalone consulting → always YES

    Test (b) — distinct within the contract:
      Is this xItem highly interrelated with others in the xPackage?
      Does the vendor significantly customize/modify this xItem using others?
      Is this xItem significantly affected by others?

      If YES to any → NOT distinct within contract → combine with related xItem(s)

  Record per xItem:
    xPackage.performance_obligations[]:
      po_id, xitem_refs, distinct (boolean), distinct_rationale,
      recognition_pattern (point_in_time / over_time)
```

### Common patterns and their PO conclusions

| xPackage content | PO analysis | Result |
|---|---|---|
| gItem.physical alone | Single delivery → single PO | 1 PO, point-in-time |
| gItem.physical + hItem.labor (installation) | Can third party install? YES → 2 POs. NO → 1 combined PO. | Usually 2 POs |
| vItem.e-svc (SaaS subscription) alone | Stand-ready each month → series of distinct (same pattern) → single PO | 1 PO, over-time (time-elapsed) |
| vItem.e-svc + hItem.consulting (implementation) | Third party could implement? YES → 2 POs. Deeply custom, only vendor → 1 PO. | **THE judgment call.** ESMA's most common IFRS 15 finding. |
| vItem.e-svc + hItem.consulting + hItem.labor (training) | Training distinct (can hire any trainer)? Usually YES → 3 POs: SaaS + implementation + training. | 3 POs (or 2 if implementation combined with SaaS) |
| hItem.consulting T&M engagement | Each hour/day is substantially same, same pattern → series → single PO. OR: right to invoice practical expedient. | 1 PO, over-time |
| hItem.consulting Fixed Price | Single deliverable → single PO. Multiple deliverables (each distinct) → multiple POs. | Depends on scope |
| xPackage.project (mixed g/v/h) | Each component tested for distinct. Likely multiple POs. | Multi-PO, mixed recognition |

---

## Output

| Target | What |
|---|---|
| `xPackage.performance_obligations[]` | Structured PO list with distinct assessment, rationale, recognition pattern |
| `edge:org-org → sells_to` | Contract confirmed, contract combination assessment |
| `doc-tamagos` → hatched_contract_ref | BC reference to the born contract |
| `node:anomaly` | "Implementation + SaaS distinct assessment unclear — HitL required" |
| `node:decision` | "Is {xItem} distinct within this contract?" |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Revenue recognized before contract exists | Premature revenue. Prosolvia pattern. | #2 Fictitious |
| Under-identifying POs (everything in one bucket) | Revenue recognized on wrong pattern — usually too early | #3 Optimistic |
| Over-identifying POs (splitting too much) | Revenue recognized too late — conservative but wrong | Rare, less risky |
| Implementation + SaaS combined when should be separate | Revenue deferred over subscription when implementation is distinct → understated early revenue | ESMA finding |
| Implementation + SaaS separated when should be combined | Revenue accelerated on implementation when it's not distinct → overstated early revenue | ESMA finding |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-01 | Initial — contract criteria mapped to Tamagos hatching, PO identification using gi-Eidos test on xItem, common xPackage patterns. |
