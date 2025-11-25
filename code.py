# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
# See NOTES.md for documentation links and pinout info.
#
import atexit
import board
import busio
import digitalio
import displayio
from fourwire import FourWire
from micropython import const
import pwmio
import terminalio
import time

from adafruit_24lc32 import EEPROM_I2C
import adafruit_apds9960
from adafruit_display_text import label
from adafruit_ds3231 import DS3231
from adafruit_st7789 import ST7789


# Begin TFT backlight dimming (100% brightness is PWM duty_cycle=0xffff)
backlight = pwmio.PWMOut(board.TFT_BACKLIGHT, frequency=500,
    duty_cycle=int(0xffff * 0.4))

# Configure CLUE's 240x240 ST7789 TFT display with a 4x scaled text label
displayio.release_displays()
spi = busio.SPI(board.TFT_SCK, MOSI=board.TFT_MOSI)
# print("spi frequency", spi.frequency) # default is 32MHz which works fine
display_bus = FourWire(spi, command=board.TFT_DC, chip_select=board.TFT_CS,
    reset=board.TFT_RESET)
display = ST7789(display_bus, width=240, height=240, rowstart=80, bgr=True,
    rotation=0, auto_refresh=False)
group = displayio.Group()
display.root_group = group
display.refresh()
textbox = label.Label(font=terminalio.FONT, scale=4, color=0xefef00)
textbox.anchor_point = (0, 0)
textbox.anchored_position = (0, 0)
textbox.line_spacing = 1.0  # default is 1.25
group.append(textbox)

# Set an atexit handler to release the display once code.py ends. This is an
# aesthetic filter to prevent CircuitPython's supervisor from hijacking the
# display to show its own stuff, which I don't want to see.
def atexit_shutdown_display():
    try:
        textbox.text = 'OFFLINE'
        display.refresh()
        displayio.release_displays()
        spi.deinit()
    except AttributeError:
        pass
atexit.register(atexit_shutdown_display)

# Prepare for talking to the I2C RTC and EEPROM chips
i2c = board.I2C()
eeprom = EEPROM_I2C(i2c)
rtc = DS3231(i2c)

def format_datetime(t):
    date = '%04d-%02d-%02d' % (t[0:3])
    time = '%02d:%02d:%02d' % (t[3:6])
    return (date, time)

# ---
# Okay, now actually do something...
# ---
print('EEPROM length:', len(eeprom))
print('EEPROM[:64]:', eeprom[:64])
print('DS3231 datetime: %s %s' % format_datetime(rtc.datetime))
t = prev_t = rtc.datetime
while True:
    # Update time on display
    textbox.text = '%s\n %s' % format_datetime(t)
    display.refresh()
    # Sleep until second rolls over
    while t.tm_sec == prev_t.tm_sec:
        time.sleep(0.05)
        t = rtc.datetime
    prev_t = t
