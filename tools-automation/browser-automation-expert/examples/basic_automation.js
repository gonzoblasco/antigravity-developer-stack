const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto("https://example.com");
  console.log("Page title:", await page.title());

  await page.screenshot({ path: "screenshot.png", fullPage: true });
  await browser.close();
})();
