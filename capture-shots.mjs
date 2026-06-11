// Capture screenshots of every *.jbf.com app for the gallery cards.
// Usage: node capture-shots.mjs
import { chromium } from "playwright-core";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";

const registry = JSON.parse(readFileSync(`${homedir()}/dev/projects.json`, "utf8"));
const apps = [];
for (const [name, v] of Object.entries(registry.projects || {})) {
  const doms = (v.custom_domains || []).filter(d => d.endsWith("jbf.com"));
  if (!doms.length) continue;
  const domain = doms[0];
  apps.push({
    name,
    domain,
    url: `https://${domain}`,
    img: `shots/${name}.jpg`,
    description: v.description || ""
  });
}
console.log(`${apps.length} jbf.com apps`);
mkdirSync("shots", { recursive: true });

const browser = await chromium.launch();
const ok = [];
const failed = [];

async function capture(app) {
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  try {
    await page.goto(app.url, { timeout: 25000, waitUntil: "load" });
    await page.waitForTimeout(6000); // let maps/animations render
    await page.screenshot({ path: app.img, type: "jpeg", quality: 72 });
    ok.push(app);
    console.log("ok  ", app.domain);
  } catch (e) {
    failed.push(app.domain);
    console.log("FAIL", app.domain, e.message.split("\n")[0]);
  } finally {
    await page.close();
  }
}

const queue = [...apps];
await Promise.all(Array.from({ length: 6 }, async () => {
  while (queue.length) await capture(queue.shift());
}));
await browser.close();

ok.sort((a, b) => a.name.localeCompare(b.name));
writeFileSync("shots/manifest.json", JSON.stringify(ok, null, 2));
console.log(`\n${ok.length} captured, ${failed.length} failed${failed.length ? ": " + failed.join(", ") : ""}`);
