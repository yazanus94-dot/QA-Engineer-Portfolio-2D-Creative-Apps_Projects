"""Agreement and preference metrics."""
from __future__ import annotations

from collections import Counter
from typing import Dict, Sequence


def cohens_kappa(a: Sequence, b: Sequence) -> float:
    """Inter-annotator agreement for two annotators labelling the same items (1 = perfect, 0 = chance)."""
    if len(a) != len(b) or not a:
        raise ValueError("label lists must be non-empty and the same length")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def mean_absolute_difference(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("score lists must be non-empty and the same length")
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def win_rates(preferences: Sequence[str]) -> Dict[str, float]:
    """Share of judgements won by each side. A tie counts as half a win for both."""
    if not preferences:
        raise ValueError("no preferences")
    n = len(preferences)
    a = sum(1 for p in preferences if p == "A") + 0.5 * sum(1 for p in preferences if p == "tie")
    b = sum(1 for p in preferences if p == "B") + 0.5 * sum(1 for p in preferences if p == "tie")
    unknown = [p for p in preferences if p not in ("A", "B", "tie")]
    if unknown:
        raise ValueError(f"invalid preference values: {set(unknown)}")
    return {"A": a / n, "B": b / n}
