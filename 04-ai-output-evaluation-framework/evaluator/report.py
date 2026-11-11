"""Load ratings, score them, and build a Markdown evaluation report."""
from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from statistics import mean
from typing import Dict, List

from .metrics import cohens_kappa, mean_absolute_difference, win_rates
from .rubric import Rubric, load_rubric, weighted_score


def load_ratings(path: str, rubric: Rubric) -> List[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            try:
                ratings = {c: float(row[c]) for c in rubric.ids}
            except (KeyError, ValueError) as e:
                raise ValueError(f"{path} line {i}: bad or missing rating ({e})") from e
            rows.append({"prompt_id": row["prompt_id"], "response_id": row["response_id"],
                         "annotator": row["annotator"], "ratings": ratings,
                         "score": weighted_score(ratings, rubric)})
    return rows


def load_preferences(path: str) -> List[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_report(data_dir: str) -> str:
    rubric = load_rubric(os.path.join(data_dir, "rubric.json"))
    rows = load_ratings(os.path.join(data_dir, "ratings.csv"), rubric)
    prefs = load_preferences(os.path.join(data_dir, "preferences.csv"))
    prompts = {p["id"]: p for p in json.load(open(os.path.join(data_dir, "prompts.json"), encoding="utf-8"))}

    per: Dict[tuple, List[float]] = defaultdict(list)
    for r in rows:
        per[(r["prompt_id"], r["response_id"])].append(r["score"])

    out = ["# Model Response Evaluation Report", "",
           f"Rubric: **{rubric.name}** ({rubric.min_score}-{rubric.max_score} scale, weighted to 0-100)", "",
           "## 1. Average score per prompt", "",
           "| Prompt | Response A | Response B | Better |", "|---|---|---|---|"]
    for pid in sorted(prompts):
        a, b = mean(per[(pid, "A")]), mean(per[(pid, "B")])
        out.append(f"| {pid}: {prompts[pid]['prompt'][:60]} | {a:.1f} | {b:.1f} | {'A' if a > b else 'B' if b > a else 'tie'} |")

    all_a = [s for (p, r), v in per.items() if r == "A" for s in v]
    all_b = [s for (p, r), v in per.items() if r == "B" for s in v]
    out += ["", f"Overall mean: **A {mean(all_a):.1f}** vs **B {mean(all_b):.1f}**", "",
            "## 2. Preference win rates (pairwise)", ""]
    w = win_rates([p["preferred"] for p in prefs])
    out.append(f"A: {w['A']:.0%} | B: {w['B']:.0%} (ties count as half)")

    out += ["", "## 3. Annotator agreement", ""]
    by_annot: Dict[str, Dict[tuple, float]] = defaultdict(dict)
    for r in rows:
        by_annot[r["annotator"]][(r["prompt_id"], r["response_id"])] = r["score"]
    names = sorted(by_annot)
    if len(names) >= 2:
        keys = sorted(set(by_annot[names[0]]) & set(by_annot[names[1]]))
        mad = mean_absolute_difference([by_annot[names[0]][k] for k in keys], [by_annot[names[1]][k] for k in keys])
        out.append(f"- Mean absolute score difference between {names[0]} and {names[1]}: **{mad:.1f} points** (0-100)")
        pa = {p["prompt_id"]: p["preferred"] for p in prefs if p["annotator"] == names[0]}
        pb = {p["prompt_id"]: p["preferred"] for p in prefs if p["annotator"] == names[1]}
        shared = sorted(set(pa) & set(pb))
        kappa = cohens_kappa([pa[k] for k in shared], [pb[k] for k in shared])
        agree = sum(pa[k] == pb[k] for k in shared) / len(shared)
        out.append(f"- Raw agreement on preferences: **{agree:.0%}** | Cohen's kappa: **{kappa:.2f}** (kappa is pulled down when almost every label is the same class)")
        out += ["", "### Items to adjudicate (annotators disagree)", "", "| Prompt | " + names[0] + " | " + names[1] + " |", "|---|---|---|"]
        diffs = [k for k in shared if pa[k] != pb[k]]
        out += [f"| {k} | {pa[k]} | {pb[k]} |" for k in diffs] or ["| none | | |"]

    out += ["", "## 4. Consistency check: preference vs own rubric scores", ""]
    flags = find_inconsistencies(rows, prefs)
    out += ["| Prompt | Annotator | Preferred | Own scores (A / B) |", "|---|---|---|---|"]
    out += [f"| {f['prompt_id']} | {f['annotator']} | {f['preferred']} | {f['a']:.1f} / {f['b']:.1f} |" for f in flags] or ["| none | | | |"]

    out += ["", "## 5. Weakest criteria for response B", "", "| Criterion | Mean rating |", "|---|---|"]
    for c in rubric.ids:
        vals = [r["ratings"][c] for r in rows if r["response_id"] == "B"]
        out.append(f"| {c} | {mean(vals):.2f} |")
    return "\n".join(out) + "\n"


def find_inconsistencies(rows: List[dict], prefs: List[dict], gap_for_tie: float = 15.0, gap_for_pick: float = 5.0) -> List[dict]:
    """Flag judgements that contradict the same annotator's rubric scores (a common annotation-quality check)."""
    score = {(r["annotator"], r["prompt_id"], r["response_id"]): r["score"] for r in rows}
    flags = []
    for p in prefs:
        a = score.get((p["annotator"], p["prompt_id"], "A"))
        b = score.get((p["annotator"], p["prompt_id"], "B"))
        if a is None or b is None:
            continue
        pick = p["preferred"]
        bad = ((pick == "A" and b - a > gap_for_pick) or (pick == "B" and a - b > gap_for_pick)
               or (pick == "tie" and abs(a - b) > gap_for_tie))
        if bad:
            flags.append({"prompt_id": p["prompt_id"], "annotator": p["annotator"], "preferred": pick, "a": a, "b": b})
    return flags
