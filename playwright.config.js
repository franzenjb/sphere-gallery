// @ts-check
const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 60_000,
  use: {
    baseURL: "http://localhost:4179",
    viewport: { width: 1280, height: 800 },
    colorScheme: "dark"
  },
  webServer: {
    command: "python3 -m http.server 4179",
    port: 4179,
    reuseExistingServer: true
  }
});
