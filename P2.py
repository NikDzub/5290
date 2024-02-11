#!/usr/bin/env python3
# 😘

import asyncio
from playwright.async_api import async_playwright, Request, Response, Route
import os
import json
from pathlib import Path
import sys
from datetime import datetime
import random
import mod
from colorama import Fore, Style

print(f"{Fore.BLUE}\n{sys.argv[0]} is running.. {datetime.now()}{Style.RESET_ALL}")


like_browsers = int(sys.argv[1])

cookies_json = mod.get_cookies(like_browsers)
new_videos = mod.get_new_vids()

eval_file = open("./etc/interval2.js", "r").read()


async def handle_vid(route: Route):
    if (
        "https://v16-webapp-prime.tiktok.com/video/" in route.request.url
        or "https://www.tiktok.com/api/related/item_list/" in route.request.url
    ):
        await route.abort()
    else:
        await route.continue_()


async def browser_l(segment, segment_index):

    async with async_playwright() as p:
        context = await p.firefox.launch(headless=False)
        page = await context.new_page(reduced_motion="reduce")

        await page.route("**/*", handle_vid)

        for cookie_index, cookie in enumerate(segment):
            try:
                print(f"\nbrowser[{segment_index}] [{cookie_index}/{len(segment)}]")
                await context.contexts[0].add_cookies(
                    json.loads(Path(f"./etc/cookies/{cookie}").read_text())
                )
                for vid in new_videos:
                    await page.goto(vid)

                    main_vid = await page.wait_for_selector("video")
                    await main_vid.evaluate("e => e.remove()")
                    side_nav = await page.wait_for_selector(
                        'div[class*="DivSideNavContainer"]'
                    )
                    await side_nav.evaluate("e => e.remove()")
                    bg_vids = await page.wait_for_selector('div[class*="DivVideoList"]')
                    await bg_vids.evaluate("e => e.remove()")

                    try:
                        await page.evaluate(eval_file)
                        await page.wait_for_selector(
                            ".target", timeout=random.randrange(30000, 50000)
                        )
                        hearts = await page.query_selector_all(".heart_box svg")

                        for heart in hearts:
                            if await heart.get_attribute("fill") == "currentColor":
                                await heart.click()
                                print(f"<3", end="")
                                sys.stdout.flush()
                                await page.wait_for_timeout(1000)

                    except Exception as error:
                        # print(error)
                        pass
            except Exception as error:
                # print(error)
                pass

        await page.wait_for_timeout(1000)
        await page.close()
        await context.close()


async def main():
    await asyncio.gather(
        *[
            browser_l(segment, segment_index)
            for segment_index, segment in enumerate(cookies_json)
        ]
    )


asyncio.run(main())
