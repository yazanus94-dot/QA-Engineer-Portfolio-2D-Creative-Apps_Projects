import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests/e2e",
  use: { baseURL: "http://localhost:4173", screenshot: "only-on-failure" },
  webServer: { command: "node serve.js", url: "http://localhost:4173", reuseExistingServer: true },
});
