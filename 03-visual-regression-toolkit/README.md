# Visual Regression Toolkit

A small Python tool that compares **baseline** and **new** screenshots pixel by pixel, flags visual regressions in UI and creative applications, and produces a diff image and an HTML report. Built for testing design software, where "it looks different" is a real defect.

## Features
- Pixel comparison across all RGBA channels (alpha differences are caught)
- **Per-channel tolerance** to ignore anti-aliasing and compression noise
- **Allowed difference %** threshold, **ignore regions** (clocks, ads, cursors)
- Detects size mismatches, missing screenshots and new screenshots awaiting approval
- Red-highlight **diff images**, bounding box of the changed area, and an **HTML report** (baseline / actual / diff side by side)
- CLI with CI-friendly exit codes (0 = pass, 1 = regression found)
- 15 automated tests

## Install
```bash
pip install -r requirements.txt
```

## Run the demo
```bash
python samples/generate_samples.py          # regenerate demo screenshots (already included)
python -m vrt samples/baseline samples/actual --tolerance 8 --max-diff 0.1
```
Expected demo result:
| Image | Result | Why |
|---|---|---|
| logo.png | PASS | Identical |
| card.png | PASS | Tiny noise inside tolerance |
| button.png | FAIL | Button color changed |
| title.png | FAIL | Title moved 10 px (layout shift) |
| banner.png | FAIL | Size mismatch (420 vs 400 px wide) |
| footer.png | FAIL | Screenshot missing from the actual run |

Open `report/report.html` to see baseline, actual and diff images.

## Use as a library
```python
from vrt import compare_images

result = compare_images("baseline.png", "actual.png", channel_tolerance=5, max_diff_percent=0.05,
                        ignore_regions=[(0, 0, 200, 40)])
print(result.summary())      # PASS 0/104000 pixels differ (0.000%), max channel delta 0
assert result.passed
```

## Project layout
| Path | Purpose |
|---|---|
| `vrt/compare.py` | Comparison engine and diff image |
| `vrt/runner.py` | Folder comparison and HTML report |
| `vrt/__main__.py` | Command line interface |
| `samples/` | Demo baseline and actual screenshots plus generator |
| `tests/` | pytest tests |

## Run the tests
```bash
pytest -q
```

## Skills demonstrated
Visual testing, Python, Pillow/NumPy, test automation design, tolerance and boundary handling, CI exit codes, reporting.

## Author
Yazan Aljabari - QA Engineer
