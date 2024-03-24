#!/usr/bin/env python3

# python3 M3.py 3 0
# python3 M3.py (# like brwsrs) (reply?)

import asyncio
from playwright.async_api import async_playwright, Request, Response, Route
import json
from pathlib import Path
import sys
from datetime import datetime
import random
import mod
from colorama import Fore, Style


like_browsers = int(sys.argv[1])
reply = int(sys.argv[2])


cookies_json = mod.get_cookies(like_browsers)
new_videos = mod.get_new_vids()

eval_file = open("./etc/interval.js", "r").read()


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
        context = await p.firefox.launch(
            headless=True,
            # proxy={
            #     "server": "181.177.87.173:9291",
            #     "username": "3jFvwU",
            #     "password": "qF5DWZ",
            # },
        )
        page = await context.new_page(reduced_motion="reduce")

        await page.route("**/*", handle_vid)

        trash_vid = []
        for cookie_index, cookie in enumerate(segment):
            try:
                print(
                    f"{Fore.LIGHTGREEN_EX}browser [{segment_index}] - {cookie} [{cookie_index}/{len(segment)}]{Style.RESET_ALL} {datetime.now()}"
                )
                await context.contexts[0].add_cookies(
                    json.loads(Path(f"./etc/cookies/{cookie}").read_text())
                )

                for vid in new_videos:
                    if trash_vid.count(vid) < 3:
                        try:
                            likes = 0
                            await page.goto(vid)

                            main_vid = await page.wait_for_selector("video")
                            await main_vid.evaluate("e => e.remove()")
                            side_nav = await page.wait_for_selector(
                                'div[class*="DivSideNavContainer"]'
                            )
                            await side_nav.evaluate("e => e.remove()")
                            bg_vids = await page.wait_for_selector(
                                'div[class*="DivVideoList"]'
                            )
                            await bg_vids.evaluate("e => e.remove()")

                            await page.evaluate(eval_file)
                            await page.wait_for_selector(
                                ".target", timeout=random.randrange(30000, 50000)
                            )

                            await page.wait_for_timeout(1000)
                            hearts = await page.query_selector_all(".heart_box svg")

                            for heart in hearts:
                                if await heart.get_attribute("fill") == "currentColor":
                                    await heart.click()
                                    likes += 1
                                    await page.wait_for_timeout(1000)

                            # if reply:
                            #     html_replies = await page.query_selector_all(
                            #         ".target span[data-e2e*='reply']"
                            #     )
                            #     for rep in html_replies:
                            #         await rep.click()
                            #         await page.keyboard.type(mod.get_reply()[0])
                            #         await page.keyboard.press("Enter")
                            #         await page.wait_for_timeout(999)

                            print(
                                f"{vid} {Fore.RED}({likes} x <3) {Fore.LIGHTGREEN_EX}({cookie}){Style.RESET_ALL}"
                            )

                        except Exception as error:
                            # print(error)
                            trash_vid.append(vid)
                            # print(f"{vid} appended to trash")
                            pass

            except Exception as error:
                # print(error)
                pass

        await page.close()
        await context.close()


async def main():
    print(f"{Fore.BLUE}\n{sys.argv[0]} is running.. {datetime.now()}{Style.RESET_ALL}")

    await asyncio.gather(
        *[
            browser_l(segment, segment_index)
            for segment_index, segment in enumerate(cookies_json)
        ]
    )


asyncio.run(main())
