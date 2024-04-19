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

            user_names = []

            for i in range(100):
                d1.swipe(145, 380, 150, 100, 0.01)
                await asyncio.sleep(1)
                d1.swipe_ext("down", scale=0.5)

                # colection = d1(resourceId="com.zhiliaoapp.musically:id/oau")
                # for user in colection:
                #     name = user.get_text()
                #     if name not in user_names:
                #         user_names.append(name)
                #         print(name)

            for i in range(100):

                await asyncio.sleep(1)
                d1.swipe_ext("down", scale=0)  # click on user
                await asyncio.sleep(1)

                # in user
                has_video = d1(resourceId="com.zhiliaoapp.musically:id/cover").exists(
                    timeout=5
                )
                if has_video:

                    d1(resourceId="com.zhiliaoapp.musically:id/cover").click()
                    d1.press(62)
                    await asyncio.sleep(1)
                    # d1(descriptionContains="Share video").up().click()
                    d1.click(x=300, y=280)
                    await asyncio.sleep(1)
                    d1(resourceId="com.android.systemui:id/back").click()
                    await asyncio.sleep(1)

                d1(descriptionContains="Back to previous screen").click()
                await asyncio.sleep(1)
                d1.swipe_ext("down", scale=0.3)

        except Exception as error:
            print(error)


async def main():

    await search()


asyncio.run(main())
