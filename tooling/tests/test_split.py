import json
import yaml
from tooling.multirepo import split, merge

BASE = "tooling/baseline/expected_structure.yaml"
BASEQ = "tooling/baseline/gold_qa.json"
PM    = "tooling/path_map.yaml"

def _sets(obj):
    ent = {(e["name"], e.get("kind"), e.get("tier"), e.get("parent")) for e in obj["entities"]}
    edg = {(e["from"], e["type"], e["to"], e.get("tier")) for e in obj["edges"]}
    return ent, edg

def test_split_then_merge_equals_v2(tmp_path):
    ev = str(tmp_path / "eval")
    split.split_structure(BASE, ev)
    assert _sets(merge.merge_structure(ev)) == _sets(yaml.safe_load(open(BASE)))

def test_cross_source_holds_only_cross_edges_no_entities(tmp_path):
    ev = str(tmp_path / "eval")
    split.split_structure(BASE, ev)
    cs = yaml.safe_load(open(f"{ev}/_cross_source/structure.yaml"))
    assert (cs.get("entities") or []) == []
    assert len(cs["edges"]) == 30   # 7 tier-0 + 23 cross-branch leaf edges

def test_qa_split_preserves_all_ids(tmp_path):
    ev = str(tmp_path / "eval")
    split.split_qa(BASEQ, ev, PM)
    merged = {q["id"] for q in merge.merge_qa(ev)["questions"]}
    assert merged == {q["id"] for q in json.load(open(BASEQ))["questions"]}

def test_qa_sources_are_repo_qualified(tmp_path):
    ev = str(tmp_path / "eval")
    split.split_qa(BASEQ, ev, PM)
    for q in merge.merge_qa(ev)["questions"]:
        for s in q.get("expected_sources", []):
            assert s.startswith("pedalworks-"), f"{q['id']}: {s} not repo-qualified"
