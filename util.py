# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# This is meant to be imported from the CircuitPython REPL to set the DS3231
# clock after installing a new battery.
#
# Usage example:
# >>> import util
# DS3231 datetime: 2000-01-01 02:06:52
# >>> util.set_clock()
# Set DS3231 RTC time...
#    year: 2025
#   month: 11
#     day: 25
#    hour: 00
#  minute: 01
# seconds: 02
# new RTC time:  2025-11-25 00:01:02
# >>>
#
import board
import time
from time import mktime, sleep, struct_time

from adafruit_datetime import datetime
from adafruit_ds3231 import DS3231


i2c = board.I2C()
rtc = DS3231(i2c)


def set_clock():
    print("Set DS3231 RTC time...")
    try:
        y    = int(input("   year: "))
        mon  = int(input("  month: "))
        d    = int(input("    day: "))
        h    = int(input("   hour: "))
        min_ = int(input(" minute: "))
        s    = int(input("seconds: "))
        t = struct_time((y, mon, d, h, min_, s, 0, -1, -1))
        rtc.datetime = t
        print("new RTC time: ", now())
    except ValueError as e:
        print("ERROR Bad value:", e)

def now():
    # Return RTC time formatted as a string
    return "%04d-%02d-%02d %02d:%02d:%02d" % ((rtc.datetime)[0:6])
