// Sketchpad core logic (pure functions, no DOM) so it can be unit-tested.
//
// QA PLAYGROUND: pass a list of bug ids to createCore({ bugs: [...] }) to switch
// on seeded defects. In the browser use  ?bugs=all  or  ?bugs=BUG-001,BUG-004
export const ALL_BUGS = ["BUG-001", "BUG-002", "BUG-003", "BUG-004", "BUG-005", "BUG-006"];

export function createCore({ bugs = [] } = {}) {
  const has = (id) => bugs.includes(id);

  // Shapes drawn right-to-left or bottom-to-top must still produce a rectangle.
  function normalizeRect(x0, y0, x1, y1) {
    if (has("BUG-002")) return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 }; // seeded: no normalisation
    return { x: Math.min(x0, x1), y: Math.min(y0, y1), w: Math.abs(x1 - x0), h: Math.abs(y1 - y0) };
  }

  // A shape is kept only if it has a visible size.
  function isDrawable(rect) {
    return rect.w > 0 && rect.h > 0;
  }

  // Brush size slider: 1..50
  function clampBrushSize(n) {
    const min = has("BUG-005") ? 0 : 1; // seeded: allows an invisible 0 px brush
    const v = Number.isFinite(Number(n)) ? Number(n) : min;
    return Math.min(50, Math.max(min, Math.round(v)));
  }

  // The eraser is twice as wide as the brush size shown in the UI.
  function eraserSize(brushSize) {
    if (has("BUG-004")) return 5; // seeded: ignores the size slider
    return clampBrushSize(brushSize) * 2;
  }

  // PNG export options: the exported image must have a white background.
  function exportOptions() {
    return { fillBackground: !has("BUG-003"), background: "#ffffff" };
  }

  // Document with snapshot-based undo/redo.
  function createDocument() {
    let shapes = [];
    let undoStack = [];
    let redoStack = [];
    const snap = () => JSON.parse(JSON.stringify(shapes));

    return {
      get shapes() { return shapes; },
      get canUndo() { return undoStack.length > 0; },
      get canRedo() { return redoStack.length > 0; },
      addShape(shape) {
        undoStack.push(snap());
        if (!has("BUG-006")) redoStack = []; // seeded: redo stack survives a new action
        shapes = [...shapes, shape];
      },
      clear() {
        if (!has("BUG-001")) undoStack.push(snap()); // seeded: Clear is not recorded in history
        redoStack = [];
        shapes = [];
      },
      undo() {
        if (!undoStack.length) return false;
        redoStack.push(snap());
        shapes = undoStack.pop();
        return true;
      },
      redo() {
        if (!redoStack.length) return false;
        undoStack.push(snap());
        shapes = redoStack.pop();
        return true;
      },
    };
  }

  return { normalizeRect, isDrawable, clampBrushSize, eraserSize, exportOptions, createDocument };
}

export function parseBugs(search) {
  const v = new URLSearchParams(search).get("bugs");
  if (!v) return [];
  if (v === "all") return [...ALL_BUGS];
  return v.split(",").map((s) => s.trim().toUpperCase()).filter((id) => ALL_BUGS.includes(id));
}
