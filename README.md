# QA Engineer Portfolio — 2D Creative Apps

[![Tests](https://github.com/yazanus94-dot/QA-Engineer-Portfolio-2D-Creative-Apps_Projects/actions/workflows/ci.yml/badge.svg)](https://github.com/yazanus94-dot/QA-Engineer-Portfolio-2D-Creative-Apps_Projects/actions/workflows/ci.yml)
![Node 20+](https://img.shields.io/badge/node-20%2B-green)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A QA engineering portfolio focused on **2D/creative applications**, covering
the full loop: test design → exploratory execution → defect reporting →
automation → visual regression → AI-output evaluation.

| # | Project | Role | Validation |
|---|---------|------|------------|
| 1 | [creative-app-manual-test-suite](01-creative-app-manual-test-suite/) | **Test design** — a complete manual QA package for a 2D design/illustration app: test plan, **57 test cases** (priority, type, steps, expected results), 6 exploratory charters, bug/execution report templates | `validate_suite.py` in CI: CSV structure, unique IDs, and **full bidirectional requirements traceability** (12 requirements) |
| 2 | [sketchpad-qa-playground](02-sketchpad-qa-playground/) | **Defects + automation** — a real 2D drawing web app (pen, shapes, eraser, undo/redo, PNG export) with **6 seeded, switchable defects** (`?bug=1`…), plus 6 written bug reports | **15 unit tests** (node:test) + **9 Playwright e2e tests** (Chromium) against the running app |
| 3 | [visual-regression-toolkit](03-visual-regression-toolkit/) | **Visual QA** — pixel-level comparison of baseline vs new screenshots across all RGBA channels, per-channel tolerance, allowed-diff %, ignore regions, red-highlight diff images, bounding box, HTML report | **15 tests**; CLI with CI-friendly exit codes (1 = regression found — demonstrated by the seeded sample defect) |
| 4 | [ai-output-evaluation-framework](04-ai-output-evaluation-framework/) | **AI-output QA** — weighted rubric scoring (0–100), pairwise preference win rates, inter-annotator agreement (Cohen's kappa), inconsistent-judgement detection | **13 tests**; report generator with strict input validation |

## What the portfolio demonstrates

- **Traceability as a discipline.** Requirements ↔ test cases are checked by
  code in CI, not maintained by hope.
- **Finding real bugs.** The sketchpad's seeded defects include brush-size
  zero crashes, eraser no-ops, undo corruption and export failures — each
  documented as a written bug report before being automated.
- **"It looks different" is measurable.** The VRT turns subjective visual
  judgement into diff percentages, tolerances and review artifacts.
- **Evaluating AI output like a QA professional.** Rubrics, agreement
  statistics and consistency checks — not vibes.

## Quick start

```bash
# 1. Manual suite (docs + traceability validation)
cd 01-creative-app-manual-test-suite && python validate_suite.py

# 2. Sketchpad app + tests (Node 20+)
cd ../02-sketchpad-qa-playground
npm install && npm start                 # app at http://localhost:4173
npm test                                 # 15 unit tests
npx playwright install chromium && npm run test:e2e   # 9 e2e tests

# 3. Visual regression toolkit
cd ../03-visual-regression-toolkit && pip install -r requirements.txt
python -m pytest -q
python -m vrt samples/baseline samples/actual --out report   # exit 1: seeded regression found

# 4. AI output evaluation framework
cd ../04-ai-output-evaluation-framework && pip install -r requirements.txt
python -m pytest -q
python -m evaluator                      # writes reports/
```

CI runs everything on Python 3.11/3.12/3.13 and Node 20, including the
Playwright Chromium e2e suite.

## Scope

Self-directed QA portfolio by Yazan Aljabari. The sketchpad is a training
target with intentional defects, not production software; the AI-evaluation
data is synthetic. Everything is reproducible from the commands above.

## License

MIT, see [LICENSE](LICENSE).
