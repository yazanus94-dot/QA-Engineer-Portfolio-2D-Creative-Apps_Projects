# AI Output Evaluation Framework

A small Python framework for **evaluating AI model responses**, the core of RLHF and model-evaluation work: score responses against a weighted rubric, compare pairs of responses, measure annotator agreement and catch inconsistent judgements.

> All prompts, responses and ratings in `data/` are **synthetic sample data** created for this demonstration.

## What it does
| Capability | Where |
|---|---|
| Weighted rubric scoring (accuracy, instruction following, completeness, clarity, safety) to a 0-100 score, with strict input validation | `evaluator/rubric.py` |
| Pairwise preference win rates (ties count as half) | `evaluator/metrics.py` |
| Inter-annotator agreement: Cohen's kappa, raw agreement, mean score difference | `evaluator/metrics.py` |
| **Consistency check**: flags preferences that contradict the same annotator's own rubric scores | `evaluator/report.py` |
| Markdown evaluation report with items to adjudicate | `python -m evaluator` |
| 13 automated tests (known kappa values, validation, report content) | `tests/` |

## Run it
```bash
python -m evaluator data --out reports/sample_report.md
pytest -q
```
`reports/sample_report.md` is a ready-made example of the output.

## Data files
| File | Content |
|---|---|
| `data/rubric.json` | Criteria, weights and a 1-5 scale guide |
| `data/prompts.json` | 8 QA/creative-tool prompts, each with Response A and B |
| `data/ratings.csv` | Two annotators rating every response on every criterion |
| `data/preferences.csv` | Which response each annotator preferred (A, B or tie) |

## Example findings from the sample data
- Response A averages 98.2 and Response B 31.4 on the 0-100 scale.
- Annotators disagree on 2 of 8 preferences (P3, P5); both are flagged for adjudication.
- Annotator 2's preference on P5 contradicts their own scores, so the consistency check lists it for review.

## Annotation guidelines used
1. Judge accuracy first: a confident wrong answer scores lower than a short correct one.
2. Check every explicit instruction (count, format, length) before rating instruction following.
3. Rate each criterion independently, then choose the preference; justify any preference that disagrees with the scores.
4. Safety issues (for example sharing passwords) cap the response at a low safety score regardless of other quality.

## Skills demonstrated
RLHF-style response ranking, rubric design, annotation quality control, inter-annotator agreement, Python, unit testing, technical writing.

## Author
Yazan Aljabari - QA Engineer
