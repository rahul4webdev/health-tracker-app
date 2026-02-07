// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Login routing E2E tests for health-tracker-app.
 *
 * These tests verify that SPA client-side routing works correctly
 * for the /login route when deployed behind LiteSpeed/OpenLiteSpeed.
 *
 * The .htaccess rewrite rule must serve index.html for all non-file
 * paths so that React Router can handle /login in the browser.
 */

test.describe('Login Route — Direct Navigation', () => {
  test('GET /login returns 200 and renders login page', async ({ page }) => {
    // Direct navigation: simulates typing https://health.gahfaudio.in/login in browser
    const response = await page.goto('/login', { waitUntil: 'networkidle' });

    // Server must return 200 (not 404) thanks to .htaccess fallback
    expect(response.status()).toBe(200);

    // React app must render the login page
    await expect(page.locator('h2')).toHaveText('Login');

    // Login form elements must be present
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('GET /login serves HTML content type', async ({ page }) => {
    const response = await page.goto('/login', { waitUntil: 'domcontentloaded' });

    // Must serve text/html (index.html), not a 404 error page
    const contentType = response.headers()['content-type'] || '';
    expect(contentType).toContain('text/html');
  });
});

test.describe('Login Route — Client-Side Navigation', () => {
  test('navigating from / to /login via navbar link works', async ({ page }) => {
    // Start at root — ProtectedRoute will redirect to /login or show dashboard
    await page.goto('/', { waitUntil: 'networkidle' });

    // Find and click the "Login" link in the navbar
    const loginLink = page.locator('nav a[href="/login"]');

    // If not authenticated, the Login link should be visible in navbar
    if (await loginLink.isVisible()) {
      await loginLink.click();

      // URL should now be /login
      await expect(page).toHaveURL(/\/login$/);

      // Login page should render
      await expect(page.locator('h2')).toHaveText('Login');
      await expect(page.locator('input[type="email"]')).toBeVisible();
    } else {
      // User is authenticated — navigate directly to /login
      await page.goto('/login', { waitUntil: 'networkidle' });
      await expect(page.locator('h2')).toHaveText('Login');
    }
  });
});

test.describe('Login Route — Refresh Test (SPA Critical)', () => {
  test('refreshing /login does not break the page', async ({ page }) => {
    // Navigate to /login
    await page.goto('/login', { waitUntil: 'networkidle' });
    await expect(page.locator('h2')).toHaveText('Login');

    // Simulate browser refresh (F5)
    const response = await page.reload({ waitUntil: 'networkidle' });

    // After refresh, server must still return 200 (not 404)
    expect(response.status()).toBe(200);

    // Page must still render correctly after refresh
    await expect(page.locator('h2')).toHaveText('Login');
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('no console errors on /login after refresh', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/login', { waitUntil: 'networkidle' });
    await page.reload({ waitUntil: 'networkidle' });

    // Filter out known non-critical errors (e.g., favicon 404, API connection)
    const criticalErrors = consoleErrors.filter(
      (e) => !e.includes('favicon') && !e.includes('healthapi.gahfaudio.in')
    );

    expect(criticalErrors).toHaveLength(0);
  });
});

test.describe('Other SPA Routes — Fallback Verification', () => {
  test('GET /register returns 200 and renders register page', async ({ page }) => {
    const response = await page.goto('/register', { waitUntil: 'networkidle' });
    expect(response.status()).toBe(200);

    // Should render the register page (not a 404)
    await expect(page.locator('h2')).toHaveText('Register');
  });
});
