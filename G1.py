#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import sys
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import mod
from datetime import datetime
import random
import json
import re
from colorama import Fore, Style

search_browsers = int(sys.argv[1])
comments_on_vid = int(sys.argv[2])

d = u2.connect()
users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)

users = mod.get_users(segments=search_browsers)
used_vids = mod.get_used_vids()
new_vids = []


async def get_vids():
    global new_vids

    async with async_playwright() as p:
        context = await p.firefox.launch(headless=True)

        async def browser_l(segment):
            page = await context.new_page(
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            )

            for user in segment:
                if len(new_vids) < len(device_profiles):
                    try:
                        print(f"|", end="")

                        sys.stdout.flush()
                        async with page.expect_request(
                            "**/api/post/item_list/**",
                            timeout=10000,
                        ) as first:
                            await page.goto(
                                f"https://www.tiktok.com/@{user}", timeout=10000
                            )

                        first_request = await first.value
                        response = await first_request.response()
                        response_body = await response.body()

                        if response_body.strip():

                            videos_json = json.loads(response_body)["itemList"]
                            current_timestamp = datetime.now().timestamp()
                            for vid in videos_json:
                                vid = mod.Video(
                                    vid["author"]["uniqueId"],
                                    vid["author"]["verified"],
                                    vid["id"],
                                    ((current_timestamp - vid["createTime"]) / 3600),
                                    vid["stats"]["commentCount"],
                                    vid["stats"]["diggCount"],
                                    vid["stats"]["playCount"],
                                    vid["stats"]["collectCount"],
                                    vid["stats"]["shareCount"],
                                )
                                used = vid.video_url() in used_vids

                                if (
                                    vid.valid()
                                    and used == False
                                    and len(new_vids) < len(device_profiles)
                                ):
                                    new_vids.append(vid.video_url())
                                    used_vids.append(vid.video_url())
                                    vid.display_info()

                    except Exception as error:
                        # print(error)
                        print(f".", end="")
                        sys.stdout.flush()
                        pass

                else:
                    break

        await asyncio.gather(
            *[browser_l(segment) for index, segment in enumerate(users)]
        )

        with open("./etc/new_videos.txt", "w") as outfile:
            for index, row in enumerate(new_vids):
                outfile.write(str(row) + "\n")

        with open("./etc/used_videos.txt", "w") as outfile:
            for index, row in enumerate(used_vids):
                outfile.write(str(row) + "\n")

        await context.close()
        print("")


async def emulator(profile_index, profile_id):
    try:
        d.shell(f"am switch-user {profile_id}")
        print(f"")
        print(f"{Fore.GREEN}user[{profile_id}]{Style.RESET_ALL}")

        if profile_id == "0":
            try:
                await asyncio.sleep(2)
                d.app_start("com.github.uiautomator")
                d(resourceId="com.github.uiautomator:id/start_uiautomator").click()
            except Exception as error:
                print(error)

        else:
            await asyncio.sleep(2)
            d(resourceId=mod.lock).exists(timeout=20)
            d.press(62)
            d.swipe_ext("up", scale=0.8)

        d.open_url(f"https://www.tiktok.com/@ihptto")
        d(text="Message").exists(timeout=10)

        random.shuffle(new_vids)
        for vid in new_vids:
            d.open_url(vid)

            d(resourceId=mod.comments).exists(timeout=20)
            d(resourceId=mod.pause).click(20)
            d(resourceId=mod.comments).click(20)
            d(resourceId=mod.actual_comment).exists(timeout=20)

            comments_list = []
            for i in range(3):
                d.swipe_ext("up", scale=0.8)

            for com in d(resourceId=mod.actual_comment):
                if com.get_text() not in comments_list:
                    comments_list.append(com.get_text())

            random.shuffle(comments_list)
            for comment_index, comment in enumerate(comments_list):
                if comment_index < comments_on_vid:
                    d(resourceId=mod.add_comment).click(10)
                    d(resourceId=mod.add_comment).set_text(comment)
                    d(resourceId=mod.send_comment).click(10)
                    print(f"user[{profile_id}]>{vid}")
                    await asyncio.sleep(1)

        d.shell(f"am force-stop {mod.app_name}")
        if profile_id != "0":
            d.shell(f"am stop-user {profile_id}")

    except Exception as error:
        print(error)
        d.shell(f"am force-stop {mod.app_name}")


async def main():
    print(f"{Fore.BLUE}\nget_vids() is running.. {datetime.now()}{Style.RESET_ALL}")
    await asyncio.gather(*[get_vids()])
    print(f"{Fore.BLUE}\nemulator() is running.. {datetime.now()}{Style.RESET_ALL}")

    for profile_index, profile_id in enumerate(device_profiles):
        await emulator(profile_index, profile_id)


asyncio.run(main())
