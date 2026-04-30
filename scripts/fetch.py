"""
fetch.py

Shared Playwright-based HTML fetcher for all parsing scripts.
Using a real headless browser avoids Cloudflare bot detection that blocks
simple urllib/requests-based scrapers.

Requires: playwright
  pip install playwright
  playwright install chromium
"""

import sys

def _get_user_agent(browser):
    """Derive a non-headless UA from the installed Chromium version."""
    page = browser.new_page()
    ua = page.evaluate("navigator.userAgent")
    page.close()
    # Playwright's headless Chromium reports "HeadlessChrome" — strip it so the
    # UA looks like a regular desktop browser to bot-detection systems.
    return ua.replace("HeadlessChrome", "Chrome")


def fetch_html(url, *, wait_until="networkidle", timeout=30000):
    """Fetch fully-rendered HTML from a URL using a headless Chromium browser."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Error: playwright not installed. Run:\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=_get_user_agent(browser))
        page.goto(url, wait_until=wait_until, timeout=timeout)
        html = page.content()
        browser.close()
        return html


class FetchSession:
    """Context manager that keeps a single browser open across multiple fetches.

    Use this when a script needs to load several pages in sequence (e.g. pagination)
    to avoid the overhead of launching a new browser for each request.

    Example:
        with FetchSession() as session:
            html1 = session.fetch(url1)
            html2 = session.fetch(url2)
    """

    def __enter__(self):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print(
                "Error: playwright not installed. Run:\n"
                "  pip install playwright\n"
                "  playwright install chromium"
            )
            sys.exit(1)

        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=True)
        self._page = self._browser.new_page(user_agent=_get_user_agent(self._browser))
        return self

    def fetch(self, url, *, wait_until="networkidle", timeout=30000):
        """Navigate to url and return the rendered HTML."""
        self._page.goto(url, wait_until=wait_until, timeout=timeout)
        return self._page.content()

    def __exit__(self, *args):
        self._browser.close()
        self._pw.stop()
