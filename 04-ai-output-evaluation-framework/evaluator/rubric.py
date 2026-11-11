"""Rubric-based scoring of model responses."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Criterion:
    id: str
    weight: float
    description: str


@dataclass(frozen=True)
class Rubric:
    name: str
    min_score: int
    max_score: int
    criteria: List[Criterion]

    @property
    def ids(self) -> List[str]:
        return [c.id for c in self.criteria]


def load_rubric(path: str) -> Rubric:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    criteria = [Criterion(c["id"], float(c["weight"]), c.get("description", "")) for c in raw["criteria"]]
    total = sum(c.weight for c in criteria)
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"criterion weights must sum to 1.0, got {total}")
    if len({c.id for c in criteria}) != len(criteria):
        raise ValueError("duplicate criterion id")
    return Rubric(raw.get("name", "rubric"), int(raw["scale"]["min"]), int(raw["scale"]["max"]), criteria)


def weighted_score(ratings: Dict[str, float], rubric: Rubric) -> float:
    """Return a 0-100 score. Every criterion must be rated and within the scale."""
    missing = [c.id for c in rubric.criteria if c.id not in ratings]
    if missing:
        raise ValueError(f"missing ratings for: {', '.join(missing)}")
    extra = [k for k in ratings if k not in rubric.ids]
    if extra:
        raise ValueError(f"unknown criteria: {', '.join(extra)}")
    span = rubric.max_score - rubric.min_score
    total = 0.0
    for c in rubric.criteria:
        v = ratings[c.id]
        if not rubric.min_score <= v <= rubric.max_score:
            raise ValueError(f"{c.id} rating {v} outside {rubric.min_score}-{rubric.max_score}")
        total += c.weight * (v - rubric.min_score) / span
    return round(total * 100, 2)
