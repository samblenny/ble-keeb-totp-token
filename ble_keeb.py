# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
# See NOTES.md for documentation links
#
from micropython import const
import time

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


ADVERTISE_TIMEOUT = const(30)


class BLEKeeb:

    def __init__(self):
        self.hid = HIDService()
        self.info = DeviceInfoService(
            software_revision=adafruit_ble.__version__,
            manufacturer="Adafruit Industries"
        )
        self.advertisement = ProvideServicesAdvertisement(self.hid)
        # see https://www.bluetooth.com/specifications/assigned-numbers/
        self.advertisement.appearance = 0x03C1  # Keyboard
        self.scan_response = Advertisement()
        self.scan_response.complete_name = "BLE Keeb"
        self.ble = adafruit_ble.BLERadio()
        self.keyboard = Keyboard(self.hid.devices)
        self.keyboard_layout = KeyboardLayoutUS(self.keyboard)

    def advertise(self):
        if not self.ble.connected:
            print("Advertising as BLE Keeb")
            if self.ble.advertising:
                self.ble.stop_advertising()
            time.sleep(0.01)
            self.ble.start_advertising(self.advertisement, self.scan_response,
                timeout=ADVERTISE_TIMEOUT)
        else:
            print("Connected:", self.ble.connections)
            self.keyboard

    def connected(self):
        return self.ble.connected

    def send_code(self, code):
        if (not self.connected()) or (not code):
            return
        self.keyboard_layout.write(code)
