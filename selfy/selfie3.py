#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import sys
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import mod
from datetime import datetime
import random
import re
from colorama import Fore, Style

n_new_videos = int(sys.argv[1])
fam_users = mod.get_users(1)
new_videos = []


d1 = u2.connect("127.0.0.1:6555")
d2 = u2.connect("127.0.0.1:6562")


d2_users_output, exit_code = d2.shell("pm list users")
d2_users = re.findall(r"UserInfo{(\d+):", d2_users_output)


async def search():
    print(
        f"{Fore.BLUE}search - {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
    )

    d1.app_start("com.github.uiautomator")
    d1(resourceId="com.github.uiautomator:id/start_uiautomator").click()

    # go2 fyp -----------------------------------------------------------------
    d1.open_url(f"https://vt.tiktok.com/")

    while len(new_videos) < n_new_videos:

        for user in fam_users:

            try:
                d1.open_url(f"https://www.tiktok.com/@{user}")
                print(f"https://www.tiktok.com/@{user}")

                print("here")
                await asyncio.sleep(2343434)

                # filter -----------------------------------------------------------------
                await asyncio.sleep(2)
                is_live = d1(text="LIVE now").exists(timeout=1)
                is_sponsor = d1(text="Sponsored").exists(timeout=1)

                if is_live or is_sponsor:
                    # print("is live/sponsor")
                    d1.swipe_ext("up", scale=0.8)
                    continue

                # check n of comments -----------------------------------------------------------------

                d1(descriptionContains="Read or add comments").exists(timeout=10)
                n_comments_desc = d1(descriptionContains="Read or add comments").info[
                    "contentDescription"
                ]
                n_comments_filtered = re.sub("[^0-9]", "", n_comments_desc)

                # print(f"comments : {int(n_comments_filtered)}")

                if int(n_comments_filtered) > 20:

                    # go2 video -----------------------------------------------------------------

                    d1(descriptionContains="Read or add comments").click(timeout=10)
                    d1(descriptionContains="Like or undo like").exists(timeout=10)

                    new = False

                    # (-h/m ago ??? ) -----------------------------------------------------------------
                    # d(text="Reply").left(className="android.widget.TextView").get_text()
                    for i in range(24):
                        if len(d1(text=f"{i}h")) or len(d1(text=f"{i}m")):
                            new = True

                    if new:

                        # get link from 1st comment -----------------------------------------------------------------

                        d1(text="Reply").left(
                            className="android.widget.TextView"
                        ).long_click(duration=5)

                        d1(text="Send to friends").exists(timeout=10)
                        d1(text="Send to friends").click(timeout=10)

                        d1(text="Copy link").exists(timeout=10)
                        d1(text="Copy link").click(timeout=10)

                        vid_link = d1(
                            textContains="https://vt.tiktok.com/",
                            resourceId="com.android.systemui:id/text_preview",
                        ).get_text()

                        # print(vid_link)

                        # comment -----------------------------------------------------------------

                        comments_list = []
                        for i in range(2):

                            for com in d1(
                                className="android.widget.TextView", focusable="True"
                            ):
                                try:
                                    comment_text = com.get_text()
                                    if comment_text not in comments_list:
                                        comments_list.append(com.get_text())
                                except:
                                    pass

                            d1.swipe_ext("up", scale=0.8)

                        random.shuffle(comments_list)
                        for comment_index, comment in enumerate(comments_list):
                            if comment_index < 2:
                                # print(f"comment : {comment}")
                                d1(textContains="Add comment...").click(10)
                                d1(textContains="Add comment...").set_text(comment)
                                d1(descriptionContains="Post comment").click(10)

                        # reopen and get comment link -----------------------------------------------------------------

                        d1.app_stop(f"{mod.app_name}")
                        d1.open_url(f"https://www.tiktok.com/@ihptto")
                        d1(text="Message").exists(timeout=10)

                        d1.open_url(vid_link)

                        d1(text="Reply").exists(timeout=10)
                        await asyncio.sleep(1)
                        d1(text="Reply")[1].left(
                            className="android.widget.TextView"
                        ).long_click(duration=5)

                        d1(text="Send to friends").exists(timeout=10)
                        d1(text="Send to friends").click(timeout=10)

                        d1(text="Copy link").exists(timeout=10)
                        d1(text="Copy link").click(timeout=10)

                        like_link = d1(
                            textContains="https://vt.tiktok.com/",
                            resourceId="com.android.systemui:id/text_preview",
                        ).get_text()

                        # print(like_link)
                        new_videos.append(like_link)
                        print(
                            f"{Fore.LIGHTYELLOW_EX}{like_link}{Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
                        )

                d1.open_url(f"https://www.tiktok.com/")
                d1.swipe_ext("up", scale=0.8)
                # print("swipe next..")

            except Exception as error:
                d1.app_stop(f"{mod.app_name}")
                # d.shell(f"am force-stop {mod.app_name}")
                d1.open_url(f"https://www.tiktok.com/")
                print(error)
                pass

    d1.app_stop(f"{mod.app_name}")
    # print(new_videos)


async def like(id):

    print(
        f"{Fore.LIGHTRED_EX}user {id} - {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
    )

    if id == 0 or id == "0":

        d2.app_start("com.github.uiautomator")
        d2(resourceId="com.github.uiautomator:id/start_uiautomator").click()

    try:
        d2.shell(f"am switch-user {id}")
        await asyncio.sleep(2)

        d2(resourceId="com.android.systemui:id/clock").exists(timeout=20)

        d2.open_url(f"https://www.tiktok.com/@ihptto")
        d2(text="Message").exists(timeout=10)

        for video in new_videos:
            d2.open_url(video)
            d2(descriptionContains="Like or undo like").click(timeout=35)
            # print("like")
            await asyncio.sleep(1)
            d2.app_stop(f"{mod.app_name}")

    except Exception as error:
        print(error)
        pass


async def main():
    await search()
    for id in d2_users:
        await like(id)


asyncio.run(main())
