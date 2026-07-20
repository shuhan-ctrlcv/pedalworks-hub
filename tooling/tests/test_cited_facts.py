from tooling.multirepo import verify

UMB = "/media/nine/HD_2/shuhan/knowledge-base/pedalworks"


def test_cited_code_facts_survive():
    assert verify.check_cited_code_facts(UMB) == []
