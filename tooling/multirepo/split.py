"""One-time migration: split the frozen v2 ground truth into per-area slices.
Entities -> owning area (by tier-0 root). Edges -> internal (same area) or
_cross_source (ends differ), regardless of tier. After migration the per-area
files are hand-maintained and this script is retired (kept for A-B reproducibility)."""
from __future__ import annotations
import os, yaml
from tooling.multirepo.areas import area_of, AREAS

def _dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    yaml.safe_dump(obj, open(path, "w"), sort_keys=False, allow_unicode=True)

def split_structure(v2_path: str, hub_eval_dir: str) -> None:
    d = yaml.safe_load(open(v2_path))
    by_name = {e["name"]: e for e in d["entities"]}
    ent_by_area = {a: [] for a in AREAS}
    for e in d["entities"]:
        ent_by_area[area_of(e["name"], by_name)].append(e)
    internal = {a: [] for a in AREAS}
    cross = []
    for edge in d["edges"]:
        af, at = area_of(edge["from"], by_name), area_of(edge["to"], by_name)
        (internal[af] if af == at else cross).append(edge)
    for a in AREAS:
        _dump(os.path.join(hub_eval_dir, a, "structure.yaml"),
              {"entities": ent_by_area[a], "edges": internal[a]})
    _dump(os.path.join(hub_eval_dir, "_cross_source", "structure.yaml"),
          {"entities": [], "edges": cross})
