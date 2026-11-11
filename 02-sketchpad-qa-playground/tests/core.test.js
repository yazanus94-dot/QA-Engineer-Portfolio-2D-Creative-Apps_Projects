// Run with: npm test   (Node 18+, no dependencies)
import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { createCore, parseBugs, ALL_BUGS } from "../src/core.js";

const clean = createCore();

describe("Correct behaviour (no seeded defects)", () => {
  test("normalizeRect handles all four drag directions", () => {
    const expected = { x: 10, y: 20, w: 100, h: 50 };
    assert.deepEqual(clean.normalizeRect(10, 20, 110, 70), expected); // down-right
    assert.deepEqual(clean.normalizeRect(110, 70, 10, 20), expected); // up-left
    assert.deepEqual(clean.normalizeRect(110, 20, 10, 70), expected); // down-left
    assert.deepEqual(clean.normalizeRect(10, 70, 110, 20), expected); // up-right
  });

  test("zero-size drag is not drawable", () => {
    assert.equal(clean.isDrawable(clean.normalizeRect(5, 5, 5, 5)), false);
    assert.equal(clean.isDrawable(clean.normalizeRect(5, 5, 6, 6)), true);
  });

  test("brush size is clamped to 1..50 and non-numbers are handled", () => {
    assert.equal(clean.clampBrushSize(0), 1);
    assert.equal(clean.clampBrushSize(-10), 1);
    assert.equal(clean.clampBrushSize(999), 50);
    assert.equal(clean.clampBrushSize("abc"), 1);
    assert.equal(clean.clampBrushSize(12.6), 13);
  });

  test("eraser is twice the brush size", () => {
    assert.equal(clean.eraserSize(5), 10);
    assert.equal(clean.eraserSize(50), 100);
  });

  test("export fills a white background", () => {
    assert.deepEqual(clean.exportOptions(), { fillBackground: true, background: "#ffffff" });
  });

  test("undo and redo walk through history", () => {
    const d = clean.createDocument();
    d.addShape({ id: 1 }); d.addShape({ id: 2 });
    assert.equal(d.shapes.length, 2);
    d.undo(); assert.equal(d.shapes.length, 1);
    d.undo(); assert.equal(d.shapes.length, 0);
    assert.equal(d.undo(), false);
    d.redo(); d.redo();
    assert.equal(d.shapes.length, 2);
    assert.equal(d.redo(), false);
  });

  test("a new action clears the redo stack", () => {
    const d = clean.createDocument();
    d.addShape({ id: 1 }); d.addShape({ id: 2 });
    d.undo();
    d.addShape({ id: 3 });
    assert.equal(d.canRedo, false);
    assert.deepEqual(d.shapes.map((s) => s.id), [1, 3]);
  });

  test("undo after Clear restores every object", () => {
    const d = clean.createDocument();
    d.addShape({ id: 1 }); d.addShape({ id: 2 });
    d.clear();
    assert.equal(d.shapes.length, 0);
    d.undo();
    assert.deepEqual(d.shapes.map((s) => s.id), [1, 2]);
  });
});

describe("Seeded defects reproduce (regression guards for the bug reports)", () => {
  test("BUG-001: Clear is not recorded, undo restores the wrong state", () => {
    const d = createCore({ bugs: ["BUG-001"] }).createDocument();
    d.addShape({ id: 1 }); d.addShape({ id: 2 });
    d.clear();
    d.undo();
    assert.deepEqual(d.shapes.map((s) => s.id), [1]); // expected [1, 2]
  });

  test("BUG-002: rectangle dragged up/left has negative size and is dropped", () => {
    const c = createCore({ bugs: ["BUG-002"] });
    const r = c.normalizeRect(110, 70, 10, 20);
    assert.ok(r.w < 0 && r.h < 0);
    assert.equal(c.isDrawable(r), false);
  });

  test("BUG-003: export has no background fill", () => {
    assert.equal(createCore({ bugs: ["BUG-003"] }).exportOptions().fillBackground, false);
  });

  test("BUG-004: eraser ignores the size slider", () => {
    const c = createCore({ bugs: ["BUG-004"] });
    assert.equal(c.eraserSize(5), c.eraserSize(50));
  });

  test("BUG-005: brush size 0 is accepted (invisible stroke)", () => {
    assert.equal(createCore({ bugs: ["BUG-005"] }).clampBrushSize(0), 0);
  });

  test("BUG-006: redo is still available after a new action", () => {
    const d = createCore({ bugs: ["BUG-006"] }).createDocument();
    d.addShape({ id: 1 }); d.addShape({ id: 2 });
    d.undo();
    d.addShape({ id: 3 });
    assert.equal(d.canRedo, true); // expected false
  });
});

describe("URL parsing", () => {
  test("parseBugs supports all, lists, and ignores unknown ids", () => {
    assert.deepEqual(parseBugs(""), []);
    assert.deepEqual(parseBugs("?bugs=all"), ALL_BUGS);
    assert.deepEqual(parseBugs("?bugs=bug-001, BUG-004,NOPE"), ["BUG-001", "BUG-004"]);
  });
});
