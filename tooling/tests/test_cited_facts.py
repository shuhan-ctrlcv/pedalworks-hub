from tooling.multirepo import verify

UMB = ".."


def test_cited_code_facts_survive():
    assert verify.check_cited_code_facts(UMB) == []
