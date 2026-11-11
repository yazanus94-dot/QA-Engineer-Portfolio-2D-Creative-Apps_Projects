# Test Plan: 2D Design / Creative Web Application

## 1. Purpose
Define how a browser-based 2D design and illustration application (vector editor, drawing and animation-style tools) is tested manually, so that defects in real designer workflows are found, reproduced and reported clearly.

## 2. Scope
**In scope:** document management, drawing tools, shapes, selection and transforms, layers, color, text, undo/redo, zoom/pan, import/export, usability and accessibility, performance and cross-browser behavior.
**Out of scope:** server-side sync, billing, third-party plugins, security penetration testing.

## 3. Test objectives
- Verify each requirement in `requirements-traceability.csv` with at least one test case (57 cases, 17 are P1).
- Find visual, functional and usability defects, including edge cases real designers hit.
- Provide reproducible bug reports: steps, expected result, actual result, evidence.

## 4. Test approach
| Technique | Where it is used |
|---|---|
| Scripted functional tests | `test-cases.csv`, executed on every build |
| Exploratory sessions | `exploratory-charters.md` (time-boxed, 45-60 min) |
| Boundary / equivalence analysis | sizes, zoom, opacity, brush size, text length |
| Visual comparison | screenshots against expected rendering, export vs canvas |
| Regression | all P1 cases + any case linked to a fixed defect |
| Compatibility | Chrome, Firefox, Safari, Edge; 100% and 200% display scaling; touch/stylus |

## 5. Environments
| Item | Detail |
|---|---|
| Browsers | Latest stable Chrome, Firefox, Safari, Edge |
| OS | Windows 11, macOS, iPadOS (touch/stylus) |
| Displays | 1080p at 100%, HiDPI at 200% |
| Tools | JIRA or GitHub Issues, screen recorder, browser DevTools, a pixel-color picker |

## 6. Entry and exit criteria
**Entry:** build deployed, smoke test passes, test data available.
**Exit:** all P1 cases executed; no open Critical/High defects; at least 95% of P2 cases executed; remaining risks documented.

## 7. Severity and priority
| Severity | Definition | Example |
|---|---|---|
| Critical | Crash, data loss, app unusable | Saved file will not reopen |
| High | Core feature wrong, no workaround | Export does not match canvas |
| Medium | Feature wrong, workaround exists | Eraser ignores size slider |
| Low | Cosmetic or minor usability | Misaligned icon |

## 8. Risk assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Rendering differs between browsers | High | High | Run compatibility cases on all four browsers |
| Undo/redo corrupts document state | Medium | High | Dedicated history cases and exploratory charter |
| Export differs from canvas | Medium | High | Compare exports visually and by pixel sampling |
| Performance drops with many objects | Medium | Medium | Performance case with 1,000 objects |
| RTL / Unicode text mis-rendering | Medium | Medium | Arabic and emoji cases |

## 9. Deliverables
Test plan, test cases, traceability matrix, exploratory charters, bug reports, execution summary.

## 10. Defect lifecycle
New -> Triaged -> In Progress -> Fixed -> Retest -> Closed (or Reopened).
