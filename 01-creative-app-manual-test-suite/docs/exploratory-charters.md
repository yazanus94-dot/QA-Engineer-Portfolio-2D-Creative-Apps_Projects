# Exploratory Testing Charters

Each charter is a time-boxed session (45-60 minutes). Record notes, defects found, questions raised and areas not covered.

## Charter format
**Explore** <area> **with** <technique/data> **to discover** <risk or information>.

---

### EC-01 Undo/redo and state integrity
**Explore** undo/redo **with** long mixed sequences (draw, move, delete, clear, layer changes) **to discover** lost or duplicated objects and inconsistent redo behavior.
Ideas: undo past a clear; redo after a new action; undo while a drag is in progress; reopen a saved file and undo.

### EC-02 Designer workflow: logo from scratch
**Explore** the full workflow of building a logo (shapes, text, align, group, export) **to discover** friction, wrong rendering and broken transforms.
Ideas: draw shapes in every direction; rotate then resize; group and scale; export at 2x.

### EC-03 Layer stacking and visibility
**Explore** layers **with** hidden, locked, reordered and blended layers **to discover** mismatches between the panel, the canvas and exports.
Ideas: export with a hidden layer; draw on a locked layer; merge layers with different opacity.

### EC-04 Extreme values
**Explore** numeric inputs and sliders **with** minimum, maximum, zero, negative and non-numeric values **to discover** unhandled boundaries.
Ideas: brush size 0 or 1000; opacity -5; zoom 1% and 6400%; document size 1x1 and above the limit.

### EC-05 Text and internationalisation
**Explore** the text tool **with** Arabic, mixed RTL/LTR, emoji, long strings and missing fonts **to discover** shaping, direction and overflow defects.

### EC-06 Export fidelity
**Explore** PNG/JPG/SVG/PDF export **with** transparency, gradients, text and many layers **to discover** any difference between canvas and output file.
Ideas: open the exported file in another viewer; sample pixel colors; check transparent vs solid background.
