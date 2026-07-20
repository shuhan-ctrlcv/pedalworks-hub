import shutil
from tooling.multirepo import verify, system_map

def test_system_map_in_sync_on_real_hub():
    # run pytest from the hub root; the committed system-map is regenerated
    assert verify.check_system_map_sync("eval") == []

def test_system_map_sync_catches_drift(tmp_path):
    # copy the real hub eval into a temp dir, then tamper the map
    ev = tmp_path / "eval"
    shutil.copytree("eval", ev)
    mp = ev / "_cross_source" / "system-map.md"
    mp.write_text(mp.read_text() + "\n- Bogus --invented--> Edge (tier 2)\n")
    assert verify.check_system_map_sync(str(ev)) != []

def test_regenerate_makes_it_sync_again(tmp_path):
    ev = tmp_path / "eval"
    shutil.copytree("eval", ev)
    mp = ev / "_cross_source" / "system-map.md"
    mp.write_text(mp.read_text() + "\n- Bogus --invented--> Edge (tier 2)\n")
    assert verify.check_system_map_sync(str(ev)) != []
    system_map.regenerate(str(ev))
    assert verify.check_system_map_sync(str(ev)) == []
