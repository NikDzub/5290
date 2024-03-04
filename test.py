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
import pyperclip


d = u2.connect()
users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)


async def emulator(profile_index, profile_id):
    try:
        print("hello")

        text = pyperclip.paste()

        print(text)

        # d.open_url(
        #     f"https://m.tiktok.com/v/7342416732826389766.html?&share_comment_id=7342400421070390022&share_item_id=7342416732826389766"
        # )
        # https://vt.tiktok.com/ZSFDBVjCG/
        # https://m.tiktok.com/v/7342416732826389766.html?_d=ecec033m312iek&comment_author_id=7146006051757130758&preview_pb=0&share_comment_id=7342430517978497798&share_item_id=7342416732826389766&sharer_language=ja-JP&source=h5_m&u_code=e91himlahab98i

        # d.set_clipboard("text", "label")
        # txt = d.clipboard()
        print(d.clipboard)
        d(text="Message").exists(timeout=1340)

    except Exception as error:
        print(error)


async def main():

    for profile_index, profile_id in enumerate(device_profiles):
        await emulator(profile_index, profile_id)


asyncio.run(main())
