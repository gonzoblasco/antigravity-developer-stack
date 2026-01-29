# Specialized Scenarios & Common Use Cases

## 1. Check for Broken Links

```javascript
const links = await page.locator('a[href^="http"]').all();
const results = { working: 0, broken: [] };

for (const link of links) {
  const href = await link.getAttribute("href");
  try {
    const response = await page.request.head(href);
    if (response.ok()) {
      results.working++;
    } else {
      results.broken.push({ url: href, status: response.status() });
    }
  } catch (e) {
    results.broken.push({ url: href, error: e.message });
  }
}

console.log(
  `✅ Working: ${results.working}, ❌ Broken: ${results.broken.length}`,
);
```

## 2. Extract Table Data

```javascript
const rows = await page.locator("table tbody tr").all();
const data = [];

for (const row of rows) {
  const cells = await row.locator("td").allTextContents();
  data.push(cells);
}

console.log(data);
```

## 3. Handle Cookie Banners

```javascript
// Dismiss common cookie banners
try {
  await page
    .getByRole("button", { name: /accept|agree|ok/i })
    .click({ timeout: 3000 });
} catch (e) {
  // No cookie banner or already dismissed
}
```

## 4. Mobile Device Emulation (Advanced)

```javascript
const { devices } = require("playwright");

const iPhone = devices["iPhone 13"];

const browser = await chromium.launch();
const context = await browser.newContext({
  ...iPhone,
  locale: "en-US",
  geolocation: { latitude: 37.7749, longitude: -122.4194 },
  permissions: ["geolocation"],
});

const page = await context.newPage();
await page.goto("https://example.com");
```

## 5. Visual Regression Testing

```javascript
import { test, expect } from "@playwright/test";

test("visual regression", async ({ page }) => {
  await page.goto("https://example.com");

  // Take screenshot and compare with baseline
  await expect(page).toHaveScreenshot("homepage.png", {
    maxDiffPixels: 100, // Allow small differences
  });
});
```
