# Playwright Setup Guide

## Installation

### Node.js / JavaScript

```bash
# Install Playwright and browser binaries
npm install --save-dev playwright
npx playwright install chromium
```

### Python

```bash
# Install Playwright and browser binaries
pip install playwright
playwright install chromium
```

## Configuration (Recommended)

### playwright.config.js

```javascript
// playwright.config.js
/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  // Run tests in files in parallel
  fullyParallel: true,
  // Fail the build on CI if you accidentally left test.only in the source code.
  forbidOnly: !!process.env.CI,
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  // Opt out of parallel tests on CI.
  workers: process.env.CI ? 1 : undefined,
  // Reporter to use. See https://playwright.dev/docs/test-reporters
  reporter: "html",

  use: {
    // Base URL to use in actions like `await page.goto('/')`.
    // baseURL: 'http://localhost:3000',

    // Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer
    trace: "on-first-retry",

    // Capture screenshot on failure
    screenshot: "only-on-failure",

    // Record video on failure
    video: "retain-on-failure",
  },
};

module.exports = config;
```
