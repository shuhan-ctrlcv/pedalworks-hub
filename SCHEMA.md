# SCHEMA.md — the PedalWorks hub data model

This file is the reference for the data in `eval/`. It is mirrored from the
design spec (`2026-07-20-pedalworks-multirepo-revamp-design.md`, §4). Read
this before editing anything under `eval/`.

## `structure.yaml` (per area, and `_cross_source`)

```yaml
entities:
  - name: <string>            # canonical name; unique across ALL areas
    kind: <string>            # viewer vocabulary (theme|system|process|part|…)
    tier: 0 | 1 | 2
    parent: <name> | null     # null only for the area's tier-0 theme node
    attrs: { <k>: <v>, … }    # optional; definitional attribute facts
    aliases: [ <string>, … ]  # optional; hand-curated surface-form variants
edges:
  - from: <entity name>
    type: <verb>              # viewer vocabulary
    to: <entity name>
    tier: 0 | 1 | 2           # the depth the edge lives at
```

- **A per-area file** contains: its Tier-0 theme node, that area's tier-1/2
  entities, and only its **internal** edges.
- **`_cross_source/structure.yaml`** contains **no entity definitions** — only
  cross-source edges. Its edges reference entities *by name* that are defined
  in the area files.

### Allowed `kind` values (entities)

`area`, `build_step`, `capacity_spec`, `concept`, `cost_kind`,
`external_actor`, `group`, `ledger_entry`, `location`, `log`, `material`,
`model`, `order_record`, `part`, `process`, `qc_check`, `running_total`,
`sensor`, `shipment_record`, `stock_record`, `subpart`, `supplier`, `system`,
`theme`.

### Allowed `tier` values

`0` (theme root), `1`, `2`.

## The tier system — what it is and why

Every entity carries a `tier` (0, 1, or 2) and every edge carries the tier it
lives at. Tiers are a **containment hierarchy of increasing detail**, linked by
`parent`:

- **Tier 0** — the six super-theme nodes (one per area): the top-level map of
  the company (Supply, Production, Finance, …).
- **Tier 1** — the main sub-nodes inside a theme (a named supplier, a product
  line, a data system).
- **Tier 2** — the fine-grained detail under a tier-1 node (one supplier's lead
  time, one product's bill of materials, one build step).

`parent` links each node to the one above it, so the graph is a tier-0 → tier-1
→ tier-2 tree (plus a few deliberate cross-branch edges — see the ownership
rules below).

We organise the ground truth this way for **two reasons**:

**1. To judge / visualise the graph at different levels of detail.** Because
every node and edge is tagged with its tier, the *same* ground truth renders at
any depth:
- a **Tier-0 visualisation** is the high-level map — just the six themes and how
  they connect;
- a **Tier-2 visualisation** is the full, most-detailed knowledge graph.
This lets extraction be checked at any zoom level — from "does the pipeline get
the Tier-0 shape right?" up to "does it recover the complete Tier-2 graph?"

**2. To make additions easy and predictable.** The tier a fact belongs to tells
you exactly where it goes:
- a whole new **general section** → a new **Tier-0** node (a new area folder +
  repo; see `UPDATE-GUIDE.md` Path B) — nothing existing changes;
- **more detail about something that already exists** → a new **Tier-1 / Tier-2**
  node under the relevant parent Tier-0 node, in that parent's area file
  (`UPDATE-GUIDE.md` Path A).
So "where does this new information go?" always has a clear answer: pick the
tier, then the owning area.

## `qa.yaml` (per area, and `_cross_source`)

```yaml
questions:
  - id: <slug>
    question: <string>
    answerable: true | false
    tier: low_level | high_level | multi_hop
    expected_sources: [ "<repo>/<path>", … ]   # REPO-QUALIFIED
    reference_key_facts: [ <string>, … ]
    format_probe: true | false
    # optional: notes, persona, chain, hops
```

- **`expected_sources` are repo-qualified** — e.g.
  `procurement/docs/supplier_catalog.pdf`, not the old flat `docs/…`.
- A question answerable from a single area lives in that area's `qa.yaml`; a
  question spanning repos (most `multi_hop`) lives in `_cross_source/qa.yaml`.

## Single authoring source

The per-area `structure.yaml` files are the **sole** authoring source. There
is no separate "current state" doc, and no `target_graph.yaml` /
`expected_structure.yaml` to keep in sync — the slices are the state.

## The two ownership rules

1. **Single home for every entity.** Each entity is *defined* in exactly
   **one** area — its home. Other repos may *reference* it by name, but
   never redefine it. Example: `Frame`'s home is `procurement` (it is a
   supplied part). Production's BOM and Warehouse's stock *reference*
   `Frame`; they do not re-declare it.
2. **Edges are filed by ownership, not by tier:**
   - Both endpoints in the same area → the edge lives in that area's
     `structure.yaml` (an **internal edge**).
   - Endpoints owned by different areas → the edge lives in
     `_cross_source/structure.yaml` (a **cross-source edge**), **regardless
     of the edge's tier**.

## Overlay honesty

`tier`, `parent`, `kind`, and edge `type` are our
**visualisation/vocabulary overlay**. The flat KV engine emits none of them
as-is. The structure check is **name-recall** of entities and edges — it
verifies required names are present, not that the extractor reproduced our
tiers or verbs.

## Repo ↔ theme mapping

The area folder in the hub (and the content-repo short name) does not always
match the Tier-0 theme entity's domain name. Use this table:

| Area / repo | Tier-0 theme entity |
|---|---|
| `order-planning` | Planning & Demand |
| `procurement` | Supply |
| `warehouse` | Inventory |
| `production` | Production |
| `shipping` | Fulfillment |
| `finance` | Finance |
