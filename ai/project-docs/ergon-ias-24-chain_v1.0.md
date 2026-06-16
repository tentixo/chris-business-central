# Ergon Chain: IAS 24 — Related Party Disclosures

**Version**: 1.0
**Status**: Draft
**IFRS Reference**: IAS 24 (complete standard)
**Intent**: Identify ALL related parties and ALL transactions with them. Disclose. The graph already has the relationships — this ergon READS from existing data, adds minimal new properties.
**Master chain**: ergon-ifrs-master-chain_v1.0.md (Phase 5 — completion, parallel)

---

## Why IAS 24 Is a Graph Problem

IAS 24 asks: "Who are your related parties and what did you do with them?" Our graph ALREADY models this:

| IAS 24 related party | Where it lives in our model |
|---|---|
| Parent | edge:org-org → owns (ultimate parent in ownership chain) |
| Subsidiaries | edge:org-org → owns (control_conclusion = true) |
| Associates / JVs | edge:org-org → owns (relationship_type = associate / jv) |
| KMP (Key Management Personnel) | edge:ind-org.kmp |
| KMP close family members | edge:ind-org.kmp → IND → family relationships (may need external data) |
| Entities controlled by KMP or family | edge:ind-org.kmp → IND → their other directorships/ownership (external data) |
| Post-employment benefit plans | node:org → type_data.pensions (IAS 19 plan references) |

**The hard part is NOT finding related parties in the group** (the graph has that). The hard part is finding **entities controlled by KMP's family members** — those are OUTSIDE the graph. The CFO's spouse's company that provides consulting to the group: that's a related party, but we might not know about it.

---

## Chain (Single Ergon)

```
┌──────────────────────────────────────────────┐
│  STEP 1: IDENTIFY ALL RELATED PARTIES        │
│  From graph: parent, subs, associates, KMP    │
│  From KMP declarations: family, other roles   │
│  IAS 24.9-11                                 │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 2: IDENTIFY ALL RPTs                   │
│  From edge:org-org.sells_to, lends_to,       │
│  guarantees. From BC: KMP compensation.       │
│  IAS 24.18-22                                │
└──────────────┬───────────────────────────────┘
               ▼
┌──────────────────────────────────────────────┐
│  STEP 3: COMPILE DISCLOSURES                 │
│  Parent name. Ultimate controlling party.     │
│  KMP compensation by category.               │
│  RPT by type: amounts, terms, balances.      │
│  IAS 24.13-18                                │
└──────────────────────────────────────────────┘
```

---

## Step 1: Identify Related Parties [MACH + IND]

### From the graph (automated)

```
MACH reads:

  Parent entity:
    Walk edge:org-org → owns upward to ultimate parent.
    IAS 24.13: disclose name of parent AND ultimate controlling party.
    If different (parent ≠ ultimate) → disclose both.

  Subsidiaries:
    All entities in IFRS 10 consolidation scope.
    RPTs between them = IC transactions (already tracked for elimination).

  Associates and JVs:
    edge:org-org → owns where relationship_type = associate or jv.
    Transactions with associates are NOT eliminated but MUST be disclosed.

  KMP:
    edge:ind-org.kmp → all INDs flagged as Key Management Personnel.
    IAS 24.9: KMP = persons having authority and responsibility for
    planning, directing, and controlling the entity's activities.
    Includes: all directors (executive and non-executive), CEO, CFO,
    and anyone else meeting the definition.
```

### From KMP declarations (HitL — requires human input)

```
IND must declare:
  The HARDEST part of IAS 24. Must identify:

  a) KMP's CLOSE FAMILY MEMBERS:
     Spouse/partner, children, children's spouse/partner,
     dependants of KMP or KMP's spouse.

  b) Entities CONTROLLED or JOINTLY CONTROLLED by KMP or family:
     The CFO owns 60% of a consulting firm → related party.
     Board member's spouse owns a cleaning company used by the group → related party.

  c) Entities where KMP has SIGNIFICANT INFLUENCE:
     KMP sits on the board of a supplier → related party.

  Source: ANNUAL KMP DECLARATION.
    Each KMP fills in a form declaring their interests, family business interests,
    other directorships/ownership.
    Shield validates: are declarations complete? Any missing? Any changes mid-year?

  Common failure (Steinhoff, Allra):
    Related parties NOT declared. Transactions structured to look arm's-length.
    The graph can't see what KMP doesn't declare.
    → Anomaly pattern: compare KMP declarations to BC vendor/customer list.
    "Is any vendor/customer linked to a KMP address, shared phone, shared director?"
```

---

## Step 2: Identify All Transactions [MACH]

```
For each related party identified:

  a) IC transactions (within the group):
     Already tracked: edge:org-org → sells_to, lends_to, guarantees.
     Already eliminated on consolidation.
     BUT: IAS 24.18 still requires DISCLOSURE of nature and terms,
     EVEN THOUGH they're eliminated.

  b) Transactions with associates/JVs:
     NOT eliminated (equity method entities).
     edge:org-org → sells_to for associate relationships.
     MUST disclose: nature, amount, outstanding balances, terms,
     provisions for doubtful debts.

  c) KMP compensation:
     IAS 24.17: disclose TOTAL KMP compensation in aggregate, by category:
       - Short-term employee benefits (salary, bonus, benefits)
       - Post-employment benefits (pension contributions/accruals)
       - Other long-term benefits (deferred compensation, jubilee)
       - Termination benefits (severance)
       - Share-based payment (IFRS 2 expense)

     Source: BC payroll + board fee registers + IFRS 2 calculations.

  d) Transactions with KMP-related entities:
     From KMP declarations → match against BC vendor/customer transactions.
     Any transaction with a KMP-controlled entity: disclose.

  e) Guarantees given/received:
     edge:org-org → guarantees.
     Parent guaranteeing subsidiary's debt = related party guarantee → disclose.

Compile for each related party category:
  Nature of relationship, nature of transactions, amounts,
  outstanding balances (including terms), provisions for doubtful debts,
  commitments.
```

---

## Step 3: Compile Disclosures [MACH]

```
IAS 24.13-18 disclosure requirements:

  a) Name of parent and ultimate controlling party (even if no transactions)
  b) KMP compensation in total and by category (5 categories above)
  c) For EACH CATEGORY of related party relationship:
     - Nature of the relationship
     - Information about transactions: amount, outstanding balances,
       terms, guarantees, provisions for doubtful debts
     - Commitments to related parties

  Categories: parent, entities with joint control/significant influence,
  subsidiaries, associates, JVs, KMP, other related parties.

  NOTE on "arm's length" claims:
    IAS 24.23: "Disclosures that related party transactions were made
    on terms equivalent to arm's length are made ONLY if such terms
    can be SUBSTANTIATED."
    → Don't claim arm's length unless you can PROVE it.
    → Many companies claim it. Auditors challenge.

ABL 16a (Swedish listed companies):
  Material RPTs must be PUBLICLY DISCLOSED (press release).
  Board (excluding conflicted members) must approve.
  Threshold: materiality defined by company policy.
```

---

## Node/Edge Properties

**No new properties needed.** IAS 24 reads entirely from existing:

| Source | What IAS 24 reads |
|---|---|
| edge:org-org → owns | Parent, subsidiaries, associates, JVs |
| edge:ind-org.kmp | KMP identification |
| edge:ind-org.board-member | Board members (subset of KMP) |
| edge:org-org → sells_to, lends_to, guarantees | IC transactions and balances |
| BC payroll | KMP compensation amounts |

**One addition on node:ind (KMP):**

| Field | Type | x-history | Why |
|---|---|---|---|
| `kmp_declaration_date` | date | yes | When KMP last submitted related party declaration. Shield: is it current? |
| `kmp_related_entities` | array of strings | yes | Entities declared by KMP as controlled/influenced by them or family. Source: annual declaration form. |

---

## S-R-S View

| Zone | What it reads | Why |
|---|---|---|
| **Shield** | All KMP identified? Declarations current? All RPTs found? ABL 16a disclosures made? Arm's length claims substantiated? | IAS 24 compliance. Steinhoff/Allra pattern: hidden RPTs. |
| **Reserve** | RPT concentration: is a significant vendor/customer a related party? If that relationship sours → dual risk (commercial + governance). | Related party dependency risk. |
| **Sword** | Are RPTs adding value? Is the KMP-related consulting firm the best option, or just convenient? | Cost optimization + governance hygiene. |

---

## Rim Consequence

| Risk | Consequence | Pattern |
|---|---|---|
| Related party not identified | Undisclosed RPT. Steinhoff: EUR 6.5B in hidden RPTs. Allra: inflated RPTs. | #4 Related party hidden |
| KMP declaration incomplete/false | Hidden interests. Personal liability for KMP. | #4 |
| Arm's length claimed without substantiation | IAS 24.23 violation. Auditor challenges. | Shield failure |
| ABL 16a material RPT not publicly disclosed | NASDAQ disciplinary. MAR implications if price-sensitive. | Swedish Rim violation |
| IC transactions disclosed but without required detail | Incomplete notes. Auditor qualification on disclosure. | Shield compliance |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-02 | Initial — graph-native (reads existing relationships), KMP declarations as the hard part, ABL 16a Swedish Rim, Steinhoff/Allra warning |
