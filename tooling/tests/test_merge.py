import os, yaml
from tooling.multirepo import merge

def _write(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    yaml.safe_dump(obj, open(p, "w"), sort_keys=False)

def test_merge_concatenates_entities_and_edges(tmp_path):
    ev = tmp_path / "eval"
    _write(str(ev/"procurement"/"structure.yaml"),
           {"entities":[{"name":"Frame","kind":"part","tier":1,"parent":"Supply"}],
            "edges":[{"from":"Frames Ltd","type":"supplies","to":"Frame","tier":1}]})
    _write(str(ev/"production"/"structure.yaml"),
           {"entities":[{"name":"Trail Blazer","kind":"model","tier":2,"parent":"Products"}],"edges":[]})
    _write(str(ev/"_cross_source"/"structure.yaml"),
           {"entities":[], "edges":[{"from":"Trail Blazer","type":"uses","to":"Frame","tier":2}]})
    m = merge.merge_structure(str(ev))
    assert {e["name"] for e in m["entities"]} == {"Frame","Trail Blazer"}
    assert {"from":"Trail Blazer","type":"uses","to":"Frame","tier":2} in m["edges"]
    assert len(m["edges"]) == 2

def test_merge_qa(tmp_path):
    ev = tmp_path / "eval"
    _write(str(ev/"procurement"/"qa.yaml"), {"questions":[{"id":"a"}]})
    _write(str(ev/"_cross_source"/"qa.yaml"), {"questions":[{"id":"b"}]})
    assert {x["id"] for x in merge.merge_qa(str(ev))["questions"]} == {"a","b"}
