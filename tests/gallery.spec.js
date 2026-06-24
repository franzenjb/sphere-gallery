// @ts-check
const { test, expect } = require("@playwright/test");

async function ready(page) {
  await page.goto("/");
  await page.waitForFunction(() => window.__app && window.__app.ready && window.__app.cards.length > 0);
  await page.waitForTimeout(800);
}

test("loads the Now atlas with one generated placard per bookmark", async ({ page }) => {
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  await ready(page);

  await expect(page.locator("#stage canvas")).toBeVisible();
  await expect(page.locator("#libraryPanel")).toBeVisible();

  const manifest = await page.evaluate(() => fetch("shots/manifest.json").then(r => r.json()));
  const state = await page.evaluate(() => ({
    cards: window.__app.cards.length,
    apps: window.__app.apps.length,
    filtered: window.__app.filtered().length
  }));
  expect(state.cards).toBe(manifest.length);
  expect(state.apps).toBe(manifest.length);
  expect(state.filtered).toBe(manifest.length);
  expect(state.cards).toBeGreaterThan(60);

  const previewSrc = await page.locator("#selectedPreview").getAttribute("src");
  expect(previewSrc).toMatch(/^(data:image|shots\/)/);

  const nonBackgroundSamples = await page.evaluate(() => {
    const { renderer } = window.__app;
    const gl = renderer.getContext();
    const canvas = renderer.domElement;
    const points = [
      [0.28, 0.24], [0.5, 0.24], [0.72, 0.24],
      [0.32, 0.5], [0.5, 0.5], [0.68, 0.5],
      [0.28, 0.76], [0.5, 0.76], [0.72, 0.76]
    ];
    let nonBackground = 0;
    const pixel = new Uint8Array(4);
    for (const [x, y] of points) {
      gl.readPixels(
        Math.floor(canvas.width * x),
        Math.floor(canvas.height * y),
        1,
        1,
        gl.RGBA,
        gl.UNSIGNED_BYTE,
        pixel
      );
      if (pixel[0] + pixel[1] + pixel[2] > 45) nonBackground++;
    }
    return nonBackground;
  });
  expect(nonBackgroundSamples).toBeGreaterThan(2);
  expect(errors).toEqual([]);
});

test("dragging rotates the atlas with eased follow", async ({ page }) => {
  await ready(page);
  const before = await page.evaluate(() => window.__app.rot.yaw);

  await page.mouse.move(700, 420);
  await page.mouse.down();
  for (let i = 1; i <= 10; i++) {
    await page.mouse.move(700 + i * 28, 420, { steps: 2 });
  }
  await page.mouse.up();

  const justAfter = await page.evaluate(() => ({
    yaw: window.__app.rot.yaw,
    target: window.__app.rot.tYaw
  }));
  expect(Math.abs(justAfter.target - before)).toBeGreaterThan(0.25);
  expect(Math.abs(justAfter.target - justAfter.yaw)).toBeGreaterThan(0.01);

  await page.waitForTimeout(1300);
  const settled = await page.evaluate(() => ({
    yaw: window.__app.rot.yaw,
    target: window.__app.rot.tYaw
  }));
  expect(Math.abs(settled.target - settled.yaw)).toBeLessThan(0.04);
});

test("search filters the atlas, board, and bookmark index", async ({ page }) => {
  await ready(page);

  await page.getByLabel("Find bookmark").fill("rapt");
  await page.waitForFunction(() => window.__app.filtered().length === 1);

  const titles = await page.evaluate(() => window.__app.filtered().map(app => app.title));
  expect(titles).toEqual(["RAPT 4 Command Console"]);
  await expect(page.locator(".result-btn")).toHaveCount(1);

  await page.locator(".mode-btn[data-view='board']").click();
  await expect(page.locator("body")).toHaveAttribute("data-view", "board");
  await expect(page.locator(".board-card")).toHaveCount(1);
  await expect(page.locator(".board-card strong")).toHaveText("RAPT 4 Command Console");
});

test("cluster filters and board selection update the detail panel", async ({ page }) => {
  await ready(page);

  await page.locator(".cluster-btn[data-cluster='arcgis']").click();
  await page.waitForFunction(() => window.__app.activeCluster() === "arcgis");
  const filtered = await page.evaluate(() => window.__app.filtered().map(app => app.kind));
  expect(filtered.length).toBeGreaterThan(0);
  expect(new Set(filtered)).toEqual(new Set(["arcgis"]));

  await page.locator(".mode-btn[data-view='board']").click();
  await page.locator(".board-card").first().click();
  const selected = await page.evaluate(() => window.__app.apps[window.__app.selected()]);
  await expect(page.locator("#selectedTitle")).toHaveText(selected.title);
  await expect(page.locator("#selectedLink")).toHaveAttribute("href", selected.url);
});

test("bookmark index is retractable and resizable", async ({ page }) => {
  await ready(page);

  const before = await page.evaluate(() => window.__app.panelWidth());
  const handle = await page.locator("#resizeHandle").boundingBox();
  expect(handle).not.toBeNull();
  await page.mouse.move(handle.x + handle.width / 2, handle.y + 120);
  await page.mouse.down();
  await page.mouse.move(handle.x + handle.width / 2 + 72, handle.y + 120, { steps: 4 });
  await page.mouse.up();

  const after = await page.evaluate(() => window.__app.panelWidth());
  expect(after).toBeGreaterThan(before + 40);

  await page.getByRole("button", { name: "Collapse bookmark index" }).click();
  await expect(page.locator("body")).toHaveAttribute("data-panel", "closed");
  await page.getByRole("button", { name: "Open bookmark index" }).click();
  await expect(page.locator("body")).toHaveAttribute("data-panel", "open");
});

test("text contrast: selected title and open button are readable", async ({ page }) => {
  await ready(page);
  const titleColor = await page.locator("#selectedTitle").evaluate(el => getComputedStyle(el).color);
  const link = await page.locator("#selectedLink").evaluate(el => {
    const s = getComputedStyle(el);
    return { color: s.color, bg: s.backgroundColor };
  });

  expect(titleColor).toBe("rgb(23, 22, 18)");
  expect(link.color).toBe("rgb(255, 250, 240)");
  expect(link.bg).toBe("rgb(212, 70, 53)");
});
