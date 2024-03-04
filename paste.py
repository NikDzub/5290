#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
from datetime import datetime
import re
from colorama import Fore, Style
import pyperclip


d = u2.connect()
users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)


async def emulator():
    try:
        text = pyperclip.paste()
        print(text)

        d(focused=True).set_text(text)
    except Exception as error:
        print(error)


async def main():

    await emulator()


asyncio.run(main())
