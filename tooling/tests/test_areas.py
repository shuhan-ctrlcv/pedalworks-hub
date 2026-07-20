import yaml
from tooling.multirepo import areas

BASE = "tooling/baseline/expected_structure.yaml"  # run pytest from the hub root

def _by_name():
    return {e["name"]: e for e in yaml.safe_load(open(BASE))["entities"]}

def test_area_of_root_theme():
    ents = _by_name()
    assert areas.area_of("Supply", ents) == "procurement"
    assert areas.area_of("Finance", ents) == "finance"

def test_area_of_leaf_follows_parent_chain():
    ents = _by_name()
    assert areas.area_of("Aluminium", ents) == "procurement"      # -> Frame -> Supply
    assert areas.area_of("Trail Blazer", ents) == "production"     # -> Products -> Production
    assert areas.area_of("Frame Stock", ents) == "warehouse"       # -> PartsDB -> Inventory

def test_every_entity_maps_to_an_area():
    ents = _by_name()
    for name in ents:
        assert areas.area_of(name, ents) in {
            "order-planning","procurement","warehouse","production","shipping","finance"}
