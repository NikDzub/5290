#!/usr/bin/env python3

# python3 M2 2
# python3 M2 (# comments)

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
import pyperclip

new_videos = ["https://vt.tiktok.com/ZSFQwPmX5/", "https://vt.tiktok.com/ZSFQwxyf1/"]


d = u2.connect("127.0.0.1:6562")

users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)


async def go_search2(id):

    try:

        print(f"user: {id}")

        d.shell(f"am switch-user {id}")

        await asyncio.sleep(2)
        d(resourceId="com.android.systemui:id/clock").exists(timeout=20)

        d.open_url(f"https://www.tiktok.com/@ihptto")
        d(text="Message").exists(timeout=10)

        for video in new_videos:

            d.open_url(video)

            d(descriptionContains="Like or undo like").click(timeout=35)

            print("like")

            await asyncio.sleep(1)
            d.app_stop(f"{mod.app_name}")

    except Exception as error:
        print(error)
        pass


async def main():
    for id in device_profiles:

        await go_search2(id)


asyncio.run(main())
