# Start here — PedalWorks hub concepts

New to this repo? Read this first, then follow the pointers to the reference docs.

## What this is (one line)

PedalWorks is a fictional bicycle company used as a knowledge-base test fixture.
The 6 content repos are the "company" (each ingested as a knowledge source);
this **hub** is the ground truth — the correct graph and Q&A used to check what
the pipeline extracts. See `../README.md` for the repo index and `README.md` for
what lives in this hub.

## The one concept to understand: tiers

The ground truth is organised in **three tiers of increasing detail**:

- **Tier 0** — six super-theme nodes (Supply, Production, Finance, …): the
  top-level map.
- **Tier 1** — the main sub-nodes inside a theme (a supplier, a product line, a
  data system).
- **Tier 2** — the fine detail under a tier-1 node (a lead time, a bill of
  materials, a build step).

We use tiers for **two reasons**:

1. **Judging / visualising the graph at different levels of detail.** The same
   data renders as a high-level **Tier-0** map or the full, most-detailed
   **Tier-2** knowledge graph — so extraction can be checked at any zoom level.
2. **Making additions easy.** The tier tells you where a fact goes: a whole new
   general section is a new **Tier-0** node (Path B); more detail about something
   that already exists is a new **Tier-1 / Tier-2** node under its parent
   (Path A). Nothing existing has to move.

Full explanation: `SCHEMA.md` → "The tier system — what it is and why".

## Setup (one-time)

The hub and the 6 content repos are separate GitHub repos, but the tooling
expects them **cloned into one parent folder** (the content repos are siblings
of `pedalworks-hub`):

```bash
mkdir pedalworks && cd pedalworks
for r in order-planning procurement warehouse production shipping finance hub; do
  git clone https://github.com/shuhan-ctrlcv/pedalworks-$r.git
done
pip install pyyaml          # the only dependency
```

If you clone only the hub, the verifier still runs the ground-truth checks but
**skips** the three checks that need the content files (it tells you so) — clone
the content repos alongside to enable them.

## Where to go next

- **Add or change content?** → `UPDATE-GUIDE.md` (Path A: extend an area · Path
  B: add a new area · re-home an entity).
- **Editing `eval/` data directly?** → `SCHEMA.md` (fields, allowed
  `kind`/`tier`, the ownership rules).
- **How the 6 areas connect?** → `eval/_cross_source/system-map.md`.
- **Check your edit is consistent:**

  ```bash
  cd pedalworks-hub && PYTHONPATH=. python3 -m tooling.multirepo.verify
  ```
