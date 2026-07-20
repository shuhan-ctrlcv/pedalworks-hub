"""Area assignment for the multi-repo split. An entity's area is the repo that
OWNS it, derived from its Tier-0 theme root via the parent chain."""
from __future__ import annotations
import yaml

THEME_TO_AREA = {
    "Planning & Demand": "order-planning",
    "Supply": "procurement",
    "Inventory": "warehouse",
    "Production": "production",
    "Fulfillment": "shipping",
    "Finance": "finance",
}
AREAS = tuple(THEME_TO_AREA.values())

def root_theme(name: str, entities_by_name: dict) -> str:
    seen, cur = set(), name
    while True:
        if cur in seen:
            raise ValueError(f"parent cycle at {cur}")
        seen.add(cur)
        parent = entities_by_name[cur].get("parent")
        if not parent:
            return cur
        cur = parent

def area_of(name: str, entities_by_name: dict) -> str:
    return THEME_TO_AREA[root_theme(name, entities_by_name)]

def load_path_map(path: str) -> dict:
    return yaml.safe_load(open(path))
