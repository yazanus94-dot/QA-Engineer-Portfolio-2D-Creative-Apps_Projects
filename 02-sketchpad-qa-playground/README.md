# Sketchpad QA Playground

A small **2D drawing web app** (pen, rectangle, ellipse, eraser, undo/redo, PNG export) built as a QA practice and demonstration project. Six realistic defects can be switched on from the URL, so you can practise finding, reproducing, reporting and automating tests for the kind of issues found in creative applications.

> The seeded defects are intentional. The app is a training target, not production software.

## Quick start
```bash
node serve.js            # opens at http://localhost:4173  (Node 18+)
```
| URL | Behavior |
|---|---|
| `/` | Clean build, all features correct |
| `/?bugs=all` | All six defects active |
| `/?bugs=BUG-001,BUG-006` | Only selected defects |

## What is in the project
| Path | Description |
|---|---|
| `src/` | The app (HTML, CSS, canvas JavaScript) and `core.js` logic |
| `bug-reports/` | 6 professional bug reports: steps, expected, actual, severity, impact |
| `tests/core.test.js` | Unit tests with Node's built-in runner: correct behavior and a regression guard for every defect |
| `tests/e2e/sketchpad.spec.js` | Playwright UI tests (run against the clean build and `?bugs=all`) |
| `docs/test-charter-and-notes.md` | Exploratory session notes |

## Run the tests
```bash
npm test                                   # unit tests (no install needed)
npm install && npx playwright install chromium
npm run test:e2e                           # UI tests
```

## Seeded defects
| ID | Area | Summary | Severity |
|---|---|---|---|
| BUG-001 | History | Undo after Clear restores wrong state | High |
| BUG-002 | Shapes | Shapes dragged up/left are not created | High |
| BUG-003 | Export | PNG exported with transparent background | Medium |
| BUG-004 | Eraser | Eraser ignores size slider | Medium |
| BUG-005 | Size | Slider accepts 0 and makes invisible strokes | Low |
| BUG-006 | History | Redo not cleared after a new action | High |

## Skills demonstrated
Exploratory testing, boundary-value analysis, bug reporting, regression guards, Playwright UI automation, JavaScript unit testing.

## Author
Yazan Aljabari - QA Engineer
