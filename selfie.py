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


async def go_search2():
    d.open_url(f"https://vt.tiktok.com/")

    for i in range(100):
        try:
            d.press(62)

            # filter
            is_live = d(text="LIVE now").exists(timeout=3)
            is_sponsor = d(text="Sponsored").exists(timeout=3)

            if is_live or is_sponsor:
                print("is live/sponsor")
                d.swipe_ext("up", scale=0.8)
                continue

            # get number of comments

            d(descriptionContains="Read or add comments").exists(timeout=10)
            n_comments_desc = d(descriptionContains="Read or add comments").info[
                "contentDescription"
            ]
            n_comments_filtered = re.sub("[^0-9]", "", n_comments_desc)

            print(f"comments : {int(n_comments_filtered)}")

            if int(n_comments_filtered) > 20:
                # go to comments

                d(descriptionContains="Read or add comments").click(timeout=10)
                d(descriptionContains="Like or undo like").exists(timeout=10)

                new = False
                # check if recent comment exists (-h ago)
                # d(text="Reply").left(className="android.widget.TextView").get_text()
                for i in range(24):
                    if len(d(text=f"{i}h")) or len(d(text=f"{i}m")):
                        print(f"recent comment from {i}h/m ago exists")
                        new = True

                if new:

                    # get link from random comment
                    d(text="Reply").left(
                        className="android.widget.TextView"
                    ).long_click(duration=8)

                    d(text="Send to friends").exists(timeout=10)
                    d(text="Send to friends").click(timeout=10)

                    d(text="Copy link").exists(timeout=10)
                    d(text="Copy link").click(timeout=10)

                    vid_link = d(
                        textContains="https://vt.tiktok.com/",
                        resourceId="com.android.systemui:id/text_preview",
                    ).get_text()

                    print(vid_link)

                    # comment
                    comments_list = []
                    for i in range(2):

                        for com in d(
                            className="android.widget.TextView", focusable="True"
                        ):
                            try:
                                comment_text = com.get_text()
                                if comment_text not in comments_list:
                                    comments_list.append(com.get_text())
                            except:
                                pass

                        d.swipe_ext("up", scale=0.8)

                    random.shuffle(comments_list)
                    for comment_index, comment in enumerate(comments_list):
                        if comment_index < 2:
                            print(f"comment : {comment}")
                            d(textContains="Add comment...").click(10)
                            d(textContains="Add comment...").set_text(comment)
                            d(descriptionContains="Post comment").click(10)

                    # d(descriptionContains="Close comments").click(timeout=10)
                    # close app and get comment

                    d.app_stop(f"{mod.app_name}")
                    d.open_url(f"https://www.tiktok.com/@ihptto")
                    d(text="Message").exists(timeout=10)

                    d.open_url(vid_link)

                    d(text="Reply").exists(timeout=10)
                    d(text="Reply")[1].left(
                        className="android.widget.TextView"
                    ).long_click(duration=5)

                    d(text="Send to friends").exists(timeout=10)
                    d(text="Send to friends").click(timeout=10)

                    d(text="Copy link").exists(timeout=10)
                    d(text="Copy link").click(timeout=10)

                    like_link = d(
                        textContains="https://vt.tiktok.com/",
                        resourceId="com.android.systemui:id/text_preview",
                    ).get_text()

                    print(like_link)

                    print("finish")
                    await asyncio.sleep(435345435)

            d.open_url(f"https://www.tiktok.com/")
            d.swipe_ext("up", scale=0.8)
            print("swipe next..")

        except Exception as error:
            d.app_stop(f"{mod.app_name}")
            # d.shell(f"am force-stop {mod.app_name}")
            d.open_url(f"https://www.tiktok.com/")
            print(error)
            pass

    print("here")
    await asyncio.sleep(435345435)

    # d(resourceId=mod.actual_comment).exists(timeout=20)

    # d.shell(f"am force-stop {mod.app_name}")
    d.app_stop(f"{mod.app_name}")


async def main():

    await go_search2()


asyncio.run(main())
