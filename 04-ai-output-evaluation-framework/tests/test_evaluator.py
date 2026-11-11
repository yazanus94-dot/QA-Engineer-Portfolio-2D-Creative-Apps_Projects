import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from evaluator import cohens_kappa, load_rubric, mean_absolute_difference, weighted_score, win_rates  # noqa: E402
from evaluator.report import build_report, find_inconsistencies, load_ratings  # noqa: E402

RUBRIC = load_rubric(os.path.join(ROOT, "data", "rubric.json"))


def raises(fn, *a, **k):
    try:
        fn(*a, **k)
    except ValueError:
        return True
    return False


def test_rubric_weights_sum_to_one_and_ids_are_unique():
    assert abs(sum(c.weight for c in RUBRIC.criteria) - 1.0) < 1e-9
    assert len(set(RUBRIC.ids)) == 5


def test_weighted_score_extremes():
    assert weighted_score({c: 5 for c in RUBRIC.ids}, RUBRIC) == 100.0
    assert weighted_score({c: 1 for c in RUBRIC.ids}, RUBRIC) == 0.0
    assert weighted_score({c: 3 for c in RUBRIC.ids}, RUBRIC) == 50.0


def test_weighted_score_respects_weights():
    only_accuracy = {c: 1 for c in RUBRIC.ids}; only_accuracy["accuracy"] = 5
    assert weighted_score(only_accuracy, RUBRIC) == 35.0


def test_weighted_score_validates_input():
    good = {c: 4 for c in RUBRIC.ids}
    assert raises(weighted_score, {k: v for k, v in good.items() if k != "safety"}, RUBRIC)
    assert raises(weighted_score, {**good, "accuracy": 6}, RUBRIC)
    assert raises(weighted_score, {**good, "accuracy": 0}, RUBRIC)
    assert raises(weighted_score, {**good, "extra": 3}, RUBRIC)


def test_bad_rubric_weights_are_rejected():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.json")
        json.dump({"scale": {"min": 1, "max": 5}, "criteria": [{"id": "a", "weight": 0.5}, {"id": "b", "weight": 0.2}]}, open(p, "w"))
        assert raises(load_rubric, p)


def test_kappa_known_values():
    assert cohens_kappa(["A", "A", "B", "B"], ["A", "A", "B", "B"]) == 1.0
    assert cohens_kappa(["A", "B", "A", "B"], ["B", "A", "B", "A"]) == -1.0
    assert abs(cohens_kappa(["A", "A", "B", "B"], ["A", "B", "A", "B"])) < 1e-9  # agreement at chance level
    assert cohens_kappa(["A", "A"], ["A", "A"]) == 1.0  # degenerate case must not divide by zero


def test_kappa_requires_matching_lengths():
    assert raises(cohens_kappa, ["A"], ["A", "B"])
    assert raises(cohens_kappa, [], [])


def test_win_rates_and_ties():
    assert win_rates(["A", "A", "B", "A"]) == {"A": 0.75, "B": 0.25}
    assert win_rates(["A", "tie"]) == {"A": 0.75, "B": 0.25}
    assert raises(win_rates, ["A", "C"])
    assert raises(win_rates, [])


def test_mean_absolute_difference():
    assert mean_absolute_difference([10, 20], [12, 17]) == 2.5


def test_sample_data_loads_and_scores_in_range():
    rows = load_ratings(os.path.join(ROOT, "data", "ratings.csv"), RUBRIC)
    assert len(rows) == 32
    assert all(0 <= r["score"] <= 100 for r in rows)


def test_report_contains_all_sections_and_picks_a_over_b():
    report = build_report(os.path.join(ROOT, "data"))
    for heading in ("Average score per prompt", "Preference win rates", "Annotator agreement", "Weakest criteria"):
        assert heading in report
    assert "Overall mean: **A" in report
    a = float(report.split("Overall mean: **A ")[1].split("**")[0])
    b = float(report.split("vs **B ")[1].split("**")[0])
    assert a > b


def test_load_ratings_reports_the_bad_line():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.csv")
        open(p, "w").write("prompt_id,response_id,annotator,accuracy,instruction_following,completeness,clarity,safety\nP1,A,x,5,5,five,5,5\n")
        try:
            load_ratings(p, RUBRIC)
        except ValueError as e:
            assert "line 2" in str(e)
        else:
            raise AssertionError("expected ValueError")


def test_inconsistency_check_flags_contradicting_preferences():
    rows = [
        {"annotator": "x", "prompt_id": "P1", "response_id": "A", "score": 90},
        {"annotator": "x", "prompt_id": "P1", "response_id": "B", "score": 30},
        {"annotator": "x", "prompt_id": "P2", "response_id": "A", "score": 80},
        {"annotator": "x", "prompt_id": "P2", "response_id": "B", "score": 78},
    ]
    prefs = [
        {"prompt_id": "P1", "annotator": "x", "preferred": "B"},    # contradicts own scores
        {"prompt_id": "P2", "annotator": "x", "preferred": "tie"},  # close scores: fine
    ]
    flags = find_inconsistencies(rows, prefs)
    assert [f["prompt_id"] for f in flags] == ["P1"]
    assert find_inconsistencies(rows, [{"prompt_id": "P1", "annotator": "x", "preferred": "A"}]) == []
    assert [f["prompt_id"] for f in find_inconsistencies(rows, [{"prompt_id": "P1", "annotator": "x", "preferred": "tie"}])] == ["P1"]
