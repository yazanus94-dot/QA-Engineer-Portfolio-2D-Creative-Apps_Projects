// End-to-end tests (Playwright). Install once:  npm install && npx playwright install chromium
// Run:  npm run test:e2e
// Clean build:   /            -> every test should pass
// Seeded build:  /?bugs=all   -> tests tagged @bug fail on purpose and prove each defect
import { test, expect } from "@playwright/test";

async function drag(page, from, to) {
  const box = await page.locator("#canvas").boundingBox();
  await page.mouse.move(box.x + from[0], box.y + from[1]);
  await page.mouse.down();
  await page.mouse.move(box.x + (from[0] + to[0]) / 2, box.y + (from[1] + to[1]) / 2);
  await page.mouse.move(box.x + to[0], box.y + to[1]);
  await page.mouse.up();
}
const count = (page) => page.evaluate(() => window.__sketchpad.doc.shapes.length);

test.describe("Drawing basics", () => {
  test.beforeEach(async ({ page }) => page.goto("/"));

  test("pen draws a stroke and enables Undo", async ({ page }) => {
    await drag(page, [100, 100], [300, 200]);
    expect(await count(page)).toBe(1);
    await expect(page.locator("#undo")).toBeEnabled();
  });

  test("rectangle can be drawn in all four directions", async ({ page }) => {
    await page.click('[data-tool="rect"]');
    await drag(page, [100, 100], [200, 180]);
    await drag(page, [400, 300], [300, 220]);
    await drag(page, [500, 100], [420, 180]);
    await drag(page, [100, 400], [200, 330]);
    expect(await count(page)).toBe(4); // @bug BUG-002 fails on the seeded build
  });

  test("a click without dragging does not create a shape", async ({ page }) => {
    await page.click('[data-tool="rect"]');
    await drag(page, [150, 150], [150, 150]);
    expect(await count(page)).toBe(0);
  });

  test("tool shortcuts switch the active tool", async ({ page }) => {
    await page.keyboard.press("r");
    await expect(page.locator('[data-tool="rect"]')).toHaveAttribute("aria-pressed", "true");
    await page.keyboard.press("e");
    await expect(page.locator('[data-tool="erase"]')).toHaveClass(/active/);
  });
});

test.describe("History", () => {
  test.beforeEach(async ({ page }) => page.goto("/"));

  test("undo then redo restores the shape", async ({ page }) => {
    await drag(page, [100, 100], [300, 200]);
    await page.click("#undo");
    expect(await count(page)).toBe(0);
    await page.click("#redo");
    expect(await count(page)).toBe(1);
  });

  test("redo is disabled after a new action", async ({ page }) => {
    await drag(page, [50, 50], [100, 100]);
    await drag(page, [150, 150], [200, 200]);
    await page.click("#undo");
    await drag(page, [250, 250], [300, 300]);
    await expect(page.locator("#redo")).toBeDisabled(); // @bug BUG-006
  });

  test("Undo after Clear restores all shapes", async ({ page }) => {
    await drag(page, [50, 50], [100, 100]);
    await drag(page, [150, 150], [200, 200]);
    await page.click("#clear");
    expect(await count(page)).toBe(0);
    await page.click("#undo");
    expect(await count(page)).toBe(2); // @bug BUG-001
  });
});

test.describe("Controls and export", () => {
  test.beforeEach(async ({ page }) => page.goto("/"));

  test("brush size slider never goes below 1", async ({ page }) => {
    await page.locator("#size").fill("0");
    expect(await page.evaluate(() => window.__sketchpad.state.size)).toBeGreaterThanOrEqual(1); // @bug BUG-005
  });

  test("exported PNG has an opaque white background", async ({ page }) => {
    await drag(page, [100, 100], [200, 200]);
    // Capture the data URL that Export PNG would download, then read a corner pixel.
    const alpha = await page.evaluate(async () => {
      let href = null;
      const original = HTMLAnchorElement.prototype.click;
      HTMLAnchorElement.prototype.click = function () { href = this.href; };
      document.getElementById("export").click();
      HTMLAnchorElement.prototype.click = original;
      const img = new Image();
      img.src = href;
      await img.decode();
      const c = document.createElement("canvas");
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext("2d");
      ctx.drawImage(img, 0, 0);
      return ctx.getImageData(2, 2, 1, 1).data[3];
    });
    expect(alpha).toBe(255); // @bug BUG-003
  });
});
