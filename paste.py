#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import re
import pyperclip


d = u2.connect()
users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)


async def paste():
    try:
        text = pyperclip.paste()
        print(text)

        d(focused=True).set_text(text)

    except Exception as error:
        print(error)


async def main():
    await paste()


asyncio.run(main())
