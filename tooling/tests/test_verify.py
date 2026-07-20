import os, yaml
from tooling.multirepo import verify

HUB = "eval"                                       # run pytest from the hub root
V2  = "tooling/baseline/expected_structure.yaml"
V2Q = "tooling/baseline/gold_qa.json"

def test_structure_equivalence_holds():
    assert verify.check_structure_equivalence(HUB, V2) == []

def test_qa_equivalence_holds():
    assert verify.check_qa_equivalence(HUB, V2Q) == []

def test_integrity_checks_pass():
    assert verify.check_referential_integrity(HUB) == []
    assert verify.check_single_ownership(HUB) == []
    assert verify.check_parent_tier(HUB) == []

def test_referential_integrity_catches_dangling(tmp_path):
    ev = tmp_path/"eval"; (ev/"a").mkdir(parents=True); (ev/"_cross_source").mkdir()
    yaml.safe_dump({"entities":[{"name":"X","tier":0,"parent":None}],
                    "edges":[{"from":"X","type":"t","to":"GHOST","tier":0}]},
                   open(ev/"a"/"structure.yaml","w"))
    open(ev/"_cross_source"/"structure.yaml","w").write("edges: []\n")
    assert any("GHOST" in v for v in verify.check_referential_integrity(str(ev)))

UMB = "/media/nine/HD_2/shuhan/knowledge-base/pedalworks"
def test_qa_sources_exist_on_disk():
    assert verify.check_qa_sources_exist("eval", UMB) == []
def test_all_format_probes_present():
    assert verify.check_format_probes(UMB) == []
