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

n_new_videos = int(sys.argv[1])
new_videos = []
fam_users = mod.get_users(1)


d1 = u2.connect("127.0.0.1:6555")
d1_users_output, exit_code = d1.shell("pm list users")
d1_users = re.findall(r"UserInfo{(\d+):", d1_users_output)


async def search():
    d1.uiautomator.start()
    d1.app_start("com.github.uiautomator")
    d1(resourceId="com.github.uiautomator:id/start_uiautomator").click()

    d1.open_url(f"https://www.tiktok.com/@ihptto")
    d1(text="Message").exists(timeout=10)

    for user in fam_users:

        try:

            # go 2 usr -----------------------------------------------------------------
            d1.open_url(f"https://www.tiktok.com/@{user}")
            d1(text="Message").exists(timeout=10)
            await asyncio.sleep(1)
            d1.swipe_ext("up", scale=0.8)
            # print(f"{user} loaded")

            # get n pins -----------------------------------------------------------------
            d1(resourceId="com.zhiliaoapp.musically:id/cover").exists(timeout=10)
            n_pins = d1(text="Pinned").count
            # print(f"pins : {n_pins}")

            # go latest vid -----------------------------------------------------------------
            d1(resourceId="com.zhiliaoapp.musically:id/cover")[n_pins].click()
            d1(resourceId="com.zhiliaoapp.musically:id/title").exists(timeout=10)
            await asyncio.sleep(1)
            d1.press(62)

            # n_ago = (
            #     d1(resourceId="com.zhiliaoapp.musically:id/title")
            #     .right(focusable="false", clickable="false")
            #     .get_text()
            # )
            # print(f"ago : {n_ago}")

            # check n of comments -----------------------------------------------------------------
            d1(descriptionContains="Read or add comments").exists(timeout=10)
            n_comments_desc = d1(descriptionContains="Read or add comments").info[
                "contentDescription"
            ]
            n_comments_filtered = re.sub("[^0-9]", "", n_comments_desc)

            if (
                "K" in n_comments_desc
                or int(n_comments_filtered) > 20
                # or "ago" in n_ago
                # or "m ago" in n_ago
            ):

                # go2 comments -----------------------------------------------------------------
                d1(descriptionContains="Read or add comments").click(timeout=10)
                d1(descriptionContains="Like or undo like").exists(timeout=10)

                new = False

                # (-h/m ago ??? ) -----------------------------------------------------------------
                # d(text="Reply").left(className="android.widget.TextView").get_text()
                for i in range(24):
                    if len(d1(text=f"{i}h")) or len(d1(text=f"{i}m")):
                        new = True

                if new:

                    # get link -----------------------------------------------------------------
                    d1(descriptionContains="Like or undo like").exists(timeout=10)
                    bounds = d1(descriptionContains="Like or undo like").info["bounds"]

                    d1.long_click(
                        y=bounds["bottom"], x=bounds["right"] - 50, duration=3
                    )

                    d1(text="Send to friends").exists(timeout=10)
                    d1(text="Send to friends").click(timeout=10)

                    await asyncio.sleep(1)
                    d1(text="Copy link").click(timeout=10)

                    like_link = d1(
                        textContains="https://vt.tiktok.com/",
                        resourceId="com.android.systemui:id/text_preview",
                    ).get_text()

                    # get link -----------------------------------------------------------------
                    # d1(descriptionContains="Close comments").long_click(duration=1)
                    # d1(descriptionContains="Share video").click()
                    # d1(text="Copy link").exists(timeout=10)
                    # await asyncio.sleep(1)
                    # d1(text="Copy link").long_click(duration=1)

                    # vid_link = d1(
                    #     textContains="https://vt.tiktok.com/",
                    #     resourceId="com.android.systemui:id/text_preview",
                    # ).get_text()

                    # new_videos.append(vid_link)

                    # print(
                    #     f"{Fore.LIGHTYELLOW_EX}{vid_link} {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
                    # )
                    #

                    #
                    # d1.open_url(f"https://www.tiktok.com/@ihptto")
                    # d1(text="Message").exists(timeout=10)

                    # d1.open_url(vid_link)

                    # d1(textContains="H2X7A").exists(timeout=10)
                    # bounds = d1(textContains="H2X7A").info["bounds"]

                    # d1.long_click(
                    #     y=bounds["bottom"] + 10, x=bounds["right"], duration=3
                    # )

                    # d1(text="Send to friends").exists(timeout=10)
                    # d1(text="Send to friends").click(timeout=10)

                    # d1(text="Copy link").exists(timeout=10)
                    # d1(text="Copy link").click(timeout=10)

                    # like_link = d1(
                    #     textContains="https://vt.tiktok.com/",
                    #     resourceId="com.android.systemui:id/text_preview",
                    # ).get_text()
                    #

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
                            d1(descriptionContains="Post comment").click(timeout=10)

                    # print(like_link)
                    new_videos.append(like_link)

                    print(
                        f"{Fore.LIGHTYELLOW_EX}{like_link} {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
                    )

                    if len(new_videos) >= n_new_videos:
                        break

        except Exception as error:
            print(error)

            d1.app_stop(f"{mod.app_name}")
            d1.open_url(f"https://www.tiktok.com/@ihptto")
            d1(text="Message").exists(timeout=10)
            pass

    d1.app_stop(f"{mod.app_name}")


async def comment(user):

    print(
        f"{Fore.LIGHTRED_EX}user {user} - {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
    )

    try:
        d1.open_url(f"https://www.tiktok.com/@ihptto")
        await asyncio.sleep(1)
        d1(text="Message").exists(timeout=20)

        for video in new_videos:
            d1.open_url(f"https://www.tiktok.com/@ihptto")
            d1(text="Message").exists(timeout=10)

            d1.open_url(video)
            await asyncio.sleep(5)

            d1(descriptionContains="Close comments").long_click(duration=1)
            d1.press(62)
            d1(descriptionContains="Read or add comments").click(timeout=20)
            d1(descriptionContains="Like or undo like").exists(timeout=20)

            # comment -----------------------------------------------------------------
            comments_list = []
            for i in range(2):

                for com in d1(className="android.widget.TextView", focusable="True"):
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
                    d1(descriptionContains="Post comment").click(timeout=10)

        d1.app_stop(f"{mod.app_name}")

    except Exception as error:
        print(error)
        pass


async def main():

    for user in d1_users:
        d1.shell(f"am switch-user {user}")
        await asyncio.sleep(2)
        d1(resourceId="com.android.systemui:id/clock").exists(timeout=20)

        if user == "0":
            await search()
        else:
            await comment(user)

    with open("./new_videos.txt", "w") as outfile:
        for index, row in enumerate(new_videos):
            outfile.write(str(row) + "\n")


asyncio.run(main())
