"""Deterministic concatenation of per-area + _cross_source slices into the single
combined structure/QA the checker consumes. Pure I/O — no LLM, no transformation."""
from __future__ import annotations
import glob, os, yaml

def _slices(hub_eval_dir: str, fname: str):
    for p in sorted(glob.glob(os.path.join(hub_eval_dir, "*", fname))):
        yield p, (yaml.safe_load(open(p)) or {})

def merge_structure(hub_eval_dir: str) -> dict:
    entities, edges = [], []
    for _, obj in _slices(hub_eval_dir, "structure.yaml"):
        entities.extend(obj.get("entities") or [])
        edges.extend(obj.get("edges") or [])
    return {"entities": entities, "edges": edges}

def merge_qa(hub_eval_dir: str) -> dict:
    questions = []
    for _, obj in _slices(hub_eval_dir, "qa.yaml"):
        questions.extend(obj.get("questions") or [])
    return {"questions": questions}
