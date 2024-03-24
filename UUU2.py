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

n_comments = int(sys.argv[1])

d = u2.connect()
users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)

new_vids = mod.get_new_vids()
share_links = []


async def go_to_comments(vid):
    d.open_url(f"https://www.tiktok.com/@ihptto")
    d(text="Follow").exists(timeout=10)

    d.open_url(vid)

    d(resourceId=mod.comments).exists(timeout=20)
    d(resourceId=mod.pause).click(20)
    d(resourceId=mod.comments).click(20)
    d(resourceId=mod.actual_comment).exists(timeout=20)


async def comment(profile_index, profile_id):
    try:
        d.shell(f"am switch-user {profile_id}")
        print(f"")
        print(f"{Fore.GREEN}user[{profile_id}] [comment]{Style.RESET_ALL}")

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

        random.shuffle(new_vids)
        for vid in new_vids:
            await go_to_comments(vid)

            comments_list = []
            for i in range(3):
                d.swipe_ext("up", scale=0.8)

            for com in d(resourceId=mod.actual_comment):
                if com.get_text() not in comments_list:
                    comments_list.append(com.get_text())

            random.shuffle(comments_list)
            for comment_index, comment in enumerate(comments_list):
                if comment_index < n_comments:
                    d(textContains="Add comment...").click(10)
                    d(textContains="Add comment...").set_text(comment)
                    d(resourceId=mod.send_comment).click(10)
                    print(f"{vid}")

                    await asyncio.sleep(1)

        d.shell(f"am force-stop {mod.app_name}")

    except Exception as error:
        print(error)
        d.shell(f"am force-stop {mod.app_name}")


async def main():

    for profile_index, profile_id in enumerate(device_profiles):
        await comment(profile_index, profile_id)


asyncio.run(main())
