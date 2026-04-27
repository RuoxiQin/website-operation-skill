---
name: website-operation
description: Operate a website through a real browser — navigate, fill forms, click, extract rendered content, capture screenshots. Use when the task involves interacting with a web UI (login flows, form submission, scraping JS-rendered content, multi-step workflows). Do NOT use for plain HTTP/REST API calls (use curl directly for those).
allowed-tools: Bash
---

# Website operation playbook

Drive a real browser via **Playwright** (Node API) executed through `bash`. Real browsers handle JS, cookies, and dynamic DOM — `curl` can't.

## Setup

Assume `playwright` is installed and `chromium` is available (`npx playwright install chromium`). If a script fails with a missing-browser error, install once and retry.

Write each automation as a single self-contained Node script in a tmp file, then run it. This keeps state (cookies, console output) in one process. Don't try to drive Playwright across multiple bash calls.

```js
// /tmp/run.mjs
import { chromium } from 'playwright';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const userDataDir = mkdtempSync(join(tmpdir(), 'pw-'));
const ctx = await chromium.launchPersistentContext(userDataDir, { headless: true });
const page = await ctx.newPage();
try {
  // ... your steps ...
} finally {
  await ctx.close();
}
```

`launchPersistentContext` keeps cookies and storage across navigations within the script — needed for any flow that crosses a login or relies on session state.

## Core rules

1. **Wait for the right thing, not for time.** Use `await page.waitForSelector(sel)`, `await page.waitForLoadState('networkidle')`, or `await locator.waitFor()`. Never use `setTimeout` / `sleep` to "let the page load" — it's the #1 cause of flaky scripts.

2. **Inspect before you act.** Before writing a selector, dump the relevant HTML and read it:
   ```js
   await page.locator('main').innerHTML().then(h => fs.writeFileSync('/tmp/page.html', h));
   ```
   Then read `/tmp/page.html` to find real selectors. Don't guess from memory — site markup changes.

3. **Prefer role/label/text locators over CSS.** They survive markup changes and read like the UI:
   ```js
   await page.getByRole('button', { name: 'Sign in' }).click();
   await page.getByLabel('Email').fill('user@example.com');
   await page.getByText('Welcome back').waitFor();
   ```
   Fall back to CSS/XPath only when the accessible name isn't unique.

4. **Screenshot meaningful steps.** Capture before+after for any state-changing action:
   ```js
   await page.screenshot({ path: '/tmp/before-submit.png', fullPage: true });
   await page.getByRole('button', { name: 'Submit' }).click();
   await page.waitForURL('**/success');
   await page.screenshot({ path: '/tmp/after-submit.png', fullPage: true });
   ```
   Screenshots help you (and the user) verify what actually happened, and let you self-correct when a step silently fails.

5. **Extract structured data, not blobs.** Use `locator.evaluateAll(...)` to map DOM nodes to plain objects, then `JSON.stringify` the result. Avoid dumping `page.content()` as your final answer.

   ```js
   const stories = await page.locator('.story').evaluateAll(rows =>
     rows.map(r => ({
       title: r.querySelector('.title')?.textContent?.trim(),
       href: r.querySelector('a')?.href,
     })),
   );
   ```

## Auth flows

When a task spans login + later actions, save and reuse storage state:

```js
// First run: log in, then save state
await page.getByLabel('Email').fill(email);
await page.getByLabel('Password').fill(password);
await page.getByRole('button', { name: 'Sign in' }).click();
await page.waitForURL('**/dashboard');
await ctx.storageState({ path: '/tmp/auth.json' });
```

```js
// Later runs: reuse state, skip login entirely
const ctx = await chromium.launchPersistentContext(userDataDir, {
  headless: true,
  storageState: '/tmp/auth.json',
});
```

Never put real credentials in scripts you echo back to the user. Read them from env vars.

## Failure recovery

When a selector times out:
1. Take a screenshot — `await page.screenshot({ path: '/tmp/fail.png', fullPage: true })`.
2. Dump current URL and title — `console.log(page.url(), await page.title())`.
3. Dump the HTML around where you expected the element.
4. Read the screenshot/HTML, fix the selector, re-run. Don't just bump the timeout.

If the page shows a captcha, cookie banner, or unexpected modal — handle it explicitly. Don't pretend it isn't there.

## Headless vs. headed

Default to `headless: true`. Switch to `headless: false` only when the user is running locally and asks to watch, or when debugging a flow that behaves differently in headless mode (rare, but happens with media/auth).

## Cleanup

Always `await ctx.close()` in a `finally` block. Tmp dirs from `mkdtempSync` are fine to leave — the OS cleans them up — but close the browser process or you'll leak chromium instances.
