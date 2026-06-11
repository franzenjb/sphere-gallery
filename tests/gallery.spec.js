// @ts-check
const { test, expect } = require("@playwright/test");

async function ready(page) {
  await page.goto("/");
  await page.waitForFunction(() => window.__app && window.__app.cards.length > 0);
  await page.waitForTimeout(1800); // intro animation settles
}

test("loads: canvas, one card per jbf.com app, no page errors", async ({ page }) => {
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  await ready(page);
  await expect(page.locator("#stage canvas")).toBeVisible();
  const manifest = await page.evaluate(() =>
    fetch("shots/manifest.json").then(r => r.json())
  );
  const count = await page.evaluate(() => window.__app.cards.length);
  expect(count).toBe(manifest.length);
  expect(count).toBeGreaterThan(40);
  expect(errors).toEqual([]);
});

test("drag rotates sphere with eased follow and inertia", async ({ page }) => {
  await ready(page);
  const before = await page.evaluate(() => window.__app.rot.yaw);

  await page.mouse.move(640, 400);
  await page.mouse.down();
  for (let i = 1; i <= 10; i++) {
    await page.mouse.move(640 + i * 30, 400, { steps: 2 });
  }
  await page.mouse.up();

  // immediately after release, rendered yaw still lags target = eased follow
  const justAfter = await page.evaluate(() => ({
    yaw: window.__app.rot.yaw,
    target: window.__app.rot.tYaw
  }));
  expect(Math.abs(justAfter.target - before)).toBeGreaterThan(0.3);
  expect(Math.abs(justAfter.target - justAfter.yaw)).toBeGreaterThan(0.01);

  // inertia: target keeps drifting after pointer released
  await page.waitForTimeout(250);
  const later = await page.evaluate(() => window.__app.rot.tYaw);
  expect(Math.abs(later - justAfter.target)).toBeGreaterThan(0.001);

  // and the eased value converges toward the target
  await page.waitForTimeout(1500);
  const settled = await page.evaluate(() => ({
    yaw: window.__app.rot.yaw,
    target: window.__app.rot.tYaw
  }));
  expect(Math.abs(settled.target - settled.yaw)).toBeLessThan(0.02);
});

test("clicking a card animates detail page in; close returns", async ({ page }) => {
  await ready(page);

  // find a card near screen centre and really click it
  const pos = await page.evaluate(() => {
    const { cards, screenPos } = window.__app;
    let best = null, bestD = Infinity;
    for (const c of cards) {
      const p = screenPos(c);
      if (!p.inFront) continue;
      const d = Math.hypot(p.x - innerWidth / 2, p.y - innerHeight / 2);
      if (d < bestD) { bestD = d; best = p; }
    }
    return best;
  });
  expect(pos).not.toBeNull();

  await page.mouse.click(pos.x, pos.y);
  await page.waitForFunction(() => window.__app.isDetailOpen(), null, { timeout: 5000 });
  await expect(page.locator("#detail")).toBeVisible();
  await expect(page.locator("#detailTitle")).not.toHaveText("");
  const href = await page.locator("#visitLink").getAttribute("href");
  expect(href).toMatch(/^https:\/\/.*jbf\.com/);

  // detail page actually covers the viewport (slid in)
  const box = await page.locator("#detail").boundingBox();
  expect(Math.abs(box.y)).toBeLessThan(5);

  await page.click("#closeDetail");
  await page.waitForFunction(() => !window.__app.isDetailOpen(), null, { timeout: 5000 });

  // camera restored to centre of the sphere
  const cam = await page.evaluate(() => {
    const p = window.__app.camera.position;
    return Math.hypot(p.x, p.y, p.z);
  });
  expect(cam).toBeLessThan(0.1);
});

test("text contrast: HUD and close button readable", async ({ page }) => {
  await ready(page);
  const hint = await page.locator("#hint").evaluate(el => getComputedStyle(el).color);
  expect(hint).toBe("rgb(185, 185, 192)"); // light on near-black

  await page.evaluate(() => window.__app.openFirst());
  await page.waitForFunction(() => window.__app.isDetailOpen());
  const btn = await page.locator("#closeDetail").evaluate(el => {
    const s = getComputedStyle(el);
    return { color: s.color, bg: s.backgroundColor };
  });
  expect(btn.color).toBe("rgb(16, 16, 20)");        // dark text
  expect(btn.bg).toBe("rgb(242, 242, 240)");        // on light button
});
