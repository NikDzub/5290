#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys

print(f"{sys.argv[0]} is running..")

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()


def start_ui(client):
    d = u2.connect(client.serial)
    print(d.info)
    # d.shell("reboot")


def start_ui_manual(client):
    d = u2.connect(client.serial)
    d.uiautomator.start()
    d.app_start("com.github.uiautomator")
    d.shell("input tap 90 180")
    # print("90 180")


for client in devices:
    try:
        start_ui(client)
    except:
        pass

    try:
        start_ui_manual(client)
    except:
        pass
