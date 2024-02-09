#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import os
import json
from pathlib import Path
import sys
from datetime import datetime
import colorama
from colorama import Fore, Style

print(f"{Fore.BLUE}\n{sys.argv[0]} is running.. {datetime.now()}{Style.RESET_ALL}")

if os.path.exists("./etc/cookies/.DS_Store"):
    os.remove("./etc/cookies/.DS_Store")
cookies_json = os.listdir("./etc/cookies")

new_videos = []
with open("./etc/new_videos.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        new_videos.append(line.replace("\n", ""))

stats = []


async def p1(video, vid_index):
    global stats
    stats.append([video, 0, ""])

    async with async_playwright() as p:
        context = await p.firefox.launch(headless=False)
        page = await context.new_page(
            # user_agent="Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
        )
        await context.contexts[0].add_cookies(
            json.loads((Path(f"./etc/cookies/{cookies_json[0]}")).read_text())
        )

        block_media = ["image", "media", "font", "stylesheet", "other"]
        await page.route(
            "**/*",
            lambda route: (
                route.abort()
                if route.request.resource_type in block_media
                else route.continue_()
            ),
        )

        await page.goto(video, wait_until="load")

        await page.wait_for_selector(
            'div[class*="DivCommentItemContainer"]', timeout=10000
        )

        eval_file = open("./etc/interval.js", "r").read()

        max_errors = 6

        try:
            for index, cookie in enumerate(cookies_json):
                if max_errors > 0:
                    try:
                        await page.evaluate(eval_file)
                        await page.wait_for_selector(".target", timeout=60000)

                        hearts = await page.query_selector_all(".heart_box svg")

                        for heart in hearts:
                            if await heart.get_attribute("fill") == "currentColor":
                                await heart.click()
                                # print(f"{video} <3")
                                stats[vid_index][1] += 1
                                await page.wait_for_timeout(2000)

                        await context.contexts[0].add_cookies(
                            json.loads(Path(f"cookies/{cookie}").read_text())
                        )

                        await page.wait_for_timeout(1000)
                        print(
                            f"{stats[vid_index][0]}, likes :{stats[vid_index][1]}, cookie: {index}/{len(cookies_json)}"
                        )
                        await page.reload(wait_until="load")

                    except Exception as error:
                        # print(error)
                        max_errors -= 1
                        await context.contexts[0].add_cookies(
                            json.loads(Path(f"./etc/cookies/{cookie}").read_text())
                        )
                        await page.wait_for_timeout(1000)
                        print(
                            f"{stats[vid_index][0]}, likes :{stats[vid_index][1]}, cookie: {index}/{len(cookies_json)}"
                        )
                        await page.reload(wait_until="load")
                        pass

        except Exception as error:
            # print(error)
            pass

        print(f"{video} closed.")
        await page.wait_for_timeout(1000)
        await page.close()
        await context.close()


async def fu():
    await asyncio.gather(
        *[p1(video, vid_index) for vid_index, video in enumerate(new_videos)]
    )


asyncio.run(fu())
