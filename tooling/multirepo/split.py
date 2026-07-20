"""One-time migration: split the frozen v2 ground truth into per-area slices.
Entities -> owning area (by tier-0 root). Edges -> internal (same area) or
_cross_source (ends differ), regardless of tier. After migration the per-area
files are hand-maintained and this script is retired (kept for A-B reproducibility)."""
from __future__ import annotations
import os, yaml, json
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

# QA that cite a SPLIT source file get explicit, reviewable re-paths.
QA_SOURCE_OVERRIDES = {
    "hl-three-systems": ["pedalworks-order-planning/docs/data-model-orderdb.md",
                          "pedalworks-warehouse/docs/data-model-partsdb.md",
                          "pedalworks-finance/docs/data-model-ledgerdb.md"],
    "ll-orderdb-readers-writers": ["pedalworks-order-planning/docs/data-model-orderdb.md"],
    "ll-ledgerentry-fields": ["pedalworks-finance/src/models.py"],
}

def _repath(qid, sources, path_map):
    if qid in QA_SOURCE_OVERRIDES:
        return QA_SOURCE_OVERRIDES[qid]
    out = []
    for s in sources:
        new = path_map.get(s)
        if new is None or new == "SPLIT":
            raise KeyError(f"{qid}: no path_map entry for {s}")
        out.append(new)
    return out

def _area_of_sources(new_sources):
    hit = {s.split("/", 1)[0].replace("pedalworks-", "") for s in new_sources}
    return next(iter(hit)) if len(hit) == 1 else None

def split_qa(v2_qa_path: str, hub_eval_dir: str, path_map_path: str) -> None:
    from tooling.multirepo.areas import load_path_map
    pm = load_path_map(path_map_path)
    buckets = {}
    for q in json.load(open(v2_qa_path))["questions"]:
        q = dict(q)
        q["expected_sources"] = _repath(q["id"], q.get("expected_sources", []), pm)
        area = _area_of_sources(q["expected_sources"]) or "_cross_source"
        buckets.setdefault(area, []).append(q)
    for area, qs in buckets.items():
        _dump(os.path.join(hub_eval_dir, area, "qa.yaml"), {"questions": qs})
