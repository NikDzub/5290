#!/usr/bin/env python3

import asyncio
import sys
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import mod
from datetime import datetime
import random
import re
from colorama import Fore, Style
import concurrent.futures


il_users = mod.get_users_il()

d1 = u2.connect("127.0.0.1:6555")
d1_users_output, exit_code = d1.shell("pm list users")
d1_users = re.findall(r"UserInfo{(\d+):", d1_users_output)


async def search():
    d1.uiautomator.start()
    d1.app_start("com.github.uiautomator")
    d1(resourceId="com.github.uiautomator:id/start_uiautomator").click()

    d1.open_url(f"https://www.tiktok.com/@ihptto")
    d1(text="Message").exists(timeout=10)

    for user in il_users:

        try:

            # go 2 usr -----------------------------------------------------------------
            d1.open_url(f"https://www.tiktok.com/@{user}")
            d1(text="Message").exists(timeout=10)
            await asyncio.sleep(1)
            # print(f"{user} loaded")

            # go 2 followers -----------------------------------------------------------------
            d1(text="Followers").exists(timeout=10)
            d1(text="Followers").click()
            d1(text="Follow").exists(timeout=10)
            # print("loadded followers")

            # scroll followers -----------------------------------------------------------------
            for i in range(100):
                print(i)
                d1.swipe(145, 380, 150, 100, 0.01)
                await asyncio.sleep(1)
                d1.swipe_ext("down", scale=0.5)

            # get last usr focused -----------------------------------------------------------------
            for i in range(5):
                d1.press(61)

            # go over usrs -----------------------------------------------------------------
            for i in range(200):
                print(f"{i} {datetime.now().strftime(f'%H:%M:%S')}")
                d1.press(66)

                # in user -----------------------------------------------------------------
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    loop = asyncio.get_event_loop()

                    def wait_video():
                        if d1(resourceId="com.zhiliaoapp.musically:id/cover").exists(
                            timeout=3
                        ):
                            return "has_video"
                        else:
                            return None

                    def wait_private():

                        if d1(text="This account is private").exists(timeout=3):
                            return "is_private"
                        else:
                            return None

                    def wait_no_videos():
                        if d1(text="No videos yet").exists(timeout=3):
                            return "no_videos"
                        else:
                            return None

                    def wait_has_ban():
                        if d1(text="Account banned").exists(timeout=3):
                            return "banned"
                        else:
                            return None

                    future_1 = loop.run_in_executor(executor, wait_video)
                    future_2 = loop.run_in_executor(executor, wait_private)
                    future_3 = loop.run_in_executor(executor, wait_no_videos)
                    future_4 = loop.run_in_executor(executor, wait_has_ban)
                    done, pending = await asyncio.wait(
                        [future_1, future_2, future_3, future_4],
                        return_when=asyncio.FIRST_COMPLETED,
                    )

                    for future in done:
                        result = future.result()
                        # print("Result:", result)

                        # if video -----------------------------------------------------------------
                        if result == "has_video":
                            d1(resourceId="com.zhiliaoapp.musically:id/cover").click()
                            d1.press(62)
                            await asyncio.sleep(1)
                            d1.click(x=300, y=280)
                            await asyncio.sleep(1)
                            d1.press(4)
                            await asyncio.sleep(1)

                    # back 2 followers -----------------------------------------------------------------
                    d1.press(4)
                    await asyncio.sleep(1)
                    d1.press(19)

        except Exception as error:
            print(error)


async def main():

    await search()


asyncio.run(main())
