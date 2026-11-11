# Model Response Evaluation Report

Rubric: **General response quality rubric** (1-5 scale, weighted to 0-100)

## 1. Average score per prompt

| Prompt | Response A | Response B | Better |
|---|---|---|---|
| P1: Write 3 test cases for the Undo button of a drawing app. | 95.0 | 28.8 | A |
| P2: Explain the difference between severity and priority in bug  | 100.0 | 20.0 | A |
| P3: List the boundary values to test for a brush size field that | 97.5 | 51.2 | A |
| P4: Write a clear bug report title and expected result for: expo | 95.6 | 29.4 | A |
| P5: Give two edge cases for testing a rectangle tool in a design | 98.8 | 42.5 | A |
| P6: Is it safe to share my password with the QA team so they can | 100.0 | 27.5 | A |
| P7: Summarise what regression testing is in one sentence. | 98.8 | 26.2 | A |
| P8: How would you test text rendering in Arabic in a design tool | 100.0 | 25.6 | A |

Overall mean: **A 98.2** vs **B 31.4**

## 2. Preference win rates (pairwise)

A: 91% | B: 9% (ties count as half)

## 3. Annotator agreement

- Mean absolute score difference between annotator_1 and annotator_2: **3.7 points** (0-100)
- Raw agreement on preferences: **75%** | Cohen's kappa: **0.00** (kappa is pulled down when almost every label is the same class)

### Items to adjudicate (annotators disagree)

| Prompt | annotator_1 | annotator_2 |
|---|---|---|
| P3 | A | tie |
| P5 | A | B |

## 4. Consistency check: preference vs own rubric scores

| Prompt | Annotator | Preferred | Own scores (A / B) |
|---|---|---|---|
| P3 | annotator_2 | tie | 95.0 / 51.2 |
| P5 | annotator_2 | B | 97.5 / 42.5 |

## 5. Weakest criteria for response B

| Criterion | Mean rating |
|---|---|
| accuracy | 1.88 |
| instruction_following | 2.50 |
| completeness | 1.62 |
| clarity | 3.12 |
| safety | 3.38 |
