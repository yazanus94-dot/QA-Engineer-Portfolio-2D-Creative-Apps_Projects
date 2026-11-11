# Creative App Manual Test Suite

A complete manual QA package for testing a **2D design / illustration web application** (vector editor, drawing tools, layers, text, export), in the style used on real creative-software projects.

## What is inside
| File | Description |
|---|---|
| `docs/test-plan.md` | Scope, approach, environments, entry/exit criteria, severity, risks |
| `test-cases.csv` | **57 test cases** with priority, type, preconditions, steps, expected results and requirement links |
| `requirements-traceability.csv` | 12 requirements mapped to test cases |
| `docs/exploratory-charters.md` | 6 time-boxed exploratory charters for designer workflows |
| `docs/bug-report-template.md` | Bug report template: steps, expected, actual, evidence |
| `docs/execution-report-template.md` | Execution summary template |

## Coverage
Document management, drawing tools, shapes (all drag directions), selection and transforms, layers and blend modes, color/alpha, text (Unicode and Arabic RTL), undo/redo, zoom/pan, import/export fidelity, accessibility, performance and cross-browser/HiDPI/touch.

## How to use
1. Open `test-cases.csv` in Excel or Google Sheets.
2. Run the cases against any 2D editor (for example Excalidraw, Photopea, Figma or your own build).
3. Update the **Status** column (Pass / Fail / Blocked) and link defects in **Defect ID**.
4. Report issues using `docs/bug-report-template.md`.

See the companion project **Sketchpad QA Playground** for real bug reports written against a demo drawing app.

## Author
Yazan Aljabari - QA Engineer
