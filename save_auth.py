# save_auth.py
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://discourse.onlinedegree.iitm.ac.in/")

        print("🔑 Please log in manually in the browser window...")

        # Give you time to log in
        await page.wait_for_timeout(60000)  # 60 seconds

        await context.storage_state(path="auth.json")
        print("✅ Session saved to auth.json")

        await browser.close()

asyncio.run(main())
