# pedalworks-hub

The single source of truth about the PedalWorks fixture. This repo is
**never ingested** — the 6 content repos are the knowledge sources; this hub
is the ground truth used to check what gets extracted from them.

## What's here

```
SCHEMA.md            the data model (structure.yaml / qa.yaml fields, rules)
UPDATE-GUIDE.md       how to add content, add a new area, or re-home an entity
repo-manifest.yaml    the 6 content repos + pinned commit shas
eval/
  order-planning/     structure.yaml, qa.yaml — Planning & Demand
  procurement/        structure.yaml, qa.yaml — Supply
  warehouse/          structure.yaml, qa.yaml — Inventory
  production/         structure.yaml, qa.yaml — Production
  shipping/           structure.yaml, qa.yaml — Fulfillment
  finance/            structure.yaml, qa.yaml — Finance
  _cross_source/      structure.yaml, qa.yaml, system-map.md — edges/questions spanning areas
tooling/              the verifier + merge/split helpers (not ingested; checker code)
```

Each area's `structure.yaml` **is** the live ground-truth graph for that
area — there's no separate "current state" doc to drift.
`eval/_cross_source/system-map.md` is the human-readable picture of how the
6 areas connect; `eval/_cross_source/structure.yaml` is its machine-readable
counterpart.

## How to use this repo

- **Adding or changing content?** Read `UPDATE-GUIDE.md` first — it has the
  exact steps (Path A: extend an existing area; Path B: add a new area;
  re-homing an entity).
- **Editing `eval/` data directly?** Read `SCHEMA.md` first — it defines the
  fields, allowed `kind`/`tier` values, and the ownership rules that decide
  whether something is an internal or cross-source edge.
- **Checking your edit is consistent:**

  ```bash
  cd pedalworks-hub && PYTHONPATH=. /home/nine/anaconda3/envs/road_asset/bin/python -m tooling.multirepo.verify
  ```

- **New to PedalWorks?** See `docs/onboarding.html` for a colleague-facing
  walkthrough, or `../README.md` (the umbrella index) for how this repo
  relates to the 6 content repos.
