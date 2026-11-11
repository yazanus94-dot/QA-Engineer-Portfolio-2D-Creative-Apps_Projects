"""Validate the manual test suite package: CSV structure and traceability."""
import csv
import sys

CASES = "test-cases.csv"
TRACE = "requirements-traceability.csv"


def main() -> int:
    problems = []

    with open(CASES, newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))
    with open(TRACE, newline="", encoding="utf-8") as f:
        reqs = list(csv.DictReader(f))

    if not cases:
        problems.append("no test cases found")
    if not reqs:
        problems.append("no requirements found")

    case_fields = set(cases[0]) if cases else set()
    for needed in ("Test ID", "Priority", "Type", "Steps", "Expected Result", "Requirement"):
        if cases and needed not in case_fields:
            problems.append(f"test-cases.csv missing column: {needed}")

    req_ids = {r["Requirement"].strip() for r in reqs if r.get("Requirement")}
    if len(req_ids) != len(reqs):
        problems.append("duplicate requirement ids in requirements-traceability.csv")

    # every case linked to requirements must reference existing requirements
    linked = set()
    for c in cases:
        raw = (c.get("Requirement") or "").strip()
        if not raw:
            problems.append(f"{c.get('Test ID', '?')} has no requirement link")
            continue
        for rid in raw.replace(";", ",").split(","):
            rid = rid.strip()
            if rid and rid not in req_ids:
                problems.append(f"{c.get('Test ID', '?')} links unknown requirement {rid}")
            elif rid:
                linked.add(rid)

    # every requirement must be covered by at least one case
    uncovered = req_ids - linked
    if uncovered:
        problems.append(f"requirements never linked from a case: {sorted(uncovered)}")

    # duplicate case ids
    case_ids = [c.get("Test ID", "").strip() for c in cases]
    if len(set(case_ids)) != len(case_ids):
        problems.append("duplicate test ids in test-cases.csv")

    if problems:
        print(f"INVALID: {len(problems)} problem(s)")
        for p in problems:
            print(" -", p)
        return 1
    print(f"OK: {len(cases)} test cases, {len(req_ids)} requirements, full bidirectional traceability")
    return 0


if __name__ == "__main__":
    sys.exit(main())
