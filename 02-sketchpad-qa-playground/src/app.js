import { createCore, parseBugs } from "./core.js";

const bugs = parseBugs(location.search);
const core = createCore({ bugs });
const doc = core.createDocument();

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const $ = (id) => document.getElementById(id);
const state = { tool: "pen", color: "#d62828", size: 6, drawing: null };

if (bugs.length) {
  const b = $("bug-banner");
  b.hidden = false;
  b.textContent = `Seeded defects active: ${bugs.join(", ")}`;
}
if (bugs.includes("BUG-005")) $("size").min = "0"; // seeded: slider allows 0

function paintShape(c, s) {
  c.save();
  c.lineCap = "round"; c.lineJoin = "round";
  c.lineWidth = s.size; c.strokeStyle = s.color;
  if (s.type === "erase") { c.globalCompositeOperation = "destination-out"; c.strokeStyle = "#000"; }
  if (s.type === "pen" || s.type === "erase") {
    c.beginPath();
    s.points.forEach(([x, y], i) => (i ? c.lineTo(x, y) : c.moveTo(x, y)));
    if (s.points.length === 1) c.lineTo(s.points[0][0] + 0.01, s.points[0][1]);
    c.stroke();
  } else if (s.type === "rect") {
    c.strokeRect(s.x, s.y, s.w, s.h);
  } else if (s.type === "ellipse") {
    c.beginPath();
    c.ellipse(s.x + s.w / 2, s.y + s.h / 2, Math.abs(s.w / 2), Math.abs(s.h / 2), 0, 0, Math.PI * 2);
    c.stroke();
  }
  c.restore();
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  doc.shapes.forEach((s) => paintShape(ctx, s));
  if (state.drawing) paintShape(ctx, state.drawing.preview());
  $("undo").disabled = !doc.canUndo;
  $("redo").disabled = !doc.canRedo;
  $("status").textContent = `${doc.shapes.length} object${doc.shapes.length === 1 ? "" : "s"} | Tool: ${state.tool} | Size: ${state.size}`;
}

function pos(e) {
  const r = canvas.getBoundingClientRect();
  return [((e.clientX - r.left) * canvas.width) / r.width, ((e.clientY - r.top) * canvas.height) / r.height];
}

canvas.addEventListener("pointerdown", (e) => {
  canvas.setPointerCapture(e.pointerId);
  const start = pos(e);
  const tool = state.tool, color = state.color;
  const size = tool === "erase" ? core.eraserSize(state.size) : state.size;
  if (tool === "pen" || tool === "erase") {
    const points = [start];
    state.drawing = {
      move: (p) => points.push(p),
      preview: () => ({ type: tool, color, size, points }),
      finish: () => ({ type: tool, color, size, points }),
    };
  } else {
    let end = start;
    state.drawing = {
      move: (p) => (end = p),
      preview: () => ({ type: tool, color, size, ...core.normalizeRect(start[0], start[1], end[0], end[1]) }),
      finish: () => {
        const s = { type: tool, color, size, ...core.normalizeRect(start[0], start[1], end[0], end[1]) };
        return core.isDrawable(s) ? s : null;
      },
    };
  }
  render();
});
canvas.addEventListener("pointermove", (e) => { if (state.drawing) { state.drawing.move(pos(e)); render(); } });
function endDraw() {
  if (!state.drawing) return;
  const shape = state.drawing.finish();
  state.drawing = null;
  if (shape) doc.addShape(shape);
  render();
}
canvas.addEventListener("pointerup", endDraw);
canvas.addEventListener("pointercancel", endDraw);

document.querySelectorAll(".tool").forEach((b) =>
  b.addEventListener("click", () => {
    state.tool = b.dataset.tool;
    document.querySelectorAll(".tool").forEach((x) => {
      x.classList.toggle("active", x === b);
      x.setAttribute("aria-pressed", String(x === b));
    });
    render();
  })
);
$("color").addEventListener("input", (e) => (state.color = e.target.value));
$("size").addEventListener("input", (e) => {
  state.size = core.clampBrushSize(e.target.value);
  $("size-out").textContent = state.size;
  render();
});
$("undo").addEventListener("click", () => { doc.undo(); render(); });
$("redo").addEventListener("click", () => { doc.redo(); render(); });
$("clear").addEventListener("click", () => { doc.clear(); render(); });
$("export").addEventListener("click", () => {
  const out = document.createElement("canvas");
  out.width = canvas.width; out.height = canvas.height;
  const c = out.getContext("2d");
  const opts = core.exportOptions();
  if (opts.fillBackground) { c.fillStyle = opts.background; c.fillRect(0, 0, out.width, out.height); }
  doc.shapes.forEach((s) => paintShape(c, s));
  const a = document.createElement("a");
  a.download = "sketch.png";
  a.href = out.toDataURL("image/png");
  a.click();
  $("status").textContent = "Exported sketch.png";
});

const keys = { p: "pen", r: "rect", o: "ellipse", e: "erase" };
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT") return;
  const mod = e.ctrlKey || e.metaKey;
  if (mod && e.key.toLowerCase() === "z") { e.preventDefault(); (e.shiftKey ? doc.redo() : doc.undo()); render(); return; }
  if (!mod && keys[e.key.toLowerCase()]) document.querySelector(`[data-tool="${keys[e.key.toLowerCase()]}"]`).click();
});

// Exposed for automated tests
window.__sketchpad = { doc, core, state, bugs };
render();
