# Browser Automation Patterns

## 1. Auto-Wait Pattern (Recommended)

Playwright automatically waits for elements. **Never** use manual timeouts.

```javascript
// ❌ BAD: Manual waits
await page.waitForTimeout(3000);
await page.click(".button");

// ✅ GOOD: Let Playwright auto-wait
await page.click(".button"); // Waits automatically until clickable
```

Playwright auto-waits for:

- Element is attached to DOM
- Element is visible
- Element is stable (not animating)
- Element receives events (not obscured)
- Element is enabled (not disabled)

## 2. User-Facing Selectors (Best Practice)

Select elements the way users see them, not by CSS classes.

```javascript
// ❌ AVOID: Implementation details
await page.click(".btn-primary.submit-form");
await page.click("#user-name-input-field-id");

// ✅ PREFER: User-facing selectors
await page.click('button:has-text("Submit")');
await page.fill('input[placeholder="Username"]', "john");
await page.click('role=button[name="Sign in"]');

// Best: Use getByRole, getByText, getByLabel
await page.getByRole("button", { name: "Submit" }).click();
await page.getByLabel("Username").fill("john");
await page.getByText("Welcome back").isVisible();
```

**Selector priority** (most to least resilient):

1. `getByRole()` - Accessibility-based (WCAG compliant)
2. `getByLabel()` - Form labels
3. `getByPlaceholder()` - Input placeholders
4. `getByText()` - Visible text
5. `getByTestId()` - data-testid attributes
6. CSS selectors - Last resort

## 3. Test Isolation Pattern

Each test runs in complete isolation with fresh state.

```javascript
import { test, expect } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  // Fresh browser context per test
  await page.goto("https://example.com");
});

test("login flow", async ({ page }) => {
  // This test is isolated
  await page.getByLabel("Username").fill("john");
  await page.getByLabel("Password").fill("secret");
  await page.getByRole("button", { name: "Login" }).click();

  await expect(page).toHaveURL(/.*dashboard/);
});

test("signup flow", async ({ page }) => {
  // Fresh state, no interference from previous test
  await page.getByRole("link", { name: "Sign up" }).click();
  // ...
});
```

## 4. Responsive Design Testing

Test across multiple viewports efficiently.

```javascript
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  const viewports = [
    { name: "Desktop", width: 1920, height: 1080 },
    { name: "Tablet", width: 768, height: 1024 },
    { name: "Mobile", width: 375, height: 667 },
  ];

  for (const viewport of viewports) {
    console.log(`Testing ${viewport.name}`);

    await page.setViewportSize({
      width: viewport.width,
      height: viewport.height,
    });

    await page.goto("https://example.com");
    await page.screenshot({
      path: `${viewport.name.toLowerCase()}.png`,
      fullPage: true,
    });
  }

  await browser.close();
})();
```

## 5. Form Automation Pattern

```javascript
// Login flow
await page.goto("https://example.com/login");

await page.getByLabel("Email").fill("user@example.com");
await page.getByLabel("Password").fill("password123");
await page.getByRole("button", { name: "Sign in" }).click();

// Wait for navigation
await page.waitForURL("**/dashboard");
console.log("✅ Login successful");

// Verify success
await expect(page.getByText("Welcome back")).toBeVisible();
```

## 6. Web Scraping Pattern

```javascript
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto("https://example.com/products");

  // Wait for content to load
  await page.waitForLoadState("networkidle");

  // Extract data
  const products = await page.$$eval(".product-card", (cards) =>
    cards.map((card) => ({
      title: card.querySelector("h3")?.textContent?.trim(),
      price: card.querySelector(".price")?.textContent?.trim(),
      link: card.querySelector("a")?.href,
    })),
  );

  console.log(`Scraped ${products.length} products`);
  console.log(JSON.stringify(products, null, 2));

  await browser.close();
})();
```

## 7. Network Interception (API Mocking)

```javascript
import { test, expect } from "@playwright/test";

test("mock API response", async ({ page }) => {
  // Intercept and modify API calls
  await page.route("**/api/users", (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([{ id: 1, name: "Mock User" }]),
    });
  });

  await page.goto("https://example.com/dashboard");

  // Verify mocked data appears
  await expect(page.getByText("Mock User")).toBeVisible();
});
```

## 8. Authentication Persistence

```javascript
import { test as setup } from "@playwright/test";

// Setup auth state once
setup("authenticate", async ({ page }) => {
  await page.goto("https://example.com/login");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("pass");
  await page.getByRole("button", { name: "Sign in" }).click();

  // Wait for auth to complete
  await page.waitForURL("**/dashboard");

  // Save auth state
  await page.context().storageState({
    path: "auth.json",
  });
});

// Reuse auth in tests
test.use({ storageState: "auth.json" });

test("access protected page", async ({ page }) => {
  // Already authenticated
  await page.goto("https://example.com/dashboard");
  await expect(page.getByText("Welcome")).toBeVisible();
});
```
