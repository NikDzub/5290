import asyncio
import mod

from undetected_playwright.async_api import async_playwright, Playwright


mod.clean_local_firefox()


async def test():
    async with async_playwright() as playwright:

        args = []

        # disable navigator.webdriver:true flag
        args.append("--disable-blink-features=AutomationControlled")
        browser = await playwright.firefox.launch_persistent_context(
            # /Applications/Firefox Nightly.app
            user_data_dir="/Users/ihpt/Library/Application Support/Firefox/Profiles/i8unqabt.default-nightly",
            # executable_path="/Applications/Firefox Nightly.app",
            executable_path="/Applications/Firefox Nightly.app/Contents/MacOS/firefox",
            # executable_path="/Users/ihpt/Library/Caches/ms-playwright/firefox-1438/firefox/Nightly.app/Contents/MacOS/firefox",
            headless=False,
            devtools=True,
        )

        page = await browser.browser.new_context()
        page.new_page()
        # page = await browser.new_page(reduced_motion="reduce")
        print("here")

        # page = await browser.new_page()
        print(browser.browser.contexts)
        # await page.close()

        await page.goto("https://nowsecure.nl/#relax")
        input("Press ENTER to continue to Creep-JS:")
        await page.goto("https://nowsecure.nl/#relax")
        await page.goto("https://abrahamjuliot.github.io/creepjs/")
        input("Press ENTER to exit:")
        await browser.close()


if __name__ == "__main__":

    asyncio.run(test())
