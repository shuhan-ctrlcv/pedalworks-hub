"""Generate the '## Cross-source edges' section of
`eval/_cross_source/system-map.md` from `eval/_cross_source/structure.yaml`,
so the human map can never drift from the machine data by hand.

The prose above that heading (the theme narrative + ASCII diagram) is
hand-authored and left untouched; only the final section is regenerated.

CLI:  python -m tooling.multirepo.system_map   (rewrites the section in place)
"""
from __future__ import annotations
import os, yaml

_HEADING = "## Cross-source edges"

def _cross_structure(hub_eval_dir):
    p = os.path.join(hub_eval_dir, "_cross_source", "structure.yaml")
    return (yaml.safe_load(open(p)) or {}).get("edges") or []

def _map_path(hub_eval_dir):
    return os.path.join(hub_eval_dir, "_cross_source", "system-map.md")

def render_section(hub_eval_dir) -> str:
    """The canonical text of the '## Cross-source edges' section, derived
    entirely from structure.yaml."""
    edges = _cross_structure(hub_eval_dir)
    lines = [
        _HEADING, "",
        f"The {len(edges)} edges below are the machine-checked cross-source edges from",
        "`eval/_cross_source/structure.yaml` — every edge whose two endpoints are",
        "owned by different areas, regardless of tier. **Generated — do not edit by",
        "hand; regenerate with `python -m tooling.multirepo.system_map`** (the",
        "verifier's `system_map_sync` check enforces this).", "",
    ]
    for e in edges:
        lines.append(f"- {e['from']} --{e['type']}--> {e['to']} (tier {e['tier']})")
    return "\n".join(lines) + "\n"

def current_section(hub_eval_dir) -> str:
    """The '## Cross-source edges' section as it currently sits in the file
    ('' if the heading is absent)."""
    text = open(_map_path(hub_eval_dir)).read()
    idx = text.find(_HEADING)
    return text[idx:] if idx != -1 else ""

def regenerate(hub_eval_dir) -> None:
    """Rewrite the section in place from structure.yaml, preserving everything
    above the heading."""
    path = _map_path(hub_eval_dir)
    text = open(path).read()
    idx = text.find(_HEADING)
    head = text[:idx] if idx != -1 else (text.rstrip() + "\n\n")
    open(path, "w").write(head + render_section(hub_eval_dir))

if __name__ == "__main__":
    regenerate("eval")
    print("regenerated eval/_cross_source/system-map.md cross-source edges")
