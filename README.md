<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2025 Sam Blenny -->
# BLE Keeb TOTP

TOTP token with BLE HID keyboard output, Adafruit CLUE, precision RTC, 4-key
NeoKey mechanical keypad, and a 4KB EEPROM for TOTP seed storage.


## Hardware

The code here is written for:

- [Adafruit CLUE - nRF52840 Express](https://www.adafruit.com/product/4500)
- [Adafruit DS3231 Precision RTC](https://www.adafruit.com/product/5188)
- [Adafruit 24LC32 I2C EEPROM](https://www.adafruit.com/product/5146)
- [Adafruit NeoKey 1x4 QT I2C Mechanical Key Switches with NeoPixels](https://www.adafruit.com/product/4980)

Additional Parts:
- [Kailh Mechanical Key Switches Cherry MX Brown Compatible](https://www.adafruit.com/product/4954)
- [Purple DSA Keycaps for MX Compatible Switches](https://www.adafruit.com/product/5003)


## Install & Setup

You will need to:

1. Ensure your CLUE board has an [up to date bootloader](https://learn.adafruit.com/adafruit-clue/update-bootloader)

2. Download CircuitPython 10.0.3 .UF2 file from the circuitpython.org downloads
   page for
   [CLUE NRF52840 Express](https://circuitpython.org/board/clue_nrf52840_express/)

3. Follow Adafruit's
   [CircuitPython on CLUE](https://learn.adafruit.com/adafruit-clue/circuitpython)
   Learn guide to install CircuitPython: plug CLUE into a computer, double-click
   CLUE's reset button, wait for CLUEBOOT drive, drag UF2 file onto CLUEBOOT
   drive, wait for copy to finish.

4. Unplug the CLUE and assemble the rest of the hardware

5. Get the project bundle from the release page and copy its code and library
   files from the 10.x directory to your board's `CIRCUITPY` drive


## Set RTC Time in UTC

When you first install a battery in the DS3231, the time will be wildly wrong.
You can set the time from the REPL by importing the `util` module then calling
`util.set_clock()`, like this:

```
Adafruit CircuitPython 10.0.3 on 2025-10-17; Adafruit CLUE nRF52840 Express with nRF52840
>>> import util
>>> util.now()
'2000-01-01 02:06:52'
>>> util.set_clock()
Set DS3231 RTC time...
   year: 2025
  month: 11
    day: 25
   hour: 00
 minute: 01
seconds: 02
new RTC time:  2025-11-25 00:01:02
>>> # wait a while, then check the time
>>> util.now()
'2025-11-25 00:06:02'
>>>
```

When you set the time, use a GPS or NTP synchronized reference that shows UTC
time with seconds (e.g. https://samblenny.github.io/totp-util/clock/ ). Don't
set the clock according to your local timezone. You must use UTC.

Each of the "year:", "month:", "day:", etc. prompts come from python's
`input()` function. The text on the left is the input prompt shown by
`set_clock()`, and the numbers on the right are an example of what you might
type for your response. When you hit return or enter for the seconds line, the
time will be set immediately.
