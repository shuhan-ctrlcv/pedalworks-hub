"""Tier-A static verification: prove the multi-repo split is faithful to v2 and
internally consistent. No LLM, no extraction."""
from __future__ import annotations
import glob, json, os, yaml
from tooling.multirepo import merge

def _load_structs(hub_eval):
    return [(p, yaml.safe_load(open(p)) or {})
            for p in sorted(glob.glob(os.path.join(hub_eval, "*", "structure.yaml")))]

def check_single_ownership(hub_eval) -> list[str]:
    seen, viol = {}, []
    for p, obj in _load_structs(hub_eval):
        for e in (obj.get("entities") or []):
            if e["name"] in seen:
                viol.append(f"entity {e['name']!r} defined in {seen[e['name']]} and {p}")
            seen[e["name"]] = p
    return viol

def check_referential_integrity(hub_eval) -> list[str]:
    m = merge.merge_structure(hub_eval)
    names = {e["name"] for e in m["entities"]}
    return [f"edge {edge} references undefined entity {edge[end]!r}"
            for edge in m["edges"] for end in ("from", "to") if edge[end] not in names]

def check_parent_tier(hub_eval) -> list[str]:
    m = merge.merge_structure(hub_eval)
    by = {e["name"]: e for e in m["entities"]}
    viol = []
    for e in m["entities"]:
        p = e.get("parent")
        if p is None:
            if e.get("tier") != 0:
                viol.append(f"{e['name']} has no parent but tier != 0")
            continue
        if p not in by:
            viol.append(f"{e['name']} parent {p!r} undefined")
        elif by[p].get("tier", 99) >= e.get("tier", 0):
            viol.append(f"{e['name']} (tier {e.get('tier')}) parent {p} not a lower tier")
    return viol

def _struct_sets(obj):
    ent = {(e["name"], e.get("kind"), e.get("tier"), e.get("parent")) for e in obj["entities"]}
    edg = {(e["from"], e["type"], e["to"], e.get("tier")) for e in obj["edges"]}
    return ent, edg

def check_structure_equivalence(hub_eval, v2_path) -> list[str]:
    me, mg = _struct_sets(merge.merge_structure(hub_eval))
    oe, og = _struct_sets(yaml.safe_load(open(v2_path)))
    viol = []
    for label, extra, missing in [("entity", me-oe, oe-me), ("edge", mg-og, og-mg)]:
        viol += [f"extra {label}: {x}" for x in extra]
        viol += [f"missing {label}: {x}" for x in missing]
    return viol

def check_qa_equivalence(hub_eval, v2_qa_path) -> list[str]:
    merged = {q["id"]: q for q in merge.merge_qa(hub_eval)["questions"]}
    orig = {q["id"]: q for q in json.load(open(v2_qa_path))["questions"]}
    viol = [f"extra qa: {i}" for i in set(merged)-set(orig)]
    viol += [f"missing qa: {i}" for i in set(orig)-set(merged)]
    for i in set(merged) & set(orig):
        for field in ("question", "answerable", "tier", "reference_key_facts"):
            if merged[i].get(field) != orig[i].get(field):
                viol.append(f"qa {i}: field {field!r} changed")
    return viol

def run_static(hub_eval, v2_struct, v2_qa) -> dict:
    return {
        "structure_equivalence": check_structure_equivalence(hub_eval, v2_struct),
        "qa_equivalence": check_qa_equivalence(hub_eval, v2_qa),
        "referential_integrity": check_referential_integrity(hub_eval),
        "single_ownership": check_single_ownership(hub_eval),
        "parent_tier": check_parent_tier(hub_eval),
    }

# Exact substrings each QA-cited code file MUST still contain after the rewrite.
CITED_CODE_FACTS = {
    "pedalworks-order-planning/src/planner.py": ["_LOW_STOCK_THRESHOLD = 1"],
    "pedalworks-production/src/quality.py": ["_inspected == 1"],
    "pedalworks-production/src/trailblazer.py": ["Assembly Floor"],
    "pedalworks-finance/src/models.py": ["LedgerEntry", "stage", "kind", "amount"],
}

def check_cited_code_facts(umbrella) -> list[str]:
    viol = []
    for rel, needles in CITED_CODE_FACTS.items():
        p = os.path.join(umbrella, rel)
        if not os.path.exists(p):
            viol.append(f"missing cited file: {rel}"); continue
        txt = open(p).read()
        for n in needles:
            if n not in txt:
                viol.append(f"{rel}: lost cited fact {n!r}")
    return viol

if __name__ == "__main__":
    import sys
    res = run_static("eval", "tooling/baseline/expected_structure.yaml",
                     "tooling/baseline/gold_qa.json")
    ok = all(not v for v in res.values())
    for k, v in res.items():
        print(f"{'OK  ' if not v else 'FAIL'} {k}" + ("" if not v else f" ({len(v)})"))
        for line in v[:20]:
            print("   -", line)
    sys.exit(0 if ok else 1)
