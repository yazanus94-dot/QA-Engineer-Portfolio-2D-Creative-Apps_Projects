# Exploratory Session Notes: Sketchpad

**Charter:** Explore undo/redo, shapes and export with unusual drag directions and extreme values to discover state and rendering defects.
**Duration:** 60 minutes | **Build:** `?bugs=all` | **Browser:** Chrome latest

## Areas covered
Pen, rectangle, ellipse, eraser, size slider (0, 1, 50), undo/redo sequences, Clear, PNG export.

## Findings
6 defects found and reported (BUG-001 to BUG-006). Highest risk: history handling (BUG-001, BUG-006) because it silently loses work.

## Questions raised
- Should Clear ask for confirmation?
- Should the eraser size be shown in the UI?
- Should export offer a transparent background option?

## Not covered
Touch/stylus input, high zoom levels, very large canvas sizes, accessibility with a screen reader.
