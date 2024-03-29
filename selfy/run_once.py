#!/usr/bin/env python3

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


for client in devices:
    start_ui(client)
