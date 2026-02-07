// @ts-check
const { defineConfig } = require('@playwright/test');

/**
 * Playwright configuration for health-tracker-app frontend E2E tests.
 *
 * Tests run against the deployed testing environment by default.
 * Override with BASE_URL env var for local testing.
 */
module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
  fullyParallel: true,
  retries: 1,
  reporter: 'list',
  use: {
    baseURL: process.env.BASE_URL || 'https://health.gahfaudio.in',
    ignoreHTTPSErrors: true,
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
