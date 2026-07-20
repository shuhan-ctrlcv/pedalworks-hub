# UPDATE-GUIDE.md — how to change the PedalWorks hub data

Written imperatively so a colleague can hand this task to an LLM. Mirrored
from the design spec (§7).

## The LLM loop

Every update follows the same loop:

1. Read `SCHEMA.md`.
2. Read the target area file(s) (`eval/<area>/structure.yaml`,
   `eval/<area>/qa.yaml`) plus `eval/_cross_source/` (`structure.yaml`,
   `qa.yaml`, `system-map.md`).
3. Make the edit.
4. Run the verifier:

```bash
cd pedalworks-hub && PYTHONPATH=. python3 -m tooling.multirepo.verify
```

Pick the path below that matches the change.

## Path A — add content to an existing area (common case)

1. Add the source doc/code to the owning content repo (e.g. a new supplier
   doc → `pedalworks-procurement/docs/…`).
2. In that area's `structure.yaml`, add/extend entities (`name, kind, tier,
   parent`). **Search first**; reuse an existing name rather than
   redefining an entity another area owns.
3. Add **internal** edges (both endpoints in this area) to the same file.
4. Add **cross-source** edges (endpoint owned elsewhere) to
   `_cross_source/structure.yaml`, referencing the other entity by its
   existing name.
5. Add ≥1 question to the area's `qa.yaml` (or `_cross_source/qa.yaml` if it
   spans repos), with **repo-qualified** `expected_sources` +
   `reference_key_facts`.
6. Update `_cross_source/system-map.md` only if a cross-source edge was
   added.
7. Run the verifier.

## Path B — add a new Tier-0 node / new repo (e.g. Forecasting, Marketing)

1. Create the new content repo (`pedalworks-forecasting`) with its
   docs/code.
2. Add it to `repo-manifest.yaml`.
3. Create `eval/<new-area>/` with `structure.yaml` (its tier-0 node + tier-1/2
   entities + internal edges) and `qa.yaml`.
4. Wire it in via `_cross_source/structure.yaml` (e.g. Marketing→Finance cost
   edges; Forecasting→Customer references) and add the node to
   `system-map.md`.
5. Run the verifier. **Nothing in existing areas changes** — growth is
   additive.

## Edge case — re-homing an entity

Moving an entity's ownership to a different area (e.g. a Part later owned by
a new PLM repo) is the one operation that touches two area files: remove the
definition from the old area, add it to the new, and re-file any edges whose
ownership changed. This is a deliberate "re-home" step; expected to be rare.
