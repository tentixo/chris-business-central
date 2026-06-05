# Walk Reference — Terminology, Physics & Tips

**Version**: 1.0
**Status**: Reference
**Purpose**: Shared vocabulary for Walks, Hammer sessions, and AI-Human collaboration. Load at session start.

---

## 0. The Missing Middle

Below are a lot of Shaw Dense words. Since the words both carry context and Intent, they speed up the discussions with
AI.
The irony is that we had to use Fluffy words to get the Shaw Dense ones. The reason is context poisoning. By using
Fluffy words you avoid injecting context that might make AI do implicit framing – choosing anchors without telling you.

Sentences like "What is that 'thing'?" is better than "What is that application?" – even quotation marks help "thing" is
better than thing. Same goes for "I see a meta-problem," vs. saying "We are in META" in capitalized letters.

When trying to coin a Shaw Dense term, use Fluffy words together with stories to avoid using the words you want
to non-use: "When I walk into a meeting with Humans knowing economy, and I want to order the 'thing' — what should I
say?" The story forces the AI to find the word without you poisoning it. Borrow from other fields. You have to help
Gödel – link it to more context areas by "What is a similar 'thing' called in Philosophy, Art, Science, and other
domains?". Note the open ending – let AI run places, not stopped by a list.

In Hammer, the high-density words become test instruments: "An IP cannot have dinner with an IND" — absurd,
but it tests edge homogeneity (Q3) in one sentence. The contradictory helps AI self-adjust according to itself, not
getting poisoned by a Human saying how AI should not think or do.

```
Fluffy                          Shaw Dense
────────────────                ────────────────
"entity", "thing", "service"   "ghost", "ctx-s", "gd-eidos"
"it depends"                   "Hammer it!, It holds! This lands."
"feels important"              "gravity"
"something is off"             "friction"
"reminds me of..."             "tessellated namespace"

Takes up space, no weight.     Small, heavy. Carries context + intent.
Cloud-shaped — many readings.  Crystal-shaped — one meaning.
```

Both sides are always present. You do not graduate from Fluffy to Shaw Dense. You use Fluffy to explore, Shaw Dense to
communicate, and Fluffy again when the next unknown appears. The terms below are the crystals. The stories that produced
them live in the quantum-eidos document and in Walk session docs.

`AI context resets between sessions. These words don't. Loading them at session start gives you the density of 38
sessions in one read.`

Be fluffy, you will not miss the middle, the Shaw is on the other side.

---

## 1. Core Framework

| Term                             | Definition                                                                                            | Physics                                                   | Walk Tip                                                                                 |
|----------------------------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------------------------------------|
| **Eidos**                        | The ontological identity level — what a thing IS. One node = one Eidos.                               | Noether symmetry: identity conserved under transformation | Ask "what IS this?" not "what does it do?"                                               |
| **Gauge-invariant (Full Eidos)** | Identity absolute, no context needed. ORG is ORG from any reference frame.                            | Observable independent of reference frame                 | If identity needs no context, stop — it's full Eidos                                     |
| **Gauge-dependent (gd-eidos)**   | Identity needs context to be unambiguous. ip-pri needs its network.                                   | Value changes with reference frame                        | Ask "what context makes this unambiguous?"                                               |
| **Gauge-fixing**                 | Choosing one representation of reality. Deciding what's a node, edge, property.                       | Choosing one reference frame                              | Every graphalize decision is a gauge-fix — name it                                       |
| **Chain**                        | Ordered structural links that restore identity. Remove one link, downstream breaks.                   | Sequential dependency                                     | Ask "what contains this thing?" Walk upward.                                             |
| **Field**                        | Simultaneous constraints + objective function. Rims carve space, gravity selects within.              | Constraint satisfaction                                   | Ask "what eliminates configurations?" Walk outward.                                      |
| **ctx-s**                        | Context structure — a query definition, not a container. The telescope, not the stars.                | Reference frame                                           | Delete it mentally. Did anything real vanish?                                            |
| **ctx-c**                        | Context composite — two+ ctx-s bridged by cross-edges. Islands become archipelago.                    | Composite frame                                           | Look for cross-edges. When islands bridge, it's ctx-c.                                   |
| **ctx-v**                        | Context view — saved filter on ctx-c or ctx-s. A named lens. Ghost of a ghost.                        | Filtered observation                                      | Don't create nodes — use ctx-v to filter what exists.                                    |
| **Ghost**                        | Artifact of how you organize, not what exists. Delete the frame, things survive.                      | Gauge artifact (BRST)                                     | Run the ghost test: "delete it — what survives?"                                         |
| **BRST**                         | Gauge-fixing introduces ghosts, but they cancel in observables. The math needs them, physics doesn't. | BRST symmetry theorem                                     | Check: do your answers change depending on which ctx-s you look through? They shouldn't. |
| **Shannon**                      | Information content independent of Intent. `H(X) = -Σ p(x) log p(x)`. Measures bits — not meaning.    | Shannon (1948) entropy                                    | Shannon counts. Shaw weighs. Same bits, different worth.                                 |
| **Shaw**                         | Information value for THIS receiver. Same bits, different worth to different people.                  | Pragmatic information (Level III)                         | Ask "who is the receiver?" Shaw is always personal.                                      |
| **Shaw Lens**                    | Surfaces what matters in raw data. Same graph, different lens, different things important.            | Observational filter                                      | Name your lens before looking. Intent drives the lens.                                   |
| **Shaw Fall**                    | Comprehension stalls — the graph needs edges you don't have yet. Each fall deposits an anchor.        | Stall (angle of attack)                                   | Nose down, regain airspeed, approach from shallower angle.                               |
| **Shaw Falling**                 | Old cognitive gauge breaks, new gauge subsumes it. Restructuring, not failure.                        | Phase transition (aufheben)                               | The fall IS learning. Don't fight it. Mark the anchor.                                   |
| **Intent**                       | The central gauge — every concept either forms, applies, or protects intent. The hub.                 | Gauge field                                               | Name the intent before the Walk. Everything flows from it.                               |
| **AVR**                          | Agency-Vector-Reality. Two paths: Agency builds toward outcomes. Reality Observer detects anomalies.  | Eigenstate of intent                                      | Check: are you on the Agency path or the Reality path? Don't mix.                        |
| **MVA**                          | Most Viable Architecture — absorb complexity early because decisions calcify.                         | Tesler's Law + calcification                              | Ask "is this load-bearing or decorative?" Decide load-bearing early.                     |
| **Backward force**               | Intent propagates upstream — what the receiver values changes what gets sampled.                      | Top-down causation                                        | When downstream work contradicts upstream decisions, trace backward.                     |
| **Codebook**                     | Reference structure (ctx-s) that maps symbols to positions. H3, postal codes, state machines.         | Shannon (1948) code table                                 | Ask "does a codebook sit behind this property?"                                          |
| **Proto-property**               | Description that could become a property but lacks a codebook to resolve against.                     | Pre-codebook state                                        | If a field feels important but unstructured, it might be proto.                          |
| **Codebook Test**                | "Property missing its codebook, or gd-eidos missing its field or chain?"                              | Diagnostic                                                | Use when something feels like a node but shouldn't be one.                               |

## 2. Discovery Toolkit

| Term                       | Definition                                                                                            | Physics                       | Walk Tip                                                                                 |
|----------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------|------------------------------------------------------------------------------------------|
| **Superposition**          | Multiple valid identities coexist until intent collapses one. The thing is undetermined.              | Quantum superposition         | Don't force a choice. Walk more. Intent will collapse it.                                |
| **Collapse**               | Intent determines what the thing IS in your model. Observation selects one state.                     | Wavefunction collapse         | Name the intent that caused the collapse.                                                |
| **Schroedinger's _doc_id** | "We have the location, we just don't know where it is." Fuzzy boundary, accept it.                    | Superposition of boundaries   | Stop subdividing. Accept fuzziness. Use properties for practical boundary.               |
| **Rims**                   | Hard constraint boundaries — do not cross. Each rim eliminates configurations.                        | Flight envelope edges         | Ask "what is forbidden?" Rims narrow the space.                                          |
| **Gravity**                | The objective function pulling toward the natural solution. Intent and usefulness.                    | Gravitational potential       | Ask "what is this thing FOR?" Gravity = usefulness in disguise.                          |
| **Anti-structure**         | What CANNOT be — as informative as what IS. The sculptor removes marble.                              | Symmetry breaking             | Discovering what's NOT a node is as valuable as discovering what IS.                     |
| **Finding chain**          | Discovery-direction chain — runs opposite to ontological chain. Outside-in, not inside-out.           | Inverse traversal             | Start from the observable surface, trace inward.                                         |
| **Forked chain**           | gd-eidos needing two independent chains. Cytonode needs both host AND ip-pri.                         | Branched dependency           | Ask "does this need TWO scoping structures?"                                             |
| **Tessellation**           | Complete tiling — every point belongs to exactly one tile. Postal codes, subnets, H3.                 | Space partition               | If it tiles completely without gaps or overlap, it's a tessellation.                     |
| **Tessellated namespace**  | Hierarchical tiling with chain dependency at each level. Subnets within networks within locations.    | Recursive partition           | Look for the deja vu — subnets feel like postal codes because they ARE the same pattern. |
| **Cytonode**               | Network endpoint: IP:port:protocol. Born from property merge on host via "how do things communicate?" | Cell + node (gd-eidos)        | Emerged from 3 properties clustering under intent. Not designed.                         |
| **Quantifact**             | Software + version on host. Fuzzy boundary, gravity saves it. Born from "what do I update?"           | Quantum + artifact (gd-eidos) | Barely passes Node Test. Keep it because observables need it.                            |
| **Node Test**              | Four criteria: Identifiable, Structural, Unambiguous, Useful. Is it a node or a property?             | Symmetry probe                | Run all four. If any fails, it's not a node.                                             |
| **Seven Questions**        | Seven transformations testing identity conservation. If all survive, it's an Eidos.                   | Noether symmetry test         | Apply all seven. Where it breaks = where gauge dependency lives.                         |
| **Graphalize**             | The act of deciding what's a node, edge, or property. Every choice is a gauge-fix.                    | Gauge-fixing a domain         | You're graphalizing whether you name it or not. Name it.                                 |
| **Load-bearing gauge**     | A gauge choice that other structures now depend on. Can't change without breaking things.             | Spontaneous symmetry breaking | Ask "what depends on this choice?" If a lot, it's load-bearing.                          |
| **Calcification**          | Load-bearing gauge that can no longer be changed. The decision fossilized.                            | Decoherence / classical limit | Recognize early. MVA says: get calcifying decisions right first.                         |
| **Entropy Patrol**         | Scouts sent to check if Reality shifted since last observation. Reality Observer Path.                | — (cybernetic)                | Agency builds → Entropy degrades → Patrol detects → Anomaly surfaces.                    |
| **Reality Walkers**        | Walk around Reality — observe, discover, find what exists. Bailiwick cut brings home what matters.    | Field survey                  | Walk wide, cut what you need, bring it back to the model.                                |

## 3. Walk Navigation

### Three Signals

```
Itch      → "look HERE"        → superposition detected (pre-verbal)
Gravity   → "go THIS WAY"      → usefulness / intent pulling
Friction  → "NOT THAT WAY"     → rim / anti-structure detected (pre-verbal)
```

### The Eidos Spectrum

```
Gauge-invariant ──── identity absolute, no context (ORG, IND, ip-pub, CVE)
gd-eidos: Chain ──── ordered links restore identity (ip-pri, host, department)
gd-eidos: Field ──── constraints + gravity → stable solution (biz-service, quantifact)
Tag / Property  ──── no identity (status, priority, loc_intent) - may become Eidos-like with a Codebook
```

### Node Test (4 criteria)

```
1. Identifiable  — unique ID within its type
2. Structural    — forms edges with same-Eidos instances
3. Unambiguous   — one clear Eidos, never maybe
4. Useful        — worth tracking as discrete thing
```

For gd-eidos, additionally: what mechanism restores symmetry (chain or field)?

### Seven Questions (symmetry probe)

```
Q1  Identity Namespace    "Who defines these IDs?"
Q2  Structural Integrity  "Can all instances form ONE coherent structure?"
Q3  Edge Homogeneity      "Are the intra-type edges the same kind?"
Q4  Substitutability      "Swap one instance for another — does structure hold?"
Q5  One Level Up          "Go broader — does structure break?" (if yes: right level)
Q6  One Level Down        "Go narrower — do you lose structure?" (if yes: right level)
Q7  Reference Line        "Can EVERY instance be assigned to exactly ONE Eidos?"
```

### Two Paths (when a property feels important)

```
Path A (Codebook): Property stays property. Structure from external reference (H3, postal codes).
                   → Ask: "does a codebook sit behind this?"

Path B (Merge):    Properties cluster into new entity. Structure from the merge.
                   → Ask: "does this cluster have its own edges? its own identity?"
```

### Seven Eidos Smells (stop and Walk)

```
1. Name Problem         People call it different things → superposition
2. "It Depends"         Answer changes with context → gd-eidos
3. Obvious Undefinable  Everyone uses the word, nobody can define it → ghost
4. Boundary Argument    Disagreement about inside vs outside → superposition
5. Inception Dilation   Boundary keeps subdividing deeper → Schroedinger's _doc_id
6. Deja Vu             This feels like something you modeled before → tessellated namespace
7. Easy Delete          Remove it and nothing real changes → ghost
```

## 4. AI-Human Interaction

### META Levels

| Level         | You Are...                          | AI Should...                        |
|---------------|-------------------------------------|-------------------------------------|
| **META-META** | Designing the process itself        | Stay abstract, no examples, no code |
| **META**      | Filling the Four Boxes, documenting | Document, don't implement           |
| **EXECUTE**   | Building from completed specs       | Write code, implement               |

**Switching rule**: AI must ask before switching levels. Confirm META level before responding.

### HitL (Human-in-the-Loop)

| Term     | Definition                                                              | Physics              | Walk Tip                                                         |
|----------|-------------------------------------------------------------------------|----------------------|------------------------------------------------------------------|
| **HitL** | AI-Human balance point. Human at gauge transitions, AI everywhere else. | Gödel incompleteness | The system can't validate its own gauge. Human is Gödel-outside. |

### Communication Shortcuts

| Pattern                    | When                           | Example                                             |
|----------------------------|--------------------------------|-----------------------------------------------------|
| **Semicolon answers**      | Multiple questions             | "1. Yes; 2. No; 3. TBD"                             |
| **Level declaration**      | Prevent drift                  | "We're at META"                                     |
| **Diversion alert**        | AI drifts to wrong level       | "You're implementing, we're at META"                |
| **Bias check**             | AI seems narrow                | "Do you have any implicit bias or anchoring?"       |
| **Dig deeper**             | Shallow answer                 | "Analyze from first principles: why does X need Y?" |
| **Socratic method**        | AI missed something            | "Is that really according to...?"                   |
| **Validate understanding** | Expose gaps                    | "What are your CONFUSION levels?"                   |
| **Side quest**             | Idea without poisoning context | "SIDE QUEST: Create a bead for X"                   |
| **Vague vs anchor**        | Low-context terms creeping in  | "Entity" (vague) vs "ORG" (anchored)                |

### Walk Protocols

| Phase         | What                  | How                                                         | Output                               |
|---------------|-----------------------|-------------------------------------------------------------|--------------------------------------|
| **Walk**      | Explore, find anchors | Probe gently, don't commit. Follow itch, gravity, friction. | Anchor points with confidence %      |
| **Hammer**    | Test candidates       | Attack from every angle. Try to break it.                   | Locked findings or killed candidates |
| **Synthesis** | Document and lock     | Write the result. Gauge-fix.                                | Reference document                   |

**Rule**: Don't Hammer until Walk has found the right words. Wrong definitions calcify wrong architecture.

### Shaw Audiences

| Audience    | Focus          | Compression      | Principle                                                       |
|-------------|----------------|------------------|-----------------------------------------------------------------|
| **Boss**    | WHY            | 10:1             | Decision-enabling — 5 minutes                                   |
| **Lead**    | WHAT           | 3:1              | Planning-enabling — 15 minutes                                  |
| **Worker**  | HOW            | 1:1              | 4am Principle — half-asleep followable                          |
| **User**    | USE            | selective        | First-time success — if it doesn't work immediately, they leave |
| **Student** | BUILD codebook | anti-compression | Deliberate gaps — each pass builds understanding                |

### Proven Useful Words

Words that speed up Walks by giving instant shared vocabulary:

- **Intent** — the gauge everything is measured against
- **Gravity** — usefulness pulling toward a solution
- **Friction** — pre-verbal rim detection
- **Itch** — pre-verbal superposition detection
- **Ghost** — artifact of organization, not reality
- **Load-bearing** — can't change without breaking dependents
- **Calcified** — can no longer change at all
- **Eigenstate** — what manifests when intent is applied

---

**Version**: 1.0
**Created**: 2026-02-18
