# Browser Automation Anti-Patterns

## 1. Arbitrary Timeouts

**Problem**: Fixed delays make tests slow and flaky
**Solution**: Use Playwright's auto-wait or specific wait conditions

```javascript
// ❌ BAD
await page.waitForTimeout(5000);
await page.click(".button");

// ✅ GOOD
await page.click(".button"); // Auto-waits
await page.waitForLoadState("networkidle"); // Specific condition
await page.waitForSelector(".result"); // Wait for element
```

## 2. CSS/XPath First

**Problem**: Brittle selectors that break with UI changes
**Solution**: Use user-facing selectors (role, text, label)

```javascript
// ❌ AVOID
await page.click("#btn-submit-form-user-registration");
await page.locator("div.container > button.primary").click();

// ✅ PREFER
await page.getByRole("button", { name: "Register" }).click();
await page.getByText("Submit").click();
```

## 3. Single Browser Context for Everything

**Problem**: Tests interfere with each other, state leaks
**Solution**: Use fresh context per test

```javascript
// ❌ BAD: Reusing same context
const context = await browser.newContext();
// all tests share this context

// ✅ GOOD: Fresh context per test
test("test 1", async ({ page }) => {
  // Isolated context
});

test("test 2", async ({ page }) => {
  // New isolated context
});
```

## 4. Not Waiting for NetworkIdle on Dynamic Apps

**Problem**: DOM inspection happens before JavaScript renders content
**Solution**: Wait for networkidle before scraping

```javascript
// ❌ BAD
await page.goto("https://spa-app.com");
const content = await page.content(); // Too early!

// ✅ GOOD
await page.goto("https://spa-app.com");
await page.waitForLoadState("networkidle"); // Wait for JS
const content = await page.content();
```

## ⚠️ Sharp Edges

| Issue                                               | Severity | Solution                                                 |
| --------------------------------------------------- | -------- | -------------------------------------------------------- |
| Using `waitForTimeout()` instead of auto-wait       | Critical | Remove all manual timeouts, use `click()`, `fill()` etc. |
| CSS selectors that depend on implementation details | High     | Use `getByRole()`, `getByText()`, `getByLabel()`         |
| Not handling popups/new tabs before triggering them | High     | Set up popup listener BEFORE clicking link               |
| Tests fail randomly due to race conditions          | High     | Use `waitForLoadState()`, `waitForURL()`, proper waits   |
| Scrapers detected and blocked                       | High     | Use stealth plugins, rotate user agents, add delays      |
| Tests run slowly due to sequential execution        | Medium   | Enable parallel execution in config                      |
| Screenshots don't capture full page                 | Medium   | Use `fullPage: true` option                              |
| Mobile tests don't match real devices               | Medium   | Use device emulation with proper userAgent               |
